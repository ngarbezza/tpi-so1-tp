'''
Created on 19/11/2009
@author: Nahuel
'''

from opsys.instruction.InstructionSet import InstructionSet
from opsys.memory.Memory import Memory

class DisplayInstructionSet(InstructionSet):
    '''Define and execute the operations available for Display Device.'''
    def show(self, *args):
        '''Print in screen instruction.'''
        pcb = args[0]
        for arg in args:
            if not arg == pcb: 
                arg.do_show(pcb, Memory.get_instance())
          
class KeyboardInstructionSet(InstructionSet):
    '''Contains functions appropriate with keyboard devices.'''
    def input(self, *args):
        '''Open a screen and request a string.'''
        args[2].do_input(args[0], args[1], Memory.get_instance(), False)
    
    def intinput(self, *args):
        '''Open a screen and request a integer.'''
        args[2].do_input(args[0], args[1], Memory.get_instance(), True)