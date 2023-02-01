#!/usr/bin/python3

import glob
import os
import sys

# Validate we have a single argument. We assume the set of files to be concatenated already exist.
if len(sys.argv) == 2:

    # Initialize the file names we need.
    log_files = f"{sys.argv[1]}[1-7].log"
    concat_file = f"{sys.argv[1]}-concat.log"
    
    read_files = glob.glob(log_files)
    read_files.sort(key=os.path.getmtime)

    with open(concat_file, "w") as outfile:
        for file in read_files:
            with open(file, "r") as infile:
                outfile.write(infile.read())
