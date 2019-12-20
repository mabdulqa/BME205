#!/usr/bin/env python3

########################################################################
# File: problem9.py
#   executable: problem9.py
# Purpose: Return the final string from Genome Path.
#   stderr: errors and status
#   stdout: any named out file of the users choosing.
#          
# Author: Mohammad Abdulqader (mabdulqa)
#
#   Notes: Problem 2 of 7 for Assignment 4
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
        lines = sys.stdin.readlines()
        kmers = []
        for line in lines: kmers.append(line.rstrip())
        print(buildSeq(kmers))

    except Usage as err:
        print(err.msg)

if __name__ == "__main__":
    main()