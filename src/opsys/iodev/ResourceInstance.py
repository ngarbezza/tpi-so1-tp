'''
Created on 19/11/2009
@author: Nahuel
'''
from opsys.osconfig import RES_INST_SLEEP_TIME
import time

class ResourceInstance():
    '''
    Represents a particular instance of a resource type.
    
    @ivar _dev_manager: the device manager.
    @ivar _pos: the position of the device manager's pool where takes
            the process to execute instructions.
    @ivar _name: the name of the instance. Example: 'display1'
    '''
    def __init__(self, dev_manager, pos, name):
        '''Constructor of ResourceInstance.'''
        self._dev_manager = dev_manager
        self._pos = pos
        self._name = name + str(pos)
            
    def get_device_manager(self):
        '''Getter of _dev_manager.'''
        return self._dev_manager
    
    def get_pos(self):
        '''Getter of _pos.'''
        return self._pos
    
    def there_is_a_process(self):
        '''
        Looks into the devManager's pool in order to take a process and
        execute its instructions.
        
        @rtype: Bool
        '''
        return self.get_device_manager().get_pool_at(self.get_pos()) is not None
    
    def start(self):
        '''Thread of the resource instance.'''
        while self.get_device_manager().is_active():
            if self.there_is_a_process():
                pos = self.get_pos()
                current_pcb  = self.get_device_manager().get_pool_at(pos)
                current_inst = current_pcb.get_next_inst()
                current_pcb.inc_pc()
                self.get_device_manager().execute(current_inst, current_pcb)
                dev = current_inst.get_device()
                if not dev == current_pcb.get_next_inst().get_device():
                    self.get_device_manager().process_finish_io(self.get_pos())
            time.sleep(RES_INST_SLEEP_TIME)