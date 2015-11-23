import sys
import getopt


global inputEnabled
inputEnabled = True


class Base(object):

    def __init__(self):
        if inputEnabled:
            opts, args = getopt.getopt(sys.argv[1:], "i:")
            op = {opt: arg for opt, arg in opts}
            if op.get("-i"):
                self.input = op.get("-i").splitlines()
            else:
                self.input = []