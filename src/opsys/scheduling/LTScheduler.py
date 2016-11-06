'''
Created on 19/11/2009
@author: Nahuel
'''

from opsys.osconfig import SCHEDULER, LTS_SLEEP_TIME
import time

class LTScheduler(object):
    '''
    Implements the Long-Term Scheduling politic.
        
    @ivar _proc_store: the process store, where the scheduler 
        takes the processes.
    @ivar _active: indicates activity in the scheduler.
    '''
    def __init__(self, proc_store):
        '''Constructor of LTScheduler.'''
        self._proc_store = proc_store
        self._active = False
        
    def get_process_store(self):
        '''Getter of _proc_store.'''
        return self._proc_store
    
    def set_process_store(self, store):
        self._proc_store = store
    
    def is_active(self):
        '''Checks if the scheduler is running.'''
        return self._active
    
    def set_active(self):
        '''Set activity in the scheduler.'''
        self._active = True
        
    def set_inactive(self):
        '''Stop the activity of the scheduler.'''
        self._active = False
    
    def start(self):
        '''
        Thread that puts process from work queue to ready queue, checks first
        if it's using priority scheduling, if not, calculate the I/O use
        average, and then decides what process goes into ready queue.
        '''
        self.set_active()
        while self.is_active():
            if not self.get_process_store().work_queue_is_empty():
                if SCHEDULER == 'Priority-No-Exp' or \
                   SCHEDULER == 'Priority-Exp':
                    chosen = self.get_max_priority_process()
                    self.get_process_store().work_to_ready_queue(chosen)
                elif self.compute_avg_io_perc() < 50:
                    chosen = self.get_cpu_oriented_process()
                    self.get_process_store().work_to_ready_queue(chosen)
                else: 
                    chosen = self.get_io_oriented_process()
                    self.get_process_store().work_to_ready_queue(chosen)
            time.sleep(LTS_SLEEP_TIME)
        self.set_inactive() 
    
    def compute_avg_io_perc(self):
        '''
        Updates (if necessary) the I/O percentage for all process
        in the operating system and returns the average of them.
        '''
        res = 0
        count = 0
        for proc in self.get_process_store().get_all_process():
            if proc.in_ready_state():
                proc.set_io_perc(self.compute_io_perc(proc))
            res += proc.get_io_perc()
            count += 1
        return res / count
    
    def compute_io_perc(self, proc):
        '''Returns the I/O use percentage of a process.'''
        total_io = 0
        inst = proc.get_instructions()
        for i in range(proc.get_pcb().get_pc(), len(inst)):
            if inst[i].is_io_inst():
                total_io += inst[i].get_time()
        try:
            return total_io * 100 / proc.get_remaining_time()
        except ZeroDivisionError:
            return 0
    
    def total_time_for_new_process(self, p):
        '''Returns the total time for a process newly created.'''
        total = 0
        for i in p.get_instructions(): total += i.get_time()
        return total
    
    def get_cpu_oriented_process(self):
        '''
        Gets a process with more CPU use than I/O use.
        
        @precondition: the work queue is not empty. 
        '''
        return self.get_oriented_process(lambda x,y : x < y)
    
    def get_io_oriented_process(self):
        '''
        Gets a process with more CPU use than I/O use.
        
        @precondition: the work queue is not empty.
        '''
        return self.get_oriented_process(lambda x,y : x > y)
    
    def get_oriented_process(self, compare):
        '''
        Generic method to get CPU and I/O oriented process.
        
        @param compare: comparing function.
        '''
        res_p = self.get_process_store().get_work_queue()[0]
        for p in self.get_process_store().get_work_queue():
            if compare(p.get_io_perc(), res_p.get_io_perc()): 
                res_p = p
        return res_p
    
    def get_max_priority_process(self):
        '''
        Get the process with more priority in the work queue.
        
        @precondition: the work queue has at least one process.
        '''
        return min(self.get_process_store().get_work_queue())