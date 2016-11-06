'''
Created on 12/12/2009
@author: Nahuel
'''

from opsys.instruction.Parameter import Parameter
from exceptions.OSException      import OSException

class String(Parameter):
    '''A Parameter (specifically a String).'''
    def __init__(self, the_value):
        Parameter.__init__(self, the_value)
    
    def __repr__(self):
        return '"' + self.get_value() + '"' 
    
    def do_mov(self, pcb, another_parameter, cpu_regs, mem):
        '''
        Operation for data moving, impossible to implement in String.
        
        @raise OSException: can't store in a value !!
        '''
        raise OSException("Error: cant' mov (store) a value in a value !!")
    
    def do_mov_in_register(self, pcb, reg, cpu_regs, mem):
        '''
        Copies its own contents into a register specified.
        Example: mov R6, "hola"
        '''
        cpu_regs[reg.get_value()] = self.get_value()
    
    def do_mov_in_mem_cell(self, pcb, mem_cell, cpu_regs, mem):
        '''
        Copies its own contents in a memory address specified.
        Example: mov #18, "hola".
        '''
        mem.store_at_relative(pcb, mem_cell.get_value(), self.get_value())

    def do_add(self, pcb, another_parameter, cpu_regs, mem):
        '''
        Operation for data adding, impossible to implement by String as a 
        first argument.
        
        @raise OSException: can't store in a value !!
        '''
        raise OSException("Error: can't add and then store in a value !!")
    
    def do_add_in_register(self, pcb, reg, cpu_regs, mem):
        '''
        Add its own contents to the register given and store
        the result in the register.
        '''
        cpu_regs[reg.get_value()] = cpu_regs[reg.get_value()] + self.get_value()
    
    def do_add_in_mem_cell(self, pcb, mem_cell, cpu_regs, mem):
        '''
        Add its own contents to the memory address given and store
        the result in the memory address.
        '''
        res = mem.get_value_at_relative(pcb, mem_cell.get_value()) + self.get_value()
        mem.store_at_relative(pcb, mem_cell.get_value(), res)
        
    def do_sub(self, pcb, another_parameter, cpu_regs, mem):
        '''
        Operation for data substract, impossible to implement by String as a 
        first argument.
        
        @raise OSException: can't store in a value !!
        '''
        raise OSException("Error: can't sub and then store in a value !!")
    
    def do_sub_in_register(self, pcb, reg, cpu_regs, mem):
        '''
        Operation for data substract, impossible to implement by String
        
        @raise OSException: can't store in a value !!
        '''
        raise OSException("Error: can't sub a String !!")
    
    def do_sub_in_mem_cell(self, pcb, mem_cell, cpu_regs, mem):
        '''
        Operation for data substract, impossible to implement by String.
        
        @raise OSException: can't store in a value !!
        '''
        raise OSException("Error: can't sub a String !!")
    
    def do_show(self, pcb, memory):
        '''Print on screen its own value.'''
        print(self.get_value())
    
    def get_write_data(self, pcb):
        '''Returns the data for a write operation (as a string).'''
        return self.get_value()