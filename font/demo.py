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

def main(args):
    with open(args.file, 'r') as f:
        fontspec = json.load(f)

    dimensions = fontspec['__dimensions__']

    if args.letter:
        for letter in args.letter:
            if letter in fontspec:
                strmatrix = render(dimensions, fontspec[letter])
                print("%s:" % letter)
                for row in strmatrix:
                    print("    %s" % ''.join(row))
            else:
                print("%s: letter missing!" % letter)

    else:
        for letter, tflist in fontspec.items():
            # Skip "private" fields
            if letter.startswith("__"):
                continue
            else:
                strmatrix = render(dimensions, tflist)
                print("%s:" % letter)
                for row in strmatrix:
                    print("    %s" % ''.join(row))


def parse(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", type=str, default="4x4.json")
    parser.add_argument("letter", type=str, default=None, nargs="*")
    return parser.parse_args(args)

if __name__ == "__main__":
    sys.exit(main(parse(sys.argv[1:])))
