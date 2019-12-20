#!/usr/bin/env python3
# Name: Mohammad Abdulqader (mabdulqa)
import sys
import math

def main():
    ''' The following main will find the square of a hypotenuse. '''
    if sys.stdin:
        infile = sys.stdin
    else: #ensures there is a standard input
        raise Exception("Please add an input file with the format: <leg1> <leg2>")

    leg1, leg2 = infile.readline().split() #get the legs of the triangle.

    hypSq = int(leg1)**2 + int(leg2)**2 #finds square of the hypotenuse.

    print("{}".format(hypSq))

    infile.close()

if __name__ == "__main__":
    main()