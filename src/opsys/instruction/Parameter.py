'''
Created on 12/12/2009
@author: Nahuel
'''
from exceptions.OSException import OSException

class Parameter():
    '''
    Abstract class, represents possible parameters in a instruction.
    
    @ivar value: the contents, information of the parameter.
    '''
    def __init__(self, the_value):
        ''' Constructor of Parameter.'''
        self.value = the_value
        
    def get_value(self):
        '''Getter of value.'''
        return self.value
    
    def set_value(self, the_value):
        '''Setter of value.'''
        self.value = the_value
    
    def do_mov(self, pcb, another_parameter, cpu_regs, mem):
        '''Subclass responsibility.'''
        pass
    
    def do_mov_in_register(self, pcb, reg, cpu_regs, mem):
        '''Abstract method'''
        pass
    
    def do_mov_in_mem_cell(self, pcb, mem_cell, cpu_regs, mem):
        '''Abstract method'''
        pass

    def do_add(self, pcb, another_parameter, cpu_regs, mem):
        '''Subclass responsibility.'''
        pass
    
    def do_add_in_register(self, pcb, reg, cpu_regs, mem):
        '''Abstract method'''
        pass
    
    def do_add_in_mem_cell(self, pcb, reg, cpu_regs, mem):
        '''Abstract method'''
        pass
    
    def do_sub(self, pcb, another_parameter, cpu_regs, mem):
        '''Subclass responsibility.'''
        pass
    
    def do_sub_in_register(self, pcb, reg, cpu_regs, mem):
        '''Abstract method'''
        pass
    
    def do_sub_in_mem_cell(self, pcb, reg, cpu_regs, mem):
        '''Abstract method'''
        pass
    
    def do_show(self, pcb, mem):
        '''Abstract method'''
        pass
    
    def do_input(self, pcb, message, mem):
        '''@raise OSException: because only can store in memory.'''
        raise OSException("Error: Input - Only can store in memory.")
    
    def do_intinput(self, pcb, message, mem, using_int):
        '''@raise OSException: because only can store in memory.'''
        raise OSException("Error: Input - Only can store in memory.")