# Puthypor Sengkeo
# ID: 11646389
# Cpts 350 - Symbolic Graph Project

from pyeda.inter import *

a0 = bddvar('a0') 
a1 = bddvar('a1') 
a2 = bddvar('a2') 
a3 = bddvar('a3') 
a4 = bddvar('a4')

b0 = bddvar('b0') 
b1 = bddvar('b1') 
b2 = bddvar('b2') 
b3 = bddvar('b3') 
b4 = bddvar('b4')

c0 = bddvar('c0') 
c1 = bddvar('c1') 
c2 = bddvar('c2') 
c3 = bddvar('c3') 
c4 = bddvar('c4')

# Get the edges into a pair
def getPair(param):
    # List of edges that satify the logic
    # logic that node i can reach node j
    for i in range(0, 32):
        for j in range(0, 32):
            if ((i+3)%32 == j%32) or ((i+8)%32 == j%32):
                pair = (i, j) # Pair the node u with node v that can reach each other
                param.append(pair) # Put them into a list
    # print(pairList)
    return param

# Make the pair binary
def getbiPairList(param):
    # Convert the Pair(i, j)
    # From i.e. Pair(0, 3) to BinaryPair(00000, 00011)
    list = []
    for i,j in param:
        iPair = '{0:05b}'.format(i) # Format the node 
        jPair = '{0:05b}'.format(j) # as a 5-bits format 
        biPair = (iPair, jPair) # put them back into a pair
        list.append(biPair) # put each pair back into a list
    # print(biPairList)
    return list

# Use the binary pair to make an expression
def getExpression(param):
    exp = ''
    for p1,p2 in param:
        # For the first part of the pair (aka the u)
        index = 0
        for i in p1:
            if i == str(0):
                exp += '~a' + str(index) + ' & '
            elif i == str(1):
                exp += 'a' + str(index) + ' & '
            index+=1

        # For the second part of the pair (aka the v)
        index = 0
        for j in p2:
            if j == str(0):
                exp += '~b' + str(index) + ' & '
            elif j == str(1):
                exp += 'b' + str(index) + ' & '
            index+=1

        exp = exp[:-3] # clear out the last ' & '
        exp += ' | ' # then add the ' | '
    
    # Clean up the expression
    exp = exp[:-3] # Clear out the last ' | '
    # print(exp)  
    expression = expr(exp)
    return expression
    # print(expression)


########## main
print("Welcome to Symbolic Graph Project - Cpts 350\n")

### Step 3.1 Obtain BDDs for R, EVEN, PRIME

pairList = []
biPairList = []
# expression = exprvar("expression")

# Get all the edges in pairs
# print("GET PAIR")
pairList = getPair(pairList)
# print("DONE\n")

# Convert those pairs from integer to binary form
# print("GET BINARY PAIR")
biPairList = getbiPairList(pairList)
# print("DONE\n")

# Convert those pairs of binary edges into an expression 
# print("GET EXPRESSION")
expression = getExpression(biPairList)
# print(expression)
# print("DONE\n")

# Get BDD RR
print("GET BDD RR")
RR = expr2bdd((expression))
# print(expr2truthtable(expression))
# print('R', len(list(R.satisfy_all())))
print('RR', RR.inputs)
print("DONE\n")

# Get BDD Even
even = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
# print("GET BINARY FOR EVEN")
biEvenList = []
for i in even:
    bii = '{0:05b}'.format(i)
    biEvenList.append(bii)
# print(biEvenList)
# print("DONE\n")

# print("GET EXPRESSION FOR EVEN")
exp = ''
# expression = exprvar("expression")
for p in biEvenList:
    index = 0
    for i in p:
        if i == str(0):
            exp += '~a' + str(index) + ' & '
        elif i == str(1):
            exp += 'a' + str(index) + ' & '
        index+=1
    exp = exp[:-3]
    exp += ' | '
exp = exp[:-3]
# print(exp)
expression = expr(exp)
# print("DONE\n")

print("GET BDD EVEN")
# print(even)
# print(exp)
# print(expression)
EVEN = expr2bdd((expression))
# print(expr2truthtable(expression))
# print('EVEN', len(list(EVEN.satisfy_all())))
print('EVEN', EVEN.inputs)

print("DONE\n")

# Get BDD Prime
prime = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
# print("GET BINARY FOR PRIME")
biPrimeList = []
for i in prime:
    bii = '{0:05b}'.format(i)
    biPrimeList.append(bii)
# print(biPrimeList)  
# print("DONE\n")

# print("GET EXPRESSION FOR PRIME")
exp = ''
# expression = exprvar("expression")
for p in biPrimeList:
    index = 0
    for i in p:
        if i == str(0):
            exp += '~b' + str(index) + ' & '
        elif i == str(1):
            exp += 'b' + str(index) + ' & '
        index+=1
    exp = exp[:-3]
    exp += ' | '
exp = exp[:-3]
expression = expr(exp)
# print("DONE\n")

print("GET BDD PRIME")
# print(expression)
PRIME = expr2bdd((expression))
# print('PRIME', len(list(PRIME.satisfy_all())))
print('PRIME', PRIME.inputs)
print("DONE\n")

### Step 3.2 Obtain BDD for R2 (reach in 2 steps) using compose({}) function
def compose(BDD1, BDD2):
    BDD2 = BDD2.compose({a0:c0, a1:c1, a2:c2, a3:c3, a4:c4})
    BDD1 = BDD1.compose({b0:c0, b1:c1, b2:c2, b3:c3, b4:c4})

    return (BDD1 & BDD2).smoothing(c0).smoothing(c1).smoothing(c2).smoothing(c3).smoothing(c4) # Clear unecessary variables


    # # Index the variables
    # A = bddvars('a', 5)
    # B = bddvars('b', 5)
    # C = bddvars('c', 5)

    # # Rename the variables
    # for index in range(0,5):
    #     BDD1 = BDD1.compose({B[index]: C[index]})
    #     BDD2 = BDD2.compose({A[index]: C[index]})

    # return (BDD1 & BDD2).smoothing(C) # Clear unecessary variables

print("GET BBD FOR RR2")
RR2 = compose(RR, RR)
# print('RR2', len(list(RR2.satisfy_all())))
print('RR2', RR2.inputs)
print("DONE\n")

### Step 3.3 Obtain BDD for RR2STAR (reach in an even number of steps) using TransitiveClosure function
def getTransitiveClosure(paramR):
    print("getTransitiveClosure is going to take about 8s, but it works :)")
    H = paramR
    while True:
        Hprime = H
        H = Hprime | compose(Hprime, paramR)

        if (H.equivalent(Hprime)):
            break
    return H

print("GET BDD FOR RR2STAR")
RR2STAR = getTransitiveClosure(RR2)
# print('RR2STAR', len(list(RR2STAR.satisfy_all())))
print('RR2STAR', RR2STAR.inputs)
print('RR2STAR', RR2STAR.equivalent(True))
print("DONE\n")

### Step 3.4 Obtain BDD PE where pair(u(prime),v(even)) u can reach v in even number of steps
print("GET BDD FOR BDD PE")
# Index the variables
# A = bddvars('a', 5)
# B = bddvars('b', 5)
# C = bddvars('c', 5)

# for index in range(0,5):
#     EVEN = EVEN.compose({A[index]: C[index]})
#     PRIME = PRIME.compose({B[index]: C[index]})
EVEN = EVEN.compose({a0:b0, a1:b1, a2:b2, a3:b3, a4:b4})
EVEN = EVEN.smoothing(b0).smoothing(b1).smoothing(b2).smoothing(b3).smoothing(b4)
# PRIME = PRIME.compose({b0:c0, b1:c1, b2:c2, b3:c3, b4:c4})
# # ENP = (EVEN & PRIME).smoothing(C)
# ENP = (EVEN & PRIME).smoothing(c0).smoothing(c1).smoothing(c2).smoothing(c3).smoothing(c4) # .smoothing(C)
# PE = ENP & RR2STAR
PE = EVEN & PRIME & RR2STAR
print('PE', PE.inputs)
print('PE', PE.equivalent(True))
print("DONE\n")

### Step 3.5 Statement A says
### For each PRIME, there is PE
### Therefore, PRIME -> PE
### OR, ~PRIME | PE
print("GET TRUTH VALUE FOR STATEMENT A")
# C = bddvars('c', 5)
# A = bddvars('a', 5)

# for index in range(0,5):
    # PE = PE.compose({A[index]: C[index]})
PE = PE.compose({a0:c0, a1:c1, a2:c2, a3:c3, a4:c4})
STATEMENT = ~PRIME | PE.smoothing(c0).smoothing(c1).smoothing(c2).smoothing(c3).smoothing(c4) # .smoothing(C)
print("Statement A", STATEMENT.equivalent(True))
print("DONE\n")