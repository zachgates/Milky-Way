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
            if _is(data[i], str):
                if data[i].isdigit():
                    data[i] = int(data[i])
        return opcodes, data

    def parse_type(self, stack, index):
        """Distinguish between opcodes and data types"""
        to_find = self.validTypes.get(stack[index])
        opener = stack[index]
        skip_from = int(index)
        stack_next = stack[index:][::-1][:-1]
        data = stack[index]
        opn, cls = 1, 0
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
            data = "Empty()"
            index = skip_from + 1
        return [range(skip_from, index + 1), eval(data)]

    def merge_stacks(self, opcodes, data):
        """Merge opcodes and data into a single stack"""
        retval = []
        for a, b in zip(opcodes, data):
            if _is(a, Empty) and _is(b, Empty):
                pass
            elif _is(a, Empty):
                retval.append(b)
            elif _is(b, Empty):
                retval.append(a)
            else:
                return []
        return retval

    def run_ops(self):
        """Evaluate the program"""
        i = 0
        while i < len(self.stack):
            n = self.stack[i]
            cmd = self.op2func.get(n) if _is(n, str) else 0
            if cmd:
                self.stack.pop(i)
                stack_next = self.stack[i:]
                self.stack = self.stack[:i]
                to_stack = getattr(self, cmd)()
                self.stack += to_stack if to_stack else []
                self.stack += stack_next
                i = 0
            else:
                i += 1

    # Helper Functions

    def from_top(self, N=1):
        """Pop N items from the stack"""
        retval = [self.stack.pop() for i in range(N)]
        retval.reverse()
        if len(retval) == 1:
            return retval[0]
        return retval

    def is_length(self, N=1):
        """Check if the stack has N or more items"""
        if len(self.stack) < length:
            return False
        return True


# Function Container


class Standard(Base):
    
    validTypes = {"(": ")", "[": "]", "{": "}", '"': '"'}
    op2func = {
        "'": "full_input",
        "_": "line_input",
        "!": "out_top",
        "#": "out_nth",
        ";": "swap_top",
        "<": "rot_left",
        "≤": "rot_left_nth",
        ">": "rot_right",
        "≥": "rot_right_nth",
        "^": "pop_top",
        "|": "pop_nth",
        ":": "dup_top",
    }
    
    def __init__(self, program=""):
        """Initialize parent class"""
        self.has_out = False
        Base.__init__(self, program)
        if not self.has_out:
            to_out = repr(self.stack.pop(0)).replace("'", '"')
            sys.stdout.write(to_out)
        sys.stdout.write('\n')

    # I/O Functions

    ## Input

    def full_input(self):
        """Push the full input to the stack: [a b] => [a b c]"""
        retval = '\n'.join(self.input)
        return [retval]

    def line_input(self):
        """Push the foremost line to the stack: [a b] => [a b c]"""
        retval = self.input.pop(0)
        return [retval]

    ## Output

    def out_top(self):
        """Output the TOS without pop-ing: [a b c] => [a b c]"""
        to_out = repr(self.stack[-1]).replace("'", '"')
        sys.stdout.write(to_out)
        self.has_out = True

    def out_nth(self):
        """Output the Nth stack item without pop-ing it where N is the TOS: [a b c 2] => [a b c]"""
        A = self.from_top()
        to_out = repr(self.stack[A]).replace("'", '"')
        sys.stdout.write(to_out)
        self.has_out = True

    # Stack-Modifying Functions

    ## Rotation

    def swap_top(self):
        """Swap the top two stack elements: [a b c] => [a c b]"""
        A, B = self.from_top(2)
        return [B, A]

    def rot_left(self):
        """Rotate the stack leftward: [a b c] => [b c a]"""
        new_stack = self.stack[1:] + self.stack[:1]
        self.stack = new_stack

    def rot_left_nth(self):
        """Rotate the top N stack elements leftward where N is the TOS: [a b c d 3] => [a c d b]"""
        N = self.from_top()
        if _is(N, int):
            sub_stack = self.from_top(N)
            if len(sub_stack) > 1:
                new_sub_stack = sub_stack[1:] + sub_stack[:1]
            elif len(sub_stack):
                new_sub_stack = sub_stack
            else:
                new_sub_stack = []
            return new_sub_stack

    def rot_right(self):
        """Rotate the stack rightward: [a b c] => [c a b]"""
        new_stack = self.stack[-1:] + self.stack[:-1]
        self.stack = new_stack

    def rot_right_nth(self):
        """Rotate the top N stack elements rightward where N is the TOS: [a b c d 3] => [a d b c]"""
        N = self.from_top()
        if _is(N, int):
            sub_stack = self.from_top(N)
            if len(sub_stack) > 1:
                new_sub_stack = sub_stack[-1:] + sub_stack[:-1]
            elif len(sub_stack):
                new_sub_stack = sub_stack
            else:
                new_sub_stack = []
            return new_sub_stack

    ## Removal

    def pop_top(self):
        """Pop the TOS without outputting it: [a b c] => [a b]"""
        self.stack.pop()

    def pop_nth(self):
        """Pop the Nth stack item without outputting it where N is the TOS: [a b 1] => [a]"""
        A = self.from_top()
        self.stack.pop(A)

    ## Amount Modifiers

    def dup_top(self):
        """Duplicate the TOS: [a b c] => [a b c c]"""
        A = self.from_top()
        return [A, A]
