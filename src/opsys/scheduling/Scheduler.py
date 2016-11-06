'''
Created on 12/11/2009
@author: Nahuel
'''
from opsys.osconfig import STS_SLEEP_TIME
import time

class Scheduler(object):
    '''
    Abstract class that represents the CPU scheduling algorithms.
        
    @ivar _cpu: The CPU.
    @ivar _proc_store: the process store, where the scheduler 
        takes the ready queue.
    @ivar _active: represent activity in the scheduler. Necessary for the OS.
    '''
    def __init__(self, cpu, proc_store):
        '''Constructor of Scheduler.'''
        self._proc_store = proc_store
        self._cpu = cpu
        self._active = False
    
    def get_cpu(self):
        '''Getter of _cpu.'''
        return self._cpu
    
    def get_process_store(self):
        '''Getter of _proc_store.'''
        return self._proc_store
    
    def set_process_store(self, store):
        self._proc_store = store
    
    def is_priority(self):
        '''Priority schedulers will override this method.'''
        return False
    
    def is_active(self):
        '''Getter of _active.'''
        return self._active
    
    def set_active(self):
        '''Set activity in the scheduler.'''
        self._active = True

    def set_inactive(self):
        '''Stop the scheduler activity.'''
        self._active = False
    
    def start(self):
        '''Template method for scheduling processing.'''
        self.set_active()
        while self.is_active():
            self.recalculate_cpu_bursts()
            if not self.get_process_store().ready_queue_is_empty():
                if self.get_cpu().get_current_pcb() is None:
                    self.get_cpu().set_current_pcb(self.get_next_pcb())
                elif self.have_to_expropiate(): 
                    self.do_expropiation()
            time.sleep(STS_SLEEP_TIME)
        self.set_inactive()
        
    def do_expropiation(self):
        '''
        Expropiation mechanism. Tells to the CPU that is expropiated,
        then waits to a instruction finished, then enter the new process.
        '''
        self.get_cpu().set_expropiated()
        while self.get_cpu().get_current_pcb() is not None:
            time.sleep(1)
        self.get_cpu().no_longer_expropiated()
        self.get_cpu().set_current_pcb(self.get_next_pcb())
        
    def set_next_burst(self, pcb):
        '''
        Compute and set to the process the next CPU burst. This happen when
        a process enter to the operating system's ready queue.
        '''
        burst = 0
        for i in range(pcb.get_pc(), len(pcb.get_process().get_instructions())):
            if pcb.get_instruction_at(i).is_io_inst():
                break
            else:
                burst += pcb.get_instruction_at(i).get_time()
        pcb.set_next_burst(burst)
    
    def have_to_expropiate(self):
        '''Expropiative schedulers will override this method.'''
        return False
    
    def get_next_pcb(self):
        '''Abstract method. All subclasses have a different way to do it.'''
        pass
    
    def set_remaining_time(self, pcb):
        '''Compute and set the new remaining time for a process.'''
        total = 0
        for i in range(pcb.get_pc(), len(pcb.get_process().get_instructions())):
            total += pcb.get_instruction_at(i).get_time()
        pcb.set_remaining_time(total)
    
    def recalculate_cpu_bursts(self):
        '''Updates the CPU bursts for all the process in the ready queue.'''
        for pcb in self.get_process_store().get_ready_queue():
            self.set_next_burst(pcb)
