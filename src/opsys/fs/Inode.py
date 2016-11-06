'''
Created on 14/12/2009
@author: Nahuel
'''

from datetime import datetime
from opsys.osconfig import SIZE_INDEX_BLOCK, SIZE_DATA_BLOCK

class DirectoryInode(object):
    '''
    Block in disk, that can represent directories.
    
    @ivar name: structure name.
    @ivar timestamp: creation date of the structure.
    @ivar levelOneBlocks: index block with the contents of the structure
        (fixed size).
    @ivar levelTwoBlocks: index block that contains in each position others
        index blocks, that contains (or not) files or directories.
    @note: the structure has a limit of entries (files/directories)
        determined by len(indexblock) + len(indexblock) ^ 2
    '''
    def __init__(self, name, fst_pos):
        '''Constructor of DirectoryInode.'''
        self.name = name
        self.timestamp = datetime.today()
        self.level_one_blocks = fst_pos
        self.level_two_blocks = None
        
    def __repr__(self):
        '''Print for view the block indirections.'''
        return 'Directory ' + self.get_name() \
                + ' ; levelOne : ' + str(self.get_level_one_blocks()) \
                + ', levelTwo : ' + str(self.get_level_two_blocks())
    
    def get_name(self):
        '''Getter of name.'''
        return self.name
    
    def get_level_one_blocks(self):
        '''Getter of level_one_blocks.'''
        return self.level_one_blocks    
    
    def get_level_two_blocks(self):
        '''Getter of level_two_blocks.'''
        return self.level_two_blocks
    
    def set_level_two_blocks(self, ltb):
        '''Setter of level_two_blocks.'''
        self.level_two_blocks = ltb
        
    def set_name(self, the_name):
        '''Setter of name'''
        self.name = the_name
        
    def is_directory(self):
        return True
    
    def is_file(self):
        return False
    
    def get_type(self):
        '''Necessary for the ls command (file manager).'''
        return 'Directorio'
 
class FileInode(object):
    '''
    Block in disk, that represents files.
        
    @ivar _size: total size, in characters.
    @note: the directory has a limit of data blocks determined by:
         x = len(indexblock) + len(indexblock) ^ 2
         with a max size of x * len(datablock)
    '''
    def __init__(self, name, fst_pos):
        '''Constructor of FileInode.'''
        self.name = name
        self.timestamp = datetime.today()
        self.level_one_blocks = fst_pos
        self.level_two_blocks = None
        self._size = 0
        
    def __repr__(self):
        '''Print for view the block indirections.'''
        return 'File ' + self.get_name() \
                + ' ; levelOne : ' + str(self.get_level_one_blocks()) \
                + ', levelTwo : ' + str(self.get_level_two_blocks())
    
    def get_name(self):
        '''Getter of name.'''
        return self.name
    
    def get_date(self):
        return self.timestamp
    
    def get_level_one_blocks(self):
        '''Getter of level_one_blocks.'''
        return self.level_one_blocks    
    
    def get_level_two_blocks(self):
        '''Getter of level_two_blocks.'''
        return self.level_two_blocks
    
    def set_level_two_blocks(self, ltb):
        '''Setter of level_two_blocks.'''
        self.level_two_blocks = ltb
        
    def set_name(self, the_name):
        '''Setter of name'''
        self.name = the_name
        
    def is_directory(self):
        return False
    
    def get_size(self):
        '''Getter of _size.'''
        return self._size
    
    def set_size(self, the_size):
        '''Setter of _size.'''
        self._size = the_size
    
    def get_type(self):
        '''Necessary for the ls command (file manager).'''
        return 'Archivo'
    
    def is_file(self):
        return True

class IndexBlock(object):
    '''
    Fixed Size structure, contains references to disk positions.
    
    @ivar _blocks: list with all the index of disk positions.
    '''
    def __init__(self):
        '''Constructor of IndexBlock. Uses a configuration parameter.'''
        self._blocks = [None] * SIZE_INDEX_BLOCK
    
    def __repr__(self):
        '''Print for view the block indirections.'''
        return 'Index block : ' + str(self._blocks)
    
    def get_blocks(self):
        '''Getter of _blocks.'''
        return self._blocks
    
    def add_ref(self, block_num):
        '''Add an entry to the index block.'''
        for i in range(len(self.get_blocks())):
            if self.get_blocks()[i] is None: 
                self.get_blocks()[i] = block_num
                break
    
    def can_add_ref(self):
        '''If the block is full, return False.'''
        return self.get_blocks()[SIZE_INDEX_BLOCK - 1] is None
    
    def remove_index(self, i):
        '''Remove a reference from the index block.'''
        self.get_blocks().remove(i)
        #keep the size and the order of the index's
        self.get_blocks().append(None)
    
class DataBlock(object):
    '''
    Only represents a block of characters in the disk.
    
    @ivar _data: the block data (string).
    '''
    def __init__(self):
        '''Constructor of DataBlock.'''
        self._data = ''
    
    def __repr__(self):
        '''Print the block ignoring the newline characters (for best view).'''
        return 'Data Block : ' + self._data.replace('\n', '')
    
    def get_data(self):
        '''Getter of _data.'''
        return self._data
    
    def set_data(self, the_data):
        '''Setter of _data.'''
        self._data = the_data
    
    def is_full(self):
        '''
        Checks if the data has reached its max size.
        Reads a configuration parameter.
        '''
        return len(self.getData()) == SIZE_DATA_BLOCK
        