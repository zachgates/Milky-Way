class UnexpectedError(Exception):

    def __str__(self):
        return "This was invoked by using the 'z' opcode."


class UnknownOpcode(Exception):
    
    def __init__(self, opcode):
        self.op = opcode

    def __str__(self):
        return "'{0}' is not a valid opcode.".format(self.op)