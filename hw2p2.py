import numpy as np
import matplotlib.pyplot as plt
import random
import math

#0 -> -b
#1 -> b

#Matrix multiple p * G -> 1x4 * 4 x 7 = 1 x 7
def encode(G, p):
    out = np.matmul(G,p)
    return out
    
#Add the AWGN to the bits and then turn it back into either 0 or 1
def modulate(x,b,noise):
    for i in range(len(x)):
        if x[i]%2 == 0:
            x[i] = -1*b + noise[i]
        else:
            x[i] = b + noise[i]
        if(x[i] >= 0):
            x[i] = 1
        if(x[i] < 0):
            x[i] = 0
    return x

#Do the parity checking    
def parityCheck(r):
    H = np.matrix('1 0 1 0 1 0 1; 0 1 1 0 0 1 1; 0 0 0 1 1 1 1')    
    z = np.matmul(H,r)
    #Get the decimal value of the parity check and flip that bit
    dec = 0
    if(z[0] == 1):
        dec += 4
    if(z[1] == 1):
        dec += 2
    if(z[2] == 1):
        dec += 1
    
    if(dec > 0):
        r[dec-1] = (r[dec-1] + 1)%2
    
    return r
 
#decode the input signal 
def decode(p,R):
    p = np.matrix(p)
    out = np.matmul(R,p)
    return out

noise = np.random.normal(0,1,70000) #Create the AWGN with mean 0 and var 1  
 
G = np.matrix('1 1 0 1; 1 0 1 1; 1 0 0 0; 0 1 1 1; 0 1 0 0; 0 0 1 0; 0 0 0 1')
R = np.matrix('0 0 1 0 0 0 0; 0 0 0 0 1 0 0; 0 0 0 0 0 1 0; 0 0 0 0 0 0 1')

#Create all the input values
xin = np.logspace(-3,3,num=300)
xaxis = []
for i in range(len(xin)):
    xaxis.append(math.log(xin[i]))
var = []
error = 0
yin = []
#Loop for values in the range of [10^-3, 10^3]
for b in xin:
    error = 0
    bits = []
    errorTrack = []
    #Generate the 10000 random bits
    for i in range(10000):
        if(i%4 == 0 and i != 0):
            p = np.matrix(bits)
            x = encode(G,p)            
            x = np.array(x.tolist())
            y = modulate(x,b,noise[i:i+7])
            y = parityCheck(y)
            y = decode(y,R)           
            for x in range(len(y)):
                if y[x] != bits[x]:
                    error+=1      
                    errorTrack.append(1)
                else:
                    errorTrack.append(0)
            bits = []   
                
        bit = random.randint(0,1)
        bits.append([bit])
        
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
