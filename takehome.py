import string
import random
import collections
import numpy as np
import matplotlib.pyplot as plt

def getDecimal(s):
    dec = 0
    s = s[::-1] #reverse s
    for i in range(len(s)):
        dec += s[i] * 2**i
    return dec

def getMatch(s, H):
    for i in range(len(H)):
        for j in range(len(H[i])):
            if s[j] != H[i][j]: #if something doesn't match then we immediately know it's wrong
                break
            if j == 3: #reached the end
                return i
    
    
def matmul(mat1, mat2):
    output = []
    for i in range(len(mat1)):
        output.append(mat1[i]*mat2[i])
    
    return np.asarray(output)

class Tree(object):
    def __init__(self, name = 'root', freq = 0, children = None):
        self.name = name
        self.children = [None, None]
        self.freq = freq
        self.real_name = ""
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name + " - " + str(self.freq)
    def add_child(self,node):
        assert isinstance(node, Tree)
        if self.children[0] is None:
            self.children[0] = node
        else: self.children[1] = node
    def set_real_name(self, real_name):
        self.real_name = real_name
    def traversePreorder(self, root, binary_sum, code_book):
        #traverse function will print all the node in the tree.             
        if root is not None:
            if len(root.real_name) != 0:
                code_book[root.real_name] = binary_sum
            self.traversePreorder(root.children[0], binary_sum + "0", code_book)
            self.traversePreorder(root.children[1], binary_sum + "1", code_book)
        return code_book
              
seq = "" #sequence of letters
freq = collections.Counter()
#Generate 10,000 random letters in a string and store frequency of each letter
alphabet = ['A','B','C','D']
numBits = 49995
for i in range(numBits):
    choice = random.randint(0,3)
    randLetter = alphabet[choice]
    seq += randLetter
    freq[randLetter] += 1
#print seq   

#-----------------------CODE PROCEEDS IN THIS ORDER:-------------------------
'''
1) Source Encoding/Compression
2) Channel Encoding
3) Modulation 
4) Addition of noise through the channel
5) Demodulation 
6) Channel Decoding
7) Calculation of Bit Error Rate
'''
#-------------------------SOURCE ENCODING------------------------------------

#ALGORITHM    
#Create a tree based on the Huffman Coding Algorthm
#Step 1. Create a parentless node for each symbol. Each node should include the symbol and its probability.
#Step 2. Select the two parentless nodes with the lowest probabilities.
#Step 3. Create a new node which is the parent of the two lowest probability nodes.
#Step 4. Assign the new node a probability equal to the sum of its children's probabilities.
#Step 5. Repeat from Step 2 until there is only one parentless node left.

treeList = []
t = Tree()
for i in range(len(freq.most_common())):
    t = Tree(freq.most_common()[i][0], freq.most_common()[i][1])
    t.real_name = freq.most_common()[i][0]
    treeList.append(t)
    print t       
while len(treeList) != 1:
    #Gets the first and second lowest values in the list
    first = {float("inf") : 0} #value : index 
    second = {float("inf") : 0} #value : index
    for i in range(len(treeList)):
        if treeList[i].freq <= first.keys()[0]:
            second, first = first, {treeList[i].freq : i}
        elif first.keys()[0] <= treeList[i].freq <= second.keys()[0]:
            second = {treeList[i].freq : i}
    #Create the a new tree node and populate it with name, frequency, and children 
    new_name = treeList[second.values()[0]].name + treeList[first.values()[0]].name
    tot_freq = treeList[second.values()[0]].freq + treeList[first.values()[0]].freq
    t = Tree(new_name, tot_freq, [treeList[second.values()[0]], treeList[first.values()[0]]]) 
    #Add new tree node before two lowest values (they should be adjacent I think w/ second in front)
    treeList.insert(second.values()[0],t)
    #Create the new name and new node for the tree and remove old values from the list
    if(first.values()[0] > second.values()[0]):
        treeList.pop(first.values()[0]+1)
        treeList.pop(second.values()[0]+1)
    else:
        treeList.pop(second.values()[0]+1)
        treeList.pop(first.values()[0])
print "\nCode words are: "
codebook = dict()
print t.traversePreorder(t,"",codebook)

#Get the message encoded through hamming
message = ""
for i in seq:
    message += codebook[i]

#--------------------------------CHANNEL ENCODING-------------------------------------


#Hamming(15,11) -> n = 15, k  = 11
n = 15
k = 11

#Get the groupings of input messages to be put through the hamming encoding
messages = []
grouping = []
print len(message)
for i in range(len(message)):
    grouping.append(int(message[i]))
    if i % k == 10:
        messages.append(grouping)
        grouping = []

#G is generator matrix (k x n)
#H is parity-check matrix (n-k x n)
P = np.array([[1, 1, 0, 0], # (k x n-k)
             [1, 0, 1, 0],
             [0, 1, 1, 0],
             [1, 1, 1, 0],
             [1, 0, 0, 1],
             [0, 1, 0, 1],
             [1, 1, 0, 1],
             [0, 0, 1, 1],
             [1, 0, 1, 1],
             [0, 1, 1, 1],
             [1, 1, 1, 1]])
G = np.c_[np.identity(k, dtype=int), P]      #G = [I_{k} P^T]
R = np.c_[np.identity(k, dtype=int), P*0]
H = np.c_[P.T, np.identity(n-k, dtype=int)]      #H = [P, I_{n-k}]

print G
print ""
print R
print ""
print H
    
#Generate the list of all codewords by doing x = msg * G    
codewords = np.empty([1,n])    
    
for i in messages:
    codewords = np.vstack((codewords,np.matmul(i,G)%2))

totCW = np.ndarray.flatten(codewords[1:]).tolist()    
#print totCW
outBits = ""
for i in totCW:
    outBits += str(int(i))

totError = []

t2 = np.linspace(-20,20,51)

#--------------------------------MODULATION-------------------------------------
for i in t2:
    print "#--------------------------------MODULATION-------------------------------------"
    print "current value of i is:",
    print i
    b = (10.0)**(i/20.0)
    
    t = np.linspace(-.5, .5, 51)

    cosines = [b*np.cos(2*np.pi*t), b*np.cos(2*np.pi*t+np.pi/2), b*np.cos(2*np.pi*t+np.pi), b*np.cos(2*np.pi*t+3*np.pi/2)]

    waveforms = []
            
    for i in range(0,len(totCW),2):
        x = str(int(totCW[i]))+str(int(totCW[i+1]))
        if x == '00':
            waveforms.append(cosines[0]) 
        elif x == '01':        
            waveforms.append(cosines[1]) 
        elif x == '11':
            waveforms.append(cosines[2]) 
        elif x == '10':   
            waveforms.append(cosines[3])
            
    #------------------------------CHANNEL NOISE-------------------------------------        
    print "#------------------------CHANNEL NOISE-------------------------------------"
    noise = np.random.normal(0,1, size = (len(waveforms), 51)) #Create the AWGN with mean 0 and var 1
    #noisyWaves = []
    noisyWaves = waveforms + noise       
    #--------------------------------DEMODULATION-------------------------------------
    print "--------------------------------DEMODULATION-------------------------------------"
    outBits = ""

    #Multiply the input wave by all possible cosine waves + phase shifts and find the
    #element wise max. The argmax of these will then be connected to the corresponding
    #output bits
    counter = 0;
    for i in noisyWaves:
        if(counter % 1000 == 0):
            print counter
        
        max = np.argmax([sum(i*cosines[0]), sum(i*cosines[1]), sum(i*cosines[2]), sum(i*cosines[3])])
        
        if max == 0:
            outBits += "00"
        elif max == 1:
            outBits += "01"
        elif max == 2:
            outBits += "11"
        elif max == 3:
            outBits += "10"
        counter+=1
               
    #------------------------------CHANNEL DECODING----------------------------------
    print "------------------------------CHANNEL DECODING----------------------------------"
    #Generate all the syndrome vectors and then the corresponding decimal bit
    #Then multiply by the matrix R to get the resulting chnnale decoded message

    noisyCodewords = []
    grouping = []
    #First split the input into groupings of 15
    for i in range(len(outBits)):
        grouping.append(int(outBits[i]))
        if i % n == 14:
            noisyCodewords.append(grouping)
            grouping = []

    #Now calculate the syndromes and flip the corresponding index of the msg
    for i in range(len(noisyCodewords)):
        s = np.matmul(noisyCodewords[i],H.T)
        for i in range(len(s)):
            s[i] %= 2
        sd = getDecimal(s)
        #print sd
        if(sd > 0): #if there is an error get the matching row and flip that bit index
            s = getMatch(s, H.T)
            #s = sd
            noisyCodewords[i][s-1] = (noisyCodewords[i][s-1] + 1) % 2 #Flip the corresponding bit
     
    #Lastly multiply by R to get the output messages and append them all together
    chnOut = ""
    for i in range(len(noisyCodewords)):
        p = np.matmul(noisyCodewords[i], R.T) #creates a (1x11) message
        for j in range(len(p)):
            chnOut += str(p[j])
     
    #------------------------------SOURCE DECODING-----------------------------------    
    counter = 0
    for i in range(len(chnOut)):
        if message[i] != chnOut[i]:
            counter+=1
    error = counter/float(numBits*2)
    totError.append(error)
    print error

plt.plot(t2,totError)
plt.title("BER vs b")
plt.xlabel("Decibel Values of b")
plt.ylabel('Bit Error rate')
plt.show()
    