import os
from collections import OrderedDict
from functools import reduce
import re

class Hashmap:
    def __init__(self):
        self.boxes = [OrderedDict() for _ in range(256)]
    
    def hash(self, key: str) -> int:
        return reduce(lambda r, c: ((r + ord(c)) * 17) % 256, key, 0)

    def put(self, key: str):
        label, fl = re.split(r'[=-]', key)
        box = self.hash(label)
        if '=' in key: self.boxes[box][label] = int(fl)
        else: self.boxes[box].pop(label, None)
    
    def fp(self) -> int:
        return sum((box + 1) * (slot + 1) * fl 
                   for box, od in enumerate(self.boxes) 
                   for slot, fl in enumerate(od.values()))

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return file.read().split(',')

if __name__ == '__main__':
    lines = process_input()
    
    hm = Hashmap()
    print(sum(hm.hash(key) for key in lines))
    
    for line in lines:
        hm.put(line)
    print(hm.fp())