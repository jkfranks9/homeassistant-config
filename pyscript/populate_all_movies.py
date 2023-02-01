#!/usr/bin/python3

# Populate the given input select from the result of a Kodi all movies query.

import sys

# File I/O is done in a called module - ensure the path includes it. Note that this only needs to be added
# to one file ... pyscript picks it up when loading the files.
if "/config/pyscript_modules" not in sys.path:
    sys.path.append("/config/pyscript_modules")

import file_ops


# This runs as a service, and is normally run from an automation.
@service
def populate_all_movies(entity=None, result=None):
    log.debug(f"got entity {entity}, result {result}")

    # Inputs are required. They are defined as optional so we can just log an error instead of encountering
    # an exception.
    if entity is None or result is None:
        log.error("entity and result are both required, exiting")

    # Domain must be input_select.
    elif not entity.startswith("input_select."):
        log.error("input entity must be domain input_select, exiting")

    # All seems well.
    else:
        # List of all movies
        movies = result['movies']
        all_movies = []
        for movie in movies:
            all_movies.append(movie['label'])
        all_movies.sort()
        log.debug(f"movie list {all_movies}")

        # Populate the input select.
        input_select.set_options(entity_id=entity, options=all_movies)

        # Write the list to a file so we can restore the input select after a restart.
        task.executor(file_ops.write_movie_file, all_movies)

