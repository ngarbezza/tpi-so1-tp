'''
Created on 01/12/2009
@author: Nahuel
'''

from opsys.scheduling.Scheduler import Scheduler

class SJFSchedulerNoExp(Scheduler):
    '''Shortest Job First scheduling politic (not expropiative version).'''
    def __init__(self, cpu, proc_store):
        '''Constructor of SJFSchedulerNoExp.'''
        Scheduler.__init__(cpu, proc_store)
        
    def get_next_pcb_dont_remove(self):
        '''
        Choose the PCB with shortest CPU burst.
        
        @precondition: the ready queue has at least one process.
        '''
        chosen = self.get_process_store().get_ready_queue()[0]
        for pcb in self.get_process_store().get_ready_queue():
            if pcb.get_next_burst() < chosen.get_next_burst(): 
                chosen = pcb
        return chosen

    def get_next_pcb(self):
        pcb = self.get_next_pcb_dont_remove()
        self.get_process_store().get_ready_queue().remove(pcb)
        return pcb
        
class SJFSchedulerExp(SJFSchedulerNoExp):
    '''Shortest Job First scheduling politic (expropiative version).'''
    def __init__(self, cpu, proc_store):
        '''Constructor of SJFSchedulerExp.'''
        SJFSchedulerNoExp.__init__(cpu, proc_store)
    
    def have_to_expropiate(self):
        '''
        Happen when the shortest burst in the work queue is less than the
        current cpu process burst.
        '''
        curr_cpu_burst = self.get_cpu().get_current_pcb().get_next_burst()
        return self.get_next_pcb_dont_remove().get_next_burst() < curr_cpu_burst
