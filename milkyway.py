import sys
import standard
from debug import *


# Interpretter


class MilkyWay(standard.Standard):
    
    def __init__(self, program=""):
        """Initialize parent class"""
        standard.Standard.__init__(self, program)
        if outputEnabled:
            if not self.has_out:
                to_out = repr(self.stack.pop(0)).replace("'", '"')
                sys.stdout.write(to_out)
        sys.stdout.write('\n')

if __name__ == "__main__":
    fn = sys.argv[1]
    if fn.endswith(".mwg"):
        try:
            f = open(fn, "r")
            code = f.read().splitlines()
            f.close()
        except:
            code = []
    else:
        code = []
    for program in code:
        MilkyWay(program)