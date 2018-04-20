import numpy as np
import matplotlib.pyplot as plt
import random

#Generate random message X
X = []
choices = [-1, 1]
for i in range(4):
    choice = random.randint(0,1)
    X.append(float(choices[choice]))

X = np.matrix(X)
X = np.matrix.transpose(X)
print "~~~~"

Nt = 4
Nr = 4
s = 1000
H = np.random.normal(0,1, size = (s, Nt, Nr)) #(mean, std dev, size)
Z = np.random.normal(0,1, size = (s, 1, 4)) #(mean, std dev, size)
#ZERO-FORCING DETECTION METHOD
P = [.1, .5, 1, 5, 10]

detectionErrors = [[],[],[],[],[]]

for i in range(len(H)):
    print i
    for j in range(len(P)):
        x = np.sqrt(P[j]) * X #sqrt(p) * x
        G = H[i]
        ztemp = Z[i]
        z = []
        for k in range(len(ztemp[0])):
            z.append([ztemp[0][k]])
        y = np.matmul(G,x) + z #y = H*X + Z
        xhat = np.matmul(np.linalg.inv(G),y) #H^1*y
        bool = True
        for k in range(len(xhat)):
            if xhat[k] < 0:
                xhat[k] = -1
            if xhat[k] > 0:
                xhat[k] = 1
            if xhat[k] != X[k]:
                bool = False
        if(bool):
            result = 1
        else:
            result = 0
        detectionErrors[j].append(result)

avgs = []
for i in range(len(detectionErrors)):
    avgs.append(1 - np.average(detectionErrors[i]))

print avgs
        
plt.plot(P,avgs)
#plt.show()
detectionErrors = [[],[],[],[],[]]

#MINIMUM MEAN-SQUARE ERROR
print "---------"

for i in range(len(H)):
    print i
    for j in range(len(P)):
        x = np.sqrt(P[j]) * X #sqrt(p) * x
        G = H[i]
        ztemp = Z[i]
        z = []
        for k in range(len(ztemp[0])):
            z.append([ztemp[0][k]])
        y = np.matmul(G,x) + z #y = H*X + Z
        w = np.matmul(np.linalg.inv(np.matmul(np.matrix.transpose(G),G)+1.0/P[j]*np.identity(4)),np.matrix.transpose(G))
        xhat = np.matmul(w,y) #w*y, w = (H*H^H + 1/SNR*I)^-1 * H^H
        bool = True
        for k in range(len(xhat)):
            if xhat[k] < 0:
                xhat[k] = -1
            if xhat[k] > 0:
                xhat[k] = 1
            if xhat[k] != X[k]:
                bool = False
        if(bool):
            result = 1
        else:
            result = 0
        detectionErrors[j].append(result)

avg = []
for i in range(len(detectionErrors)):
    avg.append(1 - np.average(detectionErrors[i]))

print "egg"
print avgs
print avg
plt.plot(P,avg)
plt.show()