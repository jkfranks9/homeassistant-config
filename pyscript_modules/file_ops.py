#!/usr/bin/python3

# This native Python module is called by pyscript modules to perform file operations.

import os
import pickle

# Constants
MOVIE_BACKUP_FILE = "/config/all_movies_backup"


# Write the movie list to a file.
def write_movie_file(all_movies):
    with open(MOVIE_BACKUP_FILE, "wb") as outfile:
        pickle.dump(all_movies, outfile)


# Read and return the movie list.
def read_movie_file():
    with open(MOVIE_BACKUP_FILE, "rb") as infile:
        return pickle.load(infile)
