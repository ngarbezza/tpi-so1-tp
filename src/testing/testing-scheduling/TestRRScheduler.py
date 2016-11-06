'''
Created on 01/12/2009
@author: Nahuel
'''

import unittest
from opsys.scheduling.RRScheduler   import RRScheduler
from opsys.process.ProcessStore     import ProcessStore
from opsys.process.Process          import Process

class MockInst():
    def __init__(self, time, io):
        self._time = time
        self._io = io
    def get_time(self):
        return self._time
    def is_io_inst(self):
        return self._io

class TestRRScheduler(unittest.TestCase):
    def setUp(self):
        self.store = ProcessStore()
        self.sched = RRScheduler(None, self.store)
        instList = self.init_instructions()
        proc_1 = Process(547, 'x', 10, instList, 2, 2)
        proc_2 = Process(123, 'y', 10, [], 2, 2)
        self.store.put_in_ready_queue(proc_1.get_pcb())
        self.store.put_in_ready_queue(proc_2.get_pcb())
        
    def init_instructions(self):
        return [MockInst(1, False), MockInst(2, False), MockInst(2, False),
                MockInst(3, True), MockInst(2, False), MockInst(1, False)]
    
    def test_setNextBurst(self):
        pcb = self.sched.get_next_pcb()
        self.sched.set_next_burst(pcb)
        self.assertEqual(pcb.get_next_burst(), 1)
        pcb.set_pc(2)
        self.sched.set_next_burst(pcb)
        self.assertEqual(pcb.get_next_burst(), 2)
        pcb.set_pc(4)
        self.sched.set_next_burst(pcb)
        self.assertEqual(pcb.get_next_burst(), 2)
        pcb.set_pc(5)
        self.sched.set_next_burst(pcb)
        self.assertEqual(pcb.get_next_burst(), 1)