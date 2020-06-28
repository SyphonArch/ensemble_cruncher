import pickle
import scheduler

data = []

for i in range(16):
    filename = f"worker#{i}.p"
    with open(filename, 'rb') as f:
        rslt = pickle.load(f)
        data.append(rslt)

bests = []
for time, orderings in data:
    if time == 9:
        bests += orderings

scores = []
for ordering in bests:
    wait, waits = scheduler.evaluate(ordering, False, True)
    score = sum(x ** 2 for x in waits)
    scores.append((ordering, score))

scores.sort(key=lambda x: x[1])

finals = []
for score in scores:
    if score[1] == 19:
        finals.append(score[0])

runtime_map = {1: 13, 2: 10, 3: 8, 4: 12, 5: 10, 6: 4, 7: 6, 8: 8, 9: 14, 10: 7, 11: 10, 12: 4, 13: 13}
member_to_idxs = scheduler.member_to_idxs


def total_wait_minutes(ordering, verbose=False):
    total_wait = 0
    for member in member_to_idxs:
        member_wait = 0
        buffer = 0
        arrived = False
        for idx in ordering:
            if idx in member_to_idxs[member]:
                arrived = True
                member_wait += buffer
                buffer = 0
            else:
                if arrived:
                    buffer += runtime_map[idx]
        total_wait += member_wait
        if verbose:
            print(f"{member} waits {member_wait} minutes")
    return total_wait


finals.sort(key=total_wait_minutes)

for ordering in finals:
    if total_wait_minutes(ordering) == 81:
        print(ordering)
