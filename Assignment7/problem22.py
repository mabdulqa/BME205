#!/usr/bin/env python3
########################################################################
# File: problem22.py
#       executable: problem19.py
# Purpose: Use soft decoding find probablity of being in each hmm state. 
#       stderr: errors and status
#       stdout: the file of choice from std out. 
#          
# Author: Mohammad Abdulqader
# History:      12/02/2019 Created
#               12/02/2019 Made backward algorithm
#               12/02/2019 Made softDecoding function
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
#   Graph
########################################################################

import copy
class Graph:
    '''
        The following graph class solves the DAG alignment problem using
        the following functions.
        - PofE: returns probability of moving to that node
        - makeMatrix: turns tables into a searchable matrix
        - makeGraph: produces the Adj matrix graph.
        - calculateNode: calculates the movement to a node
        - forwardAlgorithm: find the highest probability path.
        - topologicalOrder: find the topological order of the graph.
        - backwardAlgorithm: find reverse score of each node.
        - softDecoding: find probablity of each state.

        In Graph the following classes are included:
        - Node: makes node to hold data.
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
            self.path = None
            self.inComing = 0
            self.score = 1
            self.revScore = 1

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
        ''' make the adj matrix of the graph. '''
        self.string = string
        self.numStates = len(hmmStates)
        self.tMatrix = self.makeMatrix(hmmStates, hmmStates, transitionData)
        self.eMatrix = self.makeMatrix(emissionColumns, hmmStates, emissionData)
        self.adjMatrix = {} # graph for viterbi algorithm
        self.N = {} # set of nodes for viterbi graph.
        self.start = self.N['start'] = self.Node("start", "")
        self.end = self.N['end'] = self.Node("end", "")
        self.stateDic = None
        self.edgeDic = None
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
        self.stateDictionary = {x: 0 for x in iterable[1:-1]}
        sink = self.forwardAlgorithm(iterable)
        self.backwardAlgorithm(iterable)
        for i in self.stateDictionary:
            forward = self.N[i].score
            rev = self.N[i].revScore
            self.stateDictionary[i] = ((forward * rev)/sink)
        return self.stateDictionary

    

########################################################################
#   main
########################################################################

import sys
def main():
    ''' Find the probability of a given path and string. '''
    try:
        if sys.stdin.isatty():
            raise Usage("Usage: problem22.py <infile >outfile")
        
        # clean up the infile
        infile = sys.stdin.readlines()
        dataset = [data.rstrip().split() for data in infile]
        
        # now extract the string, and the emission and transition data.
        string = dataset[0][0]
        emissionColumns = dataset[2]
        hmmStates = dataset[4]
        emissionData = dataset[-(len(hmmStates)):]
        transitionData = dataset[7:7+len(hmmStates)]

        # call graph class and run forward
        G = Graph(string, hmmStates, transitionData, emissionColumns, emissionData)
        iterable = G.topologicalOrder()
        statesDic = G.softDecoding(iterable)

        firstLine = ''
        for i in hmmStates: firstLine+= i+'\t'
        print(firstLine.rstrip())
        data = []
        for i in range(len(string)):
            d = ''
            for k in range(len(hmmStates)):
                ind = hmmStates[k] + str(i)
                d += str(round(statesDic[ind], 4)) + '\t'
            data.append(d.rstrip())
        for d in data: print(d)
        
    except Usage as err:
        print(err.msg)

if __name__ == "__main__":
    main()