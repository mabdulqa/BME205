#!/usr/bin/env python3
# Name: Mohammad Abdulqader (mabdulqa)
import sys

def main():
    ''' The following main counts the words in a file. '''
    if sys.stdin:
        infile = sys.stdin
    else:
        raise Exception("Usage: problem7.py <infile ")

    Wordcounts = {}

    lines = infile.readlines()

    # the for loop is intended if the file has multiple lines.
    for line in lines:
        words = line.split()
        for word in words:
            if word in Wordcounts:
                Wordcounts[word] += 1
            else:
                Wordcounts.update({word:1})
    
    sortedWords = sorted(Wordcounts)

    # prints out the word and counts.
    for word in sortedWords:
       print("{}: {}".format(word, Wordcounts[word]))

    infile.close()

if __name__ == "__main__":
    main()