'''
Created on 09/11/2009
@author: Nahuel
'''

class MatrixException(Exception):
    '''Represent Matrix and NDimMatrix Errors.'''
    def __init__(self, arg):
        self.args = [arg]