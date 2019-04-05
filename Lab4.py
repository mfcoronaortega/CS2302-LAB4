#Course: CS 2302 Data Structures | Spring 2019
#Author: Maria Fernanda Corona Ortega
#Assignment: Lab 4
#Instructor: Olac Fuentes
#Purpose of Code: The purpose of this code is to implement and modify basic 
#BTree functions with a BTree of size 5
#Last Modification: 04/05/2019 1:39pm
import random
import timeit

class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=5):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items

def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    T.item.append(i)  
    T.item.sort()

def IsFull(T):
    return len(T.item) >= T.max_items

def Insert(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
        
        
def height(T):
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])
        
        
def Search(T,k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T,k)],k)
                  
def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t,end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i],end=' ')
        Print(T.child[len(T.item)])    
 
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')
    
def SearchAndPrint(T,k):
    node = Search(T,k)
    if node is None:
        print(k,'not found')
    else:
        print(k,'found',end=' ')
        print('node contents:',node.item)
        
##############################################################################
        
def CompHeight(T):#Computes height of Tree
    if T.isLeaf:
        return 0
    return 1 + CompHeight(T.child[0])

def ToList(T, L):#Extracts elements into sorted list
    if T.isLeaf:
        for t in T.item:
            L.append(t)
    else:
        for i in range(len(T.item)):
            ToList(T.child[i], L)
            L.append(T.item[i])
        ToList(T.child[len(T.item)], L)
    return L

def MinAtDepth(T,d):#Returns minimun element at depth
    if d == 0:
        return T.item[0]
    else:
        return MinAtDepth(T.child[0], d-1)

def MaxAtDepth(T,d):#Returns maximum element at depth
    if d == 0:
        return T.item[len(T.item)-1]
    else:
        return MaxAtDepth(T.child[len(T.child)-1], d-1)

def NodesAtDepth(T,d): # Returns number of nodes at given depth
    count = 0
    if d == 0: #root located at height 0 will contain a single node
        return 1
    if T.isLeaf:
        return len(T.child)
    else:
        for i in T.child:
            count += NodesAtDepth(i,d-1)
    return count

def PrintAtDepth(T,d):#Prints all items in tree at given depth
    if d == 0:
        print(T.item[:])
    else:
        for i in T.child:
            PrintAtDepth(i, d-1)

def FullNodes(T):#FIXME Returns number of nodes that are full
    count = 0
    if T is None:
        return 0
    if T.isLeaf:
        if len(T.item) == T.max_items:
            return 1
        else:
            return 0
    else:
        for i in T.child:
            count += FullNodes(i)
    return count

def FullLeaves(T):#Returns number of leaves that are full
    count = 0
    if T.isLeaf:
        if len(T.item) == T.max_items:
            return 1
        else:
            return 0
    else:
        for i in T.child:
            count += FullLeaves(i)
    return count
        
def FindDepth(T,k):#FIXME Given a key returns depth at which it is found or -1 if not there
    depth = 0
    if T is None: 
        return -1
    if T.isLeaf: #I item is not found returns -11, needs to return -1
        if k in T.item:
            return 1
        else:
            return 0
    else:
        depth =+ FindDepth(T.child[FindChild(T,k)],k)
    return depth

##############################################################################




##########################TESTIING AND IMPLEMENTATION#########################
L = []
T = BTree()

size = 100

for i in range(size):
    L.append(random.randint(0, size*2))
    
for i in L:
    print('Inserting',i)
    Insert(T,i)
    PrintD(T,'') 
    #Print(T)
    print('\n####################################')
         
##########################TESTIING COMPHEIGHT##################################

start = timeit.default_timer()

print(CompHeight(T))

stop = timeit.default_timer()

print('CompHeight Execution: ', stop - start)  

print()
          
###############################TESTIING TOLIST###################################

NL =[]

start = timeit.default_timer()

ToList(T, NL)

stop = timeit.default_timer()

print('ToList Execution: ', stop - start)
print()

###############################TESTIING MINATDEPTH###################################

for d in range(CompHeight(T)+1):
    start = timeit.default_timer()

    print("MIN at depth",d,": ",MinAtDepth(T,d))

    stop = timeit.default_timer()

    print('MinAtDepth Execution: ', stop - start)
    print()
    
###############################TESTIING MAXATDEPTH###################################

for d in range(CompHeight(T)+1):
    start = timeit.default_timer()

    print("MAX at depth",d,": ",MaxAtDepth(T,d))

    stop = timeit.default_timer()

    print('MaxAtDepth Execution: ', stop - start)
    print()
    
###############################TESTIING NODESATDEPTH###################################

for d in range(CompHeight(T)+1):
    start = timeit.default_timer()

    print("Nodes at depth",d,": ",NodesAtDepth(T,d))

    stop = timeit.default_timer()

    print('NodesAtDepth Execution: ', stop - start)
    print()
    
###############################TESTIING PRINTATDEPTH###################################

for d in range(CompHeight(T)+1):
    start = timeit.default_timer()

    print("Items at depth",d,": ")
    PrintAtDepth(T,d)

    stop = timeit.default_timer()

    print('PrintAtDepth Execution: ', stop - start)
    print()


##########################TESTIING FULLLEAVES##################################

start = timeit.default_timer()

print(FullLeaves(T))

stop = timeit.default_timer()

print('FullLeaves Execution: ', stop - start)  

print()



