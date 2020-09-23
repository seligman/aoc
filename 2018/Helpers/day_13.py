#!/usr/bin/env python

def get_desc():
    return 13, 'Day 13: Mine Cart Madness'


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
                    log.show("Collision at %d x %d" % (car.x, car.y))
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
            log.show("Final car at %d x %d" % (temp[0].x, temp[0].y))
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
