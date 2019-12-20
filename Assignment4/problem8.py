#!/usr/bin/env python3

########################################################################
# File: problem8.py
#   executable: problem8.py
# Purpose: output the unique kmers in lexogarphic order.
#   stderr: errors and status
#   stdout: any named out file of the users choosing.
#          
# Author: Mohammad Abdulqader (mabdulqa)
#
#   Notes: Problem 1 of 7 for Assignment 4
#                        
########################################################################

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
#   kmerCompostion 
########################################################################

def kmerComposition(sequence, k):
    ''' Find the unique kmers of the given sequence. '''
    composition = []
    for i in range(len(sequence)-k+1):
        kmer = sequence[i:i+k]
        composition.append(kmer)
    return composition

########################################################################
#   main 
########################################################################

import sys
def main():
    ''' Return the kmer compostion. '''
    try:
        if sys.stdin.isatty():
            raise Usage("Usage: problem8.py <infile >outfile")
        lines = sys.stdin.readlines()
        k = int(lines[0])
        sequence = lines[1]
        kmerComp = sorted(kmerComposition(sequence, k))
        for kmer in kmerComp: print(kmer)

    except Usage as err:
        print(err.msg)

if __name__ == "__main__":
    main()