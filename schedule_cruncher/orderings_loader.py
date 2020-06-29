"""This is where I ended up doing the work"""
from schedule_cruncher.scheduler import *
from sys import argv

num = int(argv[1])

print('Loading file...')
with open(f'orderings{num}.p', 'rb') as f:
    worker(num, pickle.load(f))

