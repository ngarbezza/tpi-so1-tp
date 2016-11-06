'''
Created on 19/11/2009
@author: Nahuel
'''

from opsys.iodev.ResourceInstance import ResourceInstance
from thread.ThreadRunner import ThreadRunner

class IODeviceManager():
    '''
    Manager of I/O Devices.
    
    @ivar _pool_res: where the process come to execute I/O instructions.
    @ivar _res_instances: the particular instances of the resource.
    @ivar _inst_set: the instruction set of the particular I/O manager.
    @ivar _name: the name of the device.
    @ivar _activity: boolean that indicates activity on the device.
    @ivar _proc_store: all the process data.
    '''
    def __init__(self, name, num_res, inst_set_class, proc_store):
        '''
        Constructor of a I/O Device Manager.
        
        @param num_res: how many resource instances have the manager.
        @param name: the name of the device.
        @param inst_set_class: the classname of the instruction set.
        '''
        self._name = name
        self._activity = False
        self._proc_store = proc_store
        self._pool_res = [None]* num_res
        self._inst_set = inst_set_class()
        self._res_instances = []
        for i in range(num_res):
            self._res_instances.append(ResourceInstance(self, i, self._name))
    
    def get_process_store(self):
        '''Getter of _proc_store.'''
        return self._proc_store
    
    def set_process_store(self, store):
        self._proc_store = store
    
    def get_res_instances(self):
        '''Getter of _res_instances.'''
        return self._res_instances
    
    def __instance_at(self, pos):
        '''
        Gets a particular instance of all of its instances.
        
        @return: resource instance.
        @param pos: index of the instance in _res_instances.
        @note: private method.
        '''
        return self._res_instances[pos]
    
    def get_pool(self):
        '''Getter of _pool_res.'''
        return self._pool_res
    
    def get_pool_at(self, pos):
        '''
        Gets the process at a position in the pool.
        
        @return: PCB
        @param pos: the index of process' pool
        '''
        return self._pool_res[pos]
    
    def get_name(self):
        '''Getter of _name.'''
        return self._name
    
    def get_instruction_set(self):
        '''Getter of _ins_set.'''
        return self._inst_set

    def is_active(self):
        '''Getter of _activity.'''
        return self._activity
    
    def set_active(self):
        '''Set inactive to keep the instances running.'''
        self._activity = True
    
    def set_inactive(self):
        '''Set inactive to stop the activity of the instances.'''
        self._activity = False
    
    def start(self):
        '''Start all the instances.'''
        self.set_active()
        self.start_threads()
    
    def start_threads(self):
        '''Start one thread for each instance of the resource.'''
        for i in range(len(self.get_res_instances())):
            ti = ThreadRunner(self.__instance_at(i))
            ti.setDaemon(True)
            ti.start()
    
    def execute(self, inst, pcb):
        '''Tells to the instruction set that execute some instruction.'''
        self.get_instruction_set().execute(inst, pcb)
    
    def process_finish_io(self, pos):
        '''Manages the exit of a process.'''
        self.get_process_store().put_in_ready_queue(self.get_pool()[pos])
        self.get_pool()[pos] = None
        
    def add_process(self, proc):
        '''
        Receive a process and puts in the pool.
        
        @precondition: there is at least one free space in the pool.
            Guaranteed by the banker.
        '''
        proc.set_state('Waiting')
        for i in range(len(self.get_pool())):
            if self.get_pool()[i] is None:
                self.get_pool()[i] = proc
                break

    def shutdown(self):
        '''Stop the activity of the resource.'''
        self.set_inactive()
        for i in range(len(self.get_pool())):
            self.get_pool()[i] = None