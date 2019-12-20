#!/usr/bin/env python3
# Name: Mohammad Abdulqader (mabdulqa)
import sys

def main():
    ''' The following main will splice an string to obtain deseried output. '''
    if sys.stdin:
        infile = sys.stdin
    else:
        raise Exception("Please input a file. Usage: python problem4.py <file>")

    data = infile.readlines()

    words = data[0]
    a, b, c, d = [int(x) for x in data[1].split()]

    print("{} {}".format(words[a:b+1], words[c:d+1]))

    infile.close()

if __name__ == "__main__":
    main()