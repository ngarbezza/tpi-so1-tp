'''
Created on 28/11/2009
@author: Nahuel
'''

from parsing.pyparsing_py3 import oneOf, Word, Group, ZeroOrMore, OneOrMore, \
    Suppress, alphas, nums, restOfLine, alphanums
from opsys.instruction.Instruction import Instruction
from opsys.process.Process import Process
from opsys.instruction.MemoryCell import MemoryCell
from opsys.instruction.Number import Number
from opsys.instruction.Register import Register
from opsys.instruction.String import String
from opsys.osconfig import MAX_OPENED_FILES, DEVICES, INST_MAP, ADDRESS_SPACE

class OSParser(object):
    '''
    Parse strings to generate processes, and instructions.
    
    @ivar _process_grammar: contains the mechanism to decode the strings.
    @ivar _request_order: internal representation to keep the order of 
        the requests.
    @ivar _pid_count: generates always new process ID's.
    @ivar _next_mem_assign: generates new address space for new processes.
    '''
    def __init__(self):
        '''Constructor of OSParser.'''
        self._process_grammar = self.__init_process_grammar()
        self._request_order = list(DEVICES.keys())
        self._pid_count = 1
        self._next_mem_assign = MAX_OPENED_FILES + 1
        
    def __init_process_grammar(self):
        '''Defines the grammar for creating process from strings.'''
        lista_inst = list(INST_MAP.keys())           #function names
        regs = oneOf(['R0','R1','R2','R3','R4','R5','R6','R7'])
        conv_to_register = lambda s,l,t : Register(t[0])
        regs.setParseAction(conv_to_register)
        string = Suppress('"') + Word(alphanums + " ./") + Suppress('"')
        conv_to_string = lambda s,l,t : String(t[0])
        string.setParseAction(conv_to_string)
        mem_cell = Suppress('#') + Word(nums)        #memory address
        conv_to_memcell = lambda s,l,t : MemoryCell(int(t[0]))
        mem_cell.setParseAction(conv_to_memcell)
        conv_to_num = lambda s,l,t : Number(int(t[0]))
        number = Word(nums).setParseAction(conv_to_num)
        parameter = regs | number | string | mem_cell
        instruction = Group(oneOf(lista_inst) + ZeroOrMore(parameter))
        instList = Group(OneOrMore(instruction))
        proc_name = Suppress('Name : ') + Word(alphas)
        proc_prior = Suppress('Priority : ') + Word(nums)
        process = proc_name + proc_prior + instList
        process.ignore('--' + restOfLine)            #represents comments
        return process
    
    def get_pid_count(self):
        '''Get a new pid, alwaws incrementing by one.'''
        self._pid_count += 1
        return self._pid_count
    
    def get_request_order(self):
        '''Getter of _request_order.'''
        return self._request_order
    
    def parse(self, str_prog):
        '''
        Receives a raw string and return a Process by parsing with
        the grammar defined.
        '''
        tokens = self._process_grammar.parseString(str_prog)
        return self.create_process_from(tokens)
    
    def create_process_from(self, tokens):
        '''
        Iterate over the tokens given, and make instructions,
        and then a process.
        '''
        name = tokens[0]
        prior = int(tokens[1])
        inst_list = []
        for t in tokens[2]:
            func_name = t.pop(0)
            if func_name == 'request': 
                params = self.make_request(t)
            else:
                params = [] 
                for param in t: 
                    params.append(param)
            dev = self.get_dev_for(func_name)
            time = self.get_time_for(func_name)
            inst_list.append(Instruction(func_name, params, dev, time))
        pid = self.get_pid_count()
        mem_space = self.get_next_mem_assign()
        return Process(pid, name, prior, inst_list, mem_space, ADDRESS_SPACE)
 
    def get_next_mem_assign(self):
        res = self._next_mem_assign
        self._next_mem_assign += ADDRESS_SPACE
        return res
    
    def make_request(self, tok):
        '''
        Receive a token of a 'request' instruction. Create the correct
        request that cpu (and banker) understands. Only create the arguments. 
        Example:
            request 1 "display"  can be translated to:
            request 0 1 0,
        depending of the request order defined.
        '''
        params = [Number(0)] * len(DEVICES)       #how many resources
        for i in range(0, len(tok), 2):
            #note that assume even number of tok's elements
            index = self.get_request_order().index(tok[i + 1].get_value())
            params[index] = tok[i] #put only the number in the arguments' list
            i += 2                 #increment counter
        return params
        
    def get_time_for(self, func_name):
        '''Search for a function name, and returns its time.'''
        return INST_MAP[func_name][1]
    
    def get_dev_for(self, func_name):
        '''Search for a function name, and returns its device.'''
        return INST_MAP[func_name][0]
    
    def reset(self):
        self._pid_count = 1
        self._next_mem_assign = MAX_OPENED_FILES + 1