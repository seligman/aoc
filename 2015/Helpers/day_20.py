#!/usr/bin/env python3

import math
import multiprocessing

def get_desc():
    return 20, 'Day 20: Infinite Elves and Infinite Houses'


def internal_worker(queue, work_unit, queue_done, data):
    def internal_found(value):
        queue_done.put((True, value))

    while True:
        job = queue.get()
        if job is None:
            queue_done.put(None)
            break
        worker(job, work_unit, data, internal_found)
        queue_done.put((False,))


def launch_workers(target_count, worker, data=None, work_unit=1000):
    workers = multiprocessing.cpu_count()
    procs = []
    queue = multiprocessing.Queue()
    queue_done = multiprocessing.Queue()

    for _ in range(workers):
        proc = multiprocessing.Process(target=internal_worker, args=(queue, work_unit, queue_done, data))
        proc.start()
        procs.append(proc)

    val = 0
    for _ in range(workers * 10):
        queue.put(val)
        val += work_unit

    ret = []
    while workers > 0:
        job = queue_done.get()
        if job is None:
            workers -= 1
        else:
            if job[0]:
                ret.append(job[1])
                if len(ret) == target_count:
                    for _ in range(workers):
                        queue.put(None)
            else:
                queue.put(val)
                val += work_unit
        
    for proc in procs:
        proc.join()

    ret.sort()

    return ret[0:target_count]


def get_divisors(n):
    small_divisors = [i for i in range(1, int(math.sqrt(n)) + 1) if n % i == 0]
    large_divisors = [n / d for d in small_divisors if n != d * d]
    return small_divisors + large_divisors


def worker(value, work_unit, data, found):
    for house in range(work_unit):
        house += value
        values = get_divisors(house)
        if data['mode'] == 0:
            if sum(values) * 10 >= data['value']:
                found(house)
        else:
            if sum([d for d in values if house / d <= 50]) * 11 >= data['value']:
                found(house)


def calc(values, mode):
    value = int(values[0])
    ret = launch_workers(1, worker, {'value': value, 'mode': mode})
    return ret[0]


def test(log):
    values = [
        "130",
    ]

    if calc(values, 0) == 8:
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values, 0))
    log.show(calc(values, 1))
