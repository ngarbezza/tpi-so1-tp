'''
Created on 09/11/2009
@author: Nahuel
'''

from matrix.MatrixException import MatrixException

class NDimMatrix():
    '''
    Matrix of 'n' dimensions, implemented with one dictionary.
    
    @ivar _size: tuple with the length of each dimension.
    @ivar _data: dictionary with the data.
    @note: index begins in 1. 
    '''
    def __init__(self, size):
        '''Constructor of NDimMatrix.'''
        self._size = size
        self._data = {}
    
    def dimension(self):
        '''Returns the matrix dimension.'''
        return len(self._size)
    
    def get_data(self):
        '''Getter of _data.'''
        return self._data
    
    def get_size(self):
        '''Getter of _size.'''
        return self._size
        
    def set_data(self, the_data):
        '''Setter of _data.'''
        self._data = the_data
    
    def set_size(self, the_size):
        '''Setter of _size'''
        self._size = the_size
        
    def _check_dimension(self, x):
        '''Checks if x is a position valid (looking its dimension)'''
        return self.dimension() == len(x)
    
    def _check_bounds(self, pos):
        ''' 
        Checks if the position 'pos' can exist in the matrix.
        
        @param pos: tuple with the index of each dimension. 
        '''
        return self.get_size() >= pos
        
    def at(self, pos):
        ''' 
        Returns the element at the position 'pos'.
        
        @param pos: tuple with the index of each dimension.
        @raise MatrixException: if 'pos' has less or more dimensions
            that the receiver or if some index is out of bounds.
        @note: Since the matrix is implemented with a dictionary, is
            necessary catch the 'KeyError' exception.
        '''
        if not self._check_dimension(pos):
            raise MatrixException("NDimMatrix Error #1 : the dimension passed doesn't match.")
        elif not self._check_bounds(pos):
            raise MatrixException("NDimMatrix Error #2 : out of bounds.")
        else:
            try:
                return self._data[pos]
            except KeyError:
                return None
    
    def at_put(self, pos, elem):
        '''
        Puts an element at the position 'pos' in the matrix.
        
        @param pos: tuple with the position in the matrix.
        @param elem: the element to be put.
        @raise MatrixException: if 'pos' has less or more dimensions
            that the receiver or if some index is out of bounds.
        '''
        if not self._check_dimension(pos):
            raise MatrixException("NDimMatrix Error #1 : the dimension passed doesn't match.")
        elif not self._check_bounds(pos):
            raise MatrixException("NDimMatrix Error #2 : out of bounds.")
        else: 
            self._data[pos] = elem