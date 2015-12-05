import sys
import standard
from debug import *


# Interpreter


class MilkyWay(standard.Standard):
    
    def __init__(self, program="", pre_stack=[], override=False, specVals={}):
        """Initialize parent class"""
        standard.Standard.__init__(self, program, pre_stack, specVals)
        if outputEnabled and not verboseStack:
            if not override and not self.has_out and len(self.stack):
                to_out = repr(self.stack.pop(0)).replace("'", '"')
                sys.stdout.write(to_out)
        if not override and not self.has_out:
            sys.stdout.write('\n')

    def spare(self, program, pre_stack=[], specVals={}):
        return MilkyWay(program, pre_stack, True, specVals=specVals)

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
        if verboseStack:
            print(MilkyWay(program, override=True).stack)
        else:
            MilkyWay(program)