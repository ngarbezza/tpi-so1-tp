'''
Created on 20/12/2009
@author: Nahuel47
'''
from multiprocessing.synchronize import RLock
from datetime import datetime
from opsys.osconfig import LOG_PATH

class Logger(object):
    '''
    Receives information from all the components, and saves to a file.
    
    @cvar __instance: the instance to make possible the Singleton.
    @ivar lock: the lock to keep synchronized the access to the file.
    '''
    
    __instance = None
    
    @classmethod
    def __new__(cls, *args, **kwargs):
        '''
        Redefines the constructor to make sure that you can't create 
        more than one instance.
        ''' 
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
    
    @classmethod
    def get_instance(cls):
        return cls.__instance
    
    def __init__(self):
        '''Constructor of Logger.'''
        self.lock = RLock()
    
    def open_log_file(self):
        self._log_file = open(LOG_PATH, 'a')
        self.write('The logger start its activity.')
    
    def get_log(self):
        '''Getter of _log_file.'''
        return self._log_file
    
    def close_log_file(self):
        self.write('The logger has finished its activity.')
        self._log_file.close()
        
    def get_timestamp(self):
        '''Get the current timestamp in a pretty format.'''
        timestmp = datetime.now()
        res = timestmp.strftime('%Y-%m-%d %H:%M:%S')
        return '[' + res + '] '
    
    def write(self, msg):
        '''Put into the log the message received.'''
        self.lock.acquire()
        self.get_log().write(self.get_timestamp() + msg + '\n')
        self.lock.release()
    
    def clear_log_file(self):
        pass

# file system logging
    
    def log_del(self, name, fileordir):
        self.write('FM - ' + fileordir + ' ' + name + ' was removed from the system')

    def log_create(self, name, path, dirorfile):
        res = 'FM - ' + dirorfile + ' ' + name \
            + ' was created in the directory ' + path
        self.write(res)
        
    def log_rename(self, old, new, dirorfile):
        self.write('FM - '+ dirorfile + ' ' + old + ' was renamed to ' + new)
        
    def log_datasaved(self, file_name):
        self.write('FM - Data saved to file ' + file_name)
    
    def log_openfile(self, name, pos):
        res = 'FM - file ' + name + ' was opened in the address #' + str(pos)
        self.write(res)
        
    def log_closefile(self, name):
        self.write('FM - file ' + name + ' was closed')

# CPU logging

    def log_request(self, pid, req, msg):
        res = 'CPU - request ' + str(req) + ' of process ' \
                               + str(pid) + ' was ' + msg
        self.write(res)
    
    def log_free(self, pcb):
        self.write('CPU - process ' + str(pcb.get_pid()) + ' free its resources')
    
    def log_expropiate(self, pid):
        self.write('CPU - process ' + str(pid) + ' was expropiated')
    
    def log_execinst(self, pcb):
        res = 'CPU - process ' + str(pcb.get_pid()) \
            + ' executes its instruction #' + str(pcb.get_pc())
        self.write(res)

# I/O logging

# other logging

    def log_newprocess(self, proc):
        res = 'OS - process ' + str(proc.get_pid()) + '(' \
            + proc.get_name() + ') enter to the system'
        self.write(res)
    
    def log_killprocess(self, pcb):
        res = 'OS - process ' + str(pcb.get_pid()) + '(' \
            + pcb.get_name() + ') finished or was killed.'
        self.write(res)
        print('process ' + str(pcb.get_pid()) + ' finish')
