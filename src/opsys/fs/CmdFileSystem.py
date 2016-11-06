'''
Created on 16/12/2009
@author: Nahuel
'''

from cmd import Cmd
from opsys.fs.FileManager import FileManager
from exceptions.OSException import OSException
from oslogging.Logger import Logger

class CmdFileSystem(Cmd):
    '''
    Command Line Interface to the file manager.
    
    @ivar _fm: the file manager.
    @ivar prompt: the symbol shown before every command.
    '''
    def __init__(self):
        '''Constructor of CmdFileSystem'''
        Cmd.__init__(self)
        self._fm = FileManager(True)
        self.prompt = self._fm.get_cwd()[0] + '>> '
    
    def make_prompt(self):
        '''Updates the prompt with the current directory.'''
        self.prompt = self._fm.get_cwd()[0] + '>> '
    
    def do_cd(self, arg):
        try:
            self._fm.change_directory(arg.replace(' ',''))
            self.make_prompt()
        except OSException:
            print('No se encuentra el directorio.')
    
    def do_showdisk(self, arg):
        '''Show all the blocks in the disk.'''
        self._fm.get_llfm().print_disk()
    
    def do_mkdir(self, arg):
        '''Make a new directory.'''
        self._fm.create_directory(arg.replace(' ',''))
    
    def do_rmdir(self, arg):
        '''Removes an empty directory.'''
        try: 
            self._fm.remove_directory(arg.replace(' ',''))
        except OSException: 
            print('No se encuentra el directorio o este no esta vacio.')
    
    def do_newfile(self, arg):
        '''Creates a new file.'''
        self._fm.create_file(arg.replace(' ',''))
    
    def do_open(self, arg):
        '''Load a file in memory.'''
        try: 
            self._fm.open(arg.replace(' ',''))
        except OSException: 
            print('No se encuentra el archivo.')
    
    def do_close(self, arg):
        try: 
            self._fm.close(arg.replace(' ',''))
        except OSException: 
            print('No se encuentra el archivo o este no esta abierto')
    
    def do_save(self, arg):
        try: 
            self._fm.save(arg.replace(' ',''))
        except OSException: 
            print('No se encuentra el archivo o este no esta abierto')
    
    def do_write(self, arg):
        try:
            res = arg.split(';')
            self._fm.write(res[0].replace(' ', ''), res[1])
            print('Escritura con exito en el archivo ' + res[0] + '.')
        except IndexError: 
            print('Faltan parametros.')
        except OSException: 
            print('No se encuentra el archivo o este no esta abierto.')
    
    def do_exit(self, arg):
        Logger.get_instance().close_log_file()
        return True
    
    def do_renfile(self, arg):
        try:
            res = arg.split(';')
            source = res[0].replace(' ', '')
            dest = res[1].replace(' ', '')
            self._fm.ren_file(source, dest)
            print('Archivo ' + source + ' renombrado con exito a ' + dest + '.')
        except IndexError: 
            print('Faltan parametros.')
        except OSException: 
            print('No se encuentra el archivo o este esta abierto.')
    
    def do_rendir(self, arg):
        try:
            res = arg.split(';')
            source = res[0].replace(' ', '')
            dest = res[1].replace(' ', '')
            self._fm.ren_dir(source, dest)
            print('Directorio ' + source + ' renombrado con exito a ' + dest + '.')
        except IndexError: 
            print('Faltan parametros.')
        except OSException: 
            print('No se encuentra el directorio.')
    
    def do_delete(self, arg):
        try: 
            self._fm.delete(arg.replace(' ',''))
        except OSException: 
            print('No se encuentra el archivo o esta cargado en memoria.')
    
    def do_ls(self, arg):
        print(self._fm.ls())
    
    def do_addprog(self, arg):
        try:
            res = arg.split(';')
            self._fm.add_program(res[0].replace(' ',''), res[1].replace(' ',''))
            self.make_prompt()               #updates the path
            print('Programa cargado con exito.')
        except IndexError: 
            print('Faltan parametros.')
        except OSException: 
            print('Fallo la carga del programa.')
    
    def do_dir(self, arg):
        print('Para listar archivos use el comando -ls-.')
    
    def help_ls(self):
        print('Comando ls : lista contenido del directorio actual')
        print('Sintaxis  : >> ls')
    
    def help_cd(self):
        print('Comando cd : Cambia de directorio.')
        print('Sintaxis  : >> cd <nombreDir>')
        print('  donde <nombreDir> debe estar en el directorio actual')
        print('  Usos especiales: >> cd ..   vuelve al directorio padre')
        print('                   >> cd /    vuelve al directorio raiz')
        
    def help_mkdir(self):
        print('Comando mkdir : Crea un directorio en el directorio actual.')
        print('Sintaxis : >> mkdir <nombreDir>')
        print('  donde <nombreDir> es el nombre del nuevo directorio actual.')
    
    def help_rmdir(self):
        print('Comando rmdir : Elimina un directorio que esta')
        print('                en el directorio actual.')
        print('Sintaxis : >> rmdir <nombreDir>')
        print('  donde <nombreDir> es el nombre directorio a eliminar.')
        print('Nota: El directorio debe estar vacio antes de su eliminacion')
    
    def help_rendir(self):
        print('Comando rendir : Cambia de nombre un directorio.')
        print('Sintaxis : >> rendir <nombreViejo> ; <nombreNuevo>')
        
    def help_renfile(self):
        print('Comando renfile : Cambia de nombre un archivo')
        print('Sintaxis : >> renfile <nombreViejo> ; <nombreNuevo>')
        print('Nota: Si el archivo esta cargado en memoria,')
        print('      no se puede renombrar.')
    
    def help_delete(self):
        print('Comando delete : Elimina un archivo.')
        print('Sintaxis : >> delete <nombreArchivo>')
        print('Nota: El archivo debe estar en el directorio actual')
        print('      y no debe estar cargado en memoria.')
        
    def help_newfile(self):
        print('Comando newfile : Crea archivos nuevos.')
        print('Sintaxis : >> newfile <nombre>')
    
    def help_open(self):
        print('Comando open : Carga archivo en memoria, para su lectura ')
        print('               y/o modificacion.')
        print('Sintaxis : >> open <nombreArch>')
    
    def help_close(self):
        print('Comando close : Elimina archivo en memoria, sin guardar')
        print('                cambios en el disco.')
        print('Sintaxis : >> close <nombreArch>')
    
    def help_save(self):
        print('Comando save : Actualiza en el disco los datos en memoria ')
        print('               para una archivo dado.')
        print('Sintaxis : >> save <nombreArch>')
    
    def help_write(self):
        print('Comando write : Añade datos a un archivo cargado en memoria.')
        print('Sintaxis : >> write <nombreArch>;datos')
    
    def help_addprog(self):
        print('Comando addprog : Recibe una ubicacion (path absoluto) del')
        print('                  disco real y carga ese archivo creando')
        print('                  uno nuevo en el sistema de archivos.')
        print('Sintaxis : >> addprog <rutaArch> ; <nombre>')
        print('    donde <nombre> es el nombre que tendra el nuevo archivo')
        print('El archivo se carga en el directorio //programs')