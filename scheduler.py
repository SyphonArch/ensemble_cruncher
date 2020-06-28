from data import teams
from itertools import permutations
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
    # print(member, member_to_idxs[member])
    if len(member_to_idxs[member]) > 1:
        for idx in member_to_idxs[member]:
            criticals.add(idx)


def evaluate(ordering, verbose=False):
    wait = 0
    for member in member_to_idxs:
        individual_wait = 0
        indexes = sorted([ordering.index(idx) for idx in member_to_idxs[member] if idx in ordering])
        for i in range(1, len(indexes)):
            individual_wait += indexes[i] - indexes[i - 1] - 1
        if verbose:
            print(f'\t{member} waits {individual_wait}')
        wait += individual_wait
    return wait


start = time()
orderings = list(permutations(criticals))
print('tolist', time() - start)
start = time()
best = float('inf')
best_order = None
for i, ordering in enumerate(orderings):
    value = evaluate(ordering)
    if value < best:
        best = value
        best_order = ordering
    if i == 1000000:
        break
print('time', time() - start)
print(best)
print(best_order)
evaluate(best_order, True)
