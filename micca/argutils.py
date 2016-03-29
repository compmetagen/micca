import argparse
import os.path


def outputdir(path):
    epath = os.path.expandvars(os.path.expanduser(path))
    try:
        os.makedirs(epath)
    except OSError:
        if not os.path.isdir(epath):
            msg = "directory %s cannot be created" % path
            raise argparse.ArgumentTypeError(msg)
    return epath
