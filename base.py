import sys
import getopt


global inputEnabled
inputEnabled = True


class Empty(object):
    pass


class Base(object):

    validTypes = {"(": ")", "[": "]", "{": "}", '"': '"'}
    op2func = {
        "'": "full_input",
        "_": "line_input",
    }

    def __init__(self, program=""):
        self.stack = list(program)
        if inputEnabled:
            opts, args = getopt.getopt(sys.argv[1:], "i:")
            op = {opt: arg for opt, arg in opts}
            if op.get("-i"):
                self.input = op.get("-i").splitlines()
            else:
                self.input = []
        opcodes, data = self.tokenize()
        self.stack = self.merge_stack(opcodes, data)
        self.run_ops()

    def tokenize(self):
        temp_stack = self.stack[:]
        skip = []
        opcodes, data = [Empty(), Empty()], ["", 0]
        c_op, c_dt = "", ""
        for i in range(len(temp_stack)):
            if i not in skip:
                if temp_stack[i] in Base.op2func.keys():
                    if c_op:
                        opcodes.append(c_op)
                        data.append(Empty())
                        c_op = temp_stack[i]
                    if c_dt:
                        opcodes.append(Empty())
                        data.append(c_dt)
                        c_dt = ""
                    if Base.op2func.get(temp_stack[i]):
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
                elif temp_stack[i] in Base.validTypes.keys():
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
        to_find = Base.validTypes.get(stack[index])
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

    def merge_stack(self, opcodes, data):
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
        i = 0
        while i < len(self.stack):
            n = self.stack[i]
            cmd = Base.op2func.get(n) if isinstance(n, str) else 0
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

    def full_input(self):
        retval = '\n'.join(self.input)
        return [retval]

    def line_input(self):
        retval = self.input.pop(0)
        return [retval]