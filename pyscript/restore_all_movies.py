#!/usr/bin/python3

# Restore the given input select from the previously saved list of all movies.

import file_ops


# This runs as a service, and is normally run from an automation.
@service
def restore_all_movies(entity=None):
    log.debug(f"got entity {entity}")

    # Input entity is required. It is defined as optional so we can just log an error instead of encountering
    # an exception.
    if entity is None:
        log.error("entity is required, exiting")

    # Domain must be input_select.
    elif not entity.startswith("input_select."):
        log.error("input entity must be domain input_select, exiting")

    # All seems well.
    else:

        # Read the backup file.
        try:
            all_movies = task.executor(file_ops.read_movie_file)
        except FileNotFoundError:
            log.error(f"saved movie file not found, exiting")
            sys.exit(f"file not found")
        except pickle.UnpicklingError:
            log.error(f"saved movie file not usable, exiting")
            sys.exit(f"file not usable")

        log.debug(f"movie list {all_movies}")

        # Populate the input select.
        input_select.set_options(entity_id=entity, options=all_movies)
