'''
Created on 15/11/2009
@author: Nahuel
'''

from opsys.instruction.CPUInstructionSet import CPUInstructionSet
from exceptions.OSException import OSException
from opsys.process.ProcessKiller import ProcessKiller
from opsys.osconfig import CPU_SLEEP_TIME
from oslogging.Logger import Logger
import time

class CPU(object):
    '''
    The Central Processing Unit. Can execute instructions.
    
    @ivar _proc_store: the storage of all processes.
    @ivar _io_devices: the managers of each type of resource.
    @ivar _current_pcb: the process in execution that use the CPU.
    @ivar _banker: the manager of resources requests, for deadlock avoidance.
    @ivar _state_flags: indicates activity and expropriation states.
    @ivar _registers: quick and temporal storage.
    @ivar _instruction_set: it knows and executes all the 'cpu' instructions.  
    '''
    def __init__(self, banker, io_dev, proc_store):
        '''
        Constructor of CPU
        
        @param banker: a Banker's Algorithm created and initialized.
        @param io_dev: all the I/O devices in the system.
        @param proc_store: where the process are storaged.
        '''
        self._proc_store = proc_store
        self._io_devices = io_dev
        self._current_pcb = None
        self._banker = banker
        self._state_flags = [False] * 2
        self._registers = self.__init_registers()
        self._instruction_set = CPUInstructionSet(self)
    
    def get_process_store(self):
        '''Getter of _proc_store.'''
        return self._proc_store
    
    def is_expropiated(self):
        '''Getter of the the expropiation state.'''
        return self._state_flags[1]
    
    def set_banker(self, banker):
        self._banker = banker
    
    def set_process_store(self, store):
        self._proc_store = store
    
    def get_inst_set(self):
        '''Getter of _instruction_set.'''
        return self._instruction_set
    
    def get_device_at(self, name_dev):
        '''Getter of the manager at a device name given.'''
        return self._io_devices[name_dev]
    
    def get_current_pcb(self):
        '''Getter of _current_pcb.'''
        return self._current_pcb
    
    def set_current_pcb(self, pcb):
        '''Setter of _current_pcb. Also do the context switch.'''
        self.context_switch_in(pcb)
        self._current_pcb = pcb
        
    def set_expropiated(self):
        '''Set the CPU expropiated.'''
        self._state_flags[1] = True
    
    def no_longer_expropiated(self):
        '''Make the CPU no longer expropriated.'''
        self._state_flags[1] = False
    
    def is_active(self):
        '''Getter of the CPU activity.'''
        return self._state_flags[0]
    
    def set_active(self):
        '''Set the CPU active.'''
        self._state_flags[0] = True
        
    def set_inactive(self):
        '''Set the CPU inactive.'''
        self._state_flags[0] = False
    
    def get_banker(self):
        '''Getter of _banker'''
        return self._banker
    
    def get_registers(self):
        '''Getter of _registers.'''
        return self._registers
    
    def set_registers(self, the_regs):
        '''Setter of _registers.'''
        self._registers = the_regs
    
    def __init_registers(self):
        '''Initialize the registers, with initial value "0".'''
        return {'R0': 0,'R1': 0,'R2': 0,'R3': 0,
                'R4': 0,'R5': 0,'R6': 0,'R7': 0}
    
    def start(self):
        '''Main method to manage CPU and I/O instructions.'''
        self.set_active()
        while self.is_active():
            if self.get_current_pcb() is not None:
                curr_pcb = self.get_current_pcb()
                curr_pcb.set_state('Running')
                if curr_pcb.finished():
                    curr_pcb.set_state('Finished')
                    self.no_current_process()
                    ProcessKiller.get_instance().kill_pcb(curr_pcb)
                    continue
                curr_inst = curr_pcb.get_next_inst()
                if curr_inst.is_io_inst(): 
                    self.process_io_inst(curr_inst, curr_pcb)
                    continue
                else: 
                    self.process_cpu_inst(curr_inst, curr_pcb)
                if self.is_expropiated() or self.check_burst(curr_pcb):
                    Logger.get_instance().log_expropiate(curr_pcb.get_pid())
                    self.context_switch_out(curr_pcb)
                    self.get_process_store().put_in_ready_queue(curr_pcb)
                    self.no_current_process()
            time.sleep(CPU_SLEEP_TIME)
        self.set_inactive()
        
    def process_io_inst(self, inst, pcb):
        '''Dispatch the I/O instruction to the proper device.'''
        self.get_device_at(inst.get_device()).add_process(pcb)
        self.no_current_process()
        
    def process_request(self, inst, pcb):
        '''
        Processes a request.
        
        @raise OSException: if the request is greater than the need declared.
        '''
        try:                    # handling for wrong requests
            req_args = tuple(inst.get_args_as_int())
            pid = pcb.get_pid()
            if not self.get_banker().request_algorithm(pid, req_args):
                self.context_switch_out(pcb)
                self.get_process_store().put_in_ready_queue(pcb)
                self.no_current_process()
                Logger.get_instance().log_request(pid, req_args, 'rejected')
            else:
                Logger.get_instance().log_request(pid, req_args, 'approved')
                pcb.inc_pc()
        except OSException:
            ProcessKiller.get_instance().kill_pcb(pcb)
            self.no_current_process()
            
    def process_cpu_inst(self, inst, pcb):
        '''
        Process a CPU instruction.
        
        @raise OSException: if the process make request larger 
            than the total resources.
        '''
        if inst.is_request():
            self.process_request(inst, pcb)
        elif inst.is_free(): 
            try:                           #handling for wrong max requests
                self.get_banker().do_free(pcb)
                pcb.inc_pc()
                Logger.get_instance().log_free(pcb)
            except OSException:
                ProcessKiller.get_instance().kill_pcb(pcb)
                self.no_current_process()
        else:
            self.get_inst_set().execute(inst, pcb)
            Logger.get_instance().log_execinst(pcb)
            pcb.set_remaining_time(pcb.get_remaining_time() - inst.get_time())
            pcb.set_next_burst(pcb.get_next_burst() - inst.get_time())
            pcb.inc_pc()
        
    def context_switch_in(self, pcb):
        '''Set the new values for the registers.'''
        self.set_registers(pcb.get_registers())
        
    def context_switch_out(self, pcb):
        '''Saves the registers to the PCB.'''
        pcb.set_registers(self.get_registers())
        
    def no_current_process(self):
        '''Free the CPU, now can receive others processes.'''
        self._current_pcb = None    
    
    def check_burst(self, pcb):
        '''Checks if the PCB's CPU burst it's over.'''
        try: 
            a = pcb.get_instruction_at(pcb.get_pc() + 1).is_cpu_inst()
        except IndexError: 
            a = False
        finally: 
            return pcb.get_next_burst() <= 0 and a
        
    def shutdown(self):
        '''Stop working the CPU.'''
        self.set_inactive()
        self.no_current_process()
        self.no_longer_expropiated()
