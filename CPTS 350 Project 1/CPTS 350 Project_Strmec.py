# Jocelyn Strmec, id: 11719133
# APTS 350 - Fall 2021 WSU
# Symbolic Graph Project

#imports
from pyeda.inter import *
from functools import reduce

#Graph G nodes
evenVertices = set([x for x in range(30) if x%2 == 0])
primeVertices = {3,5,7,11,13,17,19,23,29,31}# Why are 1 and 2 not included
edgesR = []
plainEdges = []

edgesRR =[]
verticesEVEN =[]
verticesPRIME = []
# Creates Edges that are binary values of corresponding decimal numbers that fit the requirements for an edge
for i in range(0,32):
    for j in range(0,32):
        if((i+3)%32 == j%32 or (i+8)%32 == j%32):
            edgesR.append(['{0:05b}'.format(i),'{0:05b}'.format(j)])
            plainEdges.append((i,j))
# Converts Binary Edge Pairs into BBB expressions
def bddEdges(e):
    for x in e:
        a = x[0][0]+'&'+x[0][1]+'&'+x[0][2]+'&'+x[0][3]+'&'+x[0][4]
        b = x[1][0]+'&'+x[1][1]+'&'+x[1][2]+'&'+x[1][3]+'&'+x[1][4]
        c = a + '|'+ b
        edgesRR.append(expr2bdd(expr(c)))
# Converts Vertixes intp BBB expressions, if s = 'e' it is append to EVENS
# if s = 'p' it is appended to PRIMES
def bddVertices(v):
    for y in v:
        result  = []
        x = '{0:05b}'.format(y)
        a = x[0]+'&'+x[1]+'&'+x[2]+'&'+x[3]+'&'+x[4]
        result.append(expr2bdd(expr(a)))
        return result
        
# Calls funtions to convert everything to BDDs
bddEdges(edgesR)
verticesEVEN = bddVertices(evenVertices)
verticesPRIME = bddVertices(primeVertices)

# Composes the RR2* and BDD vars (BDD PE)
def composeRR2(rr1, rr2):
    x = bddvars('x', 5)
    y = bddvars('y', 5)
    z = bddvars('z', 10)
    for i in range(0, 5):
        rr1 = rr1.compose({y[i]: z[i]})
        rr2 = rr2.compose({z[i]: x[i]})
    return (rr1 & rr2).smoothing(z)

# print(edgesRR)
# print(verticesEVEN)
# print(verticesPRIME)

# For all n in primes, does there exists a v in evens such that
# There exists a path from u to v in even number of steps
while bool(1):
    bDD = reduce(lambda x, y: x or y, edgesRR) #Reduces list of edgesRR for each bool expression
    B = bDD or composeRR2(bDD, bDD) #Composes RR2* and BDD vars (BDD PE)
    if B.equivalent(bDD):
        break
bDD1 = reduce(lambda x, y: x or y, verticesEVEN) #Reduces list of vertices EVEN for each bool expression
B1 = bDD1 or composeRR2(bDD1, bDD1)
r1 = B1.equivalent(bDD1)

bDD2 = reduce(lambda x, y: x or y, verticesPRIME) #Reduces list of vertices Prime for each bool expression
B2 = bDD2 or composeRR2(bDD2, bDD2)
r2 = B2.equivalent(bDD2)

result = Not(B).smoothing().equivalent(False)
result1 = Not(B1).smoothing().equivalent(False)
result2 = Not(B2).smoothing().equivalent(False)

C = result1 or result2 or result

finalResult = Not(C).smoothing().equivalent(False)
print()
print()
print("StatementA, \'For each node u in [prime], there is a node v in [even] such that \nu can reach v in even number of steps\', is",  finalResult  ,"for all [prime] in G")
print()
print()

##BONUS
###############################################
###############################################
def stepping(p,count,visited):
    count+=1
    result = (False, p)
    filteredEdges = list(filter(lambda x:x[0]==p, plainEdges))
    print(filteredEdges,count)
    for e in filteredEdges:
        visited.append(p)
        temp = list(map(lambda x:x[1], filteredEdges))
        print(temp)
        for v in temp:
            if(v%2 == 0 and count%2 == 0):
                return (True, e[1])
        if e[1] not in visited:
            stepping(e[1],count,visited)
    return result

def findEvenVertex(p):
    a = None
    #buildGraph()
    # for x in primeVertices:
    #    a =  searchForConnection(x)
    return(stepping(p, 0,[]))
    #print(a)
    #print(finalResult)
    #return (a[0] == finalResult,a[1])

def checkFunctionality(p,e):
    a = bddVertices([p,0])
    b = bddVertices([e,e])
    c = composeRR2(bDD, bDD)
    return bool(c)

testprime = 13  
a = findEvenVertex(testprime)
f = checkFunctionality(testprime,a[1])
print()
print()
print("The boolean graph with RDD and such and the recursive DFS match:", a[0]) 
print("Based on graph for prime u",testprime,", even v is :", a[1])
print("The result of testing the prime and the even can be reached in a even number of steps is:",f)
print()
print()





