from glance.util import output
import os
import pathlib


def process(paths, args):
    yield from _process_paths(paths, set(), args)


def _process_paths(paths, uniq, args):
    for path in paths:
        if path.is_dir():
            if not args.recurse:
                output.note("{0} is a directory and --recursive flag is not set, skipping".format(path))
            else:
                for _cd, _, files in os.walk(path):
                    yield from _process_paths(map(lambda it: pathlib.Path(_cd, it), files), uniq, args)
        else:
            if path in uniq:
                output.note("{0} is already processed, skipping".format(path))
            elif not path.exists():
                output.warn("{0} does not exist, skipping".format(path))
            else:
                yield path
