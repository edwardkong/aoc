import re
from collections import defaultdict
from collections import deque

class Bricks:
    def __init__(self, bricks):
        self.num_bricks = len(bricks)
        self.supported_by = self.drop_bricks(bricks) # {a: (b, c)} = a supported by b and c
        self.supports = self.invert_supports() # {d: (e, f)} = d supports e and f
    
    def invert_supports(self):
        s = defaultdict(set)
        for key, supports in self.supported_by.items():
            for brick in supports:
                s[brick].add(key)
        return s

    def drop_bricks(self, bricks):
        top_down = {}
        supports = {}
        for i, b in enumerate(bricks):
            x1, y1, z1, x2, y2, z2 = b
            b_max = 1
            b_supports = set()
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    coord_max, coord_brick = top_down.get((x, y), (0, None))
                    if coord_max >= b_max:
                        b_max = coord_max + 1
                        b_supports = {coord_brick}
                    elif coord_max == b_max - 1:
                        if coord_brick is not None:
                            b_supports.add(coord_brick)
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    top_down[(x, y)] = (b_max + z2 - z1, i)
            supports[i] = b_supports
        return supports

    def count_removable(self):
        removable = set()
        for i in range(self.num_bricks):
            if i not in self.supports:
                removable.add(i)
                continue
            for s in self.supports[i]:
                if len(self.supported_by[s]) == 1:
                    break
            else:
                removable.add(i)
        return len(removable)
    
    def sum_chains(self):
        sum = 0
        for i in range(self.num_bricks):
            sum += self.chain(i)
        return sum

    def chain(self, i) -> int:
        q = deque([i])
        removed = set()
        while q:
            removed.add(curr := q.popleft())
            for s in self.supports[curr]:
                if all(t in removed for t in self.supported_by[s]):
                    q.append(s)
        return len(removed) - 1

def main_part_one():
    with open('day22/input.txt', 'r') as file:
        lines = sorted([list(map(int, re.split(r'[,~]+', l))) 
                 for l in file.read().splitlines()], key=lambda x: x[2])
    b = Bricks(lines)
    return b.count_removable()

def main_part_two():    
    with open('day22/input.txt', 'r') as file:
        lines = sorted([list(map(int, re.split(r'[,~]+', l))) 
                 for l in file.read().splitlines()], key=lambda x: x[2])
    b = Bricks(lines)
    return b.sum_chains()

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())