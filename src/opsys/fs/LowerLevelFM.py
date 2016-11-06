'''
Created on 16/12/2009
@author: Nahuel
'''

from opsys.fs.Inode import DirectoryInode, IndexBlock
from opsys.osconfig import SIZE_INDEX_BLOCK, MAX_AVAIL_BLOCKS
import pickle

class LowerLevelFM():
    '''
    The Lower Level File Manager. Store and serialize the data, 
    assign and remove blocks in the disk.
    
    @ivar _disk: the disk (permanent storage). Dynamic size,
        implemented with a dictionary.
    @ivar _available_blocks: list that keeps 100 available blocks
            ready for use. Automatically updates its size.
    '''
    def __init__(self):
        '''Constructor of LowerLevelFM.'''
        try:                    #object serialization
            with open('disk.os', 'rb') as f:
                self._disk = pickle.load(f)
        except:                  #first time running
            iblock = IndexBlock()#make the root directory, uses blocks 0 and 1
            iblock.add_ref(0)    #the '.' directory
            iblock.add_ref(0)    #the '..' directory (special case)
            self._disk = {0 : DirectoryInode('/', 1), 1 : iblock}
            self.dump_new_data()
        self._available_blocks = self.__get_blocks_from_disk(MAX_AVAIL_BLOCKS)
        
    def get_available_blocks(self):
        '''Getter of _available_blocks.'''
        return self._available_blocks
    
    def set_available_blocks(self, av):
        '''Setter of _available_blocks.'''
        self._available_blocks = av
    
    def get_disk(self):
        '''Getter of _disk'''
        return self._disk
    
    def put_in_disk_at(self, index, block):
        '''Puts a block in the index specified.'''
        self._disk[index] = block
        self.dump_new_data()
    
    def get_disk_at(self, pos):
        '''
        Obtains the block at a given position. Since the disk is implemented 
        with a dictionary, is necessary catch the KeyError exception.
        '''
        try: 
            return self._disk[pos]
        except KeyError: 
            return None
    
    def dump_new_data(self):
        '''
        A change in the file system happened, and the file manager
        have to persist in disk the changes.
        '''
        with open('disk.os', 'wb') as file:
            pickle.dump(self.get_disk(), file, pickle.HIGHEST_PROTOCOL)
    
    def __get_blocks_from_disk(self, cant):
        '''Return a list of positions of 'cant' blocks available.'''
        pos, found = (0, 0)
        res = []
        while found <= cant:
            if self.get_disk_at(pos) is None: 
                res.append(pos)
                found += 1
            pos += 1
        return res
    
    def get_n_available_blocks(self, cant):
        '''
        Receive a request of 'cant' blocks, and gives it,
        and also updates the available blocks list.
        '''
        if len(self.get_available_blocks()) < cant:
            blocks = self.__get_blocks_from_disk(MAX_AVAIL_BLOCKS)
            self.set_available_blocks(blocks)
        res = self.get_available_blocks()[:cant]
        self.set_available_blocks(self.get_available_blocks()[cant:])
        return res
    
    def create_ib_for_two_level(self):
        '''
        Creates a second indirection level. 
        Puts index blocks into another index block.
        Returns the reference to the main index block.
        '''
        blocks = self.get_n_available_blocks(SIZE_INDEX_BLOCK + 1)
        main_index = blocks.pop(0)
        the_ib = IndexBlock()
        for b in blocks:
            self.put_in_disk_at(b, IndexBlock())
            the_ib.add_ref(b)
        self.put_in_disk_at(main_index, the_ib)
        return main_index
    
    def check_empty_dir(self, ref):
        '''Checks if a directory is empty, starting at a ref received.'''
        ib = self.get_disk_at(self.get_disk_at(ref).get_level_one_blocks())
        i = 0                   #the 'i' is to avoid the '.' and '..' dirs
        for b in ib.get_blocks():
            if b is not None and not i < 2:
                return False            
            i += 1
        #all the first indir level is empty, now check the second indir level
        ib_ref = self.get_disk_at(ref).get_level_two_blocks()
        if ib_ref is None :
            return True      #there's no second indirection level
        ib = self.get_disk_at(ib_ref)
        for b in ib.get_blocks():
            for b1 in self.get_disk_at(b).get_blocks():
                if b1 is not None :
                    return False
                i += 1
        return True
    
    def delete_indirections(self, del_dir_ref):
        '''
        Delete all the indirections (first and second level) 
        of a directory.
        '''
        dir_block = self.get_disk_at(del_dir_ref)
        self.remove_block(dir_block.get_level_one_blocks())
        ind_block = dir_block.get_level_two_blocks()
        if ind_block is not None:
            block = self.get_disk_at(ind_block)
            for b in block.get_blocks():
                self.remove_block(b)
            self.remove_block(ind_block)
    
    def remove_db_from_ib(self, iblock):
        '''Remove data block/s or index block/s from a index block.'''
        for block in iblock.get_blocks():
            if block is not None: 
                self.remove_block(block)
    
    def remove_block(self, block):
        '''Remove a unused block.'''
        del self._disk[block]
        
    def print_disk(self):
        '''Print all the blocks, to see the disk state.'''
        for k, v in self.get_disk().items():
            print(k, ' : ', v)