'''
Created on 27/11/2009
@author: Nahuel
'''

class Instruction():
    '''
    Represents the instructions, executed by the OS.
    
    @ivar _func_name: the function name.
    @ivar _args: list with the function arguments.
    @ivar _device: the device that perform the instruction. Ex: 'cpu'.
    @ivar _time: the wait time for the instruction.
    '''
    def __init__(self, nameF, args, dev, time):
        '''Constructor of Instruction.'''
        self._func_name = nameF
        self._args = args
        self._device = dev
        self._time = time
    
    def get_device(self):
        '''Getter of _device.'''
        return self._device
    
    def get_time(self):
        '''Getter of _time.'''
        return self._time

    def get_func_name(self):
        '''Getter of _func_name.'''
        return self._func_name
    
    def get_args(self):
        '''Getter of _args.'''
        return self._args
    
    def get_args_as_int(self):
        '''Convert to int the arguments and returns them.'''
        res = []
        for a in self.get_args():
            res.append(a.get_value())
        return res
    
    def is_cpu_inst(self):
        '''Returns if the instruction is of CPU.'''
        return self.get_device() == 'cpu'
    
    def is_io_inst(self):
        '''Returns if the instruction is of I/O.'''
        return not self.is_cpu_inst()
    
    def is_request(self):
        '''Returns if the instruction is a request.'''
        return self._func_name == 'request'
    
    def is_free(self):
        '''Returns if the instruction is a free.'''
        return self._func_name == 'free'