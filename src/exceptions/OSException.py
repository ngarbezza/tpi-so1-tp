'''
Created on 12/11/2009
@author: Nahuel
'''

class OSException(Exception):
    '''
    Represents all the exceptions that raises the operating system 
    and its devices.
    
    @ivar args: The exception's arguments.
    '''
    def __init__(self, arg):
        '''hola'''
        self.args = [arg]