#!/usr/bin/env python3
########################################################################
# File: problem17.py
#       executable: problem17.py
# Purpose: Find the emission probability. 
#       stderr: errors and status
#       stdout: the file of choice from std out. 
#          
# Author: Mohammad Abdulqader
# History:      11/07/2019 Created
#               11/08/2019 Made makeMatrix, copied transition
#               11/09/2019 Modified Transition into Emission
#               
########################################################################

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
#   PofE
########################################################################

def PofE(row, target):
    ''' Return the desired transition probability. '''
    for col, prob in row:
        if col == target: return prob
    return None

########################################################################
#   makeMatrix
########################################################################

def makeMatrix(columns, rows, dataset):
    ''' Make the transition matrix. '''
    Matrix = {x : [] for x in rows}
    rowCount = 0
    for i in range(len(dataset)):
        columnData = dataset[i][1:]
        for k in range(len(columns)):
            Matrix[rows[rowCount]].append((columns[k], float(columnData[k])))
        rowCount+=1
    return Matrix

########################################################################
#   Emission
########################################################################

def Emission(path, string, Matrix):
    ''' Find the probability of a given path based on a given
        emission matrix.    
    '''
    PofI = 1
    for i in range(len(path)):
        state = path[i]
        nextString = string[i]
        PofI = PofI * PofE(Matrix[state], nextString)

    return PofI

########################################################################
#   main
########################################################################

import sys
def main():
    ''' Find the probability of a given path and string. '''
    try:
        if sys.stdin.isatty():
            raise Usage("problem17.py <infile >outfile")
        
        # clean up the infile
        infile = sys.stdin.readlines()
        dataset = [data.rstrip().split() for data in infile]
        
        # now extract the path, string, and make a transition matrix.
        string = dataset[0][0]
        path = dataset[4][0]
        columns = dataset[2]
        rows = dataset[6]
        data = dataset[-len(rows):]
        EmissionMatrix = makeMatrix(columns, rows, data)
        # calculate the probability
        probability = Emission(path, string, EmissionMatrix)
        print("{:.11e}".format(probability))
        

    except Usage as err:
        print(err.msg)

if __name__ == "__main__":
    main()