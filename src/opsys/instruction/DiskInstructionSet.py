'''
Created on 13/12/2009
@author: Nahuel
'''

from opsys.instruction.InstructionSet import InstructionSet
from opsys.process.ProcessKiller import ProcessKiller
from opsys.memory.Memory import Memory
from exceptions.OSException import OSException
import time

class DiskInstructionSet(InstructionSet):
    '''
    Class that executes instructions from process, that are implemented
    by the File Manager.
    
    @ivar _file_manager: the File Manager. Implements all the disk operations.
    '''
    def __init__(self, fm = None):
        '''Constructor of DiskInstructionSet.'''
        self._file_manager = fm
        
    def get_file_manager(self):
        '''Getter of _file_manager.'''
        return self._file_manager
    
    def set_file_manager(self, the_fm):
        '''Setter of _file_manager.'''
        self._file_manager = the_fm
    
    def execute(self, inst, pcb):
        '''
        Run the code of the instruction and wait its corresponding time.
        
        @raise OSException: if the instruction fails its execution.
        '''
        self.get_file_manager().set_cwd(pcb.get_cwd())  #context switch in
        time.sleep(inst.get_time())
        try: 
            getattr(self, inst.get_func_name())(*[pcb] + inst.get_args())
        except OSException:
            ProcessKiller.get_instance().kill_pcb(pcb)
        pcb.set_cwd(self.get_file_manager().get_cwd())  #context switch out
    
    def mkdir(self, *args):
        '''Create a new directory in the current path.'''
        self.get_file_manager().create_directory(args[1].get_value())
    
    def rmdir(self, *args):
        '''Remove an empty directory in the current path.'''
        self.get_file_manager().remove_directory(args[1].get_value())
    
    def cd(self, *args):
        '''Change of current directory to directory name specified.'''
        self.get_file_manager().change_directory(args[1].get_value())
    
    def renfile(self, *args):
        '''Rename a file in the current directory.'''
        old_name = args[1].get_value()
        new_name = args[2].get_value()
        self.get_file_manager().ren_file(old_name, new_name)
    
    def rendir(self, *args):
        '''Rename a directory in the current directory.'''
        old_name = args[1].get_value()
        new_name = args[2].get_value()
        self.get_file_manager().ren_dir(old_name, new_name)
    
    def newfile(self, *args):
        '''Creates a new file in the disk.'''
        file_name = args[1].get_value()
        self.get_file_manager().create_file(file_name)
      
    def open(self, *args):
        '''Loads into memory the file with name given.'''
        curr_path = self.get_file_manager().get_current_path()
        path = curr_path + '/' + args[1].get_value()
        address = self.get_file_manager().open(args[1].get_value())
        args[0].add_file(path, address)
    
    def close(self, *args):
        '''
        Remove the reference to the pcb that it opened the file,
        if nobody has open the file, also remove from memory.
        '''
        curr_path = self.get_file_manager().get_current_path()
        self.get_file_manager().close(args[1].get_value())
        args[0].remove_file(curr_path + '/' + args[1].get_value())   
    
    def write(self, *args):
        '''
        Write a String, number or content of memory address
        to the file given. The file must be opened.
        '''
        file_name = args[1].get_value()
        the_data = args[2].get_write_data(args[0])
        self.get_file_manager().write(file_name, the_data)
    
    def writeline(self, *args):
        '''
        Same as write, with the difference that this method
        insert at the end the end-line character (\n).
        '''
        file_name = args[1].get_value()
        the_data = args[2].get_write_data(args[0])
        self.get_file_manager().write(file_name, the_data + '\n')
    
    def readall(self, *args):
        '''
        Store in memory all the data of a file opened first
        in memory, in an address specified.
        '''
        curr_path = self.get_file_manager().get_current_path()
        file_path = curr_path + '/' + args[1].get_value()
        file_data = args[0].get_file_at(file_path).get_data()
        Memory.get_instance().store_at_relative(args[0], args[2].get_value(), file_data)
    
    def delete(self, *args):
        '''Removes a file from the file system.'''
        self.get_file_manager().delete(args[1].get_value())
    
    def save(self, *args):
        '''
        Synchronize the data in the file in memory, with the
        corresponding block in disk. Persists the data.
        '''
        self.get_file_manager().save(args[1].get_value())
    
    def showdisk(self, *args):
        '''Show in screen all the disk, with its blocks and its assignments.'''
        self.get_file_manager().get_llfm().print_disk()
    
    def pwd(self, *args):
        '''Show in screen the current directory.'''
        print(self.get_file_manager().get_current_path()) 