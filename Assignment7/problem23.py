#!/usr/bin/env python3
########################################################################
# File: problem23.py
#       executable: problem23.py
# Purpose: Apply the baum-welch algorithm. 
#       stderr: errors and status
#       stdout: the file of choice from std out. 
#          
# Author: Mohammad Abdulqader
# History:      11/26/2019 Created
#               12/01/2019 copied problem 20 code
#               12/01/2019 modified viterbi algorithm
#               12/01/2019 Made main
#               12/09/2019 figured out the algorithm after a week (finally)
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
        
        The following classes are within Learning:
        - Node: holds data for viterbi algorithm.

        The following functions with in the class include:
        - emptyMatrix: produces the empty T and E matricies.
        - hmmMatrix: returns probability matrix given a string and path
        - convertMatrix: converts count matrix into a probability matrix.
        - makeMatrix: turns tables into a searchable matrix
        - makeGraph: produces the Adj matrix graph.
        - forwardAlgorithm: find the highest probability path.
        - topologicalOrder: find the topological order of the graph.
        - backwardAlgorithm: find reverse score of each node.
        - softDecoding: find probablity of each state.
        - baumWelchLearning: find the matrix using bW learning.
        - output: just ouputs for the rosalind problem.

    '''

    class Node:
        '''
            The following Node class contains:
            - self.name is the name of the node
            - self.data which holds data
            - self.hmm is what hmm state the node is
            - self.inComing which says how many incoming nodes there are
            - self.score which scores the node
            - self.prev which saves all incoming nodes
            - self.path that holds the path to that node.
        '''
        def __init__(self, name, data):
            ''' produce a node's attributes. '''
            self.data = data
            self.name = name
            self.hmm = 'None'
            self.prev = []
            self.inComing = 0
            self.score = 1
            self.revScore = 1
    
    @staticmethod
    def emptyMatrix(states, emissions):
        ''' Produce the transition and emission matricies. '''
        tMatrix = {x: None for x in states}
        eMatrix = {x: None for x in states}

        for transition in tMatrix:
            tMatrix[transition] = {i:0 for i in states}
            eMatrix[transition] = {i:0 for i in emissions}
    
        return tMatrix, eMatrix

    @staticmethod
    def makeMatrix(columns, rows, dataset):
        ''' Make the transition matrix. '''
        Matrix = {x : {} for x in rows}
        rowCount = 0
        for i in range(len(dataset)):
            columnData = dataset[i][1:]
            for k in range(len(columns)):
                Matrix[rows[rowCount]].update({columns[k]: float(columnData[k])})
            rowCount+=1
        return Matrix

    def __init__(self, string, hmmStates, transitionData, emissionColumns, emissionData):
        ''' Produce intial matricies, graph, and node dictionary. '''
        self.string = string
        self.hmmStates, self.emissions = hmmStates, emissionColumns
        self.numStates = len(hmmStates)
        self.tMatrix = self.makeMatrix(hmmStates, hmmStates, transitionData)
        self.eMatrix = self.makeMatrix(emissionColumns, hmmStates, emissionData)
        self.adjMatrix = {} # graph for viterbi algorithm
        self.N = {} # set of nodes for viterbi graph.
        self.EdgeMatrix = None
        self.start = self.N['start'] = self.Node("start", "")
        self.end = self.N['end'] = self.Node("end", "")
        self.stateDic = None
        self.makeGraph(string)

    def makeGraph(self, stringData):
        ''' make the adj matrix, and Node dictionary. '''
        states = sorted(self.tMatrix.keys())
        for i in range(len(stringData)):
            # makes the start to hmm state connections
            if i == 0:
                nodes = [self.Node(k+str(i), stringData[i]) for k in states]
                for nodeState in nodes:
                    nodeState.hmm = nodeState.name[:1]
                    self.N[nodeState.name] = nodeState
                    self.adjMatrix.setdefault(self.N['start'].name, []).append(nodeState.name)
                    nodeState.prev.append('start')
                    nodeState.inComing+=1
                continue
            # makes graph from start to end
            else:
                nodes = [self.Node(k+str(i), stringData[i]) for k in states]
                for nodeState in nodes:
                    nodeState.hmm = nodeState.name[:1]
                    self.N[nodeState.name] = nodeState
                    for state in states:
                        self.adjMatrix.setdefault(self.N[state+str(i - 1)].name, []).append(nodeState.name)
                        nodeState.prev.append(self.N[state+str(i - 1)].name)
                        nodeState.inComing+=1
                continue
        # adress connections to end
        lastItem = len(stringData) - 1
        for state in states:
            self.adjMatrix.setdefault(self.N[state+str(lastItem)].name, []).append(self.N['end'].name)
            self.N['end'].prev.append(self.N[state+str(lastItem)].name)
            self.N['end'].inComing+=1
        self.adjMatrix.update({'end':[]})

    def calculateNode(self, hmmFrom, hmmTo, emission):
        ''' calculate the wieght of the next movement.'''
        # for case where last node to end node
        if hmmTo == 'None': return 1

        # for case for start to first node
        elif hmmFrom == 'None':
            emissionOfX = self.eMatrix[hmmTo][emission]
            return (1/self.numStates) * emissionOfX

        # for node to node movement
        else:
            emissionOfX = self.eMatrix[hmmTo][emission]
            transOfX = self.tMatrix[hmmFrom][hmmTo]
            return transOfX * emissionOfX

    def topologicalOrder(self):
        ''' find the topological order of Graph G. '''
        # copy graph and node dict to save them
        refG = copy.deepcopy(self.adjMatrix)
        refN = copy.deepcopy(self.N)
        iterable = []
        candidates = []

        # add all initial nodes with no inComing edges
        for node in sorted(self.N):
            if self.N[node].inComing == 0: candidates.append(self.N[node].name)
        
        # produce the iterable list
        while len(candidates) > 0:
            a = candidates.pop(0)
            iterable.append(a)
            while len(refG[a]) > 0:
                b = refG[a].pop(0)
                refN[b].inComing -= 1
                if refN[b].inComing == 0: candidates.append(b)
        
        # ensures we have a DAG
        remainingNodes = [len(refG[node]) for node in refG]
        if sum(remainingNodes) != 0: 
            return 'The input graph G is not a DAG.'
        else: return iterable

    def forwardAlgorithm(self, iterable):
        ''' Find the longest path. '''
        # set score of all nodes
        for node in self.adjMatrix:
            self.N[node].score = 0
        self.start.score = 1

        # now score nodes as you go by comparing prev scores
        for value in iterable:
            # for case if prev empty
            # start has no hmm state so dont add it
            if self.N[value].inComing == 0: 
                continue

            # for case when prev is not empty
            else:
                forward = 0
                for node in self.N[value].prev:
                    # get the hmm states of the prev and current
                    # get the emission of the next string
                    # if the current score is higher than the max, change the max
                    hmmPrev = self.N[node].hmm
                    hmm = self.N[value].hmm
                    em = self.N[value].data
                    forward += self.N[node].score * self.calculateNode(hmmPrev, hmm, em)
                
                # gets edge weight and its hmm state and multiply it and update the path
                self.N[value].score = forward

                # end has no emission so dont add the emission or hmm state
        
        return self.end.score

    def backwardAlgorithm(self, iterable):
        ''' Find the reverse path to each node. '''
        # set score on all of my nodes
        for node in self.adjMatrix:
            self.N[node].revScore = 0
        self.end.revScore = 1
        for value in reversed(iterable):
            if len(self.adjMatrix[value]) == 0:
                continue

            # for case when prev is not empty
            else:
                background = 0
                for node in self.adjMatrix[value]:
                    # get the hmm states of the prev and current
                    # get the emission of the next string
                    # if the current score is higher than the max, change the max
                    hmmNext = self.N[node].hmm
                    hmm = self.N[value].hmm
                    emNext = self.N[node].data
                    background += self.N[node].revScore * self.calculateNode(hmm, hmmNext, emNext)
                
                # gets edge weight and its hmm state and multiply it and update the path
                self.N[value].revScore = background

                # end has no emission so dont add the emission or hmm state

    def softDecoding(self, iterable):
        ''' find the probablity of each hmm state. '''
        # initalizes stateDictionaries and EdgeMatrix
        self.stateDictionary = {x: 0 for x in iterable[1:-1]}
        self.EdgeMatrix = {x: {y:0 for y in self.adjMatrix[x]} for x in iterable[1:-(len(self.hmmStates)+1)]}
        
        # run forward and backward algorithms to get sink node
        sink = self.forwardAlgorithm(iterable)
        self.backwardAlgorithm(iterable)
        
        # calculate node responsibility matrix
        for i in self.stateDictionary:
            forward = self.N[i].score
            rev = self.N[i].revScore
            self.stateDictionary[i] = ((forward * rev)/sink)
        
        # calculate edge responsibility matrix
        for nodeFrom in self.EdgeMatrix:
            for nodeTo in self.EdgeMatrix[nodeFrom]:
                forward = self.N[nodeFrom].score
                fState = self.N[nodeFrom].hmm
                rState = self.N[nodeTo].hmm
                rev = self.N[nodeTo].revScore 
                weight = self.calculateNode(fState, rState, self.N[nodeTo].data)
                self.EdgeMatrix[nodeFrom][nodeTo] =  ((forward * rev * weight)/sink)

    def convertMatrix(self, raw, final):
        ''' Convert the count matricies into prob matricies. '''
        for i in raw:
            total = 0
            for state in raw[i]:
                total += raw[i][state]
            if total == 0:
                for state in final[i]: final[i][state] = 1/len(raw[i])
                continue
            else:
                for state in final[i]:
                    countState = raw[i][state]
                    final[i][state] = countState/total

    def hmmMatrix(self):
        ''' Fill in the data in the matrix. '''
        # copy them to use for later
        tRawMatrix, eRawMatrix = self.emptyMatrix(self.hmmStates, self.emissions)

        # handles tMatrix
        for i in self.EdgeMatrix:
            pre = self.N[i].hmm
            for k in self.EdgeMatrix[i]:
                land = self.N[k].hmm
                tRawMatrix[pre][land]+=self.EdgeMatrix[i][k]

        # handles emission
        for node in self.stateDictionary:
            ind = int(node[1:])
            state = self.N[node].hmm
            em = self.string[ind]
            eRawMatrix[state][em]+= self.stateDictionary[node]

        # convertMatrix will now turn counts into probablities
        self.convertMatrix(tRawMatrix, self.tMatrix)
        self.convertMatrix(eRawMatrix, self.eMatrix)

        return self.tMatrix, self.eMatrix

    def baumWelchLearning(self, iterations):
        ''' Finds the HMM parameters. '''
        numTimes = 0
        iterable = self.topologicalOrder()
        while numTimes < iterations:
            self.softDecoding(iterable)
            tMatrix, eMatrix = self.hmmMatrix()
            bestT = copy.deepcopy(tMatrix)
            bestE = copy.deepcopy(eMatrix) 
            numTimes +=1
        return bestT, bestE

    def output(self, tMatrix, eMatrix):
        ''' '''
        #output time!
        firstLine = ''
        for i in self.hmmStates: firstLine+= i+'\t'
        Trans =[]
        for i in tMatrix:
            line = i + '\t'
            for k in tMatrix[i]: line+= str(round(tMatrix[i][k], 3)) + '\t'
            Trans.append(line.rstrip())

        secondLine = '\t'
        for i in self.emissions: secondLine+= i + '\t'
        EM = []
        for i in eMatrix:
            line = i + '\t'
            for k in eMatrix[i]: line+= str(round(eMatrix[i][k], 3)) + '\t'
            EM.append(line.rstrip())
    
        print(firstLine.rstrip())
        for i in range(len(Trans)): print(Trans[i])
        print('--------')
        print(secondLine.rstrip())
        for i in range(len(EM)): print(EM[i])
        

########################################################################
#   main
########################################################################

import sys
def main():
    ''' Find the HMM matricies. '''
    try:
        if sys.stdin.isatty():
            raise Usage("problem23.py <infile >outfile")

        # collect the input file
        infile = sys.stdin.readlines()
        dataset = [data.rstrip().split() for data in infile]
        iterations = int(dataset[0][0])
        string = dataset[2][0]
        emissions = dataset[4]
        transitions = dataset[6]
        eData = dataset[-len(transitions):]
        tData = dataset[9:9+len(transitions)]

        # call the learning class
        L = Learning(string, transitions, tData, emissions, eData)
        tMatrix, eMatrix = L.baumWelchLearning(iterations)
        L.output(tMatrix, eMatrix)
        

    except Usage as err:
        print(err.msg)

if __name__ == "__main__":
    main()