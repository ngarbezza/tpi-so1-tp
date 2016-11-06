'''
Created on 01/12/2009
@author: Nahuel
'''

from opsys.deadlock.BankersAlgorithm import BankersAlgorithm
from matrix.Matrix import Matrix
from exceptions.OSException import OSException
from opsys.process.Process import Process
from opsys.instruction.Instruction import Instruction
from opsys.instruction.Number import Number

import unittest

class TestBanker(unittest.TestCase):

    def setUp(self):
        self.banker = BankersAlgorithm((10, 5, 7))
        self.init_allocation()
        self.init_max()
        self.init_available()
        self.banker.calculate_need()
        
    def init_allocation(self):
        m = Matrix((5, 3))      #5 process, 3 kind of resources
        m.at_put((1,1), 0)       #process 1
        m.at_put((1,2), 1)       
        m.at_put((1,3), 0)       
        m.at_put((2,1), 2)       #process 2
        m.at_put((2,2), 0)       
        m.at_put((2,3), 0)       
        m.at_put((3,1), 3)       #process 3
        m.at_put((3,2), 0)       
        m.at_put((3,3), 2)       
        m.at_put((4,1), 2)       #process 4
        m.at_put((4,2), 1)       
        m.at_put((4,3), 1)       
        m.at_put((5,1), 0)       #process 5
        m.at_put((5,2), 0)       
        m.at_put((5,3), 2)       
        self.banker.set_allocation(m)
    
    def init_max(self):
        m = Matrix((5, 3))      #5 process, 3 kind of resources
        m.at_put((1,1), 7)       #process 1
        m.at_put((1,2), 5)       
        m.at_put((1,3), 3)       
        m.at_put((2,1), 3)       #process 2
        m.at_put((2,2), 2)       
        m.at_put((2,3), 2)       
        m.at_put((3,1), 9)       #process 3
        m.at_put((3,2), 0)       
        m.at_put((3,3), 2)       
        m.at_put((4,1), 2)       #process 4
        m.at_put((4,2), 2)       
        m.at_put((4,3), 2)       
        m.at_put((5,1), 4)       #process 5
        m.at_put((5,2), 3)       
        m.at_put((5,3), 3)       
        self.banker.set_max(m)
    
    def init_available(self):
        m = Matrix((1, 3))
        m.at_put((1,1), 3)
        m.at_put((1,2), 3)
        m.at_put((1,3), 2)
        self.banker.set_available(m)
    
    def test_requestSafe(self):
        self.assertTrue(self.banker.request_algorithm(2, (1, 0, 2)))
    
    def test_requestUnsafe(self):
        self.assertFalse(self.banker.request_algorithm(5, (3, 3, 0)))
    
    def test_requestDenied(self):
        self.assertFalse(self.banker.request_algorithm(1, (4, 2, 1)))
    
    def test_requestFail(self):
        self.assertRaises(OSException, self.banker.request_algorithm, 4, (1, 0, 0))
    
    def test_free(self):
        proc = Process(2, 'test', 3, self.create_instructions(), 1, 1)
        proc.get_pcb().set_pc(1)      #2nd. instruction (free)
        self.banker.do_free(proc.get_pcb())
        self.assertEqual(self.banker.get_allocation().row_to_tuple(2), (0, 0, 0))
        self.assertEqual(self.banker.get_max().row_to_tuple(2), (2, 2, 5))
        self.assertEqual(self.banker.get_available().row_to_tuple(1), (5, 3, 2))
        
    def create_instructions(self):
        return [Instruction('skip', [], 'cpu', 2),
                Instruction('free', [], 'cpu', 1),
                Instruction('skip', [], 'cpu', 2),
                Instruction('request', [Number(0), Number(1), Number(2)], 'cpu', 2),
                Instruction('skip', [], 'cpu', 2),
                Instruction('skip', [], 'cpu', 2),
                Instruction('request', [Number(2), Number(1), Number(3)], 'cpu', 2),
                Instruction('free', [], 'cpu', 2),
                ]
    
    def test_makeCorrectFinish(self):
        self.banker.get_invalid_rows().append(2)
        self.banker.get_invalid_rows().append(4)
        finish = Matrix((1, 5))
        result = (False, True, False, True, False)
        self.assertEquals(self.banker.fill_valid_rows(finish).row_to_tuple(1), result)
    