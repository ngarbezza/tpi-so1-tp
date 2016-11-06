'''
Created on 17/12/2009
@author: Nahuel
'''
from oslogging.Logger import Logger

class ProcessKiller():
    '''
    Singleton class that kill process.
    
    @cvar __instance: the instance, necessary to implement the Singleton.
    @ivar _banker: the banker algorithm, that store information of the process.
    @ivar _store: the process store, where resides all the processes. 
    '''
    __instance = None
    
    @classmethod
    def __new__(cls, *args, **kwargs): 
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
    
    @classmethod
    def get_instance(cls):
        '''Getter of the unique instance.'''
        return cls.__instance
        
    def __init__(self, banker, store):
        '''Constructor of ProcessKiller.'''
        self._banker = banker
        self._store = store
    
    def get_banker(self):
        '''Getter of _banker.'''
        return self._banker
    
    def get_process_store(self):
        '''Getter of _store.'''
        return self._store
    
    def set_process_store(self, store):
        self._store = store
        
    def set_banker(self, banker):
        self._banker = banker
    
    def kill_pcb(self, pcb):
        '''Delete all the references and the data of the PCB given.'''
        self.get_banker().process_finished(pcb.get_pid())
        self.get_process_store().kill_pid(pcb.get_pid())
        Logger.get_instance().log_killprocess(pcb)
