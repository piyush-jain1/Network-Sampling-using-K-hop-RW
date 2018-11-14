import numpy as np

A = 162298
AP = 317487
AC = 162919
APC = 318108

ac = np.fromfile('data/aca.bin', np.float32).reshape(AC, 100)
ap = np.fromfile('data/apa.bin', np.float32).reshape(AP, 100)
apc = np.fromfile('data/apc.bin', np.float32).reshape(APC, 100)

Ac = ac[:A]
Ap = ap[:A]
Apc = apc[:A]

fac = open('data/aca.txt', 'w')
fap = open('data/apa.txt', 'w')
fapc = open('data/apc.txt', 'w')

fac.write(str(A) + ' ' + str(100) + '\n')
fap.write(str(A) + ' ' + str(100) + '\n')
fapc.write(str(A) + ' ' + str(100) + '\n')

for a in range(A):
	fac.write(str(a) + ' ' + ' '.join([str(x) for x in Ac[a]]) + '\n')
	fap.write(str(a) + ' ' + ' '.join([str(x) for x in Ap[a]]) + '\n')
	fapc.write(str(a) + ' ' + ' '.join([str(x) for x in Apc[a]]) + '\n')
