#!/usr/bin/env python3

import hashlib
import multiprocessing

def get_desc():
    return 5, 'Day 5: How About a Nice Game of Chess?'


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


def worker(value, work_unit, data, found):
    for i in range(work_unit):
        test = hashlib.md5((data['value'] + str(i + value)).encode("utf8")).hexdigest()
        if test.startswith("00000"):
            found((i + value, test[5:6], test[6:7]))


def calc(values, mode):
    temp = []
    for job in launch_workers(8 if mode == 0 else 32, worker, {"value": values[0]}):
        temp.append(job)

    if mode == 0:
        return "".join([x[1] for x in temp[0:8]])
    else:
        ret = [None] * 8
        for cur in temp:
            if cur[1] in "01234567":
                if ret[int(cur[1])] is None:
                    ret[int(cur[1])] = cur[2]
        return "".join(ret)


def test(log):
    values = [
        "abc",
    ]

    if calc(values, 0) == "18f47a30":
        return True
    else:
        return False


def run(log, values):
    log.show(calc(values, 0))
    log.show(calc(values, 1))
