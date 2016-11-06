'''
Created on 18/12/2009
@author: Nahuel
'''

from cmd import Cmd
from opsys.OS import OS
from thread.ThreadRunner import ThreadRunner
from exceptions.OSException import OSException

class CmdOS(Cmd):
    '''Class with the Command line interface to the operating system.'''
    def __init__(self):
        '''Constructor of CmdOS.'''
        Cmd.__init__(self)
        self._os = OS()
        self.prompt = 'LittleOS >> '
    
    def do_start(self, arg):
        '''Run the main thread and start it.'''
        try: 
            thr = ThreadRunner(self._os)
            thr.setDaemon(True)
            thr.start()
        except OSException: 
            print('Ha ocurrido un error. Abortado el inicio')
    
    def do_load(self, arg):
        '''Load a program for its execution.'''
        if not self._os.is_active():
            print('Hay que iniciar el sistema')
            return
        try:
            self._os.load(arg)
        except OSException:
            print('Fallo al cargar el programa.')
    
    def do_shutdown(self, arg):
        '''Stop the OS and all its threads.'''
        try:
            self._os.shutdown()
        except OSException:
            print('Ha ocurrido un error.')
    
    def do_addprog(self, arg):
        try:
            res = arg.split(';')
            real_path = res[0].replace(' ', '')
            new_file = res[1].replace(' ', '')
            self._os.add_program(real_path, new_file)
        except OSException:
            print('Ha ocurrido un error al cargar el nuevo programa.')

    def do_exit(self, arg):
        return True
    
    def help_start(self):
        print('Comando start: inicia actividades del sistema operativo.')
    
    def help_shutdown(self):
        print('Comando shutdown: detiene la ejecucion del sistema operativo.')
    
    def help_load(self):
        print('Comando load: inicia la ejecucion de un programa.')
        print('Sintaxis: load <nombreProg> , donde nombreProg es el nombre')
        print('          del archivo a correr. Debe estar almacenado en el')
        print('          sistema de archivos en la carpeta "//programs."')
    
    def help_addprog(self):
        print('Comando addprog: carga un programa desde un archivo real y lo')
        print('ubica en el sistema de archivos en la carpeta "programs."')
        print('Sintaxis: load <path> ; <nombreArch>, donde <path> es la ruta')
        print('          completa del archivo a cargar, y <nombreArch> es el')
        print('          nombre que el archivo tendra en el sistema.')
        print('Nota: este comando se ejecuta cuando el sistema esta detenido.')
    
    def help_exit(self):
        print('Comando exit: sale de la consola. Asegurese de haber detenido')
        print('el sistema por medio del comando shutdown.')