�}q (K copsys.fs.Inode
DirectoryInode
q)�q}q(X	   timestampqcdatetime
datetime
qC
�9d|q�qRqX   level_one_blocksq	KX   nameq
X   /qX   level_two_blocksqNubKcopsys.fs.Inode
IndexBlock
q)�q}qX   _blocksq]q(K K KKcNNNNNNesbKh)�q}q(hhC
�	�lq�qRqh	Kh
X   programsqhNubKh)�q}qh]q(KK KKK6K[NNNNesbKcopsys.fs.Inode
FileInode
q)�q}q(hhC
� tq�qRq h	Kh
X   ej1.prq!hKX   _sizeq"MubKh)�q#}q$h]q%(KKKK	K
KKKKKesbKcopsys.fs.Inode
DataBlock
q&)�q'}q(X   _dataq)X2   Name : Ejemplo
Priority : 6
-- este es un comentarq*sbKh&)�q+}q,h)X2   io y se ignora completamente
mov R0 "Hola "
mov #4q-sbKh&)�q.}q/h)X2    " como andas..."
request 1 "keyboard" 1 "display"q0sbK	h&)�q1}q2h)X2   
input "Ingrese su nombre... " #7
add R0 #7
mov #3q3sbK
h&)�q4}q5h)X2    R0
add #3 #4
show #3
free
request 1 "disk"
cd "/"q6sbKh&)�q7}q8h)X2   
cd "ejemplos"
-- asume que existe el directorio "q9sbKh&)�q:}q;h)X2   ejemplos"
newfile "prueba"
open "prueba"
write "prq<sbKh&)�q=}q>h)X2   ueba" #3
save "prueba"
close "prueba"
delete "prueq?sbKh&)�q@}qAh)X2   ba"
-- los archivos se borran para que el programaqBsbKh&)�qC}qDh)X2    pueda correr
-- varias veces sin problemas (de arqEsbKh)�qF}qGh]qH(KKKKKKKKKKesbKh)�qI}qJh]qK(KNNNNNNNNNesbKh)�qL}qMh]qN(NNNNNNNNNNesbKh)�qO}qPh]qQ(NNNNNNNNNNesbKh)�qR}qSh]qT(NNNNNNNNNNesbKh)�qU}qVh]qW(NNNNNNNNNNesbKh)�qX}qYh]qZ(NNNNNNNNNNesbKh)�q[}q\h]q](NNNNNNNNNNesbKh)�q^}q_h]q`(NNNNNNNNNNesbKh)�qa}qbh]qc(NNNNNNNNNNesbKh)�qd}qeh]qf(NNNNNNNNNNesbKh&)�qg}qhh)X   chivos duplicados)
free
qisbKh)�qj}qk(hhC
���ql�qmRqnh	Kh
X	   family.prqohK(h"M}ubKh)�qp}qqh]qr(KKK K!K"K#K$K%K&K'esbKh&)�qs}qth)X2   Name : MakeFamily
Priority : 4

skip
request 1 "kequsbKh&)�qv}qwh)X2   yboard"
input "Cual es tu nombre ..." #1
input "CoqxsbK h&)�qy}qzh)X2   mo se llama tu madre ..." #2
input "Como se llama q{sbK!h&)�q|}q}h)X2   tu padre ..." #3
free
mov #4 "Mi nombre es..."
movq~sbK"h&)�q}q�h)X2    #5 "El nombre de mi madre es..."
mov #6 "El nombrq�sbK#h&)�q�}q�h)X2   e de mi padre es..."
add #4 #1
add #5 #2
add #6 #3q�sbK$h&)�q�}q�h)X2   
request 1 "disk"
cd "/"
mkdir "family"
cd "familyq�sbK%h&)�q�}q�h)X2   "
newfile "family.tmp"
open "family.tmp"
writelineq�sbK&h&)�q�}q�h)X2    "family.tmp" #4
writeline "family.tmp" #5
writeliq�sbK'h&)�q�}q�h)X2   ne "family.tmp" #6
save "family.tmp"
readall "famiq�sbK(h)�q�}q�h]q�(K)K*K+K,K-K.K/K0K1K2esbK)h)�q�}q�h]q�(K3K4K5NNNNNNNesbK*h)�q�}q�h]q�(NNNNNNNNNNesbK+h)�q�}q�h]q�(NNNNNNNNNNesbK,h)�q�}q�h]q�(NNNNNNNNNNesbK-h)�q�}q�h]q�(NNNNNNNNNNesbK.h)�q�}q�h]q�(NNNNNNNNNNesbK/h)�q�}q�h]q�(NNNNNNNNNNesbK0h)�q�}q�h]q�(NNNNNNNNNNesbK1h)�q�}q�h]q�(NNNNNNNNNNesbK2h)�q�}q�h]q�(NNNNNNNNNNesbK3h&)�q�}q�h)X2   ly.tmp" #7
close "family.tmp"
delete "family.tmp"
q�sbK4h&)�q�}q�h)X2   cd ".."
rmdir "family"
free
request 1 "display"
shq�sbK5h&)�q�}q�h)X%   ow "Esta es mi familia"
show #7
free
q�sbK6h)�q�}q�(hhC
�%2wq��q�Rq�h	K7h
X   super.prq�hKBh"M�ubK7h)�q�}q�h]q�(K8K9K:K;K<K=K>K?K@KAesbK8h&)�q�}q�h)X2   Name : SuperProgram
Priority : 5

-- Un programa qq�sbK9h&)�q�}q�h)X2   ue prueba todas las instrucciones posibles

-- Todq�sbK:h&)�q�}q�h)X2   as las combinaciones de mov
mov #1 4
mov #2 "y"
moq�sbK;h&)�q�}q�h)X2   v #3 R0
mov #4 #1
mov R0 2
mov R1 "x"
mov R2 R0
moq�sbK<h&)�q�}q�h)X2   v R3 #2
-- Todas las combinaciones de add
add #3 5q�sbK=h&)�q�}q�h)X2   
add #2 "z"
add #1 R2
add #4 #1
add R2 5
add R1 "aq�sbK>h&)�q�}q�h)X2   "
add R0 R2
add R3 #2
-- Todas las combinaciones dq�sbK?h&)�q�}q�h)X2   e sub
sub #1 5
sub #3 R5
sub #1 #3
sub R0 1
sub R0q�sbK@h&)�q�}q�h)X2    R6
sub R2 #1
-- la instruccion que no hace nada
sq�sbKAh&)�q�}q�h)X2   kip
-- la instruccion de pedido
request 1 "keyboarq�sbKBh)�q�}q�h]q�(KCKDKEKFKGKHKIKJKKKLesbKCh)�q�}q�h]q�(KMKNKOKPKQKRKSKTKUKVesbKDh)�q�}q�h]q�(KWKXKYKZNNNNNNesbKEh)�q�}q�h]q�(NNNNNNNNNNesbKFh)�q�}q�h]q�(NNNNNNNNNNesbKGh)�q�}q�h]q�(NNNNNNNNNNesbKHh)�q�}q�h]q�(NNNNNNNNNNesbKIh)�q�}q�h]q�(NNNNNNNNNNesbKJh)�q�}q�h]q�(NNNNNNNNNNesbKKh)�q�}q�h]q�(NNNNNNNNNNesbKLh)�r   }r  h]r  (NNNNNNNNNNesbKMh&)�r  }r  h)X2   d" 1 "display" 1 "disk"
-- instrucciones de entradr  sbKNh&)�r  }r  h)X2   a de teclado
input "Por favor ingrese un texto" #1r  sbKOh&)�r	  }r
  h)X2   
intinput "Por favor ingrese un numero" #2
-- combr  sbKPh&)�r  }r  h)X2   inaciones de show
show 547
show "Hola"
show #4
-- r  sbKQh&)�r  }r  h)X2   instrucciones de disco
cd "/"
cd "programs"
cd "."r  sbKRh&)�r  }r  h)X2   
cd ".."
mkdir "temp"
rendir "temp" "pmet"
cd "pmer  sbKSh&)�r  }r  h)X2   t"
newfile "temp.tmp"
renfile "temp.tmp" "pmt.pmetr  sbKTh&)�r  }r  h)X2   "
open "pmt.pmet"
write "pmt.pmet" "file..."
writer  sbKUh&)�r  }r  h)X2    "pmt.pmet" #2
write "pmt.pmet" 5
writeline "pmt.pr  sbKVh&)�r  }r  h)X2   met" "file..."
writeline "pmt.pmet" #2
writeline "r   sbKWh&)�r!  }r"  h)X2   pmt.pmet" 5
readall "pmt.pmet" #12
save "pmt.pmet"r#  sbKXh&)�r$  }r%  h)X2   
close "pmt.pmet"
delete "pmt.pmet"
cd ".."
rmdir r&  sbKYh&)�r'  }r(  h)X2   "pmet"
showdisk
pwd
-- y por ultimo... la instruccr)  sbKZh&)�r*  }r+  h)X   ion de liberacion
free
r,  sbK[h)�r-  }r.  (hhC
�x�r/  �r0  Rr1  h	K\h
X   readyourself.prr2  hNh"MubK\h)�r3  }r4  h]r5  (K]K^K_K`KaKbNNNNesbK]h&)�r6  }r7  h)X2   Name : ReadYourself
Priority : 4

-- un programa qr8  sbK^h&)�r9  }r:  h)X2   ue se lee a si mismo e imprime su codigo

skip
reqr;  sbK_h&)�r<  }r=  h)X2   uest 1 "disk"
cd "programs"
open "readyourself.pr"r>  sbK`h&)�r?  }r@  h)X2   
readall "readyourself.pr" #1
close "readyourself.rA  sbKah&)�rB  }rC  h)X2   pr"
free
request 1 "display"
show "Puedo leerme a rD  sbKbh&)�rE  }rF  h)X   mi mismo..."
show #1
free
rG  sbKch)�rH  }rI  (hhC
���rJ  �rK  RrL  h	Kdh
X   ejemplosrM  hNubKdh)�rN  }rO  h]rP  (KcK NNNNNNNNesbu.