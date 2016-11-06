'''
Created on 11/11/2009
@author: Nahuel
'''

from opsys.process.PCB import PCB

class Process():
    '''
    Represents the process executed by the operating system.
    
    @ivar _pcb: the Process Control Block, with information of the process.
    @ivar __intructions: the instruction list.
    @ivar _name: the process name.
    '''
    def __init__(self, pid, name, prior, inst_list, base_reg, address_space):
        '''Constructor of Process.'''
        self._pcb = PCB(pid, prior, self, base_reg, address_space)
        self._name = name
        self._instructions = inst_list
        
    def __repr__(self):
        '''Printing for Process objects.'''
        res = 'PID : ' + str(self.get_pid()) + '\n'
        res += 'Name: ' + self.get_name() + '\n'
        res += 'Status: ' + self.get_pcb().get_state() + '\n'
        res += 'Priority: ' + str(self.get_pcb().get_priority()) + '\n'
        res += 'Program Counter: ' + str(self.get_pcb().get_pc()) + '\n'
        res += 'Registers: ' + str(self.get_pcb().get_registers()) + '\n'
        res += 'Files opened: ' + str(self.get_pcb().get_files_opened()) + '\n'
        return res
    
    def __lt__(self, another_proc):
        '''Process a < Process b <==> pid(a) < pid(b).'''
        return self.get_pcb().get_pid() < another_proc.get_pcb().get_pid()
    
    def __eq__(self, another_proc):
        '''Process a == Process b <==> pid(a) == pid(b).'''
        return self.get_pcb().get_pid() == another_proc.get_pcb().get_pid()
    
    def get_name(self):
        '''Getter of _name.'''
        return self._name
    
    def get_pcb(self):
        '''Getter of _pcb.'''
        return self._pcb
    
    def get_instructions(self):
        '''Getter of _instructions.'''
        return self._instructions
    
#---------------------delegated methods---------------------
    def get_pid(self):
        return self.get_pcb().get_pid()

    def get_state(self):
        return self.get_pcb().get_state()
    
    def get_priority(self):
        return self.get_pcb().get_priority()

    def in_ready_state(self):
        return self.get_pcb().in_ready_state()
    
    def get_remaining_time(self):
        return self.get_pcb().get_remaining_time()
    
    def set_remaining_time(self, rtime):
        self.get_pcb().set_remaining_time(rtime)
    
    def get_io_perc(self):
        return self.get_pcb().get_io_perc()
    
    def set_io_perc(self, the_perc):
        self.get_pcb().set_io_perc(the_perc)

    def finished(self):
        return self.get_pcb().get_pc() == len(self.get_instructions())