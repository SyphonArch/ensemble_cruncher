import pickle
from schedule_cruncher import scheduler

data = []

for i in range(16):
    filename = f"schedule_cruncher/worker#{i}.p"
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
                    buffer += scheduler.runtime_map[idx]
        total_wait += member_wait
        if verbose:
            print(f"{member} waits {member_wait} minutes")
    return total_wait


finals.sort(key=total_wait_minutes)

final_finals = []
for ordering in finals:
    if total_wait_minutes(ordering) == 81:
        final_finals.append(ordering)

answer = final_finals[-1]

answer += (5,)
# print(answer)

prefix = [0]
for idx in answer:
    prefix.append(prefix[-1] + scheduler.runtime_map[idx])

# print(prefix[1:])

if __name__ == '__main__':
    print('\n앙상블 프로그램 순서')
    for i, idx in enumerate(answer):
        print(i, '\t', scheduler.idx_to_name[idx])

    print()
    total_wait_minutes(answer, True)
