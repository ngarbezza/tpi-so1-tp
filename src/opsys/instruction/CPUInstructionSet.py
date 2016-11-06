'''
Created on 15/11/2009
@author: Nahuel
'''

from opsys.instruction.InstructionSet import InstructionSet
from opsys.memory.Memory import Memory

class CPUInstructionSet(InstructionSet):
    '''
    Defines the functions that a CPU can do and execute them.
    
    @ivar _cpu: the CPU, in which get the registers values.
    '''
    def __init__(self, cpu):
        '''Constructor of CPUInstructionSet.'''
        self._cpu = cpu
        
    def get_cpu(self):
        '''Getter of _cpu.'''
        return self._cpu
    
    def request(self, *args):
        '''Do nothing because Banker process the request.'''
        pass
    
    def mov(self, *args):
        '''
        Instruction for data moving.
        
        @param args: tuple with PCB, destination and source of the mov.
        '''
        mem = Memory.get_instance()
        args[1].do_mov(args[0], args[2], self.get_cpu().get_registers(), mem)
    
    def add(self, *args):
        '''
        Instruction for data adding. Concatenation in Strings.
        
        @param args: tuple with PCB and the instruction arguments.
        '''
        mem = Memory.get_instance()
        args[1].do_add(args[0], args[2], self.get_cpu().get_registers(), mem)
    
    def sub(self, *args):
        '''
        Instruction for data substract. Not implemented in Strings.
        
        @param args: tuple with PCB and the instruction arguments.
        '''
        mem = Memory.get_instance()
        args[1].do_sub(args[0], args[2], self.get_cpu().get_registers(), mem)
    
    def skip(self, *args):
        '''Instruction specially designed for do nothing.'''
        pass