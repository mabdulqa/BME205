#!/usr/bin/env python3
########################################################################
# File: program15.py
#       executable: program15.py
# Purpose: Find the longest path in a DAG problem. 
#       stderr: errors and status
#       stdout: the file of choice from std out. 
#          
# Author: Mohammad Abdulqader
# History:      10/26/2019 Created
#               10/28/2019 Made init and the Graph class
#               10/30/2019 Make topological function
#               11/04/2019 Laptop returned today did longestPath
#               11/05/2019 figured out a bug in the longestPath function
#               
########################################################################

########################################################################
#   Graph
########################################################################

import random
import copy
class Graph:
    '''
        The following graph class solves the DAG alignment problem using
        the following functions.
        - makeGraph: produces the Adj matrix graph.
        - longestPath: find the longestPath.
        - topologicalOrder: find the topological order of the graph.
        - Edge: return edge weight between (a, b)

        In Graph the following classes are included:
        - Node: makes node to hold data.
    '''
    class Node:
        '''
            The following Node class contains:
            - self.data which holds data
            - self.inComing which says how many incoming nodes there are
            - self.score which scores the node
            - self.prev which saves all incoming nodes
            - self.path that holds the path to that node.
        '''
        def __init__(self, data):
            ''' produce a node's attributes. '''
            self.data = data
            self.inComing = 0
            self.prev = []
            self.path = None
            self.score = None
      
    def __init__(self, start, end, dataset):
        ''' make the adj matrix of the graph. '''
        self.INF = (10**23)
        self.G = {}
        self.N = {}
        self.start = self.N[start] = self.Node(start)
        self.sink = self.N[end] = self.Node(end)
        self.makeGraph(dataset)

    
    def makeGraph(self, setOfEdges):
        ''' make the adj matrix '''
        for i in setOfEdges:
            # initalizes the values. 
            key, value = i.split("->")
            number = int(key)
            valueEdge, edgeWeight = [int(x) for x in value.rstrip().split(":")]

            # checks if current node already in self.N
            if number in self.N: currentNode = self.N[number]
            else: currentNode = self.N[number] = self.Node(number)

            # check if node at end of arc already in self.N
            if valueEdge in self.N: nextNode = self.N[valueEdge]
            else: nextNode = self.N[valueEdge] = self.Node(valueEdge)
      
            # Now we add to adjmatrix
            self.G.setdefault(self.N[number].data, []).append((valueEdge, edgeWeight))
            if valueEdge not in self.G: self.G.update({valueEdge: []})
            self.N[valueEdge].inComing += 1
            self.N[valueEdge].prev.append(number)

        self.start.inComing = 0

    def topologicalOrder(self):
        ''' find the topological order of Graph G. '''
        # copy graph and node dict to save them
        refG = copy.deepcopy(self.G)
        refN = copy.deepcopy(self.N)
        iterable = []
        candidates = []

        # add all inital nodes with no inComing edges
        for node in sorted(self.N):
            if self.N[node].inComing == 0: candidates.append(self.N[node].data)
        
        # produce the iterable list
        while len(candidates) > 0:
            a = candidates.pop(0)
            iterable.append(a)
            while len(refG[a]) > 0:
                b, bWeight = refG[a].pop(0)
                refN[b].inComing -= 1
                if refN[b].inComing == 0: candidates.append(b)
        
        # ensures we have a DAG
        remainingNodes = [len(refG[node]) for node in refG]
        if sum(remainingNodes) != 0: 
            return 'The input graph G is not a DAG.'
        else: return iterable

    def longestPath(self, iterable):
        ''' Find the longest path. '''
        # set score of all nodes
        for node in self.G:
            self.N[node].score = -self.INF
        self.start.score = 0

        # now score nodes as you go by comparing prev scores
        for value in iterable:
            # for case if prev empty
            if self.N[value].inComing == 0: 
                self.N[value].path = [value]
                continue

            # for case when prev is not empty
            else:
                maxPrev = self.N[value].prev[0]
                for node in self.N[value].prev:
                    if self.N[node].score + self.Edge(node, value) > \
                        self.N[maxPrev].score + self.Edge(maxPrev, value): maxPrev = node
                
                # gets edge weight and add it and update the path
                valueWeight = self.Edge(maxPrev, value)
                self.N[value].score = valueWeight + self.N[maxPrev].score
                self.N[value].path = self.N[maxPrev].path + [value]

        for i in sorted(self.N):
            print("{}\t{}\t{}\t{}".format(i, self.N[i].inComing, self.N[i].score, self.N[i].path))
        return self.sink.score, self.sink.path

    def Edge(self, a, b):
        ''' return the edge weight. '''
        for edge in self.G[a]:
            if edge[0] == b: return edge[1]
                

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
    ''' Find the longest path from the data set. '''
    try:
        if sys.stdin.isatty():
            raise Usage('Usage: problem15.py <infile >outfile')
    
        # This handles stdin file.
        infile = sys.stdin.readlines()
        sink = int(infile[1])
        start = int(infile[0])
        dataset = infile[2:]

        # call Graph class and find topological order
        G = Graph(start, sink, dataset)
        iterable = G.topologicalOrder()

        # if it is not a DAG, exit program.
        if iterable == 'The input graph G is not a DAG.':
            raise Usage(iterable)
        
        # otherwise find the longestPath
        score, path = G.longestPath(iterable)

        # print the output
        print("{}".format(score))
        outPath = ''
        for i in range(len(path) - 1):
            outPath += str(path[i]) +'->'
        outPath += str(path[-1])
        print(outPath)

    except Usage as err:
        print(err.msg)
    
if __name__ == "__main__":
    main()
