'''
Created on 12/11/2009
@author: Nahuel
'''

from opsys.scheduling.Scheduler import Scheduler

class FCFSScheduler(Scheduler):
    '''First Come, First Served scheduling politic.'''
    def __init__(self, cpu, proc_store):
        '''Constructor of FCFSScheduler.'''
        Scheduler.__init__(self, cpu, proc_store)
    
    def get_next_pcb(self):
        '''
        Always select the first process in the ready queue.
        
        @note: Override method.
        '''
        return self.get_process_store().get_ready_queue().pop(0)