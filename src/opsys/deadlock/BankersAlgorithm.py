'''
Created on 10/11/2009
@author: Nahuel
'''

from matrix.Matrix import Matrix
from exceptions.OSException import OSException

class BankersAlgorithm(object):
    '''
    Implements the Banker's Algorithm, for deadlock avoidance.
    
    @ivar _allocation: matrix of resources assigned to a process.
    @ivar _max: matrix that saves the maximum resource's instances
        that a process can request.
    @ivar _available: for each kind of resource, the instances available
        at this moment.
    @ivar _need: matrix that indicates the instances needed for each 
        process to complete its task. need = max - allocation.
    @ivar _totalRes : tuple with total amount of instances of 
        each resource.
    @ivar _total_res: tuple with the number of total resources.
    @ivar _invalid_rows: rows that banker doesn't consider.
    '''
    def __init__(self, avail):
        '''
        Constructor of BankersAlgorithm.
        
        @param avail: tuple with the number of total resources.
        '''
        res_num = len(avail)
        self._total_res = avail
        self._allocation = Matrix((0, res_num))
        self._available = Matrix((1, res_num))
        self._max = Matrix((0, res_num))
        self._need = self._max.substract(self._allocation)
        self._invalid_rows = []
        self._available.fill_row(1, avail)
        self._allocation.fill_with(0)
        
    def get_need(self):
        '''Getter of _need.'''
        return self._need
    
    def get_max(self):
        '''Getter of _max.'''
        return self._max
    
    def get_available(self):
        '''Getter of _available.'''
        return self._available
    
    def get_allocation(self):
        '''Getter of _allocation.'''
        return self._allocation
        
    def get_invalid_rows(self):
        '''Getter of _invalid_rows.'''
        return self._invalid_rows
    
    def get_total_resources(self):
        '''Getter of _total_res.'''
        return self._total_res
    
    def get_res_num(self):
        '''How many types of resources there are in the system.'''
        return len(self._total_res)
    
    def set_available(self, new_avail):
        '''Setter of _available.'''
        self._available = new_avail
    
    def set_need(self, new_need):
        '''Setter of _need.'''
        self._need = new_need
        
    def set_allocation(self, new_alloc):
        '''Setter of _allocation.'''
        self._allocation = new_alloc
    
    def set_max(self, new_max):
        '''Setter of _max.'''
        self._max = new_max
        
    def calculate_need(self):
        '''Keep _need = _max - _allocation'''
        self.set_need(self.get_max().substract(self.get_allocation()))

    def request_algorithm(self, pid, request):
        '''
        Evaluate a request for the process 'pid'. If this request isn't
        possible, returns False, and the cpu manages this situation.
        
        @param pid: the ID of the process that do the request.
        @param request: tuple of resource instances.
        '''        
        new_need = self.get_need().copy()
        new_allocation = self.get_allocation().copy()
        new_available = self.get_available().copy()
        if request > new_need.row_to_tuple(pid):
            raise OSException("Error: Request more than need declared.")
        elif request > new_available.row_to_tuple(1): 
            return False
        else:
            self.get_available().substract_row(1, request)
            self.get_allocation().sum_row(pid, request)
            self.get_need().substract_row(pid, request)
            if not self.check_available() or not self.safety_algorithm(\
                self.get_need(), self.get_allocation(), self.get_available()):
                self.set_need(new_need)               #restore previous state
                self.set_allocation(new_allocation)
                self.set_available(new_available)
                return False
            else: 
                return True
    
    def check_available(self):
        '''Check if an assign leave some resource in a value less than 0.'''
        for i in range(1, self.get_available().cols() + 1):
            if self.get_available().at((1, i)) < 0: 
                return False
        return True
#-------------------------Safety Algorithm--------------------------------

    def safety_algorithm(self, need, allocation, available):
        '''
        Finds a safe sequence and then indicates if the system
        keeps safe or it turns unsafe. Returns a boolean.
        '''
        work = available.copy()
        finish = Matrix((1, self.get_max().rows()))
        self.fill_valid_rows(finish)
        while not finish.has_all(True) \
        and self.check_condition_row(need, work.row_to_tuple(1), finish):
            for i in range(1, finish.cols() + 1):
                if need.row_to_tuple(i) <= work.row_to_tuple(1) \
                and not finish.at((1, i)):
                    work.sum_row(1, allocation.row_to_tuple(i))
                    finish.at_put((1, i), True)
        return finish.has_all(True)
    
    def fill_valid_rows(self, finish):
        '''
        Fill with True those rows that are invalid and don't participate
        in the result, then the banker think that process this rows.
        '''
        for i in range(1, finish.cols() + 1):
            finish.at_put((1, i), i in self.get_invalid_rows())
        return finish
        
    def check_condition_row(self, need, work, finish):
        '''Check a condition necessary for the security algorithm.'''
        for i in range(1, need.cols() + 1):
            if need.row_to_tuple(i) <= work and not finish.at((1, i)): 
                return True
        return False
    
    def new_process_come(self, max_res):
        '''
        A new process has come, and the Banker's Algorithm needs to know
        the max resources of this process. Add necessary data to the matrix.
        
        @precondition: the process id corresponds with the new row.
        '''
        self.get_allocation().new_row(tuple([0] * self.get_res_num()))
        self.get_max().new_row(max_res)
        self.calculate_need()
    
    def do_free(self, pcb):
        '''
        Update the resources because a process reachs a free instruction.
        Compute the new max for this process.
        
        @param pcb: the PCB of the process that executes "free" instruction
        '''
        self.get_available().sum_row(1, \
                self.get_allocation().row_to_tuple(pcb.get_pid()))
        self.get_allocation().fill_row(pcb.get_pid(), \
                tuple([0] * self.get_res_num()))
        self.calculate_and_set_new_max(pcb)
        self.calculate_need()
        
    def calculate_new_max(self, pcb):
        '''
        Sum all the request until reach a free instruction.
        This method is called for first time by the operating system,
        then is called after each free instruction by the CPU.
        '''
        detected_free = False
        pcb.inc_pc()
        i = pcb.get_pc()
        new_max = [0] * self.get_res_num()
        while not detected_free and i < len(pcb.get_process().get_instructions()):
            inst = pcb.get_instruction_at(i)
            if inst.is_free(): 
                detected_free = True
            elif inst.is_request():
                req = inst.get_args_as_int()
                for x in range(len(new_max)):
                    new_max[x] = new_max[x] + req[x]
            i += 1
        pcb.dec_pc()
        if self.check_wrong_max(tuple(new_max)): 
            return tuple(new_max)
        else: 
            raise OSException('Error: Request more resources than total available.')
    
    def check_wrong_max(self, max_res):
        '''
        Verify the max requested resources of a process, comparing with
        total resources.
        '''
        return self.get_total_resources() >= max_res
    
    def calculate_and_set_new_max(self, pcb):
        '''Compute the new max for a process, and also sets to it.'''
        self.get_max().fill_row(pcb.get_pid(), self.calculate_new_max(pcb))
    
    def process_finished(self, pid):
        '''A process has finished, and the corresponding data will be ignored.'''
        values = tuple([0]* self.get_res_num())
        self.get_allocation().fill_row(pid, values)
        self.get_need().fill_row(pid, values)
        self.get_max().fill_row(pid, values)
        self.get_invalid_rows().append(pid)       #the banker will not consider this row
    
    def loader_come(self, max):
        '''Enable the process loader in the banker.'''
        try:
            self.get_invalid_rows().remove(1)
        except ValueError:
            self.new_process_come(max)
            return
        self.get_allocation().fill_row(1, tuple([0] * self.get_res_num()))
        self.get_max().fill_row(1, max)
        self.calculate_need()