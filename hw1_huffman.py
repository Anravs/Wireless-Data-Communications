import string
import random
import collections

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
for i in range(10000):
    randLetter = random.choice(string.lowercase)
    seq += randLetter
    freq[randLetter] += 1
    
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
print codebook
codeword = ""
     
print "\nAverage Code Length is: "
average = 0
for key, value in codebook.items():
    average += len(value)
print (float(average) / len(codebook.keys()))