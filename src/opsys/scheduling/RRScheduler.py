'''
Created on 12/11/2009
@author: Nahuel
'''

from opsys.scheduling.Scheduler import Scheduler
from opsys.osconfig import QUANTUM

class RRScheduler(Scheduler):
    '''Round Robin scheduling politic.'''
    def __init__(self, cpu, proc_store):
        '''Constructor of RRScheduler.'''
        Scheduler.__init__(self, cpu, proc_store)
        self._quantum = QUANTUM
    
    def get_quantum(self):
        '''Getter of _quantum.'''
        return self._quantum
    
    def get_next_pcb(self):
        '''
        Always select the first process in the ready queue (same as FCFS).
        
        @note: Override method.
        '''
        return self.get_process_store().get_ready_queue().pop(0)
    
    def set_next_burst(self, pcb):
        '''Compute and set to the process the next CPU burst.'''
        burst = 0
        for i in range(pcb.get_pc(), len(pcb.get_process().get_instructions())):
            burst += pcb.get_instruction_at(i).get_time()
            if burst > self.get_quantum():
                burst -= pcb.get_instruction_at(i).get_time()
                break
        pcb.set_next_burst(burst)