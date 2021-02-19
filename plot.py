#!/usr/bin/env python3

import subprocess
import sys

def plot(res):
    print(res)
def main():
    res = []
    for line in sys.stdin :
        res.append(line.strip("\n").split("\t"))
    plot(res)


if __name__ == "__main__":
    main()
