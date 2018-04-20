"""
Victor Yu
HW 2
"""
import random
import numpy as np
import matplotlib.pyplot as plt
B = np.logspace(-3,3,1000)
biterrorrate = []
#a)
mes = np.array([random.randint(0,1) for n in range(0,10000)])
#%%
def encoder(b,m):
#b)
    y = []
    for i in m:
        if i == 1:
            y.append(b)
        if i == 0:
            y.append(-b)
    y = np.array(y)
#c)
    w = np.array([np.random.normal(0,1,None) for r in range(0,len(m))])
    z = y + w
#d)
    mhat = []
    for i in z:
        if i >= 0:
            mhat.append(1)
        if i < 0:
            mhat.append(0)
    mhat = np.array(mhat)
#e)
    ber = sum(abs(mhat-m)/len(m))*100
    return [ber,m,y,w,z,mhat]
#%% 
biterrorrate = []
for i in B:
    [ber,m,y,w,z,mhat] = encoder(i,mes)
    biterrorrate.append(ber)
#f)
plt.semilogx(B,biterrorrate,'ro')
#%%
mes = np.array([random.randint(0,1) for n in range(0,10000)])
p = np.reshape(np.asmatrix(mes),(int(len(mes)/4),4))
G = np.matrix('1 1 0 1;1 0 1 1;1 0 0 0;0 1 1 1;0 1 0 0;0 0 1 0;0 0 0 1')
x = np.empty([7,1])
for row in p:
    x = np.vstack((x,np.matmul(G,row.T)%2))
x = np.ndarray.flatten(np.asarray((x[7:])))
#%%
biterrorrate = []
R = np.matrix('0 0 1 0 0 0 0;0 0 0 0 1 0 0;0 0 0 0 0 1 0;0 0 0 0 0 0 1')
def endecoder(b,m):
#b)
    y = []
    for i in m:
        if i == 1:
            y.append(b)
        if i == 0:
            y.append(-b)
    y = np.array(y)
#c)
    w = np.array([np.random.normal(0,1,None) for r in range(0,len(m))])
    z = y + w
#d)
    mhat = []
    for i in z:
        if i >= 0:
            mhat.append(1)
        if i < 0:
            mhat.append(0)
    mhat = np.array(mhat)
    P = np.reshape(np.asmatrix(mhat),(int(len(mhat)/7),7))
    Pr = np.empty([4,1])
    for row in P:
        Pr = np.vstack((Pr,np.matmul(R,row.T)%2))
    Pr = np.ndarray.flatten(np.asarray((Pr[4:])))
#e)
    ber = sum(abs(Pr-mes)/len(mes))*100
    return [ber,m,y,w,z,mhat]

for i in B:
    [ber,m,y,w,z,mhat] = endecoder(i,x)
    biterrorrate.append(ber)