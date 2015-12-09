import math
import sys
import time
import base
import shorthand as sh
from debug import *


# Function Container


class Standard(base.Base):
    
    comment = "`"
    clause_sig = "{}"
    state_sig = {
        "?": "if",
        "%": "for",
        "&": "while",
        "§": "map",
    }
    state_splitter = {
        "if": "_",
        "for": "£",
        "while": "~",
    }
    validTypes = {
        "(": ")",
        "[": "]",
        '"': '"',
    }
    global_error = "z"
    specVals = {}
    op2func = {
        ";": "swap_top",
        "<": "rot_left",
        "≤": "rot_left_nth",
        ">": "rot_right",
        "≥": "rot_right_nth",
        "^": "pop_top",
        "|": "pop_nth",
        ":": "dup_top",
        "+": "add",
        "-": "subtract",
        "*": "multiply",
        "/": "divide",
        "a": "log_not",
        "b": "log_eqs",
        "c": "log_and",
        "d": "log_or",
        "e": "log_gthan",
        "f": "log_lthan",
        "g": "root",
        "h": "power",
        "i": "prime",
        "j": "absval",
        "k": "negabsval",
        "l": "scinot",
        "m": "dmod",
        "n": "modulo",
        "o": "sin",
        "p": "cos",
        "q": "tan",
        "r": "arcsin",
        "s": "arccos",
        "t": "arctan",
        "u": "round_to",
        "v": "roundf",
        "w": "roundc",
        "x": "nearest",
        "y": "length",
        "\\": "split",
        "=": "dump",
        "@": "terminate",
        "Ω": "cast_lst",
        "ß": "cast_tup",
        "A": "to_int",
        "B": "to_str",
        "C": "to_lst",
        "D": "to_tup",
        "E": "primes",
        "F": "expand",
        "G": "sum",
        "H": "reverse",
        "I": "empty",
        "J": "collect",
        "K": "range_ex",
        "L": "range_in",
        "M": "time",
        "R": "one",
        "S": "two",
        "T": "three",
        "U": "four",
        "V": "five",
        "W": "ten",
        "X": "twenty",
        "Y": "fifty",
        "Z": "hundred",
    }
    
    if inputEnabled:
        inputFuncs = {
            "'": "full_input",
            "_": "line_input",
        }
        op2func.update(inputFuncs)
    
    if outputEnabled:
        outputFuncs = {
            "!": "out_top",
            "#": "out_nth",
            "¡": "tma_wout",
        }
        op2func.update(outputFuncs)

    def __init__(self, program, pre_stack, specVals={}):
        """Initialize parent class"""
        if outputEnabled:
            self.has_out = False
        self.specVals.update(specVals)
        base.Base.__init__(self, program, pre_stack)

    # I/O Functions

    ## Input

    if inputEnabled:
    
        def full_input(self):
            """Push the full input to the stack: [a b] => [a b c]"""
            if len(self.input) == 1:
                retval = self.input[0]
            else:
                retval = '\n'.join(self.input)
            return [retval]
        
        def line_input(self):
            """Push the foremost line to the stack: [a b] => [a b c]"""
            retval = self.input.pop(0)
            return [retval]
    
    ## Output
    
    if outputEnabled:
        
        def out_top(self):
            """Output the TOS without pop-ing: [a b c] => [a b c]"""
            if not verboseStack:
                to_out = repr(self.stack[-1]).replace("'", '"')
                if sh._is(self.stack[-1], str):
                    to_out = self.stack[-1]
                sys.stdout.write(to_out)
                sys.stdout.write("\n")
                self.has_out = True
        
        def out_nth(self):
            """Output the Nth stack item without pop-ing it where N is the TOS: [a b c 2] => [a b c]"""
            if not verboseStack:
                A = self.from_top()
                to_out = repr(self.stack[A]).replace("'", '"')
                sys.stdout.write(to_out)
                sys.stdout.write("\n")
                self.has_out = True

        def tma_wout(self):
            """Output the TOS and terminate the program"""
            self.out_top()
            exit()
    
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
        if sh._is(N, int):
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
        if sh._is(N, int):
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
        """Pop the Nth stack item without outputting it where N is the TOS: [a b c 1] => [a c]"""
        A = self.from_top()
        self.stack.pop(A)

    ## Amount Modifiers

    def dup_top(self):
        """Duplicate the TOS: [a b c] => [a b c c]"""
        A = self.from_top()
        return [A, A]
    
    # Logical Functions
    
    def log_not(self):
        """Perform logical not on the TOS: [0 0 1] => [0 0 0]"""
        A = self.from_top()
        retval = int(not bool(A))
        return [retval]
    
    def log_eqs(self):
        """Perform logical equals on the top two stack elements: [a a] => [1]"""
        A, B = self.from_top(2)
        retval = int(A == B)
        return [retval]
    
    def log_and(self):
        """Perform logical and on the top two stack elements: [0 1] => [0]"""
        A, B = self.from_top(2)
        retval = int(bool(A) and bool(B))
        return [retval]
    
    def log_or(self):
        """Perform logical or on the top two stack elements: [0 1] => [1]"""
        A, B = self.from_top(2)
        retval = int(bool(A) or bool(B))
        return [retval]
    
    def log_gthan(self):
        """Perform logical greater than on the top two stack elements: [1 2] => [0]"""
        A, B = self.from_top(2)
        retval = int(A > B)
        return [retval]
    
    def log_lthan(self):
        """Perform logical less than on the top two stack elements: [1 2] => [1]"""
        A, B = self.from_top(2)
        retval = int(A < B)
        return [retval]
    
    # Arithmetic Functions
    
    def add(self):
        """Push the sum the top two stack elements to the stack: [1 2] => [3]"""
        if self.is_length(2):
            A, B = self.from_top(2)
        else:
            return []
        if type(A) == type(B):
            retval = A + B
        elif sh._either(A, B, str):
            retval = str(A) + str(B)
        elif sh._either(A, B, int):
            retval = round(A + B)
        elif sh._either(A, B, list):
            retval = list(A) + list(B)
        elif sh._both(A, B, tuple):
            retval = tuple(list(A) + list(B))
        else:
            return []
        return [retval]
    
    def subtract(self):
        """Push the difference of the top two stack elements to the stack: [5 2] => [3]"""
        if self.is_length(2):
            A, B = self.from_top(2)
        else:
            return []
        if sh._both(A, B, int):
            retval = round(A - B)
        elif sh._either(A, B, float):
            retval = A - B
        elif sh._either(A, B, list):
            A = list(A)
            for i in B:
                while i in A:
                    A.remove(i)
            retval = A
        elif sh._both(A, B, tuple):
            A = list(A)
            for i in B:
                while i in A:
                    A.remove(i)
            retval = tuple(A)
        else:
            return []
        return [retval]
    
    def multiply(self):
        """Push the product of the top two stack elements to the stack: [5 5] => [25]"""
        if self.is_length(2):
            A, B = self.from_top(2)
        else:
            return []
        if sh._is(A, str) and sh._is(B, int):
            retval = A * B
        elif sh._both(A, B, int):
            retval = round(A * B)
        elif sh._either(A, B, float):
            retval = A * B
        else:
            return []
        return [retval]
    
    def divide(self):
        """Push the quotient of the top two stack elements to the stack: [25 5] => [5]"""
        if self.is_length(2):
            A, B = self.from_top(2)
        else:
            return []
        if sh._both(A, B, str):
            retval = A.count(B)
        elif sh._of([A, B], [int, float]):
            retval = A / B
        elif sh._is(A, list) or sh._is(A, tuple):
            retval = int(B in A)
        else:
            return []
        return [retval]
    
    # Loose Integer Functions
    
    def root(self):
        """Push the Nth root of the top stack element (default to 2) to the stack: [25] => [5]"""
        retval = []
        if self.is_length(2):
            A, B = self.from_top(2)
            if not sh._is(A, int) or not A:
                retval.append(A)
                A = 2
        else:
            A = 2
            B = self.from_top()
        k = 1 / A
        if sh._is(B, int):
            retval.append(round(B ** k))
        else:
            retval.append(B ** k)
        return retval
    
    def power(self):
        """Push the TOS to the power of second stack element to the stack: [3 3] => [27]"""
        if self.is_length(2):
            A, B = self.from_top(2)
        else:
            return []
        if sh._of([A, B], [int, float]):
            retval = A ** B
        else:
            return []
        return [retval]
    
    def prime(self):
        """Push the primality of the TOS to the stack: [9] => [0]"""
        A = self.from_top()
        if sh._is(A, int):
            i = int(A) - 1
            while i > 1:
                if A % i == 0:
                    return [0]
                i -= 1
            return [1]
        else:
            return []

    def absval(self):
        """Push the absolute value of the TOS to the stack: [-3] => [3]"""
        A = self.from_top()
        if sh._of([A], [int, float]):
            retval = abs(A)
        else:
            return []
        return [retval]

    def negabsval(self):
        """Push the negative absolute value of the TOS to the stack: [3] => [-3]"""
        A = self.from_top()
        if sh._of([A], [int, float]):
            retval = -abs(A)
        else:
            return []
        return [retval]

    def scinot(self):
        """Push 10 to the Nth power to the stack: [5] => [100000]"""
        A = self.from_top()
        if sh._of([A], [int, float]):
            retval = 10 ** A
        else:
            return []
        return [retval]

    # Strict Integer Functions

    def dmod(self):
        """Push A/B and A%B to the stack where A and B are the top two stack elements: [10 5] => [2 0]"""
        if self.is_length(2):
            A, B = self.from_top(2)
        else:
            return []
        if sh._both(A, B, int):
            retval = list(divmod(A, B))
        else:
            retval = []
        return retval

    def modulo(self):
        """Push A%B to the stack where A and B are the top two stack elements: [12 5] => [2]"""
        if self.is_length(2):
            A, B = self.from_top(2)
        else:
            return []
        if sh._both(A, B, int):
            retval = A % B
        else:
            return []
        return [retval]

    # Strict Float Functions

    def sin(self):
        """Push the sine of the TOS to the stack: [90] => [0.8939966636005579]"""
        A = self.from_top()
        if sh._of([A], [int, float]):
            retval = math.sin(A)
        else:
            return []
        return [retval]

    def cos(self):
        """Push the cosine of the TOS to the stack: [90] => [-0.4480736161291701]"""
        A = self.from_top()
        if sh._of([A], [int, float]):
            retval = math.cos(A)
        else:
            return []
        return [retval]

    def tan(self):
        """Push the tangent of the TOS to the stack: [90] => [-1.995200412208242]"""
        A = self.from_top()
        if sh._of([A], [int, float]):
            retval = math.tan(A)
        else:
            return []
        return [retval]

    def arcsin(self):
        """Push the inverse sine of the TOS to the stack: [0.5] => [0.5235987755982988]"""
        A = self.from_top()
        if sh._of([A], [int, float]):
            retval = math.asin(A)
        else:
            return []
        return [retval]

    def arccos(self):
        """Push the inverse cosine of the TOS to the stack: [0.5] => [1.0471975511965976]"""
        A = self.from_top()
        if sh._of([A], [int, float]):
            retval = math.acos(A)
        else:
            return []
        return [retval]

    def arctan(self):
        """Push the inverse tangent of the TOS to the stack: [0.5] => [0.46364760900080615]"""
        A = self.from_top()
        if sh._of([A], [int, float]):
            retval = math.atan(A)
        else:
            return []
        return [retval]

    # Rounding Functions

    def round_to(self):
        """Push the rounded TOS to the stack: [3.8] => [4]"""
        A = self.from_top()
        if sh._is(A, int):
            retval = round(A)
        else:
            return []
        return [retval]

    def roundf(self):
        """Push the floor of the TOS to the stack: [3.8] => [3]"""
        A = self.from_top()
        if sh._of([A], [int, float]):
            retval = math.floor(A)
        else:
            return []
        return [retval]

    def roundc(self):
        """Push the ceiling of the TOS to the stack: [3.8] => [4]"""
        A = self.from_top()
        if sh._of([A], [int, float]):
            retval = math.ceil(A)
        else:
            return []
        return [retval]

    def nearest(self):
        """Push A rounded to the nearest multiple of B to the stack: [10 12] => [12]"""
        if self.is_length(2):
            A, B = self.from_top(2)
        else:
            return []
        if sh._of([A, B], [int, float]):
            retval = int(B * round(A / B))
        else:
            return []
        return [retval]

    # Assorted Functions

    def length(self):
        """Push the length of the TOS to the stack: [[1, 2, 3]] => [3]"""
        A = self.from_top()
        if sh._of([A], [str, list, tuple]):
            retval = len(A)
        else:
            return []
        return [retval]

    def split(self):
        """Split A at B where A and B are the top two stack elements: [abc b] => [[a c]]"""
        if self.is_length(2):
            A, B = self.from_top(2)
        else:
            return []
        retval = []
        if sh._both(A, B, str):
            retval.append(A.split(B))
        elif sh._of([A], [list, tuple]):
            ist = False
            if sh._is(A, tuple):
                ist = True
                A = list(A)
            acc, bcc = [], []
            for i in A:
                if i == B:
                    if ist:
                        bcc = tuple(bcc)
                    acc.append(bcc)
                    bcc = []
                else:
                    bcc.append(i)
            if ist:
                bcc = tuple(bcc)
            acc.append(bcc)
            retval.append(acc)
        else:
            return []
        return retval

    def dump(self):
        """Dump the TOS to the stack: [1 2 [3 4 5]] => [1 2 3 4 5]"""
        A = self.from_top()
        if sh._of([A], [str, list, tuple]):
            retval = []
            for i in A:
                retval.append(i)
        else:
            retval = [A]
        return retval

    def terminate(self):
        """Terminate the program"""
        exit()

    def cast_lst(self):
        """Push a list of the top N stack elements: [1 2 3 3] => [[1 2 3]]"""
        A = self.from_top()
        if sh._is(A, int):
            if self.is_length(A):
                retval = self.from_top(A)
            else:
                retval = A
        else:
            retval = A
        return [retval]

    def cast_tup(self):
        """Push a tuple of the top N stack elements: [1 2 3 3] => [(1 2 3)]"""
        A = self.from_top()
        if sh._is(A, int):
            if self.is_length(A):
                retval = tuple(self.from_top(A))
            else:
                retval = A
        else:
            retval = A
        return [retval]

    def to_int(self):
        """Push the integer representation of the TOS to the stack: ['2'] => [2]"""
        A = self.from_top()
        if sh._is(A, str):
            try: retval = int(A)
            except: pass
        elif sh._is(A, int):
            retval = A
        elif sh._of([A], [list, tuple]):
            if all(sh._is(i, int) for i in A):
                retval = sum(A)
            else:
                retval = A
        else:
            return []
        return [retval]

    def to_str(self):
        """Push the string representation of the TOS to the stack: [2] => ['2']"""
        A = self.from_top()
        if sh._of([A], [list, tuple]):
            retval = str(A)[1:-1]
        else:
            retval = str(A)
        return [retval]

    def to_lst(self):
        """Push the list representation of the TOS to the stack: ['123'] => ['1' '2' '3']"""
        A = self.from_top()
        if sh._is(A, str):
            retval = [i for i in A]
        elif sh._is(A, int):
            retval = [A]
        else:
            retval = list(A)
        return [retval]

    def to_tup(self):
        """Push the tuple representation of the TOS to the stack: [[1 2 3]] => [(1 2 3)]"""
        A = self.to_lst()
        retval = tuple(*A)
        return [retval]

    def primes(self):
        """Push the first N primes to the stack as a list: [3] => [[2 3 5]]"""
        A = self.from_top()
        retval = sh._nprimes(A)
        return [retval]

    def expand(self):
        """Push the sum of elements A+B, B+C, C+D, etc. from the TOS: [[1 2 3 4] => [[3 5 7]]"""
        A = self.from_top()
        retval = []
        if sh._of([A], [list, tuple]):
            for i in range(len(A)-1):
                retval.append([A[i], A[i+1]])
        else:
            return []
        return [retval]

    def sum(self):
        """Push the sum of the TOS: [[1 2 3]] => [6]"""
        A = self.from_top()
        if sh._is(A, list):
            if all(sh._is(i, list) for i in A):
                retval = sum(A, [])
            elif all(sh._is(i, int) for i in A):
                retval = sum(A)
            elif any(sh._is(i, str) for i in A):
                retval = "".join(str(i) for i in A)
            else:
                return []
        else:
            return []
        return [retval]

    def reverse(self):
        """Push the reversed TOS: [[1 2 3]] => [[3 2 1]]"""
        A = self.from_top()
        if sh._of([A], [list, tuple]):
            retval = list(A)
            retval.reverse()
            if sh._is(A, tuple):
                retval = tuple(retval)
        else:
            return []
        return [retval]

    def empty(self):
        """Empty the stack: [1 2 3] => []"""
        self.stack = []

    def collect(self):
        """Push the stack to a list: [1 2 3 4] => [[1 2 3 4]]"""
        retval = [i for i in self.stack]
        self.empty()
        return retval

    def range_ex(self):
        """Push a range of the TOS as a list (exclusive): [5] => [[0 1 2 3 4]]"""
        A = self.from_top()
        if sh._is(A, int):
            retval = list(range(A))
        else:
            return []
        return [retval]

    def range_in(self):
        """Push a range of the TOS as a list (inclusive): [5] => [[0 1 2 3 4 5]]"""
        A = self.from_top()
        if sh._is(A, int):
            retval = list(range(A))
            retval.append(A)
        else:
            return []
        return [retval]
        
    def time(self):
    	"""Push the current time string: [] => ["Wed Dec  9 08:51:59 2015"]"""
    	retval = time.asctime()
    	return [retval]

    def one(self):
        """Push 1 to the stack: [] => [1]"""
        return [1]

    def two(self):
        """Push 2 to the stack: [] => [2]"""
        return [2]

    def three(self):
        """Push 3 to the stack: [] => [3]"""
        return [3]

    def four(self):
        """Push 4 to the stack: [] => [4]"""
        return [4]

    def five(self):
        """Push 5 to the stack: [] => [5]"""
        return [5]

    def ten(self):
        """Push 10 to the stack: [] => [10]"""
        return [10]

    def twenty(self):
        """Push 20 to the stack: [] => [20]"""
        return [20]

    def fifty(self):
        """Push 50 to the stack: [] => [50]"""
        return [50]

    def hundred(self):
        """Push 100 to the stack: [] => [100]"""
        return [100]
