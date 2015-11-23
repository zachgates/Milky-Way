import sys
import getopt


# Debug Globals

global inputEnabled
inputEnabled = True


# Shorthand

def _is(val, typ):
    if isinstance(val, typ):
        return True
    return False


# Filler Class

class Empty(object):
    pass


# Language Base


class Base(object):

    def __init__(self, program=""):
        """Initialize program"""
        self.has_out = False
        if inputEnabled:
            opts, args = getopt.getopt(sys.argv[1:], "i:")
            op = {opt: arg for opt, arg in opts}
            if op.get("-i"):
                self.input = op.get("-i").splitlines()
            else:
                self.input = []
        opcodes, data = self.tokenize(program)
        self.stack = self.merge_stacks(opcodes, data)
        self.run_ops()

    def tokenize(self, program):
        """Separate opcodes from data types"""
        temp_stack = list(program)
        skip = []
        opcodes, data = [Empty(), Empty()], ["", 0]
        c_op, c_dt = "", ""
        for i in range(len(temp_stack)):
            if i not in skip:
                if temp_stack[i] in self.op2func.keys():
                    if c_op:
                        opcodes.append(c_op)
                        data.append(Empty())
                        c_op = temp_stack[i]
                    if c_dt:
                        opcodes.append(Empty())
                        data.append(c_dt)
                        c_dt = ""
                    if self.op2func.get(temp_stack[i]):
                        opcodes.append(c_op + temp_stack[i])
                        data.append(Empty())
                        c_op = ""
                elif temp_stack[i].isdigit():
                    if c_dt.isdigit():
                        c_dt += temp_stack[i]
                    else:
                        if c_dt:
                            opcodes.append(Empty())
                            data.append(c_dt)
                            c_op = ""
                        c_dt = temp_stack[i]
                elif temp_stack[i] in self.validTypes.keys():
                    if c_dt:
                        opcodes.append(Empty())
                        data.append(c_dt)
                        c_dt = ""
                    rng, dat = self.parse_type(temp_stack, i)
                    skip += rng
                    opcodes.append(Empty())
                    data.append(dat)
                    c_op = ""
            else:
                raise Exception()
        if c_dt:
            opcodes.append(Empty())
            data.append(c_dt)
        for i in range(len(data)):
            if isinstance(data[i], str):
                if data[i].isdigit():
                    data[i] = int(data[i])
        return opcodes, data

    def parse_type(self, stack, index):
        """Distinguish between opcodes and data types"""
        to_find = self.validTypes.get(stack[index])
        opener = stack[index]
        skip_from = int(index)
        stack_next = stack[index:]
        data = ""
        opn, cls = 0, 0
        while stack_next:
            index += 1
            n = stack_next.pop()
            data += n
            if n == to_find:
                cls += 1
                if opn == cls:
                    stack_next = 1
                    break
            elif n == opener:
                opn += 1
            else:
                pass
        if not stack_next:
            data += to_find
        return [range(skip_from, index), eval(data)]

    def merge_stacks(self, opcodes, data):
        """Merge opcodes and data into a single stack"""
        retval = []
        for a, b in zip(opcodes, data):
            if isinstance(a, Empty):
                retval.append(b)
            elif isinstance(b, Empty):
                retval.append(a)
            else:
                return []
        return retval

    def run_ops(self):
        """Evaluate the program"""
        i = 0
        while i < len(self.stack):
            n = self.stack[i]
            cmd = self.op2func.get(n) if isinstance(n, str) else 0
            if cmd:
                self.stack.pop(i)
                stack_next = self.stack[i:]
                self.stack = self.stack[:i]
                to_stack = getattr(self, cmd)()
                self.stack += to_stack
                self.stack += stack_next
                i = 0
            else:
                i += 1
        if not self.has_out:
            to_out = repr(self.stack.pop(0)).replace("'", '"')
            sys.stdout.write(to_out + '\n')

    # Helper Functions

    def from_top(self, num_items=1):
        retval = [self.stack.pop() for i in range(num_items)]
        retval.reverse()
        if len(retval) == 1:
            return retval[0]
        return retval

    def is_length(self, length=1):
        if len(self.stack) < length:
            return False
        return True


class Standard(Base):
    
    validTypes = {"(": ")", "[": "]", "{": "}", '"': '"'}
    op2func = {
        "'": "full_input",
        "_": "line_input",
    }
    
    def __init__(self, program=""):
        """Initialize the parent class"""
        Base.__init__(self, program)

    def full_input(self):
        """Push the full input to the stack"""
        retval = '\n'.join(self.input)
        return [retval]

    def line_input(self):
        """Push the foremost line to the stack"""
        retval = self.input.pop(0)
        return [retval]