#!/usr/bin/python3

# Restore the given input select from the previously saved list of options.

import sys
import os
import json


@pyscript_executor
def read_file(file):
    with open(file, "r") as infile:
        return json.load(infile)

# This runs as a service, and is normally run from a script or automation.
@service
def restore_input_select_options(entity=None, file=None):
    log.debug(f"got entity {entity}, file {file}")

    # Inputs are required. They are defined as optional so we can just log an error instead of encountering
    # an exception.
    if entity is None or file is None:
        log.error("all inputs are required, exiting")

    # Domain must be input_select.
    elif not entity.startswith("input_select."):
        log.error("input entity must be domain input_select, exiting")

    # All seems well.
    else:

        # Read the backup file.
        try:
            list = read_file(file)
        except FileNotFoundError:
            log.error(f"saved file not found, exiting")
            sys.exit(f"file not found")
        except pickle.UnpicklingError:
            log.error(f"saved file not usable, exiting")
            sys.exit(f"file not usable")

        log.debug(f"list {list}")

        # Populate the input select.
        input_select.set_options(entity_id=entity, options=list)
