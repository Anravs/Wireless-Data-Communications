import numpy as np
import matplotlib.pyplot as plt
#Now populate the entire viterbi tree with all values iteratively
#Replace a value with a smaller version along that path   
#for j in range(lenBits+1): #+1 because there is an initial placement before all other bits are compared for hamming distance
#    for k in range(4): #Go through each row at column j 
#        if(i = 

#Find the hamming distance of the current spot to the next spot
def hammingdistance(t, start, end,msg):
    #testBits = ["110","110","110","111","010","101","101"]
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
    
def viterbi(t, path, row, total,msg): #data array, which column we're in, which row we're in, path thus far, total hamming distance, and the input message
    print t
    path.append(row)
    #base case
    if(t == len(msg)-1): #Will not complete the path and so can be ignored
        #print "here"
        if(row == 2 or row == 3):
            return (total, "-1", path) #return that this path fails
        else:
            dist = hammingdistance(t, row, 0,msg) #get hamming distance to 0
            finalTotal = total + dist #sum final distance
            return(finalTotal, "0",path) #return the final total along this path, output bit (0 for last bit), and path traveled
                
    #actual recursion
    
    bool1 = True #booleans used to see if the path has succeeded or not (if a -1 was returned at the end)
    bool2 = True
    if(row == 0 or row == 1): #return what the output should be when it returns to previous state
        output = "0"
        #run the recursion on the two possible paths from the current location
        dist1 = hammingdistance(t,row,0,msg)
        dist2 = hammingdistance(t,row,2,msg)
        (finalTotal1, output1, finalPath1) = viterbi(t+1, path, 0, total+dist1,msg)
        (finalTotal2, output2, finalPath2) = viterbi(t+1, path, 2, total+dist2,msg)
    else:
        output = "1"
        #run the recursion on the two possible paths from the current location
        dist1 = hammingdistance(t,row,1,msg)
        dist2 = hammingdistance(t,row,3,msg)
        (finalTotal1, output1, finalPath1) = viterbi(t+1, path, 1, total+dist1,msg)
        (finalTotal2, output2, finalPath2) = viterbi(t+1, path, 3, total+dist2,msg)

        
    #analyze the output from running viterbi on both paths and appropriately return something
    if(output1 == "-1"):
        bool1 = False
    
    if(output2 == "-1"):
        bool2 = False

    if(bool1 == False and bool2 == False): #if both path fails
        return (total, "-1", path) #return that this path fails
    
    elif(bool1 == False): #if the first path fails only use the second path
        output += output2
        return(finalTotal2,output,path)
    
    elif(bool2 == False): #if the second path fails only use the first path
        output += output1
        return(finalTotal1,output,path)
    
    else: #otherwise if both paths are valid choose to return the minimum final total path
        if(finalTotal1 < finalTotal2): #use the first path
            output += output1
            return(finalTotal1, output, path)
        else: #otherwise use the second path
            output += output2
            return(finalTotal2, output, path)            

def viterbi_enc(m):
    c = []
    for i in g:
        c.append(np.convolve(m, i) % 2)
    m_enc = np.array(c).T.flatten()
    return m_enc

g = np.array([[1,0,0],[1,0,1],[1,1,1]])
b_num = 100
n = 10  # n is number of information bits
m = np.random.choice(2, n)  # m is message (1 x n) m_n binary
orig = m
m_enc = viterbi_enc(m)  # encode from 4 to 7
print m
print "______________"
b = np.logspace(-1, 1, b_num)[:,None]   # b is real value modulation scheme - column vector
yb = 2*(m_enc-0.5)*b                     # y is modulated signal
w = np.random.normal(0, 1, yb.shape[1])  # w is gaussian noise, u=0, var=1
zb = yb+w                                 # z is received signal at receiver
rb = (zb >= 0).astype('int')              # r is received symbols
print rb
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~888"
messages = []
for r in rb:  # iterate over all signal power values
    t_total = r.size//3
    msg = r.reshape(t_total, 3)  # break into chunks of 3 per message
    #The msg at this point is the list of the input sets of 3 for the entire message

t_total = rb[99].size//3
msg = rb[99].reshape(t_total,3)
#convert all elements in msg to string
for m in msg:
    bits = ""
    for i in m:
        bits += str(i)
    messages.append(bits)
#print msg
#msg = ["110","110","110","111","010","101","101"]
vit = viterbi(0,[],0,0,messages)
print ""
print vit[1][1:len(vit[1])-1]
out = []
for i in range(len(vit[1])-1):
    if i > 0:
        out.append(int(vit[1][i]))
print out
print orig.tolist()

#words = []
#for t, word in enumerate(msg):
#    words.append(word.tolist())       
#print viterbi(0,[],0,0) #run viterbi on starting column, empty path, row 0, and total = 0
    