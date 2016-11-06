'''
Created on 13/12/2009
@author: Nahuel
'''

from opsys.memory.Memory import Memory
from opsys.fs.LowerLevelFM import LowerLevelFM
from opsys.fs.Inode import DirectoryInode, FileInode, IndexBlock, DataBlock
from exceptions.OSException import OSException
from opsys.fs.File import File
from opsys.osconfig import MAX_OPENED_FILES, SIZE_DATA_BLOCK
from oslogging.Logger import Logger

class FileManager(object):
    '''
    Manage the file system with a set of instructions over files 
    and directories. Use the i-node system.
        
    @ivar _limit_address: determines the addressing space for file loading.
    @ivar _low_level_fm: it resolves operations of alloc and remove from disk.
    @ivar _current_dir: the path in where the file system is working.
    '''
    def __init__(self, is_console):
        '''
        Constructor of FileManager. This class can be instantiated by the
        operating system, or by the console.
        '''
        if is_console: 
            Memory()
            Logger()
            Logger.get_instance().open_log_file()
        self._limit_address = MAX_OPENED_FILES
        self._current_dir = ('/', 0)      #the root directory
        self._low_level_fm = LowerLevelFM()
    
    def get_limit_address(self):
        '''Getter of _limit_address.'''
        return self._limit_address
    
    def get_llfm(self):
        '''Getter of _low_level_fm.'''
        return self._low_level_fm
    
    def get_cwd(self):
        '''Getter of _current_dir.'''
        return self._current_dir
    
    def get_current_path(self):
        '''Get the complete current path.'''
        return self._current_dir[0]
    
    def get_block_current_dir(self):
        '''Get the block of the current directory.'''
        return self._current_dir[1]
    
    def set_cwd(self, the_dir):
        '''Setter of _current_dir.'''
        self._current_dir = the_dir
    
    def check_available_space(self):
        '''Look for a memory address empty, if found it, returns it.'''
        for i in range(0, self._limit_address): 
            if Memory.get_instance().get_value_at(i) is None: 
                return True
        return False
    
    def get_level_one_current_dir(self):
        '''Get the first indirection level of blocks of the current dir.'''
        block_curr = self.get_block_current_dir()
        fst_ib_ref = self.get_llfm().get_disk_at(block_curr).get_level_one_blocks()
        fst_ib = self.get_llfm().get_disk_at(fst_ib_ref)
        return (fst_ib_ref, fst_ib)
    
    def get_level_two_current_dir(self):
        '''
        Get the second indirection level of blocks of the current 
        directory. If not found (can be possible) returns None.
        '''
        block_curr = self.get_block_current_dir()
        snd_ib_ref = self.get_llfm().get_disk_at(block_curr).get_level_two_blocks()
        if snd_ib_ref is None: 
            return (None, None)
        snd_ib = self.get_llfm().get_disk_at(snd_ib_ref)
        return (snd_ib_ref, snd_ib)
    
    def create_generic(self, name, klass):
        '''
        Generic method for creation of files and directories.
        
        @param name: the name of the new file / directory.
        @param klass: class name used to instantiate file or directory.
        '''
        new_blocks = self.get_llfm().get_n_available_blocks(2) 
        new_ib = IndexBlock()
        if klass == DirectoryInode:
            new_ib.add_ref(new_blocks[0])               #the '.' directory
            new_ib.add_ref(self.get_block_current_dir()) #the '..' directory
            self.get_llfm().put_in_disk_at(new_blocks[0], klass(name, new_blocks[1]))
        else: 
            self.get_llfm().put_in_disk_at(new_blocks[0], klass(name, new_blocks[1]))
        self.get_llfm().put_in_disk_at(new_blocks[1], new_ib)
        #now add the reference to the current directory
        (fst_ib_ref, fst_ib) = self.get_level_one_current_dir()#@UnusedVariable
        if fst_ib.can_add_ref(): 
            fst_ib.add_ref(new_blocks[0])    #found
        else:
            (snd_ib_ref, snd_ib) = self.get_level_two_current_dir() 
            if snd_ib_ref is None:  #creates the second level (if necessary)
                dir_block = self.get_llfm().get_disk_at(self.get_block_current_dir())
                sndlv_new_blocks = self.get_llfm().create_ib_for_two_level()
                dir_block.set_level_two_blocks(sndlv_new_blocks)
                (snd_ib_ref, snd_ib) = self.get_level_two_current_dir()
            for ref in snd_ib.get_blocks():
                curr_ib = self.get_llfm().get_disk_at(ref) 
                if curr_ib.can_add_ref(): 
                    curr_ib.add_ref(new_blocks[0])
                    break
        self.get_llfm().dump_new_data()
    
    def create_directory(self, name):
        '''Creates a directory inside the current directory.'''
        self.create_generic(name, DirectoryInode)
        Logger.get_instance().log_create(name, self.get_current_path(), 'directory')
    
    def create_file(self, name):
        '''Creates a file inside the current directory.'''
        self.create_generic(name, FileInode)
        Logger.get_instance().log_create(name, self.get_current_path(), 'file')
    
    def change_directory(self, dir_name):
        '''
        Special cases (. , .. and /) are treated apart, because their position
        in the index block are always the same (0 and 1 respectively), 
        or is the root directory (/). 
        '''
        if dir_name == '.': 
            pass                #nothing to do, it's the same directory
        elif dir_name == '..':
            new_ref = self.get_level_one_current_dir()[1].get_blocks()[1]
            self.set_cwd((self.remove_last_dir_from_path(), new_ref))
        elif dir_name == '/': 
            self.set_cwd(('/', 0))               #shortcut to go to the root
        else:
            f = lambda x: x.is_directory()
            lv_one = self.get_level_one_current_dir()[1]
            new_ref = self.search_name_in_ib(lv_one, dir_name, False, f)
            if new_ref is None:
                (snd_ib_ref, snd_ib) = self.get_level_two_current_dir()
                if snd_ib_ref is None: 
                    raise OSException("Error: Directory not found.")
                for b in snd_ib.get_blocks():
                    block = self.get_llfm().get_disk_at(b)
                    new_ref = self.search_name_in_ib(block, dir_name, True, f)
                    if new_ref is not None: 
                        break
            if new_ref is None: 
                raise OSException("Error: Directory not found.")
            else: 
                self.set_cwd(((self.get_cwd()[0] + '/' + dir_name), new_ref))
    
    def search_name_in_ib(self, ib, name, snd_i, f):
        '''
        Search a block with name 'name' and return its position in the disk.
        Generic for directories and files.
        
        @param ib: the index block in which make the search.
        @param name: the name to search.
        @param snd_i: boolean that indicates if the method have to include
            in the search the two first index.
        @param f: the function for search files or directories.
        '''
        i = 0                        #'i' count for avoid '.' and '..' dirs
        for b in ib.get_blocks():
            curr_b = self.get_llfm().get_disk_at(b)
            if curr_b is not None and curr_b.get_name() == name \
            and f(curr_b) and (i > 1 or snd_i):
                return b
            i += 1
        return None
    
    def remove_directory(self, dir_name):
        '''Remove a directory in the current path, if exists.'''
        ib = self.get_level_one_current_dir()[1]
        f = lambda x: x.is_directory()
        del_ref = self.search_name_in_ib(ib, dir_name, False, f)
        if del_ref is None:
            ib = self.get_level_two_current_dir()[1]
            if ib is None: 
                raise OSException("Error: Directory not found.")
            for b in ib.get_blocks():
                ib = self.get_llfm().get_disk_at(b)
                del_ref = self.search_name_in_ib(ib, dir_name, True, f)
                if del_ref is not None: 
                    break
        if del_ref is None: 
            raise OSException("Error: Directory not found.")
        elif self.get_llfm().check_empty_dir(del_ref):
            ib.remove_index(del_ref)
            self.get_llfm().delete_indirections(del_ref) 
            self.get_llfm().remove_block(del_ref)
            self.get_llfm().dump_new_data()
            Logger.get_instance().log_del(dir_name, 'directory')
        else: 
            raise OSException("Error: Attempt to delete a non-empty directory.")
            
    def remove_last_dir_from_path(self):
        '''Take the path (string) and remove the last directory from it.'''
        i, new_index = (0, 0)
        curr_path = self.get_current_path()
        if curr_path == '/': 
            return curr_path
        for ch in curr_path:
            if ch == '/' : 
                new_index = i
            i += 1
        return curr_path[:new_index]
        
    def open(self, name, rw = True):
        '''
        Loads a file into the memory. 
        If it's already loaded, updates its ref_count.
        '''
        complete_name = self.get_cwd()[0] + '/' + name
        if self.is_opened(complete_name):
            self.search_file_in_memory(complete_name).inc_ref_count()
        else:
            (file_i, file_b) = self.search_file_name(name)
            res = ''
            fst_ib = self.get_llfm().get_disk_at(file_b.get_level_one_blocks())
            for index in fst_ib.get_blocks():
                curr_db = self.get_llfm().get_disk_at(index)
                if curr_db is not None: 
                    res += curr_db.get_data() #appending each block (1st ind)
            snd_ib = self.get_llfm().get_disk_at(file_b.get_level_two_blocks())
            if snd_ib is not None:               #there are more data
                for ib in snd_ib.get_blocks():
                    iblock = self.get_llfm().get_disk_at(ib)
                    for dbi in iblock.get_blocks():
                        curr_db = self.get_llfm().get_disk_at(dbi)
                        if curr_db is not None: 
                            res += curr_db.get_data()
            if not self.check_available_space(): 
                raise OSException('Error: Full memory.')
            else:
                date = file_b.get_date()
                size = file_b.get_size()
                open_file = File(complete_name, rw, date, res, file_i, size)
                pos = self.store_in_memory(open_file)
                Logger.get_instance().log_openfile(name, pos)
                return pos
    
    def is_opened(self, file_name):
        '''Verify that a file is loaded in the memory.'''
        for a in range(self.get_limit_address()):
            value = Memory.get_instance().get_value_at(a) 
            if value is not None and value.get_name() == file_name: 
                return True
        return False
    
    def store_in_memory(self, the_file):
        '''Puts a file into the memory. Search for an address available.'''
        for a in range(self.get_limit_address()):
            if Memory.get_instance().get_value_at(a) is None:
                Memory.get_instance().store_at(a, the_file)
                break
        return a          
    
    def search_file_name(self, name):
        '''Search for a file name and return its position and its block.'''
        f = lambda x: x.is_file()
        lev_one_dir = self.get_level_one_current_dir()[1]
        res_i = self.search_name_in_ib(lev_one_dir, name, True, f)
        if res_i is not None: 
            return (res_i, self.get_llfm().get_disk_at(res_i))
        else:
            (snd_ib_ref, snd_ib) = self.get_level_two_current_dir()
            if snd_ib_ref is None: 
                raise OSException("Error: File not found.")
            for b in snd_ib.get_blocks():
                curr_ib = self.get_llfm().get_disk_at(b)
                res_i = self.search_name_in_ib(curr_ib, name, True, f)
                if res_i is not None: 
                    break
        if res_i is not None: 
            return (res_i, self.get_llfm().get_disk_at(res_i))
        else: 
            raise OSException("Error: File not found.")

    def close(self, file_name):
        '''
        Decrement the ref_count of the file. 
        If ref_count reaches 0, removes the file from memory.
        '''
        complete_name = self.get_current_path() + '/' + file_name
        for a in range(self.get_limit_address()):
            the_file = Memory.get_instance().get_value_at(a)
            if the_file is not None and the_file.get_name() == complete_name:
                the_file.dec_ref_count()
                if the_file.get_ref_count() <= 0: 
                    Memory.get_instance().remove(a)
                break
        Logger.get_instance().log_closefile(file_name)

    def search_file_in_memory(self, name):
        '''Search for a file in memory by receiving a file name.'''
        for a in range(self.get_limit_address()):
            the_file = Memory.get_instance().get_value_at(a)
            if the_file is not None and the_file.get_name() == name: 
                return the_file
        return None
    
    def save(self, file_name):
        '''
        Synchronize the contents of a file in memory 
        and persist its data in the disk.
        '''
        the_path = self.get_current_path()
        the_file = self.search_file_in_memory(the_path + '/' + file_name)
        if the_file is None: 
            raise OSException("Error: File isn't in memory or doesn't exists.")
        data = the_file.get_data()
        file_inode = self.get_llfm().get_disk_at(the_file.get_disk_pos())
        file_inode.set_size(the_file.get_size())
        fst_ib = self.get_llfm().get_disk_at(file_inode.get_level_one_blocks())
        data = self.set_data_to_blocks(fst_ib, data)
        if file_inode.get_level_two_blocks() is None and not data == '':
            ltb = self.get_llfm().create_ib_for_two_level()
            file_inode.set_level_two_blocks(ltb)
        snd_ib = self.get_llfm().get_disk_at(file_inode.get_level_two_blocks())
        if not data == '':
            for iblock in snd_ib.get_blocks():
                curr_ib = self.get_llfm().get_disk_at(iblock)
                data = self.set_data_to_blocks(curr_ib, data)
                if data == '':
                    break
        self.get_llfm().dump_new_data()
        Logger.get_instance().log_datasaved(file_name)
    
    def set_data_to_blocks(self, ib, data):
        '''
        Store a data string into separated and distributed data blocks in the 
        disk. If the blocks aren't sufficient to store all data, return the 
        data that cannot be inserted.
        
        @param ib: the index block with references (or not) to a data blocks.
            if there's no references, creates the necessary data blocks.
        '''
        new_data = data
        for iblock in ib.get_blocks():
            if iblock is None: 
                curr_db = self.create_and_get_data_block(ib)
            else:
                curr_db = self.get_llfm().get_disk_at(iblock)
            curr_db.set_data(new_data[:SIZE_DATA_BLOCK])
            if len(new_data) <= SIZE_DATA_BLOCK: 
                new_data = ''
            else: 
                new_data = new_data[SIZE_DATA_BLOCK:]
            if new_data == '':
                return new_data
        return new_data
    
    def create_and_get_data_block(self, ib):
        '''Creates one new data block and return its reference.'''
        new_pos = self.get_llfm().get_n_available_blocks(1)
        self.get_llfm().put_in_disk_at(new_pos[0], DataBlock())
        ib.add_ref(new_pos[0])
        return self.get_llfm().get_disk_at(new_pos[0])
   
    def write(self, file_name, data):
        '''Write to the end of a file given, a data also given.'''
        the_path = self.get_current_path()
        the_file = self.search_file_in_memory(the_path + '/' + file_name)
        if the_file is None: 
            raise OSException("Error: The file isn't open or doesn't exists.")
        the_file.append_data(data)
    
    def delete(self, file_name):
        '''
        Delete a file from the file system and delete all its 
        references, index blocks, and data blocks.
        '''
        the_path = self.get_current_path()
        if self.search_file_in_memory(the_path + '/' + file_name) is not None:
            raise OSException("Error: Can't delete. The file is in memory.")
        (file_i, file_b) = self.search_file_name(file_name)
        fst_lev = file_b.get_level_one_blocks()
        self.get_llfm().remove_db_from_ib(self.get_llfm().get_disk_at(fst_lev))
        self.get_llfm().remove_block(fst_lev)
        snd_i = file_b.get_level_two_blocks()
        if snd_i is not None:
            snd_b = self.get_llfm().get_disk_at(snd_i)
            for b in snd_b.get_blocks():
                block = self.get_llfm().get_disk_at(b)
                self.get_llfm().remove_db_from_ib(block)
            self.get_llfm().remove_db_from_ib(snd_b)
            self.get_llfm().remove_block(snd_i)
        self.get_llfm().remove_block(file_i)
        try: 
            self.get_level_one_current_dir()[1].remove_index(file_i)
        except:
            lt = self.get_level_two_current_dir()[1]
            if lt is not None:
                for b in lt.get_blocks():
                    try:
                        self.get_llfm().get_disk_at(b).remove_index(file_i)
                    except:
                        continue
        self.get_llfm().dump_new_data()
        Logger.get_instance().log_del(file_name, 'file')

    def ls(self):
        '''Make a string with the contents of the current directory.'''
        res = 'Listado de ' + self.get_current_path() + ': \n'
        for b in self.get_level_one_current_dir()[1].get_blocks():
            if b is not None:
                inode = self.get_llfm().get_disk_at(b)
                res += '\t' + inode.get_name() + '(' + inode.get_type() + ')\n'
        snd_i = self.get_level_two_current_dir()[1]
        if snd_i is not None:
            for b in snd_i.get_blocks():
                for b1 in self.get_llfm().get_disk_at(b).get_blocks():
                    if b1 is not None:
                        inode = self.get_llfm().get_disk_at(b)
                        res += '\t' + inode.get_name() + \
                            '(' + inode.get_type() + ')\n'
        return res
                
    
    def ren_file(self, old_name, new_name):
        '''Rename a file in the current directory. Fail if it's in memory.'''
        the_path = self.get_current_path()
        if self.search_file_in_memory(the_path + '/' + old_name) is not None:
            raise OSException("Error: Can't delete. The file is in memory.")
        self.rename(old_name, new_name, lambda x: x.is_file())
        Logger.get_instance().log_rename(old_name, new_name, 'file')
    
    def ren_dir(self, old_name, new_name):
        '''Rename a directory in the current directory.'''
        self.rename(old_name, new_name, lambda x: x.is_directory())
        Logger.get_instance().log_rename(old_name, new_name, 'directory')
    
    def rename(self, old_name, new_name, f):
        '''
        Generic method. Rename directories or files.
        
        @param f: a function that determines if the element 
            is a file or directory.
        '''
        lev_one = self.get_level_one_current_dir()[1]
        new_ref = self.search_name_in_ib(lev_one, old_name, False, f)
        if new_ref is None:
            (snd_ib_ref, snd_ib) = self.get_level_two_current_dir()
            if snd_ib_ref is None: 
                raise OSException("Error: Directory or file not found.")
            for b in snd_ib.get_blocks():
                block = self.get_llfm().get_disk_at(b)
                new_ref = self.search_name_in_ib(block, old_name, True, f)
                if new_ref is not None:
                    break
        if new_ref is None:
            raise OSException("Error: Directory or file not found.")
        self.get_llfm().get_disk_at(new_ref).set_name(new_name)
        self.get_llfm().dump_new_data()
    
    def add_program(self, file_name, new_name):
        '''
        Take a file from the real disk and put in the file system, 
        in the folder "programs", in the root directory.
        
        @param new_name: the name that the file will have in the file system.
        @precondition: This method only must be executed in console mode.
        '''
        try: 
            the_file = open(file_name)
            data = the_file.read()
            the_file.close()
        except: 
            raise OSException('Error: Cannot open file name.')
        self.change_directory('/')
        self.change_directory('programs')
        self.create_file(new_name)
        self.open(new_name)
        self.write(new_name, data)
        self.save(new_name)
        self.close(new_name)