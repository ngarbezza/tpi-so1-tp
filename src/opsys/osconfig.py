'''
Created on 19/12/2009
@author: Nahuel
'''

#------------------------------------------------------------------------------ 
#------------------LittleOS Configuration File---------------------------------
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------ 
#---------------------Process Configuration-----------------------------------
#------------------------------------------------------------------------------
# how many memory address can use each process
ADDRESS_SPACE = 20

#------------------------------------------------------------------------------ 
#-------------------Instruction Configuration----------------------------------
#------------------------------------------------------------------------------

# all the instructions with device and time
INST_MAP = {'add' : ('cpu', 0.1), 'sub' : ('cpu', 0.1), 'mov' : ('cpu', 0.1),
            'request' : ('cpu', 0), 'free' : ('cpu', 0), 'skip' : ('cpu', 1),
            'show' : ('display', 1),
            'input' : ('keyboard', 1), 'intinput' : ('keyboard', 0.5),
            'mkdir' : ('disk', 0.2), 'rmdir' : ('disk', 0.2), 
            'newfile' : ('disk', 0.2), 'open' : ('disk', 0.5),
            'close' : ('disk', 0.1), 'save' : ('disk', 0.5),
            'pwd' : ('disk', 0.1), 'cd' : ('disk', 0.1), 
            'renfile' : ('disk', 0.2), 'rendir' : ('disk', 0.2),
            'writeline' : ('disk', 0.5), 'readall' : ('disk', 0.5),
            'delete' : ('disk', 0.5), 'write' : ('disk', 0.5),
            'showdisk' : ('disk', 0.5)}


#------------------------------------------------------------------------------ 
#-------------------Scheduling Configuration-----------------------------------
#------------------------------------------------------------------------------

# the short-term scheduler to use:
# possible values:
#    *. 'Priority-No-Exp'
#    *. 'Priority-Exp'
#    *. 'Round-Robin'
#    *. 'SJF-No-Exp'
#    *. 'SJF-Exp'
#    *. 'FCFS'
SCHEDULER = 'Priority-Exp'

# the quantum (only affects to round robin)
QUANTUM = 2

# time sleep of long-term scheduler
LTS_SLEEP_TIME = 5

# time sleep of short-term scheduler
STS_SLEEP_TIME = 1

#------------------------------------------------------------------------------ 
#-----------------------I/O Configuration--------------------------------------
#------------------------------------------------------------------------------
# device_name : amount_of_instances
DEVICES = {'display' : 2, 
           'disk' : 1,
           'keyboard' : 1}

# time interval of a resource instance
RES_INST_SLEEP_TIME = 2

#------------------------------------------------------------------------------ 
#--------------------File System Configuration---------------------------------
#------------------------------------------------------------------------------

# how many files can be opened at the same time
MAX_OPENED_FILES = 20

# the size of the index block 
#    (affects to the max capacity of a directory, and the max file size)
# IMPORTANT: if you change this, you have to create a new disk. The data of the
#            old disk will not work.
SIZE_INDEX_BLOCK = 10

# the size of the data block
#    (affects to the max file size)
# IMPORTANT: if you change this, you have to create a new disk. The data of the
#            old disk will not work.
SIZE_DATA_BLOCK = 50

# how many entries of available blocks have the lower level file manager
MAX_AVAIL_BLOCKS = 50

#------------------------------------------------------------------------------ 
#-----------------Other Configuration Parameters-------------------------------
#------------------------------------------------------------------------------

# time sleep for the operating system
OS_SLEEP_TIME = 10

# time sleep for the CPU
CPU_SLEEP_TIME = 0.4

# log file path (relative to this file)
LOG_PATH = 'littleos.log'