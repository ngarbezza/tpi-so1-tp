'''
Created on 15/11/2009
@author: Nahuel
'''

from opsys.cpu.CPU import CPU 
from opsys.deadlock.BankersAlgorithm import BankersAlgorithm
from opsys.scheduling.LTScheduler import LTScheduler
from opsys.process.ProcessStore import ProcessStore
from opsys.memory.Memory import Memory
from opsys.fs.FileManager import FileManager
from thread.ThreadRunner import ThreadRunner
from parsing.OSParser import OSParser
from opsys.process.ProcessKiller import ProcessKiller
from opsys.process.Process import Process
from opsys.instruction.Instruction import Instruction
from opsys.instruction.MemoryCell import MemoryCell
from opsys.instruction.Number import Number
from opsys.instruction.String import String
from exceptions.OSException import OSException
from opsys.osconfig import SCHEDULER, DEVICES, OS_SLEEP_TIME
from opsys.iodev.IODeviceManager import IODeviceManager
from opsys.instruction.IOInstructionSet import DisplayInstructionSet
from opsys.instruction.IOInstructionSet import KeyboardInstructionSet
from opsys.instruction.DiskInstructionSet import DiskInstructionSet
from opsys.scheduling.FCFSScheduler import FCFSScheduler
from opsys.scheduling.RRScheduler import RRScheduler
from opsys.scheduling.SJFScheduler import SJFSchedulerExp
from opsys.scheduling.SJFScheduler import SJFSchedulerNoExp
from opsys.scheduling.PriorityScheduler import PrioritySchedulerExp
from opsys.scheduling.PriorityScheduler import PrioritySchedulerNoExp
from oslogging.Logger import Logger
import time

# the scheduler classes
SCHED_CLASSES = {'FCFS' : FCFSScheduler,
                 'Priority-No-Exp' : PrioritySchedulerNoExp,
                 'Priority-Exp' : PrioritySchedulerExp,
                 'SJF-No-Exp' : SJFSchedulerNoExp,
                 'SJF-Exp' : SJFSchedulerExp,
                 'Round-Robin' : RRScheduler}

# the classes of each instruction set
DEV_CLASSES = {'display' : DisplayInstructionSet,
               'keyboard' : KeyboardInstructionSet,
               'disk' : DiskInstructionSet}

class OS(object):
    '''
    The operating system.
    
    @ivar _parser: the process creator (parse strings).
    @ivar _proc_store: all the process data.
    @ivar _file_manager: interface to manage a disk with i-node file system.
    @ivar _io_devices: the I/O device managers.
    @ivar _cpu: the Central Process Unit. Understand all the instructions.
    @ivar _scheduler: the short-term scheduler.
    @ivar _lt_scheduler: the long-term scheduler.
    @ivar _active: boolean, indicate activity in the operating system.
    '''
    def __init__(self):
        ''' Constructor of OS.'''
        Memory()       #create the singleton memory
        Logger()       #initialize the logger 
        self._parser = OSParser()
        self._file_manager = FileManager(False)
        self._proc_store = ProcessStore()
        self._io_devices = self.create_io_devices()
        banker = BankersAlgorithm(self.get_total_resources())
        ProcessKiller(banker, self._proc_store)
        self._cpu = CPU(banker, self._io_devices, self._proc_store)
        self._scheduler = self.create_scheduler(self._cpu, self._proc_store)
        self._lt_scheduler = LTScheduler(self._proc_store)
        self._active = False
    
    def get_cpu(self):
        '''Getter of _cpu.'''
        return self._cpu
    
    def get_lt_scheduler(self):
        '''Getter of _lt_scheduler.'''
        return self._lt_scheduler
    
    def get_file_manager(self):
        '''Getter of _file_manager.'''
        return self._file_manager
    
    def get_scheduler(self):
        '''Getter of _scheduler.'''
        return self._scheduler
    
    def get_io_devices(self):
        '''Getter of _io_devices.'''
        return self._io_devices
    
    def get_parser(self):
        '''Getter of _parser.'''
        return self._parser
    
    def get_process_store(self):
        '''Getter of _proc_store.'''
        return self._proc_store
    
    def set_process_store(self, store):
        self._proc_store = store
    
    def set_active(self):
        self._active = True
        
    def set_inactive(self):
        self._active = False
        
    def is_active(self):
        return self._active
    
    def create_scheduler(self, cpu, proc_store):
        klass = SCHED_CLASSES[SCHEDULER]
        return klass(cpu, proc_store)
    
    def get_total_resources(self):
        '''
        Returns a tuple with amount of each resource. 
        Necessary for the banker.
        '''
        res = []
        for dev in self.get_parser().get_request_order():
            res.append(DEVICES[dev])
        return tuple(res)
    
    def create_io_devices(self):
        '''Creates and initialize the I/O Devices.'''
        res = {}
        store = self.get_process_store()
        for name, klass in DEV_CLASSES.items():
            res[name] = IODeviceManager(name, DEVICES[name], klass, store)
        file_m = self.get_file_manager()
        res['disk'].get_instruction_set().set_file_manager(file_m)   
        return res
    
    def start_scheduler_threads(self):
        thr_lts = ThreadRunner(self.get_lt_scheduler())
        thr_sts = ThreadRunner(self.get_scheduler())
        thr_lts.setDaemon(True)
        thr_sts.setDaemon(True)
        thr_lts.start()
        thr_sts.start()
    
    def start_cpu_thread(self):
        thr_cpu = ThreadRunner(self.get_cpu())
        thr_cpu.setDaemon(True)
        thr_cpu.start()
        
    def start_io_devices_threads(self):
        for k in self.get_io_devices():
            self.get_io_devices()[k].start()
    
    def start(self):
        try:
            Logger.get_instance().open_log_file()
        except IOError:
            print('Error in the log file. Aborting.')
            return
        self.set_active()
        self.start_scheduler_threads()
        self.start_cpu_thread()
        self.start_io_devices_threads()
        while self.is_active():
            time.sleep(OS_SLEEP_TIME)
        self.set_inactive()
    
    def shutdown(self):
        self.set_inactive()
        self.get_cpu().shutdown()
        self.get_lt_scheduler().set_inactive()
        self.get_scheduler().set_inactive()
        for d in self.get_io_devices():
            self.get_io_devices()[d].shutdown()
        Memory.get_instance().clear_all()
        Logger.get_instance().close_log_file()
        self.reset()
    
    def reset(self):
        self.get_parser().reset()
        store = ProcessStore()
        banker = BankersAlgorithm(self.get_total_resources())
        self.set_process_store(store)
        self.get_cpu().set_process_store(store)
        self.get_cpu().set_banker(banker)
        ProcessKiller.get_instance().set_banker(banker)
        ProcessKiller.get_instance().set_process_store(store)
        self.get_scheduler().set_process_store(store)
        self.get_lt_scheduler().set_process_store(store)
        for dev in self.get_io_devices():
            self.get_io_devices()[dev].set_process_store(store)
        
    def add_program(self, file_name, new_name):
        '''
        Take a file from the real disk and put in the file system, 
        in the folder "//programs".
        @precondition: the system must not be running, because other 
            processes fight for the disk control.
        '''
        try: 
            file = open(file_name)
            data = file.read()
        except: 
            print('Error during load.')
        finally: 
            file.close()
        try:
            fm = self.get_file_manager()
            fm.change_directory('/')
            fm.change_directory('programs')
            fm.create_file(new_name)
            fm.open(new_name)
            fm.write(new_name, data)
            fm.save()
            fm.close()
        except OSException:
            print('Error during store in the file system')
        
    def __make_loader(self, file_name):
        return Process(1, 'loader', 1, \
            [Instruction('skip', [], 'cpu', 0),
             Instruction('request', self.get_parser().make_request([Number(1), String('disk')]), 'cpu', 0),
             Instruction('cd', [String('/')], 'disk', 0),
             Instruction('cd', [String('programs')], 'disk', 0),
             Instruction('open', [String(file_name)], 'disk', 0),
             Instruction('readall', [String(file_name), MemoryCell(0)], 'disk', 0),
             Instruction('close', [String(file_name)], 'disk', 0),
             Instruction('free', [], 'cpu', 0)
            ], 1, 1)
    
    def __loader_is_running(self):
        return self.get_process_store().exists_pid(1)
    
    def load(self, file_name):
        '''
        Executes a file storaged in the file system, in the folder "programs". 
        First load the loader :-) , to leave in memory the program to run.
        '''
        if self.__loader_is_running(): 
            raise OSException('Error: The loader is running.')
        loader = self.__make_loader(file_name)
        self.__set_time_parameters(loader)
        banker = self.get_cpu().get_banker()
        banker.loader_come(banker.calculate_new_max(loader.get_pcb()))
        self.get_process_store().put_in_all_process(loader)
        self.get_process_store().put_in_ready_queue(loader.get_pcb())
        while Memory.get_instance().get_value_at(1) is None:
            time.sleep(1)
        self.__load_program(Memory.get_instance().get_value_at(1))
        Memory.get_instance().remove(1)
    
    def __set_time_parameters(self, proc):
        self.get_scheduler().set_next_burst(proc.get_pcb())
        total_time = self.get_lt_scheduler().total_time_for_new_process(proc)
        proc.set_remaining_time(total_time)
        proc.set_io_perc(self.get_lt_scheduler().compute_io_perc(proc))

    def __store(self, proc):
        self.get_process_store().put_in_work_queue(proc.get_pcb())
        self.get_process_store().put_in_all_process(proc)
        Logger.get_instance().log_newprocess(proc)

    def __load_program(self, data):
        proc = self.get_parser().parse(data)
        self.__set_time_parameters(proc)
        proc.set_io_perc(self.get_lt_scheduler().compute_io_perc(proc))
        banker = self.get_cpu().get_banker()
        banker.new_process_come(banker.calculate_new_max(proc.get_pcb()))
        self.__store(proc)
