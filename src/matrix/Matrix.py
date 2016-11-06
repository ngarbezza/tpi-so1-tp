'''
Created on 09/11/2009
@author: Nahuel
'''

from matrix.NDimMatrix import NDimMatrix
from matrix.MatrixException import MatrixException

class Matrix(NDimMatrix):
    '''Two dimension Matrix.'''
    def __init__(self, size):
        ''' 
        Constructor of Matrix.
        @note: checks if size has a dimension = 2.
        @raise MatrixException: if the size has more or less dimension than 2.
        '''
        if not len(size) == 2: 
            raise MatrixException("Matrix Error #3 : Dimension isn't 2.")
        else: 
            NDimMatrix.__init__(self, size)
    
    def rows(self):
        '''Returns the number of rows in the matrix.'''
        return self.get_size()[0]

    def cols(self):
        '''Returns the number of columns in the matrix.'''
        return self.get_size()[1]

    def substract(self, another_matrix):
        '''
        Subtract element by element the receiver with a matrix received.
        
        @param another_matrix: is 'y' in (x - y). x is the receiver.
        @note: Don't alter the receiver. Returns a new Matrix.
        @precondition: The two matrix has the same size.
        @precondition: The two matrix are complete (don't have None's).
        '''
        res = Matrix(self.get_size())
        for i in range(1, self.rows() + 1):
            for j in range(1, self.cols() + 1):
                res.at_put((i, j), self.at((i, j)) - another_matrix.at((i, j)))
        return res
    
    def add(self, another_matrix):
        ''' 
        Add element by element the receiver with a matrix received.
        
        @note: Alter the receiver. Don't create a new matrix.
        @precondition: The two matrix has the same size.
        @precondition: The two matrix are complete (don't have None's).
        '''
        for i in range(1, self.rows() + 1):
            for j in range(1, self.cols() + 1):
                self.at_put((i, j), self.at((i, j)) + another_matrix.at((i, j)))
    
    def fill_with(self, obj):
        '''
        Fills the entire matrix with the received element.
        
        @param obj: the element that fills the matrix.
        '''
        for i in range(1, self.rows() + 1):
            for j in range(1, self.cols() + 1):
                self.at_put((i, j), obj)
    
    def get_max(self):
        ''' 
        Returns the max element in the matrix.
        
        @note: if all the elements are None's, returns 0.
        '''
        max = 0
        for i in range(1, self.rows() + 1):
            for j in range(1, self.cols() + 1):
                curr_elem = self.at((i, j))
                if curr_elem is not None and curr_elem > max: 
                    max = curr_elem
        return max

    def fill_row(self, row, values):
        '''
        Fills a row (index received) with values received.
        
        @param row: the row number.
        @param values: tuple with the new values.
        '''
        for i in range(1, self.cols() + 1):
            self.at_put((row, i), values[i-1])
            
    def have_some_none(self):
        '''Checks if there is some None in the matrix.'''
        for i in range(1, self.rows() + 1):
            for j in range(1, self.cols() + 1):
                if self.at((i, j)) is None: 
                    return True
        return False
    
    def row_to_tuple(self, row_num):
        '''
        Make a tuple with a row specified.
        
        @param row_num: the row number.
        '''
        res = []
        for j in range(1, self.cols() + 1):
            res.append(self.at((row_num, j)))
        return tuple(res)
    
    def sum_row(self, row_num, tup):
        '''
        Add element by element a row specified 
        with values received as argument.
        
        @note: Alter the receiver.
        '''
        for j in range(1, self.cols() + 1):
            self.at_put(((row_num, j)), self.at((row_num, j)) + tup[j - 1])
    
    def substract_row(self, row_num, tup):
        '''
        Add element by element a row specified 
        with values received as argument.
        
        @note: Alter the receiver.
        '''
        for j in range(1, self.cols() + 1):
            self.at_put(((row_num, j)), self.at((row_num, j)) - tup[j - 1])
    
    def __repr__(self):
        '''Pretty print for two dimension Matrix.'''
        spaces = len(str(self.get_max())) + 1
        res = ''
        if self.have_some_none() and spaces < 4:
            spaces = 5                            #necessary space for "None"
        for i in range(1, self.rows() + 1):
            res += '| '
            for j in range(1, self.cols() + 1):
                str_elem = str(self.at((i, j)))
                res += str_elem
                res += ' ' * (spaces - len(str_elem))
            res += ' |\n'
        return res
    
    def has_all(self, obj):
        '''Checks if all the elements in the matrix are 'obj'.'''
        for i in range(1, self.rows() + 1):
            for j in range(1, self.cols() + 1):
                if not self.at((i, j)) == obj: 
                    return False
        return True
    
    def copy(self):
        '''Returns a new matrix, copy of the receiver.'''
        new_matrix = Matrix(self.get_size())
        new_matrix.set_data(self.get_data().copy())
        return new_matrix
    
    def new_row(self, values):
        '''
        Add a new row in the matrix (at the end) 
        and fills it with 'values'.
        '''
        self.set_size((self.rows() + 1, self.cols()))
        last_row = self.rows()
        for j in range(1, self.cols() + 1):
            self.at_put((last_row, j), values[j - 1])