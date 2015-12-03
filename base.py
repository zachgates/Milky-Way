import sys
import getopt
import re
import synclist
import errors
import shorthand as sh
from debug import *


# Language Base


class Base(object):

    def __init__(self, program, pre_stack):
        """Initialize program"""
        self.p_stack = pre_stack
        if inputEnabled:
            opts, args = getopt.getopt(sys.argv[2:], ":i:")
            op = {opt: arg for opt, arg in opts}
            if op.get("-i"):
                self.input = op.get("-i").splitlines()
                try:
                    self.input = list(map(int, self.input))
                except:
                    pass
            else:
                self.input = []
        self.stack = self.tokenize(program)
        self.run_ops()

    def tokenize(self, program):
        """Separate functions from data in the stack"""
        temp_stack = list(program)
        skip = []
        stacks = synclist.ParallelLists("opcodes", "data")
        if self.p_stack:
            stacks.append(*self.p_stack, sl="data")
        else:
            stacks.append("", 0, sl="data")
        op, dt = "", ""
        for i in range(len(temp_stack)):
            j = temp_stack[i]
            if i not in skip:
                if j in self.op2func.keys():
                    if op:
                        stacks.append(op, sl="opcodes")
                        op = j
                    if dt:
                        stacks.append(dt, sl="data")
                        dt = ""
                    if self.op2func.get(j):
                        stacks.append(op + j, sl="opcodes")
                        op = ""
                elif j.isdigit():
                    if dt.isdigit():
                        dt += j
                    else:
                        if dt:
                            stacks.append(dt, sl="data")
                            op = ""
                        dt = j
                elif j in self.validTypes.keys():
                    if dt:
                        stacks.append(dt, sl="data")
                        dt = ""
                    rng, dat = self.parse_type(temp_stack, i)
                    skip += rng
                    stacks.append(dat, sl="data")
                    op = ""
                elif j in self.state_sig.keys():
                    if dt:
                        stacks.append(dt, sl="data")
                        dt = ""
                    rng, dat = self.parse_state(stacks.merge(), temp_stack, i)
                    skip += rng
                    stacks = dat
                    op = ""
                elif j == self.global_error:
                    raise errors.UnexpectedError()
                else:
                    raise errors.UnknownOpcode(self.global_error)
        if dt:
            stacks.append(dt, sl="data")
        stack = stacks.merge()
        for i in range(len(stack)):
            j = stack[i]
            if sh._is(j, str):
                if j.isdigit():
                    stack[i] = int(j)
        return stack

    def parse_state(self, c_stack, t_stack, index):
        """Handle the execution of loops and if-statements"""
        typ = self.state_sig.get(t_stack[index])
        skip_from = int(index)
        index += 1
        stack_next = t_stack[index:][::-1]
        opener = self.clause_sig[0]
        to_find = self.clause_sig[1]
        if stack_next.pop() != opener:
            return [range(skip_from, skip_from + len(stack_next)), synclist.Empty()]
        state = ""
        opn, cls = 1, 0
        while stack_next:
            index += 1
            n = stack_next.pop()
            if n == to_find:
                cls += 1
                if opn == cls:
                    stack_next = 1
                    break
            elif n == opener:
                opn += 1
            else:
                pass
            state += n
        eos = index + 1
        if typ == "if":
            if_else = state.split("_")
            data = c_stack
            if len(if_else) == 3:
                if self.spare(if_else[0], c_stack).stack[-1]:
                    mw = self.spare(if_else[1], c_stack)
                    data = mw.stack
                    has_out = mw.has_out
                else:
                    mw = self.spare(if_else[2], c_stack)
                    data = mw.stack
                    has_out = mw.has_out
                self.has_out = has_out
            retval = synclist.ParallelLists("opcodes", "data")
            retval.append(*data, sl="data")
            return [range(skip_from, eos), retval]
        elif typ == "while":
            loop = state.split("~")
            data = c_stack
            has_out = self.has_out
            if len(loop) == 1:
                while True:
                    mw = self.spare(loop[0], data)
                    data = mw.stack
                    has_out = mw.has_out or has_out
            elif len(loop) == 2:
                while data[-1]:
                    mw = self.spare(loop[1], data)
                    data = mw.stack
                    has_out = mw.has_out or has_out
            elif len(loop) == 3:
                while data[-1]:
                    mw = self.spare(loop[1], data)
                    data = mw.stack
                    has_out = mw.has_out or has_out
                mw = self.spare(loop[2], data)
                data = mw.stack
                has_out = has_out or mw.has_out
            self.has_out = has_out
            retval = synclist.ParallelLists("opcodes", "data")
            retval.append(*data, sl="data")
            return [range(skip_from, eos), retval]

    def parse_type(self, stack, index):
        """Distinguish between opcodes and data types"""
        to_find = self.validTypes.get(stack[index])
        opener = stack[index]
        skip_from = int(index)
        stack_next = stack[index:][:0:-1]
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
            data = "synclist.Empty()"
            index = skip_from + 1
        return [range(skip_from, index + 1), eval(data)]

    def run_ops(self):
        """Evaluate the program"""
        i = 0
        while i < len(self.stack):
            n = self.stack[i]
            cmd = self.op2func.get(n) if sh._is(n, str) else 0
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
        if len(self.stack) < N:
            return False
        return True
