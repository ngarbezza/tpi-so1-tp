'''
Created on 29/11/2009
@author: Nahuel
'''
import unittest
from opsys.process.ProcessStore import ProcessStore
from opsys.process.Process import Process

class TestProcessStore(unittest.TestCase):
    
    def setUp(self):
        self.store = ProcessStore()
        self.testPCB = Process(547, 'x', 10, [], 1, 1).get_pcb()
        
    def test_emptyWorkQueue(self):
        self.assertTrue(self.store.work_queue_is_empty())
        self.store.put_in_work_queue(self.testPCB)
        self.assertFalse(self.store.work_queue_is_empty())
    
    def test_emptyReadyQueue(self):
        self.assertTrue(self.store.ready_queue_is_empty())
        self.store.put_in_ready_queue(self.testPCB)
        self.assertFalse(self.store.ready_queue_is_empty())
    
    def test_work2ReadyQueue(self):
        self.store.put_in_work_queue(self.testPCB)
        self.assertFalse(self.store.work_queue_is_empty())
        self.assertTrue(self.store.ready_queue_is_empty())
        self.store.work_to_ready_queue(self.testPCB)
        self.assertTrue(self.store.work_queue_is_empty())
        self.assertFalse(self.store.ready_queue_is_empty())