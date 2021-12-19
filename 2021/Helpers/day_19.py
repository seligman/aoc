#!/usr/bin/env python3

from multiprocessing import Pool

def get_desc():
    return 19, 'Day 19: Beacon Scanner'

def rotations():
    return [
        (-1, 0, -1, 1, +1, 2),
        (-1, 0, -1, 2, -1, 1),
        (-1, 0, +1, 1, -1, 2),
        (-1, 0, +1, 2, +1, 1),
        (-1, 1, -1, 0, -1, 2),
        (-1, 1, -1, 2, +1, 0),
        (-1, 1, +1, 0, +1, 2),
        (-1, 1, +1, 2, -1, 0),
        (-1, 2, -1, 0, +1, 1),
        (-1, 2, -1, 1, -1, 0),
        (-1, 2, +1, 0, -1, 1),
        (-1, 2, +1, 1, +1, 0),
        (+1, 0, -1, 1, -1, 2),
        (+1, 0, -1, 2, +1, 1),
        (+1, 0, +1, 1, +1, 2),
        (+1, 0, +1, 2, -1, 1),
        (+1, 1, -1, 0, +1, 2),
        (+1, 1, -1, 2, -1, 0),
        (+1, 1, +1, 0, -1, 2),
        (+1, 1, +1, 2, +1, 0),
        (+1, 2, -1, 0, -1, 1),
        (+1, 2, -1, 1, +1, 0),
        (+1, 2, +1, 0, +1, 1),
        (+1, 2, +1, 1, -1, 0),
    ]

def rotate(xyz, val):
    return (
        xyz[val[1]] * val[0],
        xyz[val[3]] * val[2],
        xyz[val[5]] * val[4],
    )


def find_overlap(job):
    i, a, b = job
    for b_rotated in b:
        done = set()
        for x, y, z in a:
            for tx, ty, tz in b_rotated:
                tx, ty, tz = x - tx, y - ty, z - tz
                if (tx, ty, tz) not in done:
                    done.add((tx, ty, tz))
                    offset = set((bx + tx, by + ty, bz + tz) for bx, by, bz in b_rotated)
                    found = len(offset & a)
                    if found >= 12:
                        return i, offset, (tx, ty, tz)
    return None, None, None

def calc(log, values, mode):
    grids = []
    for cur in values:
        if len(cur) > 0:
            if cur.startswith("--"):
                grids.append(set())
            else:
                grids[-1].add(tuple(int(x) for x in cur.split(",")))

    dest = grids.pop(0)
    offsets = []

    for i in range(len(grids)):
        grids[i] = [[rotate(y, x) for y in grids[i]] for x in rotations()]

    with Pool() as pool:
        while len(grids) > 0:
            to_remove = []
            temp = set(dest)
            for i, fixed, offset in pool.imap(find_overlap, [[i, dest, x] for i, x in enumerate(grids)]):
                if i is not None:
                    temp |= fixed
                    to_remove.append(i)
                    log(f"Found: {len(temp)}, {len(grids) - len(to_remove)} left")
                    offsets.append(offset)
            grids = [x for i, x in enumerate(grids) if i not in to_remove]
            dest = temp

    max_dist = 0
    for a in offsets:
        for b in offsets:
            dist = abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
            if dist > max_dist:
                max_dist = dist

    return len(dest), max_dist

def test(log):
    values = log.decode_values("""
        --- scanner 0 ---
        404,-588,-901
        528,-643,409
        -838,591,734
        390,-675,-793
        -537,-823,-458
        -485,-357,347
        -345,-311,381
        -661,-816,-575
        -876,649,763
        -618,-824,-621
        553,345,-567
        474,580,667
        -447,-329,318
        -584,868,-557
        544,-627,-890
        564,392,-477
        455,729,728
        -892,524,684
        -689,845,-530
        423,-701,434
        7,-33,-71
        630,319,-379
        443,580,662
        -789,900,-551
        459,-707,401

        --- scanner 1 ---
        686,422,578
        605,423,415
        515,917,-361
        -336,658,858
        95,138,22
        -476,619,847
        -340,-569,-846
        567,-361,727
        -460,603,-452
        669,-402,600
        729,430,532
        -500,-761,534
        -322,571,750
        -466,-666,-811
        -429,-592,574
        -355,545,-477
        703,-491,-529
        -328,-685,520
        413,935,-424
        -391,539,-444
        586,-435,557
        -364,-763,-893
        807,-499,-711
        755,-354,-619
        553,889,-390

        --- scanner 2 ---
        649,640,665
        682,-795,504
        -784,533,-524
        -644,584,-595
        -588,-843,648
        -30,6,44
        -674,560,763
        500,723,-460
        609,671,-379
        -555,-800,653
        -675,-892,-343
        697,-426,-610
        578,704,681
        493,664,-388
        -671,-858,530
        -667,343,800
        571,-461,-707
        -138,-166,112
        -889,563,-600
        646,-828,498
        640,759,510
        -630,509,768
        -681,-892,-333
        673,-379,-804
        -742,-814,-386
        577,-820,562

        --- scanner 3 ---
        -589,542,597
        605,-692,669
        -500,565,-823
        -660,373,557
        -458,-679,-417
        -488,449,543
        -626,468,-788
        338,-750,-386
        528,-832,-391
        562,-778,733
        -938,-730,414
        543,643,-506
        -524,371,-870
        407,773,750
        -104,29,83
        378,-903,-323
        -778,-728,485
        426,699,580
        -438,-605,-362
        -469,-447,-387
        509,732,623
        647,635,-688
        -868,-804,481
        614,-800,639
        595,780,-596

        --- scanner 4 ---
        727,592,562
        -293,-554,779
        441,611,-461
        -714,465,-776
        -743,427,-804
        -660,-479,-426
        832,-632,460
        927,-485,-438
        408,393,-506
        466,436,-512
        110,16,151
        -258,-428,682
        -393,719,612
        -211,-452,876
        808,-476,-593
        -575,615,604
        -485,667,467
        -680,325,-822
        -627,-443,-432
        872,-547,-609
        833,512,582
        807,604,487
        839,-516,451
        891,-625,532
        -652,-548,-490
        30,-46,-14
    """)

    points, dist = calc(log, values, 1)
    log.test(points, 79)
    log.test(dist, 3621)

def run(log, values):
    points, dist = calc(log, values, 1)
    log(points)
    log(dist)