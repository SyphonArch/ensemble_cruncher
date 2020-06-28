"""This is where I attempted to do the work."""
from data import teams
from itertools import permutations
from multiprocessing import Process
import pickle
from time import time

idx_to_name = {}
member_to_idxs = {}

for team in teams:
    idx_to_name[team.idx] = team.name
    for member in team.members:
        if member not in member_to_idxs:
            member_to_idxs[member] = []
        member_to_idxs[member].append(team.idx)

criticals = set()

for member in member_to_idxs:
    print(member, member_to_idxs[member])
    if len(member_to_idxs[member]) > 1:
        for idx in member_to_idxs[member]:
            criticals.add(idx)

input("Press Enter to proceed")


def evaluate(ordering, verbose=False, return_individual_waits=False):
    individual_waits = []
    wait = 0
    for member in member_to_idxs:
        individual_wait = 0
        indexes = sorted([ordering.index(idx) for idx in member_to_idxs[member] if idx in ordering])
        for i in range(1, len(indexes)):
            individual_wait += indexes[i] - indexes[i - 1] - 1
        if verbose:
            print(f'\t{member} waits {individual_wait}')
        wait += individual_wait
        individual_waits.append(individual_wait)
    if return_individual_waits:
        return wait, individual_waits
    else:
        return wait


def worker(num, orderings):
    print(f"[worker {num}] INITIATE", flush=True)
    start = time()
    best = float('inf')
    best_orders = []
    for i, ordering in enumerate(orderings):
        value = evaluate(ordering)
        if value < best:
            best = value
            best_orders = [ordering]
        elif value == best:
            best_orders.append(ordering)
        if i % 100000 == 0:
            print(f"[worker {num}]: {i + 1} / {len(orderings)}", flush=True)
    with open(f"worker#{num}.p", 'wb') as f:
        pickle.dump([best, best_orders], f)
    print(f"[worker {num}] FINISHED in {time() - start} seconds", flush=True)


worker_count = 16
if __name__ == '__main__':
    print('Creating permutations...', flush=True)
    start = time()
    orderings = list(permutations(criticals))
    print('Created list of permutations:', time() - start, 'seconds', flush=True)

    chunk_size = len(orderings) // worker_count

    print("Dividing workload...", flush=True)
    orderings_divided = []
    for i in range(worker_count):
        if i != worker_count - 1:
            orderings_divided.append(orderings[i * chunk_size: (i + 1) * chunk_size])
        else:
            orderings_divided.append(orderings[(worker_count - 1) * chunk_size:])
        with open(f"orderings{i}.p", 'wb') as f:
            pickle.dump(orderings_divided[i], f)
        print(f"Workload {i} ready", flush=True)

    input("Proceed with process assignment?")
    print("Assigning processes...", flush=True)
    start = time()
    processes = []
    for i in range(worker_count):
        p = Process(target=worker, args=(i, orderings_divided[i]))
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

    print(f'-ALL PROCESSES FINISHED in {time() - start} seconds-', flush=True)
