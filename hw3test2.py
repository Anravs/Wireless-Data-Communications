import numpy as np
import matplotlib.pyplot as plt

#Find the hamming distance of the current spot to the next spot
def hammingdistance(t, start, end,msg):
    testBits = msg
    bits = 0
    #Assign the bits based on the trellis diagram
    if(start == 0):
        if(end == 0):
            bits = "000"
        else: #else end is 2
            bits = "111"
    if(start == 1):
        if(end == 0):
            bits = "011"
        else: #else end is 2
            bits = "100"
    if(start == 2):
        if(end == 1):
            bits = "001"
        else: #else end is 3
            bits = "110"
    if(start == 3):
        if(end == 1):
            bits = "010"
        else: #else end is 3
            bits = "101"   
    error = 0
    for i in range(3):
        if(bits[i] != testBits[t][i]):
            error += 1
    
    return error

def viterbi(msg,vit):
    vit[0][0] = 0 #set the starting point to have distance 0
    for col in range(len(msg)):
        for row in range(4): #Go through each row at each col
            if(col == len(msg)-1):
                if(row == 0 or row == 1):
                    dist1 = hammingdistance(col,row,0,msg)
                    if(dist1 + vit[col][row] < vit[col+1][0]):
                        vit[col+1][0] = dist1 + vit[col][row]
            elif(row == 0 or row == 1):
                dist1 = hammingdistance(col,row,0,msg)
                dist2 = hammingdistance(col,row,2,msg)
                if(dist1 + vit[col][row] < vit[col+1][0]):
                    vit[col+1][0] = dist1 + vit[col][row]
                if(dist2 + vit[col][row] < vit[col+1][2]):
                    vit[col+1][2] = dist2 + vit[col][row]
            elif(row == 2 or row == 3):
                dist1 = hammingdistance(col,row,1,msg)
                dist2 = hammingdistance(col,row,3,msg)
                if(dist1 + vit[col][row] < vit[col+1][1]):
                    vit[col+1][1] = dist1 + vit[col][row]
                if(dist2 + vit[col][row] < vit[col+1][3]):
                    vit[col+1][3] = dist2 + vit[col][row]    
    output = []
    #determine the first "next" chain to go into
    if(vit[len(vit)-2][0] < vit[len(vit)-2][1]):
        curr = [len(msg)-1, 0] #col, row
    else:
        curr = [len(msg)-1, 1]
    output.append(0)
    #backpropogate along all of the optimal "next" values
    for col in range(len(msg)-1, -1, -1):
        if(curr[1] == 0 or curr[1] == 1):
            out = 0
            output.append(out)
            if(curr[1] == 0): #goes to either 0 or 1
                if(vit[col-1][0] <= vit[col-1][1]):
                    curr = [col-1, 0] #col, row
                else:
                    curr = [col-1, 1]
            else: #goes to either 2 or 3
                if(vit[col-1][2] <= vit[col-1][3]):
                    curr = [col-1, 2] #col, row
                else:
                    curr = [col-1, 3]
        elif(curr[1] == 2 or curr[1] == 3):
            out = 1
            output.append(out)
            if(curr[1] == 2): #goes to either 0 or 1
                if(vit[col-1][0] <= vit[col-1][1]):
                    curr = [col-1, 0] #col, row
                else:
                    curr = [col-1, 1]
            else: #goes to either 2 or 3
                if(vit[col-1][2] <= vit[col-1][3]):
                    curr = [col-1, 2] #col, row
                else:
                    curr = [col-1, 3]
    output = output[::-1] #everything was appended in reverse order  
    output = output[1:]
    return output

def viterbi_enc(m):
    c = []
    for i in g:
        c.append(np.convolve(m, i) % 2)
    m_enc = np.array(c).T.flatten()
    return m_enc    
    
g = np.array([[1,0,0],[1,0,1],[1,1,1]])
b_num = 100
n = 10000 # n is number of information bits
m = np.random.choice(2, n)  # m is message (1 x n) m_n binary
orig = m
m_enc = viterbi_enc(m)  # encode from 4 to 7
b = np.logspace(-1, 1, b_num)[:,None]   # b is real value modulation scheme - column vector
yb = 2*(m_enc-0.5)*b                     # y is modulated signal
w = np.random.normal(0, 1, yb.shape[1])  # w is gaussian noise, u=0, var=1
zb = yb+w                                 # z is received signal at receiver
rb = (zb >= 0).astype('int')              # r is received symbols
messages = []
totalerror = []
for r in rb:  # iterate over all signal power values
    t_total = r.size//3
    msg = r.reshape(t_total, 3)  # break into chunks of 3 per message
    #The msg at this point is the list of the input sets of 3 for the entire message
    #convert all elements in msg to string
    for m in msg:
        bits = ""
        for i in m:
            bits += str(i)
        messages.append(bits)
    testBits = messages    
          
    lenBits = len(testBits)
    inf = float("inf")
    vit = []
    #Populate the entire viterbi array with infinity values at all points
    for i in range(lenBits+1):
        vit.append([])
        for j in range(4):
            vit[i].append(inf) 

    vit = viterbi(testBits, vit)
    vit = vit[0:len(orig)]
    error = 0
    for i in range(len(orig)):
        if(vit[i] != orig[i]):
            error+=1
    totalerror.append(float(error)/len(orig))
    messages = []

plot_prob, = plt.semilogx(b, totalerror, label='Error Rate')
plt.ylabel('Error Rate')
plt.xlabel('b')
plt.xlim([.1, 10])  # zoom in
plt.show()