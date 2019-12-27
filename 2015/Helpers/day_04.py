#!/usr/bin/env python

import multiprocessing
import hashlib

def get_desc():
    return 4, 'Day 4: The Ideal Stocking Stuffer'


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
        m = hashlib.md5((data['prefix'] + str(i + value)).encode("utf8")).hexdigest()
        if m.startswith(data['target_val']):
            found(i + value)


def calc(target_val, values):
    return launch_workers(1, worker, data={"target_val": target_val, "prefix": values[0].strip()})[0]


def test(log):
    values = [
        "pqrstuv",
    ]

    if calc("00000", values) == 1048970:
        return True
    else:
        return False


def run(log, values):
    log.show("For 5 zeroes: " + str(calc("00000", values)))
    log.show("For 6 zeroes: " + str(calc("000000", values)))
