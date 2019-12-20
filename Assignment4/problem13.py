#!/usr/bin/env python3

########################################################################
# File: problem13.py
#   executable: problem13.py
# Purpose: Return the Eulerian path of the given sequence.
#   stderr: errors and status
#   stdout: any named out file of the users choosing.
#          
# Author: Mohammad Abdulqader (mabdulqa)
#
#   Notes: Problem 6 of 7 for Assignment 4
#                        
########################################################################

########################################################################
#   Graph 
########################################################################

class Graph:
    '''
        The goal of Genome class is to find the the DeBruijn sequence.

        The following functions are used in the Genome class.
        - EulerianCycle: function finds the Eulerian Path of a given set of cycles.
        - Visit: Visits all adj nodes until a cycle is completed.
        - buildSeq: connects cycles produced from Visit
        - makeGraph: produces adjMatrix for graph.

        Classes within Graph:
        - Node: holds number.

    '''
    class Node:
        ''' 
            Node class has the following duties

            - Holds the data in the node.
            - next and prev
        '''
        def __init__(self, number):
            ''' The information within the node. '''
            self.data = number
            self.next = []
            self.prev = []

    @staticmethod
    def buildSeq(cycles):
        ''' Connect the cycles together. '''
        finalPath = [x for x in cycles[0]]
        # adds the first cycle
        # for all cycles adds cycle[1:] in to 
        for i in range(1, len(cycles)):
            finalPath += cycles[i][1:]
        return finalPath 

    @staticmethod
    def makeGraph(adjMatrix):
        ''' make an adj matrix for Graph '''
        G = {}
        for edge in adjMatrix:
            base, arrow = edge.split(" -> ")
            node = int(base)
            try:
                item = int(arrow)
                out = [item]
            except ValueError:
                items = arrow.split(",")
                out = [int(number) for number in items]
            G.update({node: out})
            for i in out:
                if i not in G: G.update({i:[]})
        return G

    def __init__(self, adjMatrix):
        ''' Set up graph to find Euler's Path. '''
        self.G = self.makeGraph(adjMatrix)
        self.N = {x: self.Node(x) for x in self.G}
        for number in self.G:
            for end in self.G[number]:
                self.N[number].next.append(end)
                self.N[end].prev.append(number)
        self.degree = [len(self.N[x].next) - len(self.N[x].prev) \
            for x in self.N]
        
    def EulerianCycle(self):
        ''' Find the Eulerian Cycle. '''
        if sum(self.degree) is not 0: 
            return "Not Eulerian"
        sequences = []
        refG = dict.copy(self.G)
        for number in self.G:
            if len(self.G[number]) > 0:
                sequence = []
                walkpath = self.Visit(number)
                for i in walkpath[::-1]: sequence.insert(0, i)
                sequences.append(sequence)
        self.G = dict.copy(refG)
        return self.buildSeq(sequences[::-1])

    def Visit(self, node):
        ''' Visits all the nodes until a node with no exit is found. '''
        walkpath = []
        currentNode = node
        walkpath.append(currentNode)
        while len(self.G[currentNode]) > 0:
            adjNode = self.G[currentNode].pop() # pops next node
            walkpath.append(adjNode)
            currentNode = adjNode # changes current node to next node
        return walkpath

########################################################################
#   Usage
########################################################################
    
class Usage(Exception):
    '''
    Used to signal a Usage error, evoking a usage statement and eventual exit when raised.
    '''
    def __init__(self, msg):
        self.msg = msg 

########################################################################
#   main 
########################################################################

import sys
def main():
    ''' Return the kmer compostion. '''
    try:
        if sys.stdin.isatty():
            raise Usage("Usage: problem14.py <infile >outfile")
        # parse data
        lines = sys.stdin.readlines()
        data = [line.rstrip() for line in lines]
        G = Graph(data)
        pathSeq = G.EulerianCycle()
        output =''
        for i in pathSeq[:-1]:
            output += str(i) +"->"
        output+= str(pathSeq[-1])
        print(output)
            
    except Usage as err:
        print(err.msg)

if __name__ == "__main__":
    main()