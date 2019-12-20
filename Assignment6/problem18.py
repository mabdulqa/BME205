#!/usr/bin/env python3
########################################################################
# File: problem18.py
#       executable: problem18.py
# Purpose: Find the best path using veterbi algorithm. 
#       stderr: errors and status
#       stdout: the file of choice from std out. 
#          
# Author: Mohammad Abdulqader
# History:      11/07/2019 Created
#               11/11/2019 Made main and Usage
#               11/12/2019 Made transition and emission functions.
#               11/14/2019 Modified transition and emission functions.
#               11/15/2019 removed transition and emission
#               11/17/2019 used the DAG algorithm for longest path
#               11/19/2019 modified alogrithm to find state path
#               11/20/2019 modified to also give probablity.
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

import random
import copy
class Graph:
    '''
        The following graph class solves the DAG alignment problem using
        the following functions.
        - PofE: returns probability of moving to that node
        - makeMatrix: turns tables into a searchable matrix
        - makeGraph: produces the Adj matrix graph.
        - calculateNode: calculates the movement to a node
        - viterbiAlgorithm: find the highest probability path.
        - topologicalOrder: find the topological order of the graph.

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
    
    @staticmethod
    def PofE(row, target):
        ''' Return the desired transition probability. '''
        for col, prob in row:
            if col == target: return prob
        return None

    @staticmethod
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

    def __init__(self, string, hmmStates, transitionData, emissionColumns, emissionData):
        ''' make the adj matrix of the graph. '''
        self.string = string
        self.numStates = len(hmmStates)
        self.transitionMatrix = self.makeMatrix(hmmStates, hmmStates, transitionData)
        self.emissionMatrix = self.makeMatrix(emissionColumns, hmmStates, emissionData)
        self.G = {} # graph for viterbi algorithm
        self.N = {} # set of nodes for viterbi graph.
        self.start = self.N['start'] = self.Node("start", "")
        self.end = self.N['end'] = self.Node("end", "")
        self.makeGraph(string)

    def makeGraph(self, stringData):
        ''' make the adj matrix, and Node dictionary. '''
        states = sorted(self.transitionMatrix.keys())
        for i in range(len(stringData)):
            # makes the start to hmm state connections
            if i == 0:
                nodes = [self.Node(k+str(i), stringData[i]) for k in states]
                for nodeState in nodes:
                    nodeState.hmm = nodeState.name[:1]
                    self.N[nodeState.name] = nodeState
                    self.G.setdefault(self.N['start'].name, []).append(nodeState.name)
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
                        self.G.setdefault(self.N[state+str(i - 1)].name, []).append(nodeState.name)
                        nodeState.prev.append(self.N[state+str(i - 1)].name)
                        nodeState.inComing+=1
                continue
        # adress connections to end
        lastItem = len(stringData) - 1
        for state in states:
            self.G.setdefault(self.N[state+str(lastItem)].name, []).append(self.N['end'].name)
            self.N['end'].prev.append(self.N[state+str(lastItem)].name)
            self.N['end'].inComing+=1
        self.G.update({'end':[]})

    def calculateNode(self, hmm, hmmPrev, emission):
        ''' calculate the wieght of the next movement.'''
        # for case where last node to end node
        if hmm == 'None': return 1

        # for case for start to first node
        elif hmmPrev == 'None':
            eM = self.emissionMatrix[hmm]
            emissionOfX = self.PofE(eM, emission)
            return (1/self.numStates) * emissionOfX

        # for node to node movement
        else:
            eM = self.emissionMatrix[hmm]
            emissionOfX = self.PofE(eM, emission)
            tM = self.transitionMatrix[hmmPrev]
            transOfX = self.PofE(tM, hmm)
            return transOfX * emissionOfX

    def topologicalOrder(self):
        ''' find the topological order of Graph G. '''
        # copy graph and node dict to save them
        refG = copy.deepcopy(self.G)
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

    def viterbiAlgorithm(self, iterable):
        ''' Find the longest path. '''
        # set score of all nodes
        for node in self.G:
            self.N[node].score = 0
        self.start.score = 1

        # now score nodes as you go by comparing prev scores
        for value in iterable:
            # for case if prev empty
            # start has no hmm state so dont add it
            if self.N[value].inComing == 0: 
                self.N[value].path = ""
                continue

            # for case when prev is not empty
            else:
                maxPrev = self.N[value].prev[0]
                for node in self.N[value].prev:
                    # get the hmm states of the prev and current
                    # get the emission of the next string
                    # if the current score is higher than the max, change the max
                    hmmPrev = self.N[node].hmm
                    hmm = self.N[value].hmm
                    em = self.N[value].data
                    maxHmm = self.N[maxPrev].hmm
                    if self.N[node].score * self.calculateNode(hmm, hmmPrev, em) > \
                        self.N[maxPrev].score * self.calculateNode(hmm, maxHmm, em): 
                        maxPrev = node
                
                # gets edge weight and its hmm state and multiply it and update the path
                maxHmm = self.N[maxPrev].hmm
                valueWeight = self.calculateNode(hmm, maxHmm, em)
                self.N[value].score = valueWeight * self.N[maxPrev].score

                # end has no emission so dont add the emission or hmm state
                if self.N[value] == self.end:
                    self.end.path = self.N[maxPrev].path
                else:
                    self.N[value].path = self.N[maxPrev].path + self.N[value].hmm
        
        return self.end.score, self.end.path
    

########################################################################
#   main
########################################################################

import sys
def main():
    ''' Find the probability of a given path and string. '''
    try:
        if sys.stdin.isatty():
            raise Usage("Usage: problem18.py <infile >outfile")
        
        # clean up the infile
        infile = sys.stdin.readlines()
        dataset = [data.rstrip().split() for data in infile]
        
        # now extract the string, and the emission and transition data.
        string = dataset[0][0]
        emissionColumns = dataset[2]
        hmmStates = dataset[4]
        emissionData = dataset[-(len(hmmStates)):]
        transitionData = dataset[7:7+len(hmmStates)]

        # call graph class and run viterbi
        G = Graph(string, hmmStates, transitionData, emissionColumns, emissionData)
        iterable = G.topologicalOrder()
        score, path = G.viterbiAlgorithm(iterable)
        print(path)

    except Usage as err:
        print(err.msg)

if __name__ == "__main__":
    main()