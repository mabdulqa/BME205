#!/usr/bin/env python3

########################################################################
# File: missingMotif.py
#   executable: missingMotif.py
# Purpose: To find the most under represented motif sequences in a 
#           genome.
#   stderr: errors and status
#   stdout: any named out file of the users choosing.
#          
# Author: Mohammad Abdulqader (mabdulqa)
#
#   Notes: Zm4 genome computing time: 41 seconds
#          A.platensis genome computing time: 121 seconds 
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
        self.parser.add_argument('--minMotif', type = int, choices = range(3, 9), action = 'store', default = 3, help = 'give an integer for motif minimum')
        self.parser.add_argument('--maxMotif', type = int, choices = range(3, 9), action = 'store', default = 8, help = 'give an integer for motif maximum')
        self.parser.add_argument('--cutoff', type = float, action = 'store', default = 0.0, help = 'give a Z-score cutoff')
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
# Genome
########################################################################

class Genome:
    """ Find the Z-score, Expected Value, and count of all motifs. 

        The following functions are included in Genome class:
        - Zscore: calculates Z score of given kmer.
        - eValue: calculate eValue of given kmer.
        - kmerList: returns the kmer data.
    """
    @staticmethod
    def reverseSeq(sequence):
        """ Find the reverse compliment. """
        return sequence.translate(str.maketrans("ATCG", "TAGC"))[::-1]
    
    def __init__(self, sequences, N, minVal, maxVal, Zcutoff):
        """Find the counts of all possible kmers in the sequence."""
        self.sequences = sequences
        self.cutoff = Zcutoff
        self.kmerCounts = dict()
        self.minVal = minVal
        self.maxVal = maxVal
        self.N = N

        for seq in self.sequences:
            for k in range(self.minVal - 2, self.maxVal + 1):
                for i in range(len(seq) - k + 1):
                    kmer = ''.join(seq[i:i+k])
                    if self.reverseSeq(kmer) in self.kmerCounts:
                        self.kmerCounts[kmer] = self.kmerCounts[self.reverseSeq(kmer)]
                        self.kmerCounts[kmer][0]+=1
                    elif kmer in self.kmerCounts:
                        self.kmerCounts[kmer][0]+=1
                    else:
                        self.kmerCounts[kmer] = [1]

    def Zscore(self, kmer):
        """ Find the Z-score of the given kmer. """
        mean = self.eValue(kmer)
        N = self.N
        p = mean/N #finds p from the mean.
        stdDev = (N*p*(1 - p))**0.5 #finds stdDeviation

        Ztop = self.kmerCounts[kmer][0] - mean
        
        return Ztop/stdDev

    def eValue(self, kmer):
        """ Find the expected number of the given kmer. """
        end = len(kmer)-1
        expectedNum = self.kmerCounts[kmer[:-1]][0] * self.kmerCounts[kmer[1:]][0] 
        #reports counts of each k-1mer and multiplies them
        expectedDen = self.kmerCounts[kmer[1:end]][0] # divides by the k-2mer that contains the middle sequnces.
        return expectedNum/expectedDen
                
    def kmerList(self):
        """ Return a list of the kmer data. """
        kmax = 8
        kmerlist = list() # empty list, intended to be a list of lists.
        listcheck = list() # list of what has been added.
        for kmer in self.kmerCounts.keys():
            if len(kmer) >= self.minVal and len(kmer) <= self.maxVal and \
                self.reverseSeq(kmer) not in listcheck and self.Zscore(kmer) < self.cutoff:
                #    ensures the following:
                # 1. the kmer size between min and max
                # 2. the reverse has not been added yet
                # 3. the Zscore is below the cutoff
                thek = kmax - len(kmer)
                kmerlist.append([kmer, self.reverseSeq(kmer), self.kmerCounts[kmer][0], self.eValue(kmer), self.Zscore(kmer), thek])
                listcheck.append(kmer)
        
        return sorted(kmerlist, key=lambda kmer:(kmer[5], kmer[4]))


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
    if sys.stdin:
        sequences = [] #an array of all the sequences in the fasta file.
        N = 0 # the len of each sequence.
        for head, seq in FastAreader().readFasta():
            sequences.append(seq)
            N+=len(seq)
        #set up for printing.
        G = Genome(sequences, N, command.args.minMotif, command.args.maxMotif, command.args.cutoff) 
        # feeds the commandline options to the Genome class
        kmerList = G.kmerList() #produces a list with the 

        print("sequence:reverse\tcount\tExpect\tZscore")
        for kmer in kmerList: # prints the kmer and thier respective data.
            print('{0:8}:{1:8}\t{2:0d}\t{3:0.2f}\t{4:0.2f}'.format(kmer[0], kmer[1], kmer[2], kmer[3], kmer[4]))
    else:
        raise Usage("Usage: missingMotif.py [options] <infile >outfile")


if __name__ == "__main__":
    main()