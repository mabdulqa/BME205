#!/usr/bin/env python3
# Name: Mohammad Abdulqader (mabdulqa)
import sys

def main():
    ''' The following main program will print the even lines of a file. '''
    if sys.stdin:
        infile = sys.stdin
    else:
        raise Exception("Usage: python problem6.py <infile>")
    
    # list of all the lines in input file
    listOfLines = infile.readlines()

    for i in range(len(listOfLines)):
        if (i+1)%2 is 0: print("{}".format(listOfLines[i].strip()))

    infile.close()

if __name__ == "__main__":
    main()