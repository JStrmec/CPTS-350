"""
Programmer: Edgar Villasenor
WSU ID: 11536698
CptS 350
BDD Project
"""

from pyeda.inter import *

# Step 1. Create the bddvars
x = bddvars('x', 5)
y = bddvars('y', 5)
z = bddvars('z', 5)



def createBoolEdge(edge, node1, node2):
    c = None
    n = None
    boolString = ""

    for i, value in enumerate(edge):
        if i < 5:
            c = node1
            n = i
        else:
            c = node2
            n = i - 5

        if(i != 0):
            boolString += " & "
        if value == '0':
            boolString += "~"
        boolString += c + "[" + str(n) + "]"

    return expr(boolString)

def createNode(edge, c):
    n = None
    boolString = ""

    for i, value in enumerate(edge):
        n = i
        if(i != 0):
            boolString += " & "
        if value == '0':
            boolString += "~"
        boolString += c + "[" + str(n) + "]"

    return expr(boolString)


def createBoolString(nnode):
    return(format(nnode, '05b'))


def main():

    # Create boolean formula for graph by evaluating valid edges    
    R = None 
    for i in range(32):
        for j in range(32):
            if((i + 3) % 32 == j % 32 or (i + 8) % 32 == j % 32):
                if R == None:
                    R = createBoolEdge(createBoolString(i) + createBoolString(j), 'x', 'y')
                else:
                    Or(R, createBoolEdge(createBoolString(i) + createBoolString(j), 'x', 'y'))

    # R is now a boolean expression: ~X0, ~X1, ~X2, ~X3, ~X4, ~y[0], ~y[1], ~y[2], y[3], y[4] 
    
    RR = expr2bdd(R) # Convert R into a bdd over 10 bddvars, we now have the bdd RR for the graph G 
    print("BDD RR created")


    # create Boolean formula P for the set [prime] and a boolean formula for the set even
    # P is over [x1, ..., x5], E is over [y1, ..., y5]
    primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    evens = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    

    # Create boolean formula to represent primes
    P = None
    for el in primes:
        if P == None:
            P = createNode(createBoolString(el), 'x')
        else:
            Or(P, createNode(createBoolString(el), 'x'))
    PP = expr2bdd(P) # PP is a bdd
    print("BDD PP created")

    # Create boolean formula to represent evens
    E = None
    for el in evens:
        if E == None:
            E = createNode(createBoolString(el), 'y')
        else:
            Or(E, createNode(createBoolString(el), 'y'))
    EE = expr2bdd(E) # Now EE is a bdd
    print("BDD EE created")


    # For all n in primes, does there exists a v in evens such that
    # There exists a path from u to v in even number of steps
    HPrime = RR
    
    R1 = RR
    R2 = RR 
    
    R1 = R1.compose({y[0]: z[0], y[1]: z[1], y[2]: z[2], y[3]: z[3], y[4]: z[4]})
    R2 = R2.compose({x[0]: z[0], x[1]: z[1], x[2]: z[2], x[3]: z[3], x[4]: z[4]})
    R = R1 & R2
    R = R.smoothing(z)

    H =  R | RR  # Compute BDD over x, y, z   

    # Check condition
    while not H.equivalent(HPrime):
        H = HPrime
        H = H.compose({y[0]: z[0], y[1]: z[1], y[2]: z[2], y[3]: z[3], y[4]: z[4]})
        RR = RR.compose({x[0]: z[0], x[1]: z[1], x[2]: z[2], x[3]: z[3], x[4]: z[4]})
        H = H & RR
        H = H.smoothing(z)
        HPrime = H | R


    QQ = (EE & HPrime).smoothing(y)

    Res = False
    if(PP.equivalent(QQ)):
        Res = And(PP.smoothing(x).equivalent(False))

    if Res == True:
        print("True")
    else:
        print("False")

main()
