#!/usr/bin/env python3

import sys, argparse, json

def render(dimensions, tflist):
    strmatrix = []

    # Split the flat tflist up into a matrix
    for rownum, row in enumerate((tflist[i:i+dimensions[0]]
            for i in range(0, len(tflist), dimensions[0]))):
        strmatrix.append([])
        for colnum, pixel in enumerate(row):
            if pixel == 1:
                strmatrix[rownum].append("#")
            else:
                strmatrix[rownum].append(" ")

    return strmatrix

def printletter(fontspec, letter):
    dimensions = fontspec['__dimensions__']
    if letter in fontspec:
        strmatrix = render(dimensions, fontspec[letter])
        for row in strmatrix:
            print("    %s" % ''.join(row))
    else:
        print("%s: letter missing!" % letter)

def main(args):
    with open(args.file, 'r') as f:
        fontspec = json.load(f)


    if args.string:
        for letter in args.string:
            printletter(fontspec, letter)
    elif args.letter:
        for letter in args.letter:
            print("%s:" % letter)
            printletter(fontspec, letter)

    else:
        for letter, tflist in fontspec.items():
            # Skip "private" fields
            if letter.startswith("__"):
                continue
            else:
                print("%s:" % letter)
                printletter(fontpsec, letter)


def parse(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", type=str, default="4x4.json")
    parser.add_argument("--letter", "-l", type=str, default=None, nargs="*")
    parser.add_argument("--string", "-s", type=str, default=None, nargs="?")
    return parser.parse_args(args)

if __name__ == "__main__":
    sys.exit(main(parse(sys.argv[1:])))
