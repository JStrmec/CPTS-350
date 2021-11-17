# Jocelyn Strmec, id: 11719133
# CPTS 350 - Fall 2021 WSU
# Symbolic Graph Project

#imports
from pyeda.inter import *
from functools import reduce

#Declarations of Variables
evenVertices = set([x for x in range(30) if x%2 == 0])
primeVertices = {3,5,7,11,13,17,19,23,29,31}# Why are 1 and 2 not included? They're prime.
edgesR = []
plainEdges = []

edgesRR =[]
verticesEVEN =[]
verticesPRIME = []
# Creates Edges that are binary values of corresponding decimal numbers 
# that fit the requirements for an edge
for i in range(0,32):
    for j in range(0,32):
        if((i+3)%32 == j%32 or (i+8)%32 == j%32):
            edgesR.append(['{0:05b}'.format(i),'{0:05b}'.format(j)])
            plainEdges.append((i,j))

# Converts Binary Edge Pairs into BDD expressions
def bddEdges(e):
    for x in e:
        a = x[0][0]+'&'+x[0][1]+'&'+x[0][2]+'&'+x[0][3]+'&'+x[0][4]
        b = x[1][0]+'&'+x[1][1]+'&'+x[1][2]+'&'+x[1][3]+'&'+x[1][4]
        c = a + '|'+ b
        edgesRR.append(expr2bdd(expr(c)))

# Converts Vertices to BDDs expressions
def bddVertices(v):
    for y in v:
        result  = []
        x = '{0:05b}'.format(y)
        a = x[0]+'&'+x[1]+'&'+x[2]+'&'+x[3]+'&'+x[4]
        result.append(expr2bdd(expr(a)))
    return result
        
# Calls funtions to convert everything to BDDs
bddEdges(edgesR)
print(edgesR)
print(edgesRR)
verticesEVEN = bddVertices(evenVertices)
verticesPRIME = bddVertices(primeVertices)

# Composes the RR and BDD vars 
def composeRR(rr1, rr2):
    x = bddvars('x', 5)#Creates Variables
    y = bddvars('y', 5)
    z = bddvars('z', 10)
    for i in range(0, 5):
        rr1 = rr1.compose({y[i]: z[i]})# Comopses rr1, rr2 into bdd variables
        rr2 = rr2.compose({z[i]: x[i]})
    return (rr1 & rr2).smoothing(z)

# Composes the RR2 and RR2*
def composeRR2STAR(var):
    bDD = reduce(lambda x, y: x or y, var) #Reduces list of edgesRR for each bool expression
    B = bDD or composeRR(bDD, bDD) #Composes RR2* and BDD vars (BDD PE)
    return Not(B).smoothing().equivalent(False)

result = composeRR2STAR(edgesRR)
result1 = composeRR2STAR(verticesEVEN)
result2 = composeRR2STAR(verticesPRIME)

def computePE(r,r1,r2):
    PE = result1 and result2 and result # PE = result1 or result2 or result
    return Not(PE).smoothing().equivalent(True)# Not(PE).smoothing().equivalent(False)

finalResult = computePE(result,result1,result2)
print()
print()
print("StatementA, \n\'For each node u in [prime], there is a node v in [even] such that \nu can reach v in even number of steps\', is",  finalResult  ,"for all [prime] in G")
print()
print()

##BONUS
###############################################
###############################################
# This is a recursive function similar to a DFS search that finds a even for a prime to 
# test the functionality of the BDDs above
def stepping(p,count,visited,result):
    count+=1
    visited.append(p)
    filteredEdges = list(filter(lambda x:x[0]==p, plainEdges)) #filters out edges that are out of p #print(filteredEdges,count)
    filterEvenEdges = list(filter(lambda x: x[1]%2 == 0 , filteredEdges))#filters out even vertices in the edges that are out of p
    if(filterEvenEdges != [] and count %2 == 0):
        result.append(filterEvenEdges[0][1])
    else:
        for e in filteredEdges:
            if e[1] not in visited:
                stepping(e[1],count,visited,result)# recursive call that checks all edges
                # out of p if a even number and even count has not been found
    b = True if result != [] else False
    return (b, result[0])

def findEvenVertex(p):
    a = None
    return(stepping(p, 0,[],[]))
    
def checkFunctionality(p,e):
    a = bddVertices([p])
    b = bddVertices([e])
    r = composeRR2STAR(a)
    r1 = composeRR2STAR(b)
    r2 = composeRR2STAR(edgesRR)
    return computePE(r,r1,r2)

testprime = 13  
a = findEvenVertex(testprime)
f = checkFunctionality(testprime,a[1])
print()
print("BONUS")
print("The boolean graph with BDD, RR2 and such and the recursive DFS match:", a[0]) 
print("Based on graph for prime u",testprime,", even v is :", a[1])
print("The result of testing whether the prime and the even can be reached in a even number of steps in the PE with bool graphs stuff is:",f)
print()
print()





