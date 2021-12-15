import sys
inf = sys.argv[1] if len(sys.argv) > 1 else 'input'

ll = [[int(y) for y in x] for x in open(inf).read().strip().split('\n')]

def inr(pos, arr):
    return pos[0] in range(len(arr)) and pos[1] in range(len(arr[0]))

expanded = [[0 for x in range(5*len(ll[0]))] for y in range(5*len(ll))]

for x in range(len(expanded)):
    for y in range(len(expanded[0])):
        dist = x//len(ll) + y//len(ll[0])
        newval = ll[x%len(ll)][y%len(ll[0])]
        for i in range(dist):
            newval+=1
            if newval==10:
                newval=1
        expanded[x][y] = newval

ll = expanded

q = [(0, 0, 0)]
costs = {}
while True:
    cost,x,y = q[0]
    if x==len(ll)-1 and y==len(ll[0])-1: 
        print(cost)
        break
    q=q[1:]
    for xx,yy in [(x+1,y),(x,y+1)]:
        if inr((xx,yy),ll):
            nc = cost + ll[xx][yy]
            if (xx,yy) in costs and costs[(xx,yy)]<=nc:
                continue
            costs[(xx,yy)]=nc
            q.append((nc,xx,yy))
    q = sorted(q)