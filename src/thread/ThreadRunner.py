'''
Created on 19/11/2009
@author: Nahuel
'''

from threading import Thread

class ThreadRunner(Thread):
    '''
    Subclase de Thread que corre threads para un objeto.
    El objeto tiene que definir un metodo start().
    Hecho para que el objeto no tenga que extender de Thread.
    '''
    def __init__(self, obj):
        '''Constructor of ThreadRunner.'''
        Thread.__init__(self)
        self._object = obj
    
    def get_object(self):
        '''Getter of _object'''
        return self._object
    
    def run(self):
        '''Start the thread.'''
        self.get_object().start()