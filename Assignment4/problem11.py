#!/usr/bin/env python3

########################################################################
# File: problem11.py
#   executable: problem11.py
# Purpose: Make DeBruijn graph of a string.
#   stderr: errors and status
#   stdout: any named out file of the users choosing.
#          
# Author: Mohammad Abdulqader (mabdulqa)
#
#   Notes: Problem 4 of 7 for Assignment 4
#                        
########################################################################

########################################################################
#   Genome 
########################################################################

class Genome:
    '''
        The goal of Genome class is to find the the DeBruijn sequence.

        The following functions are used in the Genome class.
        - DeBruijn: function finds the deBruijn sequnce of a given set of sequences.
        - Visit: Visits all adj nodes until a contig is completed.
        - buildSeq: Builds a sequence produced from Visit
        - buildContigs: connects contigs that may be related.
        - getGraph: returns the graph to the user.
        - writeNodes: writes out the patterns of the kmers
        - kmerComposition: returns the kmers in a given sequence

        Classes within Genome:
        - Node: produces a note to hold all k-1mers.

    '''
    class Node:
        ''' 
            Node class has the following duties

            - Holds the data in the node.
        '''
        def __init__(self, kmer):
            ''' The information within the node. '''
            self.data = kmer

    @staticmethod
    def buildSeq(Nodes):
        ''' Build the sequence from all the nodes. '''
        seq = ''
        seq+= Nodes[0]
        for nucleotide in range(1, len(Nodes)): seq+= Nodes[nucleotide][-1:]
        return seq

    @staticmethod
    def buildConitgs(Nodes, k):
        ''' Connect all possible contigs. '''
        sequences = []
        seq = Nodes[0]
        for i in range(len(Nodes)-1):
            if Nodes[i][-(k):] == Nodes[i+1][:k]:
                seq+=Nodes[i+1][k:]
            else: 
                sequences.append(seq)
                seq = Node[i+1] 
        sequences.append(seq)

        return sequences

    @staticmethod
    def kmerComposition(sequence, k):
        ''' return all kmers of size k from sequence. '''
        for i in range(len(sequence) - k + 1):
            kmer = sequence[i:i+k]
            yield kmer

    def __init__(self, sequence, k):
        ''' Initalize the head tail and cursor. '''
        self.N = {} # dictionary with all the Nodes
        self.Graph = {} # adj matrix
        self.k = k

        for kmer in self.kmerComposition(sequence, k):
            # set up the k-1mers and thier node pointers
            k1left, k1right = kmer[:-1], kmer[1:]
            leftNode, rightNode = None, None

            # check if k-1mer in dictionary N
            if k1left in self.N: leftNode = self.N[k1left]
            else: leftNode = self.N[k1left] = self.Node(k1left)

            if k1right in self.N: rightNode = self.N[k1right]
            else: rightNode = self.N[k1right] = self.Node(k1right)

            # add to adj matrix
            self.Graph.setdefault(leftNode.data, []).append(rightNode.data)

    def DeBruijn(self):
        ''' Find the DeBruijn sequence. '''
        contigs = []
        refG = dict.copy(self.Graph) # to save a copy of the graph
        for node in self.Graph:
            if len(self.Graph[node]) > 0:
                walkpath = self.Visit(node)
                contigs.append(walkpath)
                #contigs.append(self.buildSeq(walkpath))
        self.Graph = dict.copy(refG)

        return self.buildConitgs(contigs[::-1], self.k -1)

    def Visit(self, node):
        ''' Visits all the nodes until a node with no exit is found. '''
        walkpath = []
        currentNode = node
        walkpath.append(currentNode)
        while len(self.Graph[currentNode]) > 0:
            adjNode = self.Graph[currentNode].pop()
            walkpath.append(adjNode)
            currentNode = adjNode
        return self.buildSeq(walkpath)

    def getGraph(self):
        ''' Gives Graph G of Genome class. '''
        return dict.copy(self.Graph)

    def writeNodes(self):
        ''' write the nodes '''
        nodes = []
        for i in self.Graph:
            kmer = i
            seq = ''
            length = len(self.Graph[i]) - 1
            kmers = sorted(self.Graph[i])
            for k in range(length): seq+= kmers[k] +","
            seq+= kmers[length]
            nodes.append((kmer, seq))

        return nodes

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
            raise Usage("Usage: problem12.py <infile >outfile")
        
        # parse the file
        lines = sys.stdin.readlines()
        sequence = lines[1].rstrip()
        k = int(lines[0].rstrip())
        # call the Genome class and get the nodes
        G = Genome(sequence, k)
        Graph = G.writeNodes()

        # print
        for kmer in Graph:
            print("{} -> {}".format(kmer[0],kmer[1]))
        
    except Usage as err:
        print(err.msg)

if __name__ == "__main__":
    main()