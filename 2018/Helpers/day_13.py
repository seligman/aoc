#!/usr/bin/env python3

DAY_NUM = 13
DAY_DESC = 'Day 13: Mine Cart Madness'


class Car:
    def __init__(self, x, y, train_dir):
        self.x = x
        self.y = y
        self.dir = train_dir
        self.choice = 0
        self.remove = False


def calc(log, values, test_mode):
    trains = {
        "<": "-",
        ">": "-",
        "^": "|",
        "v": "|",
    }

    cars = {}

    for y in range(len(values)):
        values[y] = list(values[y])
        for x in range(len(values[y])):
            if values[y][x] in trains:
                car = Car(x, y, values[y][x])
                values[y][x] = trains[car.dir]
                cars[(car.x, car.y)] = car

    while True:
        todo = list(cars.values())
        todo.sort(key=lambda x:(x.y, x.x))

        for car in todo:
            if not car.remove:
                del cars[(car.x, car.y)]
                if car.dir == "<":
                    car.x -= 1
                if car.dir == ">":
                    car.x += 1
                if car.dir == "^":
                    car.y -= 1
                if car.dir == "v":
                    car.y += 1
                
                if (car.x, car.y) in cars:
                    log("Collision at %d x %d" % (car.x, car.y))
                    cars[(car.x, car.y)].remove = True
                    car.remove = True
                    del cars[(car.x, car.y)]
                    if test_mode:
                        return
                else:
                    cars[(car.x, car.y)] = car

                    if values[car.y][car.x] == "/":
                        car.dir = {"<": "v", ">": "^", "v": "<", "^": ">"}[car.dir]
                    if values[car.y][car.x] == "\\":
                        car.dir = {"<": "^", ">": "v", "v": ">", "^": "<"}[car.dir]
                    if values[car.y][car.x] == "+":
                        if car.choice == 0:
                            car.dir = {"<": "v", ">": "^", "v": ">", "^": "<"}[car.dir]
                        if car.choice == 2:
                            car.dir = {"<": "^", ">": "v", "v": "<", "^": ">"}[car.dir]
                        car.choice = (car.choice + 1) % 3
        
        if len(cars) == 1:
            temp = list(cars.values())
            log("Final car at %d x %d" % (temp[0].x, temp[0].y))
            return


def test(log):
    values = [
        "/->-\\        ",
        "|   |  /----\\",
        "| /-+--+-\\  |",
        "| | |  | v  |",
        "\\-+-/  \\-+--/",
        "  \\------/   ",
    ]

    calc(log, values, True) == 1234
    return True


def run(log, values):
    calc(log, values, False)

if __name__ == "__main__":
    import sys, os
    def find_input_file():
        for fn in sys.argv[1:] + ["input.txt", f"day_{DAY_NUM:0d}_input.txt", f"day_{DAY_NUM:02d}_input.txt"]:
            for dn in [[], ["Puzzles"], ["..", "Puzzles"]]:
                cur = os.path.join(*(dn + [fn]))
                if os.path.isfile(cur): return cur
    fn = find_input_file()
    if fn is None: print("Unable to find input file!\nSpecify filename on command line"); exit(1)
    print(f"Using '{fn}' as input file:")
    with open(fn) as f: values = [x.strip("\r\n") for x in f.readlines()]
    print(f"Running day {DAY_DESC}:")
    run(print, values)
