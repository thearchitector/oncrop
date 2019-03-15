"""
Detects AR markers within a single frame, and replaces them with given faces.

@author: Elias Gabriel and Duncan Mazza
@revision: v1.0
"""
import sys, getopt, cv2
import ar_markers as ar
from PIL import Image


def process_cmd(argv):
    """ Accepts command arguments and acts accordingly. """
    pass


if __name__ == "__main__":
    # Get the command arguments, omit the first (which will always be the file name), and
    # pass for processing and response
    process_cmd(sys.argv[1:])
