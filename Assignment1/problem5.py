#!/usr/bin/env python3
# Name: Mohammad Abdulqader (mabdulqa)
import sys

def main():
    ''' The following main finds the sum of odds from a to b. '''
    if sys.stdin:
        infile = sys.stdin
    else:
        raise Exception("Usage: problem5.py <infile")

    sumOfOdds = 0
    start, end = infile.readline().split()

    for i in range(int(start), int(end)+1):
        if i%2 == 1:
            sumOfOdds+= i

    print("{}".format(sumOfOdds))
    
    infile.close()

if __name__ == "__main__":
    main()