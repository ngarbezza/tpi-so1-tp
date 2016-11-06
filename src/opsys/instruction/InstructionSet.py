'''
Created on 19/11/2009
@author: Nahuel
'''

import time

class InstructionSet():
    '''
    Abstract class that represents the set of instructions appropiate
    for each kind of device (includes CPU).
    '''
    def execute(self, inst, pcb):
        '''Run the code of the instruction and wait its corresponding time.'''
        time.sleep(inst.get_time())
        return getattr(self, inst.get_func_name())(*[pcb] + inst.get_args())