#!/usr/bin/env python3

import hashlib
from collections import deque
import multiprocessing

def get_desc():
    return 14, 'Day 14: One-Time Pad'


def get_hash(i, key, stretch):
    key += str(i)
    ret = hashlib.md5(key.encode("utf8")).hexdigest()
    if stretch > 0:
        for _ in range(stretch):
            ret = hashlib.md5(ret.encode("utf8")).hexdigest()
    return ret


def worker(queue, queue_done, work_size, key, stretch):
    while True:
        job = queue.get()
        if job is None:
            queue_done.put(None)
            break
        ret = []
        for i in range(work_size):
            ret.append((job + i, get_hash(job + i, key, stretch)))
        queue_done.put((job, ret))


def calc(values, stretch):
    key = values[0]
    deck = deque()
    found = 0

    workers = max(1, multiprocessing.cpu_count() - 1)
    queue = multiprocessing.Queue()
    queue_done = multiprocessing.Queue()
    procs = []
    work_size = 50
    next_job = 0
    next_pull = 0
    pending = {}

    for _ in range(workers):
        proc = multiprocessing.Process(target=worker, args=(queue, queue_done, work_size, key, stretch))
        proc.start()

    for _ in range(workers*2):
        queue.put(next_job)
        next_job += work_size

    while True:
        while len(deck) < 1500:
            if next_pull in pending:
                for cur in pending[next_pull]:
                    deck.append(cur)
                del pending[next_pull]
                next_pull += work_size
            else:
                job, ret = queue_done.get()
                queue.put(next_job)
                next_job += work_size
                pending[job] = ret

        cur_i, cur_hash = deck.popleft()

        best = None
        best_i = None

        for x in "0123456789abcdef":
            x = x * 3
            test = cur_hash.find(x)
            if test >= 0:
                if best_i is None or test < best_i:
                    best_i = test
                    best = x[0]

        if best is not None:
            best = best * 5
            to_check = 1000
            for _sub_i, sub_hash in deck:
                if best in sub_hash:
                    found += 1
                    if found == 64:
                        for _ in range(workers):
                            queue.put(None)
                        while workers > 0:
                            job = queue_done.get()
                            if job is None:
                                workers -= 1
                        for proc in procs:
                            proc.join()
                        return cur_i
                    break
                to_check -= 1
                if to_check == 0:
                    break

    return 0


def test(log):
    values = [
        "abc",
    ]

    if calc(values, 0) == 22728:
        log.show("First pass is good")
        if calc(values, 2016) == 22551:
            return True
        else:
            return False
    else:
        return False


def run(log, values):
    a = calc(values, 0)
    b = calc(values, 2016)

    log.show("With no key stretching: " + str(a))
    log.show("With key stretching: " + str(b))
