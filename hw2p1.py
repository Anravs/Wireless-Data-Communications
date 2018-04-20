import numpy as np
import matplotlib.pyplot as plt
import random
import math

noise = np.random.normal(0,1,10000) #Create the AWGN with mean 0 and var 1
infoBits = []
infoBitsMod = []
#generates the list of modulated bits
#0 -> -b
#1 -> b
error = 0
xin = np.logspace(-3,3,num=1000)
xaxis = []
var = []
for i in range(len(xin)):
    xaxis.append(math.log(xin[i]))
test = []
for x in xin:
    test.append(math.log(x,10))
yin = []
for b in xin:
    error = 0
    errorTrack = []
    for i in range(10000):
        bit = random.randint(0,1)
        bitMod = bit
        infoBits.append(bit) #keep track of the list of original bits
        if bit == 0:
            bitMod = -1*b
        if bit == 1:
            bitMod = b
        bitMod += noise[i]
        if(bitMod >= 0):
            bitMod = 1
        if(bitMod < 0):
            bitMod = 0
        infoBitsMod.append(bitMod) #keep track of the  demodulated bits
        
        if(bitMod != bit):
            error += 1
            errorTrack.append(1)
        else:
            errorTrack.append(0)
        
    finalError = float(error)/10000
    yin.append(finalError)
    print finalError,
    print " ",
    print b
    varCurr = np.var(errorTrack)
    var.append(abs(np.var(errorTrack)))
    
plt.plot(xaxis,yin,'ro')
plt.plot(xaxis,var)
plt.axis([-3,3,0,1]);
plt.show();    
