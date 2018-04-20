import numpy as np
import matplotlib.pyplot as plt
import random
s = 100
P = np.logspace(-1,2,s)
H = np.random.normal(0,1, size = (s, 2, 2)) #(mean, std dev, size)
rzf = []
col = []
for i in range(s):
    valsrzf = []
    valscol = []
    for j in range(s):
        print i
        w = np.linalg.norm(np.linalg.inv(H[j]), axis = 1)
        w1 = w[0] ** 2
        w2 = w[1] ** 2
        val = np.log2(1+(P[i])/(2*w1))+np.log2(1+(P[i])/(2*w2))
        valsrzf.append(val)

        
        eigs = np.linalg.eig(np.linalg.inv(H[j]))
        eigs = list(eigs[0])
        lamb1 = np.abs(eigs[0])**2
        lamb2 = np.abs(eigs[1])**2
        val2 = np.log2(1+(P[i]/2)*lamb1)+np.log2(1+(P[i]/2)*lamb2)
        valscol.append(val2)

    valrzf = np.average(valsrzf)
    valscol = np.average(valscol)
    rzf.append(valrzf)
    col.append(valscol)

plt.loglog(P, rzf)
plt.loglog(P, col)
plt.show()