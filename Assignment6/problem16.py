#!/usr/bin/env python3
########################################################################
# File: problem16.py
#       executable: problem16.py
# Purpose: Find the P(pi) given transition matrix. 
#       stderr: errors and status
#       stdout: the file of choice from std out. 
#          
# Author: Mohammad Abdulqader
# History:      11/07/2019 Created
#               11/08/2019 Made Transition function and PofT function
#               11/08/2019 Made main
#               
########################################################################

########################################################################
#   PofT
########################################################################

def PofT(row, target):
    ''' Return the desired transition probability. '''
    for col, prob in row:
        if col == target: return prob
    return None

########################################################################
#   Transition
########################################################################

def Transition(path, Matrix):
    ''' Find the probability of a given path based on a given
        transition matrix.    
    '''
    items = len(Matrix)
    PofPi = 1/items #makes initial value.
    for i in range(len(path) - 1):
        prev = path[i]
        nextPath = path[i+1]
        PofPi = PofPi * PofT(Matrix[prev], nextPath)

    return PofPi

########################################################################
#   Usage
########################################################################

class Usage(Exception):    
    '''   
        Used to signal a Usage error, evoking a usage statement and eventual
        exit when raised.    
    '''    
    def __init__(self, msg):
        self.msg = msg 

########################################################################
#   main
########################################################################

import sys
def main():
    ''' Find the probability of a given path. '''
    try:
        if sys.stdin.isatty():
            raise Usage("problem16.py <infile >outfile")
        
        # clean up the infile
        infile = sys.stdin.readlines()
        dataset = [data.rstrip().split() for data in infile]
        
        # now extract the path, and make a transition matrix.
        path = dataset[0][0]
        columns = dataset[2]
        rows = [dataset[i][0] for i in range(5, len(dataset))]
        transitionMatrix = {x : [] for x in rows}
        rowCount = 0
        for i in range(5, len(dataset)):
            columnData = dataset[i][1:]
            for k in range(len(columns)):
                transitionMatrix[rows[rowCount]].append((columns[k], float(columnData[k])))
            rowCount+=1

        # calculate the probability
        probability = Transition(path, transitionMatrix)
        print("{:.11e}".format(probability))
        

    except Usage as err:
        print(err.msg)

if __name__ == "__main__":
    main()