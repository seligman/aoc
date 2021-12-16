#!/usr/bin/env python3

import math

class Program:
    def __init__(self, values, print_formula=False):
        self.print_formula = print_formula
        self.formula = []

        temp = bin(int(values[0], 16))[2:]
        temp = ("0" * (len(values[0]) * 4) + temp)[-len(values[0]) * 4:]

        self.value = temp
        self.version_sum = 0
        self.result = None

    def get_bits(self, len):
        ret = "".join(self.value[:len])
        self.value = self.value[len:]
        return ret

    def run(self):
        ver = int(self.get_bits(3), 2)
        self.version_sum += ver
        pid = int(self.get_bits(3), 2)

        operators = {
            0: {'open': "(", "join": "+", "end": ")", "func": lambda x: sum(x)},
            1: {'open': "(", "join": "*", "end": ")", "func": lambda x: math.prod(x)},
            2: {'open': "min(", "join": ",", "end": ")", "func": lambda x: min(x)},
            3: {'open': "max(", "join": ",", "end": ")", "func": lambda x: max(x)},
            5: {'open': "(1 if ", "join": ">", "end": " else 0)", "func": lambda x: 1 if x[0] > x[1] else 0},
            6: {'open': "(1 if ", "join": "<", "end": " else 0)", "func": lambda x: 1 if x[0] < x[1] else 0},
            7: {'open': "(1 if ", "join": "==", "end": " else 0)", "func": lambda x: 1 if x[0] == x[1] else 0},
        }

        if pid == 4:
            # Just get the value, 5 bits at a time
            val = ""
            while True:
                x = self.get_bits(5)
                val += x[1:]
                if x[0] == '0':
                    # Lack of a '1' continue bit
                    break
            val = int(val, 2)
            if self.print_formula:
                self.formula.append(str(val))
            return val
        else:
            # Determine how the length is encoded
            length = self.get_bits(1)
            stack = []
            operator_pos = []

            if self.print_formula:
                operator_pos.append(len(self.formula))
                self.formula.append(operators[pid]['open'])

            if length == '0':
                # This means it's encoded as a length number, 
                # so pull out that many bits, and recurse into them
                sub_len = int(self.get_bits(15), 2)
                new_value = self.get_bits(sub_len)
                old_value = self.value
                self.value = new_value

                while len(self.value) > 0:
                    if self.print_formula and len(stack) > 0:
                        operator_pos.append(len(self.formula))
                        self.formula.append(operators[pid]['join'])
                    stack.append(self.run())
                
                # Done with the recursion, so reset the state to whatever's
                # left over in the script
                self.value = old_value
            else:
                # This means it's encoded as a number of tokens
                # so recurse that many times, since each call
                # will parse one token
                sub_count = int(self.get_bits(11), 2)
                for _ in range(sub_count):
                    if self.print_formula and len(stack) > 0:
                        operator_pos.append(len(self.formula))
                        self.formula.append(operators[pid]['join'])
                    stack.append(self.run())

            if self.print_formula:
                operator_pos.append(len(self.formula))
                self.formula.append(operators[pid]['end'])

                if len(operator_pos) == 2:
                    operator_pos.sort(reverse=True)
                    for x in operator_pos:
                        self.formula.pop(x)

            self.result = operators[pid]['func'](stack)
            return self.result
