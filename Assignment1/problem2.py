#!/usr/bin/env python3
# Name: Mohammad Abdulqader (mabdulqa)
import sys

def main():
    ''' The following main will count all possible nucleotides. '''
    if sys.stdin:
        infile = sys.stdin
    else:
        raise Exception("Please input a nucelotide sequence.")
    sequence = infile.readline()

    countDic = {i:0 for i in "ATGC"} #dictionary is created to nuc counts

    for nucleotide in sequence: #iterates through sequence to count each nuc
        if nucleotide in countDic:
            countDic[nucleotide]+= 1
    
    print("{} {} {} {}".format(countDic["A"], countDic["C"], \
         countDic["G"], countDic["T"]))

    infile.close()

if __name__ == "__main__":
    main()