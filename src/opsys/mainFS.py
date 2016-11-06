'''
Created on 18/12/2009
@author: Nahuel
'''

# Agregar aca el path hasta la carpeta src (anda para linux y win)
#       siempre usar barras /, no \
#==============================================================================
# import sys
# sys.path.append("aca va el path")
#==============================================================================

import sys
sys.path.append("F:/Entrega final SO1/SO1-NahuelGarbezza-20328/src")

from opsys.fs.CmdFileSystem import CmdFileSystem

if __name__ == '__main__':
    CmdFileSystem().cmdloop()
