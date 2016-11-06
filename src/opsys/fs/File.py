'''
Created on 13/12/2009
@author: Nahuel
'''

class File(object):
    '''
    Represent files loaded in memory, not in disk.
    
    @ivar _name: total path + file name.
    @ivar _permission: indicates write permission.
    @ivar _creation_date: creation date (in disk).
    @ivar _data: string with all the file data.
    @ivar _disk_pos: the position of the block in which the file is storaged.
    @ivar _size: the total size (in number of characters) of the file.
    @ivar _ref_count: count how many processes opened the file.
    '''
    def __init__(self, name, permission, date, data, pos, size):
        '''Constructor of File.'''
        self._name = name
        self._permission = permission      #write permission
        self._creation_date = date
        self._data = data
        self._disk_pos = pos
        self._size = size
        self._ref_count = 1                 #first open
    
    def __repr__(self):
        return 'File : ' + self.get_name()
    
    def inc_ref_count(self):
        '''Add one reference to the file.'''
        self._ref_count += 1
    
    def get_ref_count(self):
        '''Getter of _ref_count.'''
        return self._ref_count
    
    def dec_ref_count(self):
        '''Remove one reference to the file.'''
        self._ref_count -= 1
    
    def get_name(self):
        '''Getter of _name.'''
        return self._name
    
    def get_disk_pos(self):
        '''Getter of _disk_pos.'''
        return self._disk_pos
    
    def get_data(self):
        '''Getter of _data'''
        return self._data
    
    def get_date(self):
        '''Getter of _creation_date.'''
        return self._creation_date
    
    def get_size(self):
        '''Getter of _size.'''
        return self._size
    
    def append_data(self, new_data):
        '''Add to the end of the file the new data and updates the size.'''
        self._data = self._data + new_data
        self._size = len(self._data)