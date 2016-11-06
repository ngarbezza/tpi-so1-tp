'''
Created on 15/11/2009
@author: Nahuel
'''

file = open('../oslogging/littleos.log', 'a')
file.write('Hola')
file.close()

#===============================================================================
# #Singleton
#
# class A():
#    instance = None
#    
#    def __new__(cls, *args, **kwargs): 
#        if cls.instance is None:
#            cls.instance = object.__new__(cls)
#        return cls.instance
#    
#    @classmethod
#    def getInstance(cls):
#        return cls.instance
#    
#    def __init__(self, v):
#        self.valuea = v
#    
# a2 = A(23)
# a1 = A.getInstance()
# a3 = A.getInstance()
# 
# print(a1)
# print(a2)
# print(a3)
# print(a1 == a2)
# assert a1 is a2
# assert a2 is a3
# print(a1.valuea, a2.valuea, a3.valuea)
#===============================================================================

#from pyparsing_py3 import * #@UnusedWildImport

#===============================================================================
# import pickle
# from opsys.fs.Inode import *
# 
# with open('dump.tmp', 'rb') as fopen:
#    datos = pickle.load(fopen)
# 
# datos[3] = DirectoryInode('/', 1)
# 
# with open('dump.tmp', 'wb') as f:
#    pickle.dump(datos, f, pickle.HIGHEST_PROTOCOL)
# 
# with open('dump.tmp', 'rb') as fopen:
#    datos = pickle.load(fopen)
# 
# print(datos)
#===============================================================================


#stri = '1'
#lista = ['1', 'zz']
#exp = oneOf(lista).setParseAction(lambda s,l,t : int(t[0]))
#print(exp.parseString(stri))

#===============================================================================
# from parsing.pyparsing_py3 import * #@UnusedWildImport
# 
# file = open('../../config/osconfig.cfg')
# assign = Word(alphas) + Literal('=').suppress() + Word(alphanums)
# config = Dict(OneOrMore(Group(assign)))
# commentLine = '--' + restOfLine
# config.ignore(commentLine)
# res = config.parseString(file.read())
# file.close()
# print(res)
#===============================================================================

#simbolo = Group(Word(alphas) + Literal("=").suppress() + Word(alphas))
#dicti = Dict(OneOrMore(simbolo))
#file = open('testFile')
#tok = dicti.parseString(file.read())
#print(tok)
#print(tok.keys())
#print(tok['chau'])
#file.close()

#class X:
#    def add(self, *args):
#        return int(args[0]) + int(args[1])
#
#class Y:
#    def armaunX(self, clase):
#        return clase()

#===============================================================================
# listaInst =['MOV', 'ADD', 'SUB']
# regs = ['R0','R1','R2','R3','R4','R5','R6','R7']
# digits = "0123456789"
# parameter = oneOf(regs) | Word(digits)
# instruction = Group(oneOf(listaInst) + ZeroOrMore(parameter))
# instList = Group(OneOrMore(instruction))
# procName = Suppress('Name : ') + Word(alphas)
# procPriority = Suppress('Priority : ') + Word(digits)
# process = procName + procPriority + instList
#===============================================================================

#===============================================================================
# #pasar de string a nombre de clase y usarlo
# #forma 1: usando la funcion getattr (feo)
#
# import matrix.Matrix
# 
# clase = "Matrix"
# clasePosta = getattr(matrix.Matrix, clase)
# miMatrix = clasePosta((1, 2))
# print(miMatrix)
#
# #forma 2: usando la funcion eval (que feeeeo)
#
# from matrix.Matrix import Matrix
# clase = "Matrix"
# miMatrix = eval(clase)((1,2))
# print(miMatrix)
#
# #forma 3: usando mapeos (esta es mejor, porque se pueden manejar exceptions)
#
# from matrix.Matrix import Matrix
# clase = "Matrix"
# classMap = {"Matrix" : Matrix}
# miMatrix = classMap[clase]((1,2))
# print(miMatrix)

#===============================================================================
