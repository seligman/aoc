#!/usr/bin/env python3

import sys

def main():
    if len(sys.argv) != 3:
        print("Need input and output filenames")
        return

    lines = []
    labels = {}
    consts = {}
    inifdef = [True]
    with open(sys.argv[1]) as f:
        for l in f:
            l = l.strip()
            if l == "#if TRUE":
                inifdef.append(True)
            elif l == "#if FALSE":
                inifdef.append(False)
            elif l == "#endif":
                inifdef.pop(-1)
            else:
                if inifdef[-1]:
                    if l.startswith("CONST:"):
                        l = l[6:].split("=")
                        consts[l[0]] = eval(l[1], consts.copy(), {})
                    elif not l.startswith("#") and len(l) > 0:
                        l = l.split(",")
                        for x in l:
                            x = x.strip()

                            if ":" in x:
                                x = x.split(":")
                                labels[x[0]] = len(lines)
                                if len(x) > 1:
                                    x = x[1]
                                else:
                                    x = ""
                            
                            if len(x) > 0:
                                if x in consts:
                                    x = str(consts[x])
                                lines.append(x)

    for i in range(len(lines)):
        if lines[i] in labels:
            lines[i] = labels[lines[i]]
        else:
            op = 0
            ops = {
                "add": 1,
                "mult": 2,
                "output": 4,
                "jump_if_true": 5,
                "jump_if_false": 6,
                "less_than": 7,
                "equals": 8,
                "debug": 90,
                "terminate": 99,
            }
            is_op = False
            for key in ops:
                if lines[i].startswith(key):
                    is_op = True
                    op = ops[key]
                    lines[i] = lines[i][len(key):]
                    break

            if is_op:
                extra = 100
                while len(lines[i]) > 0:
                    if lines[i].startswith("_po"):
                        pass
                    elif lines[i].startswith("_im"):
                        op += extra
                    else:
                        raise Exception(lines[i])
                    lines[i] = lines[i][3:]
                    extra *= 10
                lines[i] = op
            else:
                lines[i] = int(lines[i])

    while lines[-1] == 0:
        lines.pop(-1)

    with open(sys.argv[2], "w") as f:
        f.write(",".join(map(str, lines)))

    return lines


if __name__ == "__main__":
    main()
