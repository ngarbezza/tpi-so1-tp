'''
Created on 12/12/2009
@author: Nahuel
'''

from opsys.instruction.Parameter import Parameter
from exceptions.OSException import OSException

class Register(Parameter):
    '''A parameter (specifically a Register).'''
    def __init__(self, the_value):
        '''Constructor of Register.'''
        Parameter.__init__(self, the_value)
    
    def __repr__(self):
        return self.get_value()
    
    def do_mov(self, pcb, another_parameter, cpu_regs, mem):
        '''Double dispatching method.'''
        another_parameter.do_mov_in_register(pcb, self, cpu_regs, mem)
    
    def do_mov_in_register(self, pcb, reg, cpu_regs, mem):
        '''
        Copies the contents of its own value into the register received.
        Example: mov R6, R3.
        '''
        cpu_regs[reg.get_value()] = cpu_regs[self.get_value()]
    
    def do_mov_in_mem_cell(self, pcb, mem_cell, cpu_regs, mem):
        '''
        Copy the value at the register into the memory address.
        Example: mov #22, R1
        '''
        mem.store_at_relative(pcb, mem_cell.get_value(), cpu_regs[self.get_value()])

    def do_add(self, pcb, another_parameter, cpu_regs, mem):
        '''Double dispatching method.'''
        another_parameter.do_add_in_register(pcb, self, cpu_regs, mem)
    
    def do_add_in_register(self, pcb, reg, cpu_regs, mem):
        self_value = cpu_regs[self.get_value()]
        cpu_regs[reg.get_value()] = cpu_regs[reg.get_value()] + self_value
    
    def do_add_in_mem_cell(self, pcb, mem_cell, cpu_regs, mem):
        reg_value = cpu_regs[self.get_value()]
        mem_value = mem.get_value_at_relative(pcb, mem_cell.get_value()) + reg_value 
        mem.store_at_relative(pcb, mem_cell.get_value(), mem_value)
    
    def do_sub(self, pcb, another_parameter, cpu_regs, mem):
        '''Double dispatching method.'''
        another_parameter.do_sub_in_register(pcb, self, cpu_regs, mem)
    
    def do_sub_in_register(self, pcb, reg, cpu_regs, mem):
        self_value = cpu_regs[self.get_value()]
        cpu_regs[reg.get_value()] = cpu_regs[reg.get_value()] - self_value 
    
    def do_sub_in_mem_cell(self, pcb, mem_cell, cpu_regs, mem):
        reg_value = cpu_regs[self.get_value()]
        mem_value = mem.get_value_at_relative(pcb, mem_cell.get_value()) - reg_value 
        mem.store_at_relative(pcb, mem_cell.get_value(), mem_value)

    def do_show(self, pcb, memory):
        raise OSException("Error: I/O operation with CPU registers.")
    
    def get_write_data(self, pcb):
        raise OSException("Error: I/O operation with CPU registers.")