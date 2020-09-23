import re

r1 = re.compile('<span class="calendar-color-(.)">')
r2 = re.compile('</span>')
decoded = "#r"
with open("test.html") as f:
    for cur in f:
        if not cur.startswith('<!--'):
            while cur.endswith("\n") or cur.endswith(" "):
                cur = cur[:-1]
            cur = r1.sub("#\\1", cur)
            cur = r2.sub("", cur)
            decoded += cur + "\n"

last_color = ""
is_color = False
simplified = ""
for cur in decoded:
    if is_color:
        if last_color != cur:
            last_color = cur
            simplified += "#" + cur
        is_color = False
    else:
        if cur == "#":
            is_color = True
        else:
            simplified += cur
while simplified[-1] == " " or simplified[-1] == "\n":
    simplified = simplified[:-1]
simplified += "\n"

codes = []
max_num = 0
for cur in simplified:
    if is_color:
        codes[-1].append(cur)
        codes.append(["text"])
        is_color = False
    else:
        if cur == "#":
            codes.append(["color"])
            is_color = True
        else:
            code = ord(cur)
            if code == 10:
                code = 0
            else:
                code = code - 32 + 1
            codes[-1].append(code)
            max_num = max(max_num, code)

codes2 = []
last_dig = 0

for i in range(len(codes)):
    if codes[i][0] == "text":
        for cur in codes[i][1:]:
            codes2.append(cur - last_dig)
            last_dig = cur
    else:
        colors = {
            "r": "91",
            "d": "31",
            "y": "93",
            "g": "92",
            "w": "97",
            "a": "90",
        }
        codes2.append(100)
        codes2.append(ord(colors[codes[i][1]][0]))
        codes2.append(ord(colors[codes[i][1]][1]))

def chunks(values, size):
    for i in range(0, len(values), size):
        yield values[i:i + size]



i = 0
while i < len(codes2):
    if codes2[i] == 0 and codes2[i+1] == 0:
        count = 0
        while codes2[i+1] == 0:
            codes2 = codes2[:i+1] + codes2[i+2:]
            count += 1
        codes2[i] = 100 + count
    i += 1

codes2.append(99)


for cur in chunks(codes2, 26):
    print(",".join(map(str, cur)) + ",")

i = -1
val = 0
output = ""
while True:

    i += 1
    if codes2[i] == 99:
        break
    if codes2[i] == 100:
        i += 2
        # READ COLOR
        #output += chr(codes2[i])
        continue
    if codes2[i] > 100:
        while codes2[i] >= 100:
            output += chr(val+31)
            codes2[i] -= 1
        continue
    val += codes2[i]
    if val == 0:
        output += "\n"
    else:
        output += chr(val+31)

print(output)

# print(max_num)

# for cur in codes:
#     if cur[0] == "text":
#         digs, value = cur[1:]
#         digs
#         for _ in range(digs-1):
#         while digs > 0:
#             value