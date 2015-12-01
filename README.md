# Milky Way
Milky Way is a stack-based programming language

# Usage

```
python3 milkyway.py test.mwg
```

All program files must end with `.mwg` to be valid.

# Input

Input is taken through the command line with the `-i` option.

```
python3 milkyway.py test.mwg -i "test"
```

# Commands

<table>
    <thead>
        <tr>
            <td><b>Opcode</td>
            <td>Description</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>;</td>
            <td>Swap the top two stack elements</td>
        </tr>
        <tr>
            <td><</td>
            <td>Rotate the stack leftward</td>
        </tr>
        <tr>
            <td>≤</td>
            <td>Rotate the top N stack elements leftward where N is the TOS</td>
        </tr>
        <tr>
            <td>></td>
            <td>Rotate the stack rightward</td>
        </tr>
        <tr>
            <td>≥</td>
            <td>Rotate the top N stack elements rightward where N is the TOS</td>
        </tr>
        <tr>
            <td>^</td>
            <td>Pop the TOS without outputting it</td>
        </tr>
        <tr>
            <td>|</td>
            <td>Pop the Nth stack item without outputting it where N is the TOS</td>
        </tr>
        <tr>
            <td>:</td>
            <td>Duplicate the TOS</td>
        </tr>
        <tr>
            <td>+</td>
            <td>Push the sum the top two stack elements to the stack</td>
        </tr>
        <tr>
            <td>-</td>
            <td>Push the difference of the top two stack elements to the stack</td>
        </tr>
        <tr>
            <td>*</td>
            <td>Push the product of the top two stack elements to the stack</td>
        </tr>
        <tr>
            <td>/</td>
            <td>Push the quotient of the top two stack elements to the stack</td>
        </tr>
        <tr>
            <td>a</td>
            <td>Perform logical not on the TOS</td>
        </tr>
        <tr>
            <td>b</td>
            <td>Perform logical equals on the top two stack elements</td>
        </tr>
        <tr>
            <td>c</td>
            <td>Perform logical and on the top two stack elements</td>
        </tr>
        <tr>
            <td>d</td>
            <td>Perform logical or on the top two stack elements</td>
        </tr>
        <tr>
            <td>e</td>
            <td>Perform logical greater than on the top two stack elements</td>
        </tr>
        <tr>
            <td>f</td>
            <td>Perform logical less than on the top two stack elements</td>
        </tr>
        <tr>
            <td>g</td>
            <td>Push the Nth root of the top stack element (default to 2) to the stack</td>
        </tr>
        <tr>
            <td>h</td>
            <td>Push the TOS to the power of second stack element to the stack</td>
        </tr>
        <tr>
            <td>i</td>
            <td>Push the primality of the TOS to the stack</td>
        </tr>
        <tr>
            <td>j</td>
            <td>Push the absolute value of the TOS to the stack</td>
        </tr>
        <tr>
            <td>k</td>
            <td>Push the negative absolute value of the TOS to the stack</td>
        </tr>
        <tr>
            <td>l</td>
            <td>Push 10 to the Nth power to the stack</td>
        </tr>
        <tr>
            <td>m</td>
            <td>Push A/B and A%B to the stack where A and B are the top two stack elements</td>
        </tr>
        <tr>
            <td>n</td>
            <td>Push A%B to the stack where A and B are the top two stack elements</td>
        </tr>
        <tr>
            <td>o</td>
            <td>Push the sine of the TOS to the stack</td>
        </tr>
        <tr>
            <td>p</td>
            <td>Push the cosine of the TOS to the stack</td>
        </tr>
        <tr>
            <td>q</td>
            <td>Push the tangent of the TOS to the stack</td>
        </tr>
        <tr>
            <td>r</td>
            <td>Push the inverse sine of the TOS to the stack</td>
        </tr>
        <tr>
            <td>s</td>
            <td>Push the inverse cosine of the TOS to the stack</td>
        </tr>
        <tr>
            <td>t</td>
            <td>Push the inverse tangent of the TOS to the stack</td>
        </tr>
        <tr>
            <td>u</td>
            <td>Push the rounded TOS to the stack</td>
        </tr>
        <tr>
            <td>v</td>
            <td>Push the floor of the TOS to the stack</td>
        </tr>
        <tr>
            <td>w</td>
            <td>Push the ceiling of the TOS to the stack</td>
        </tr>
        <tr>
            <td>x</td>
            <td>Push A rounded to the nearest multiple of B to the stack</td>
        </tr>
    </tbody>
</table>

# If-Else Statements

An `if` statement is signified by the `?` operator followed by a set of braces.

```
?{}
```

The conditional and code blocks are separated by `~`.

```
?{1~1~0}
```

The above statement is equivalent to the following Python code, where the literals in each block are analogous with pushing to the stack.

```python
if 1:
	1
else:
	0
```

`if` statements can have empty blocks, as shown below. The following code does nothing.

```
?{1~~}
```

They can also have empty conditionals. In this case, the truth of the TOS is evaluated as the conditional.

```
?{~1~0}
```