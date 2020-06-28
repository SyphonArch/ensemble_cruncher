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

for score in scores:
    if score[1] == 19:
        print('hi')
        scheduler.evaluate(score[0], True)
