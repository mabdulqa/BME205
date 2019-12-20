#!/usr/bin/env python3

########################################################################
# File: randomizedMotifSearch.py
#   executable: randomizedMotifSearch.py
# Purpose: To find the consensus motif sequence in a 
#           genome.
#   stderr: errors and status
#   stdout: any named out file of the users choosing.
#          
# Author: Mohammad Abdulqader (mabdulqa)
#
#   Notes: I turned in once more, a day late, to fix a few bugs.
#                        
########################################################################

########################################################################
# CommandLine
########################################################################
class CommandLine():
    '''
    Handle the command line, usage and help requests.

    CommandLine uses argparse, now standard in 2.7 and beyond. 
    it implements a standard command line argument parser with various argument options,
    a standard usage and help, and an error termination mechanism do-usage_and_die.

    attributes:
    all arguments received from the commandline using .add_argument will be
    avalable within the .args attribute of object instantiated from CommandLine.
    For example, if myCommandLine is an object of the class, and requiredbool was
    set as an option using add_argument, then myCommandLine.args.requiredbool will
    name that option.
 
    '''
    
    def __init__(self, inOpts=None) :
        '''
        CommandLine constructor.
        
        Implements a parser to interpret the command line argv string using argparse.
        '''
        
        import argparse
        self.parser = argparse.ArgumentParser(description = 'Program prolog - a brief description of what this thing does', 
                                             epilog = 'Program epilog - some other stuff you feel compelled to say', 
                                             add_help = True, #default is True 
                                             prefix_chars = '-', 
                                             usage = '%(prog)s [options] -option1[default] <input >output' 
                                             )
        self.parser.add_argument('-i','--iterations', type = int, action = 'store', \
            default = 100, help = 'give an integer for iterations')
        self.parser.add_argument('-k','--motifLength', type = int, action = 'store', \
            default = 3, help = 'give an integer for motif length')
        self.parser.add_argument('-p','--psuedocounts', type = float, action = 'store', \
            default = 0, help = 'Give an integer for pseudocount')
        if inOpts is None :
            self.args = self.parser.parse_args()
        else :
            self.args = self.parser.parse_args(inOpts)
  

class Usage(Exception):
    '''
    Used to signal a Usage error, evoking a usage statement and eventual exit when raised.
    '''
    def __init__(self, msg):
        self.msg = msg 

########################################################################
# FastAreader
########################################################################
import sys
class FastAreader:
    '''
    Define objects to read FastA files.

    instantiation:
    thisReader = FastAreader ('testTiny.fa')
    usage:
    for head, seq in thisReader.readFasta():
        print (head,seq)
    '''

    def __init__(self, fname=''):
        '''contructor: saves attribute fname '''
        self.fname = fname

    def doOpen(self):
        ''' Handle file opens, allowing STDIN.'''
        if self.fname is '':
            return sys.stdin
        else:
            return open(self.fname)

    def readFasta(self):
        ''' Read an entire FastA record and return the sequence header/sequence'''
        header = ''
        sequence = ''

        with self.doOpen() as fileH:

            header = ''
            sequence = ''

            # skip to first fasta header
            line = fileH.readline()
            while not line.startswith('>'):
                line = fileH.readline()
            header = line[1:].rstrip()

            for line in fileH:
                if line.startswith('>'):
                    yield header, sequence
                    header = line[1:].rstrip()
                    sequence = ''
                else:
                    sequence += ''.join(line.rstrip().split()).upper()

        yield header, sequence

########################################################################
# RandomizedMotif
########################################################################
import sys
import random
import math
import copy

class RandomizedMotif:
    ''' The following class will find the consensus kmer. '''
    def __init__(self, DNA, kmer, pseudocount):
        ''' Set up the class for needed action. '''
        self.DNA = DNA
        self.k = kmer
        self.pseudocounts = pseudocount

        # Place holders for RandomMotifSearch call
        self.MotifMatrix = None
        self.ProfileMatrix = None
        self.BestProfileMatrix = None
        self.BestMotif = None
        self.setOfMotifs = {x:[] for x in range(len(DNA))}

        for i in self.setOfMotifs:
            for kmerSeq in range(len(DNA[i]) - self.k + 1):
                sequence = DNA[i][kmerSeq:kmerSeq + self.k]
                self.setOfMotifs[i].append(sequence)

    def RandomMotifSearch(self):
        ''' Main algorithm to find the consensus Motif. '''
        self.MotifMatrix = [random.choice(self.setOfMotifs[x]) for x in range(len(self.DNA))]
        self.BestMotif = copy.deepcopy(self.MotifMatrix)

        while True:
            self.ProfileMatrix = self.Profile() # get the profile
            self.MotifMatrix = self.Motif() # get the matrix from the profile 
            if self.entropy(self.ProfileMatrix) < self.entropy(self.BestProfileMatrix):
                self.BestMotif = copy.deepcopy(self.MotifMatrix)
                self.BestProfileMatrix = copy.deepcopy(self.ProfileMatrix)
            else:
                return copy.deepcopy(self.BestMotif), copy.deepcopy(self.BestProfileMatrix)

    def Profile(self):
        ''' Produce a profile for the given motif matrix. '''
        base = len(self.DNA) + 4 * (self.pseudocounts) # base to divide all the counts

        # initalize the profile matrix
        profileMatrix = {x: [self.pseudocounts/base for y in range(self.k)] for x in "ACGT"}

        # now we count
        for seq in self.MotifMatrix:
            indicy = 0
            for nuc in seq:
                if nuc in profileMatrix: 
                    profileMatrix[nuc][indicy] += 1/base
                    indicy += 1
        
        return profileMatrix

    def Motif(self):
        ''' Find the next set of eligible motifs. '''

        # initial empty matrix
        motifMatrix = []

        # have an inital max score and after each sequence
        # chose the kmer with highest score and add to motif
        for i in range(len(self.DNA)):
            maxScore = (" ", 0)
            for motif in self.setOfMotifs[i]:
                score = 1
                for nuc in range(len(motif)): 
                    score *= self.ProfileMatrix[motif[nuc]][nuc]
                if score > maxScore[1]: 
                    maxScore = (motif, score)
            motifMatrix.append(maxScore[0])
        
        return motifMatrix

    def entropy(self, matrix):
        ''' Find entropy of given matrix. '''

        # for the case when the None matrix is called
        if matrix is None: return 10000
        else:
            # adding scores by indicy postion of the profile matrix
            score = 0
            for i in range(self.k):
                scoreArray = []
                for x in matrix:
                    try:
                        # entropy equation
                        value = -1 *((matrix[x][i])*math.log(matrix[x][i], 2))
                    except ValueError:
                        # for cases when there is log2(0)
                        value = 0
                    scoreArray.append(value)
                score += sum(scoreArray)
        
            return score

    def consensus(self, matrix):
        ''' Find the concensus sequence of the given matrix. '''
        sequence = ''
        for i in range(self.k):
            bestNuc = 'A' #starting nucleoitide, can be changed. 
            for nuc in matrix:
                if matrix[bestNuc][i] < matrix[nuc][i]: 
                    bestNuc = nuc
            sequence += bestNuc
        return sequence         

########################################################################
# Main
########################################################################

def main(myCommandLine=None):
    '''
    Implement the Usage exception handler that can be raised from anywhere in process.

    '''
    if myCommandLine is None:
        command = CommandLine()  # read options from the command line
    else :
        command = CommandLine(myCommandLine) # interpret the list passed from the caller of main as the commandline.
    try:
        DNA = [] #an array of all the sequences in the fasta file.
        headers = []
        N = 0 # the len of each sequence.
        for head, seq in FastAreader().readFasta():
            DNA.append(seq.upper())
            pieces = head.split()
            headers.append(pieces[0])

        # set up for printing.
        M = RandomizedMotif(DNA, command.args.motifLength, command.args.psuedocounts)
        # feeds the commandline options to the Genome class

        # initalize -i and holder values for BestProfile and BestMotif
        iterations = command.args.iterations
        BestMotif = None
        BestProfile = None

        while iterations > 0:
            MotifMatrix, ProfileMatrix = M.RandomMotifSearch()
            if BestMotif is None or M.entropy(ProfileMatrix) < M.entropy(BestProfile):
                BestMotif = copy.deepcopy(MotifMatrix)
                BestProfile = copy.deepcopy(ProfileMatrix)
            iterations-=1

        # Now we print the output
        # first is the concensus sequence. with its entropy score.
        print("{}\tScore: {}".format(M.consensus(BestProfile), M.entropy(BestProfile)))
        # print each of the bestMotif's per string.
        for motif in range(len(BestMotif)):
            print("{}: {}".format(headers[motif], BestMotif[motif]))

    except:
        raise Usage("Usage: randomizedMotifSearch.py [options] <infile >outfile")

if __name__ == "__main__":
    main()