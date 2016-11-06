'''
Created on 27/11/2009
@author: Nahuel
'''

class ProcessStore():
    '''
    This class contains all the process data.
    
    @ivar _work_queue: here are the process recently created, with state 'new'
        and waiting for long-term scheduler.
    @ivar _ready_queue: here are the process with state 'ready' waiting to be 
        dispatched by the short-term scheduler.
    @ivar _all_process: all the process in the system. 
    '''
    def __init__(self):
        '''Constructor of ProcessStore.'''
        self._all_process = []
        self._ready_queue = []
        self._work_queue = []
        
    def get_all_process(self):
        '''Getter of _all_process.'''
        return self._all_process
    
    def get_ready_queue(self):
        '''Getter of _ready_queue.'''
        return self._ready_queue
    
    def get_work_queue(self):
        '''Getter of _work_queue.'''
        return self._work_queue
    
    def work_queue_is_empty(self):
        return not self.get_work_queue()
                        
    def ready_queue_is_empty(self):
        return not self.get_ready_queue()
    
    def work_to_ready_queue(self, proc):
        '''
        Move a process from work queue to ready queue.
        
        @param proc: the process to be moved.
        @precondition: the process 'proc' is in the work queue.
        '''
        for p in self.get_work_queue():
            if p == proc:
                self.put_in_ready_queue(p)
                self.get_work_queue().remove(p)
                
    def put_in_ready_queue(self, proc):
        proc.set_state('Ready')
        self.get_ready_queue().append(proc)
    
    def kill_pcb(self, pcb):
        self.kill_pid(pcb.get_pid())
    
    def kill_pid(self, pid):
        '''Delete all the references to the process with pid 'pid'.'''
        for p in self.get_all_process():
            if p.get_pid() == pid : 
                self.get_all_process().remove(p)
                break
        for p in self.get_work_queue():
            if p.get_pid() == pid : 
                self.get_all_process().remove(p)
                break
        for p in self.get_ready_queue():
            if p.get_pid() == pid : 
                self.get_all_process().remove(p)
                break
    
    def put_in_work_queue(self, proc):
        self.get_work_queue().append(proc)
    
    def put_in_all_process(self, proc):
        self.get_all_process().append(proc)
        
    def exists_pid(self, pid):
        for p in self.get_all_process():
            if p.get_pid() == pid: 
                return True
        return False
    
    def remove_all_process(self):
        '''Clear all the data in the store.'''
        self._all_process = []
        self._ready_queue = []
        self._work_queue = []