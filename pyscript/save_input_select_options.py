#!/usr/bin/python3

# Populate the given input select from a list of options.

import sys
import os
import json


@pyscript_executor
def write_file(list, file):
    with open(file, "w") as outfile:
        json.dump(list, outfile)

# This runs as a service, and is normally run from a script or automation.
@service
def save_input_select_options(entity=None, list=None, file=None):
    log.debug(f"got entity {entity}, list {list}, file {file}")

    # Inputs are required. They are defined as optional so we can just log an error instead of encountering
    # an exception.
    if entity is None or list is None or file is None:
        log.error("all inputs are required, exiting")

    # Domain must be input_select.
    elif not entity.startswith("input_select."):
        log.error("input entity must be domain input_select, exiting")

    # All seems well.
    else:

        # Populate the input select.
        input_select.set_options(entity_id=entity, options=list)

        # Write the list to a file so we can restore the input select after a restart.
        write_file(list, file)

