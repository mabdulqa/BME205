#!/usr/bin/env python3
########################################################################
# File: problem20.py
#       executable: problem20.py
# Purpose: Given a string and a path produce a 
#          a transition and an emission matrix. 
#       stderr: errors and status
#       stdout: the file of choice from std out. 
#          
# Author: Mohammad Abdulqader
# History:      11/26/2019 Created
#               11/30/2019 Made Transition function and PofT function
#               11/30/2019 Made main
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
#   Learning
########################################################################

import copy
class Learning:
    '''
        The following class has the following goals:
        - To find the transition and emission matricies given
            a string and a path.
        
        The following functions with in the class include:
        - makeMatrix: produces the empty T and E matricies.
        - returnCell: returns data of a specific cell in a matrix.
        - hmmMatrix: returns probability matrix given a string and path
        - convertMatrix: converts count matrix into a probability matrix.

    '''
    @staticmethod
    def emptyMatrix(states, emissions):
        ''' Produce the transition and emission matricies. '''
        tMatrix = {x: None for x in states}
        eMatrix = {x: None for x in states}

        for transition in tMatrix:
            tMatrix[transition] = {i:0 for i in states}
            eMatrix[transition] = {i:0 for i in emissions}
    
        return tMatrix, eMatrix

    def __init__(self, transition, emissions, string, path):
        ''' Produce intial matricies. '''
        self.tMatrix, self.eMatrix = self.emptyMatrix(transition, emissions)
        self.hmmStates, self.emissions = transition, emissions
        self.string = string 
        self.path = path

    def convertMatrix(self, raw, final):
        ''' Convert the count matricies into prob matricies. '''
        for i in raw:
            total = 0
            for state in raw[i]:
                total += raw[i][state]
            if total == 0:
                for state in final[i]: final[i][state] = round(1/len(raw[i]), 3)
                continue
            else:
                for state in final[i]:
                    countState = raw[i][state]
                    final[i][state] = round(countState/total, 3)

    def hmmMatrix(self):
        ''' Fill in the data in the matrix. '''
        # copy them to use for later
        tRawMatrix, eRawMatrix = self.emptyMatrix(self.hmmStates, self.emissions)

        # add for all but the end
        for i in range(len(self.string) - 1):
            state = self.path[i]
            em = self.string[i]
            nextState = self.path[i + 1]
            eRawMatrix[state][em]+=1
            tRawMatrix[state][nextState]+=1

        # add the last emission
        state = self.path[-1]
        em = self.string[-1]
        eRawMatrix[state][em]+=1

        # convertMatrix will now turn counts into probablities
        self.convertMatrix(tRawMatrix, self.tMatrix)
        self.convertMatrix(eRawMatrix, self.eMatrix)

        return self.tMatrix, self.eMatrix

########################################################################
#   main
########################################################################

import sys
def main():
    ''' Find the HMM matricies. '''
    try:
        if sys.stdin.isatty():
            raise Usage("problem20.py <infile >outfile")

        # collect the input file
        rawData = sys.stdin.readlines()
        string = rawData[0].rstrip()
        emissions = rawData[2].rstrip().split()
        path = rawData[4].rstrip()
        transitions = rawData[6].rstrip().split()

        # call the learning class
        L = Learning(transitions, emissions, string, path)
        tMatrix, eMatrix = L.hmmMatrix()

        #output time!
        firstLine = ''
        for i in transitions: firstLine+= i+'\t'
        Trans =[]
        for i in tMatrix:
            line = i + '\t'
            for k in tMatrix[i]: line+= str(tMatrix[i][k]) + '\t'
            Trans.append(line.rstrip())

        secondLine = '\t'
        for i in emissions: secondLine+= i + '\t'
        EM = []
        for i in eMatrix:
            line = i + '\t'
            for k in eMatrix[i]: line+= str(eMatrix[i][k]) + '\t'
            EM.append(line.rstrip())
    
        print(firstLine.rstrip())
        for i in range(len(Trans)): print(Trans[i])
        print('--------')
        print(secondLine.rstrip())
        for i in range(len(EM)): print(EM[i])

    except Usage as err:
        print(err.msg)

if __name__ == "__main__":
    main()