'''
Created on 29/11/2009
@author: Nahuel
'''

import unittest
from opsys.scheduling.FCFSScheduler import FCFSScheduler
from opsys.process.ProcessStore import ProcessStore
from opsys.process.Process import Process

class MockInst():
    def __init__(self, time, io):
        self._time = time
        self._io = io
    def get_time(self):
        return self._time
    def is_io_inst(self):
        return self._io

class TestScheduler(unittest.TestCase):
    '''
    This class test the abstract class Scheduler, and the FCFS Scheduling.  
    '''
    def setUp(self):
        self.store = ProcessStore()
        self.sched = FCFSScheduler(None, self.store)
        inst_list = self.init_instructions()
        proc_1 = Process(547, 'x', 10, inst_list, 2, 2)
        proc_2 = Process(123, 'y', 10, [], 2, 2)
        self.store.put_in_ready_queue(proc_1.get_pcb())
        self.store.put_in_ready_queue(proc_2.get_pcb())
        
    def init_instructions(self):
        return [MockInst(3, False), MockInst(1, False), MockInst(2, False),
                MockInst(3, True), MockInst(1, False), MockInst(9, False)]
        
    def test_getNextPCB(self):
        p1 = self.sched.get_next_pcb()
        self.assertEqual(p1.get_pid(), 547)
        p1 = self.sched.get_next_pcb()
        self.assertEqual(p1.get_pid(), 123)
        self.assertTrue(self.store.ready_queue_is_empty())
    
    def test_setNextBurst(self):
        pcb = self.sched.get_next_pcb()
        self.sched.set_next_burst(pcb)
        self.assertEqual(pcb.get_next_burst(), 6)
        pcb.set_pc(4)
        self.sched.set_next_burst(pcb)
        self.assertEqual(pcb.get_next_burst(), 10)
    
    def test_setRemainingTime(self):
        pcb = self.sched.get_next_pcb()
        self.sched.set_remaining_time(pcb)
        self.assertEqual(pcb.get_remaining_time(), 19)
        pcb.set_pc(3)
        self.sched.set_remaining_time(pcb)
        self.assertEqual(pcb.get_remaining_time(), 13)
        pcb.set_pc(6)
        self.sched.set_remaining_time(pcb)
        self.assertEqual(pcb.get_remaining_time(), 0)