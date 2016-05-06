#!/usr/bin/env python
"""this script takes two command line arguments in: MOD and OFFSET. It then
reads lines from stdin, printing every MOD-th line starting at OFFSET 

This is useful for piping a different subset of files from a directory into
different scripts, e.g.

ls path/to/files | python skip.py 10 0 | processing_script
ls path/to/files | python skip.py 10 1 | processing_script
ls path/to/files | python skip.py 10 2 | processing_script
...
ls path/to/files | python skip.py 10 8 | processing_script
ls path/to/files | python skip.py 10 9 | processing_script

^ this would split the contents of 'files' evenly among 10 processing scripts
"""
import sys

if len(sys.argv) < 3:
	print("usage:", sys.argv[0], "MOD OFFSET")

mod = int(sys.argv[1])
off = int(sys.argv[2])

for i, line in enumerate(sys.stdin):
	line = line.strip()
	if (i % mod) == off:
		print(line)

