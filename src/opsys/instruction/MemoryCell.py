'''
Created on 12/12/2009
@author: Nahuel
'''

from opsys.instruction.Parameter import Parameter
from tkinter.simpledialog import *                  #@UnusedWildImport
from opsys.memory.Memory import Memory

class MemoryCell(Parameter):
    '''A parameter (specifically a MemoryCell).'''
    def __init__(self, the_value):
        '''Constructor of MemoryCell.'''
        Parameter.__init__(self, the_value)
    
    def __repr__(self):
        return '#' + str(self.get_value())
    
    def do_mov(self, pcb, another_parameter, cpu_regs, memory):
        '''Double dispatching method.'''
        another_parameter.do_mov_in_mem_cell(pcb, self, cpu_regs, memory)
    
    def do_mov_in_register(self, pcb, reg, cpu_regs, mem):
        '''
        The second argument is a register, and self is a memory address.
        Copy the value at the memory address specified into the register.
        Example: mov R6, #32
        '''
        cpu_regs[reg.get_value()] = mem.get_value_at_relative(pcb, self.get_value())
    
    def do_mov_in_mem_cell(self, pcb, mem_cell, cpu_regs, mem):
        '''
        The second argument is a memory address, and self too.
        Copy the value at the mem address specified into the first mem address.
        Example: mov #7, #32.
        '''
        mem_add = mem.get_value_at_relative(pcb, self.get_value())
        mem.store_at_relative(pcb, mem_cell.get_value(), mem_add)

    def do_add(self, pcb, another_parameter, cpu_regs, mem):
        '''Double dispatching method.'''
        another_parameter.do_add_in_mem_cell(pcb, self, cpu_regs, mem)
    
    def do_add_in_register(self, pcb, reg, cpu_regs, mem):
        '''
        Add the contents of self (memory) with the register received
        and store the result in this register.
        '''
        mem_add = mem.get_value_at_relative(pcb, self.get_value())
        cpu_regs[reg.get_value()] = cpu_regs[reg.get_value()] + mem_add
    
    def do_add_in_mem_cell(self, pcb, mem_cell, cpuRegisters, mem):
        '''
        Sub the contents of self (memory) with an address received
        and store the result in this memory address.
        '''
        self_value = mem.get_value_at_relative(pcb, self.get_value())
        other_value = mem.get_value_at_relative(pcb, mem_cell.get_value())
        mem.store_at_relative(pcb, mem_cell.get_value(), other_value + self_value)

    def do_sub(self, pcb, another_parameter, cpu_regs, mem):
        '''Double dispatching method.'''
        another_parameter.do_sub_in_mem_cell(pcb, self, cpu_regs, mem)
    
    def do_sub_in_register(self, pcb, reg, cpu_regs, mem):
        '''
        Sub the contents of self (memory) with the register received
        and store the result in this register.
        '''
        mem_sub = mem.get_value_at_relative(pcb, self.get_value())
        cpu_regs[reg.get_value()] = cpu_regs[reg.get_value()] - mem_sub
    
    def do_sub_in_mem_cell(self, pcb, mem_cell, cpu_regs, mem):
        '''
        Sub the contents of self (memory) with an address received
        and store the result in this memory address.
        '''
        self_value = mem.get_value_at_relative(pcb, self.get_value())
        other_value = mem.get_value_at_relative(pcb, mem_cell.get_value())
        mem.store_at_relative(pcb, mem_cell.get_value(), other_value - self_value)
        
    def do_show(self, pcb, mem):
        '''Print on screen the value of self.'''
        print(mem.get_value_at_relative(pcb, self.get_value()))
    
    def do_input(self, pcb, message, memory, using_int):
        '''
        Open a window and prompt with a message requesting some data.
        Save the data in the address specified by self.
        
        @param using_int: boolean that indicates if the result have to be
            saved as a integer.
        @note: overrides the definition in Parameter
        '''
        p = Tk()            #create the main window
        p.withdraw()        #hide it (don't care, only cares the dialog)
        res = askstring('Input', message.get_value(), parent = p)
        if using_int:
            if res is None:
                res = 0
            memory.store_at_relative(pcb, self.get_value(), int(res))
            p.destroy()
            return
        elif res is None: 
            res = ''
        memory.store_at_relative(pcb, self.get_value(), res)
        p.destroy()         #close all widgets
        
    def get_write_data(self, pcb):
        '''Get the data for a write operation (as a string).'''
        mem = Memory.get_instance()
        return str(mem.get_value_at_relative(pcb, self.get_value()))
        