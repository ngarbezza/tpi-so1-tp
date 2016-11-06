'''
Created on 12/12/2009
@author: Nahuel
'''

from exceptions.OSException import OSException
from oslogging.Logger import Logger

class Memory(object):
    '''
    Singleton class. Represents the memory (primary storage) in the system. 
    All process can write in memory, and also the file manager.
    
    @cvar __instance: the unique instance necessary to implement the Singleton.
    @ivar _data: dictionary with all the data address:value.
    '''
    __instance = None
    
    @classmethod
    def __new__(cls, *args, **kwargs):
        '''
        Redefines the constructor to make sure that you can't create 
        more than one instance.
        ''' 
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
    
    @classmethod
    def get_instance(cls):
        '''Class method. return the unique instance.'''
        return cls.__instance
    
    def __init__(self):
        '''Constructor of Memory.'''
        self._data = {}
        
    def get_value_at(self, address):
        '''Returns the value stored in the position 'address'.'''
        try:
            return self._data[address]
        except KeyError:        #There's nothing in the memory
            return None
        
    def store_at(self, address, value):
        '''Store a value given in an address given.'''
        self._data[address] = value
        Logger.get_instance().write('Memory store at #' \
                + str(address) + ' the value ' + value.__repr__())
    
    def __get_and_check_real_address(self, pcb, address):
        '''
        Checks if an address is valid to the pcb given.
        If it's valid, returns it.
        '''
        real_address = pcb.get_base_reg() + address
        if real_address > pcb.get_limit_reg(): 
            raise OSException("Error: Process out of addressing space")
        else: 
            return real_address
        
    def get_value_at_relative(self, pcb, address):
        '''
        Receive an address relative to the pcb. Memory computes the
        real direction by adding the address to the pcb's base register.
        if the real direction exceed the limit register, raise an error.
        '''
        real_address = self.__get_and_check_real_address(pcb, address)
        return self.get_value_at(real_address)
    
    def store_at_relative(self, pcb, address, value):
        '''
        Receive an address relative to the pcb. Memory computes the
        real direction by adding the address to the pcb's base register.
        if the real direction exceed the limit register, raise an error.
        Store in the real address a value given.
        '''
        self.store_at(self.__get_and_check_real_address(pcb, address), value)
    
    def remove(self, k):
        '''Remove a cell making more dynamic the storage.'''
        del self._data[k]
    
    def clear_all(self):
        '''Erases all the data in the memory.'''
        self._data = {}