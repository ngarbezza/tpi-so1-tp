'''
Created on 12/11/2009
@author: Nahuel
'''

from opsys.scheduling.Scheduler import Scheduler

class PrioritySchedulerNoExp(Scheduler):
    '''Implements the priority scheduling (not expropiative version).'''
    def __init__(self, cpu, proc_store):
        '''Constructor of PrioritySchedulerNoExp.'''
        Scheduler.__init__(self, cpu, proc_store)
        
    def get_next_pcb(self):
        pcb = min(self.get_process_store().get_ready_queue())
        self.get_process_store().get_ready_queue().remove(pcb)
        return pcb

class PrioritySchedulerExp(PrioritySchedulerNoExp):
    '''Implements the priority scheduling (expropiative version).'''
    def __init__(self, cpu, proc_store):
        '''Constructor of PrioritySchedulerExp.'''
        PrioritySchedulerNoExp.__init__(self, cpu, proc_store)
    
    def have_to_expropiate(self):
        '''
        If the max priority process of the ready queue is more priority than
        the current cpu process, the expropiation have to happen.
        '''
        candidate = min(self.get_process_store().get_ready_queue())
        curr_pcb_prior = self.get_cpu().get_current_pcb().get_priority()
        return candidate.get_priority() < curr_pcb_prior
