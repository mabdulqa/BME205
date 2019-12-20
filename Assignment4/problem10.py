#!/usr/bin/env python3

########################################################################
# File: problem10.py
#   executable: problem10.py
# Purpose: Build the overlap Graph.
#   stderr: errors and status
#   stdout: any named out file of the users choosing.
#          
# Author: Mohammad Abdulqader (mabdulqa)
#
#   Notes: Problem 3 of 7 for Assignment 4
#                        
########################################################################

########################################################################
#   buildSeq
########################################################################

def buildSeq(Nodes):
    ''' Build the sequence from all the nodes. '''
    seq = ''
    seq+= Nodes[0]
    for nucleotide in range(1, len(Nodes)): seq+= Nodes[nucleotide][-1:]
    return seq

########################################################################
#   buildSeq
########################################################################

def buildGraph(Nodes):
    ''' Build the sequence from all the nodes. '''
    graph = {}
    for i in range(len(Nodes) - 1):
        graph.update({Nodes[i]: Nodes[i+1]})
    return graph

########################################################################
#   writeNodes
########################################################################

def writeNodes(graph):
    ''' write the nodes '''
    nodes = []
    for i in graph:
        kmer = i
        seq = graph[i]
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
#   kmerComposition
########################################################################

def kmerComposition(sequence, k):
    ''' Find the unique kmers of the given sequence. '''
    composition = set()
    for i in range(len(sequence)-k+1):
        kmer = sequence[i:i+k]
        composition.add(kmer)
    return composition

########################################################################
#   main 
########################################################################

import sys
def main():
    ''' Return the kmer compostion. '''
    try:
        if sys.stdin.isatty():
            raise Usage("Usage: problem9.py <infile >outfile")
        
        # parse the data
        lines = sys.stdin.readlines()
        kmers = [line.rstrip() for line in lines]

        # get the graph and its data and print
        contigs = writeNodes(buildGraph(kmers))
        for contig in contigs:
            print("{} -> {}".format(contig[0], contig[1]))

    except Usage as err:
        print(err.msg)

if __name__ == "__main__":
    main()