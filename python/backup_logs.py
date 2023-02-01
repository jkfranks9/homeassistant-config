#!/usr/bin/python3

# Backup a current log file similar to logrotate. For example:
#
#   example.log  -> example1.log
#   example1.log -> example2.log
#   etc.
#
# Note that we create the full set of potential files, based on the maximum
# count. This of course results in some empty files until we've filled them up.

import os
from os.path import exists
import shutil
import itertools
import sys

# Constants
MAX_LOG_FILES_COUNT = 7


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


# Validate we have a single argument and that the input file exists.
if len(sys.argv) == 2 and exists(target_log_file := sys.argv[1]):

    # Separate the log file name into the prefix (name) and suffix (extension).
    log_file_name, log_file_ext = os.path.splitext(target_log_file)

    # Generate the complete set of potential file names.
    files = [
        "{}{}{}".format(log_file_name, i, log_file_ext)
        for i in range(1, MAX_LOG_FILES_COUNT + 1)
    ]

    # Create any files that don't exist.
    for file in files:
        if not exists(file):
            open(file, 'w').close()

    # Now copy all non-empty files
    for older, newer in pairwise(reversed([target_log_file] + files)):
        if newer:
            if not os.stat(newer).st_size == 0:
                shutil.copy2(newer, older)

    # Finally, clear the base file.
    open(target_log_file, 'w').close()
