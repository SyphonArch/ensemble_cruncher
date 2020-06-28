"""This is where I ended up doing the work"""
from scheduler import *
from sys import argv

num = int(argv[1])

with open(f'orderings{num}.p', 'rb') as f:
    worker(num, pickle.load(f))

