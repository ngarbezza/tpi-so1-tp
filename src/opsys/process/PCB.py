'''
Created on 14/11/2009
@author: Nahuel
'''

from exceptions.OSException import OSException
from opsys.memory.Memory import Memory

class PCB():
    '''
    The process control block.
    
    @ivar _priority: the priority in range 1-10. Less number, more priority.
    @ivar _pc: the Program Counter.
    @ivar _state: string with the state of the process.
    @ivar _process: the process related.
    @ivar _pid: the ID that identify the process in the system.
    @ivar _registers: keep the values of CPU registers.
    @ivar _io_perc: use percentage of I/O.
    @ivar _remaining_time: time before the process finish.
    @ivar _next_burst: the next CPU burst. Used by the schedulers.
    @ivar _mem_parameters: defines addressing space for the process.
        Contain a pair with (base register, limit register).
    @ivar _current_dir: the current directory used by the process.
        Initially start at root (/) directory.
    @ivar _files_opened: references file:memaddress of all files opened.
    '''
    def __init__(self, pid, prior, process, base_reg, address_space):
        '''Constructor of Process Control Block.'''
        self._priority = prior
        self._pc = 0
        self._state = 'New'
        self._process = process
        self._pid = pid
        self._registers = self.__init_registers()
        self._io_perc = 0
        self._remaining_time = 0
        self._next_burst = 0 
        self._mem_parameters = (base_reg, base_reg + address_space)
        self._current_dir = ('/', 0)        #dir name, position in disk 
        self._files_opened = {}             #dict of fileName:memory address
        
    def get_cwd(self):
        '''Getter of _current_dir.'''
        return self._current_dir
    
    def get_files_opened(self):
        '''Getter of _files_opened.'''
        return self._files_opened
    
    def add_file(self, path, mem_pos):
        '''Add a file to the opened files dictionary.'''
        self._files_opened[path] = mem_pos
    
    def remove_file(self, path):
        '''Remove a file path from the opened files dictionary.'''
        del self._files_opened[path]

    def set_cwd(self, dir):
        '''Setter of _current_dir.'''
        self._current_dir = dir
    
    def get_base_reg(self):
        '''Get the base register.'''
        return self._mem_parameters[0]
    
    def get_limit_reg(self):
        '''Get the limit register.'''
        return self._mem_parameters[1]
    
    def get_priority(self):
        '''Getter of _priority.'''
        return self._priority

    def get_pc(self):
        '''Getter of _pc.'''
        return self._pc
    
    def get_name(self):
        return self.get_process().get_name()
    
    def get_process(self):
        '''Getter of _process.'''
        return self._process
    
    def get_state(self):
        '''Getter of _state.'''
        return self._state
    
    def get_pid(self):
        '''Getter of _pid.'''
        return self._pid
    
    def get_next_burst(self):
        '''Setter of _next_burst.'''
        return self._next_burst
    
    def __lt__(self, another_pcb):
        '''Used to order the process by its priority.'''
        return self.get_priority() < another_pcb.get_priority()
    
    def set_next_burst(self, the_burst):
        '''Setter of _next_burst.'''
        self._next_burst = the_burst
    
    def set_priority(self, prior):
        '''Setter of _priority.'''
        if prior not in range(1, 11):
            raise OSException('Error: Wrong process priority')
        else:
            self._priority = prior
    
    def set_state(self, state):
        '''Setter of _state.'''
        if state not in ['New', 'Ready', 'Running', 'Waiting', 'Finished']:
            raise OSException('Error: Wrong process state')
        else:
            self._state = state
    
    def set_pc(self, pc):
        '''Setter of _pc.'''
        if pc > len(self.get_process().get_instructions()):
            raise OSException('Error: Program Counter out of bounds')
        else:
            self._pc = pc
    
    def inc_pc(self):
        '''Increment by one the PC. Used to progress in the instructions.'''
        self.set_pc(self.get_pc() + 1)
    
    def dec_pc(self):
        '''Decrement by one the pc. Used for control of some methods.'''
        self.set_pc(self.get_pc() - 1)
    
    def get_next_inst(self):
        '''Obtains the next instruction to execute, determined by the PC.'''
        return self.get_process().get_instructions()[self.get_pc()]
    
    def in_ready_state(self):
        '''Checks if the process is in ready state.'''
        return self.get_state() == 'Ready'
    
    def get_remaining_time(self):
        '''Getter of _remaining_time.'''
        return self._remaining_time
    
    def set_remaining_time(self, the_time):
        '''Setter of _remaining_time.'''
        self._remaining_time = the_time
        
    def get_io_perc(self):
        '''Getter of _io_perc.'''
        return self._io_perc
    
    def set_io_perc(self, the_perc):
        '''Setter of _io_perc.'''
        self._io_perc = the_perc
        
    def finished(self):
        '''Checks if the process has executed all its instructions.'''
        return self.get_pc() >= len(self.get_process().get_instructions())
        
    def get_instruction_at(self, pos):
        '''Obtains the instruction at a given position.'''
        return self.get_process().get_instructions()[pos]
    
    def get_registers(self):
        '''Getter of _registers.'''
        return self._registers
    
    def set_registers(self, regs):
        '''Setter of _registers.'''
        self._registers = regs
    
    def __init_registers(self):
        '''Initialize the registers, with default value '0'.'''
        return {'R0': 0,'R1': 0,'R2': 0,'R3': 0,'R4': 0,'R5': 0,'R6': 0,'R7': 0}
    
    def get_file_at(self, path):
        '''Search for a opened file.'''
        return Memory.get_instance().get_value_at(self.get_files_opened()[path])