import numpy as np
import matplotlib.pyplot as plt
import random
import math

#Matrix multiple p * G -> 4x7 * 7 x 1 = 1 x 7
def encode(G, p):
    out = np.matmul(G,p)
    return out

def decode(p):
    R = np.matrix('0 0 1 0 0 0 0; 0 0 0 0 1 0 0; 0 0 0 0 0 1 0; 0 0 0 0 0 0 1')
    p = np.matrix(p)
    out = np.matmul(R,p)
    return out
    
noise = np.random.normal(0,1,10000) #Create the AWGN with mean 0 and var 1
infoBits = []
infoBitsMod = []
#generates the list of modulated bits
#0 -> -b
#1 -> b

G = np.matrix('1 1 0 1; 1 0 1 1; 1 0 0 0; 0 1 1 1; 0 1 0 0; 0 0 1 0; 0 0 0 1')

error = 0
#xin = np.logspace(-3,3,num=1000)
p = [[1],[0],[1],[1]]
p = np.matrix(p)
x = encode(G,p)
x = np.array(x.tolist())
y = []
for i in range(len(x)):
    if x[i]%2 == 0:
        x[i] = 0
    else:
        x[i] = 1
    y.append(x[i])
#x = np.matrix(x)        
print x
print "---"
noise = np.random.normal(0,1,10000) #Create the AWGN with mean 0 and var 1
b = .5
for i in range(len(x)):
    if x[i]%2 == 0:
        x[i] = -1*b + noise[i]
    else:
        x[i] = b + noise[i]
    if(x[i] >= 0):
        x[i] = 1
    if(x[i] < 0):
        x[i] = 0

print x
print "---"
y = decode(x)
print y
print "---"
bits = [[1],[0],[1],[1]]
print len(bits)
print len(y)

error = 0

for x in range(len(y)):
    if y[x] != bits[x]:
        error+=1
print error

'''for x in xin:
    test.append(math.log(x,10))
yin = []
for b in xin:
    error = 0
    p = [[]]
    for i in range(10000):
        if((i+1)%4 == 0):
            p = np.matrix(p)
            x = encode(G,p)
            p = [[]]
            x = np.array(a.tolist())
            
        bit = random.randint(0,1)
        p[0].append(bit)
  '''          
