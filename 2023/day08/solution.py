import os
import math

def lcm_list(nums: list[int]):
    if not nums:
        return 0
    res = nums[0]
    for num in nums[1:]:
        res = abs(num*res) // math.gcd(num, res)
    return res

class Network:
    def __init__(self, directions: str, map: list[str]):
        self.directions = directions.strip()
        self.map = {x[:3]: (x[7:10], x[12:15]) for x in map}
    
    def follow_map_naive(self):
        node = 'AAA'
        step = 0
        n = len(self.directions)
        while node != 'ZZZ':
            if self.directions[step % n] == 'L':
                node = self.map[node][0]
            elif self.directions[step % n] == 'R':
                node = self.map[node][1]
            step += 1
        return step
    
    def multi_path(self):
        """
        The input is intentionally designed such that the number of steps
        to transform a node from the start to the end is equal to the length
        of the cycle, which is unnatural, but makes the solution simple.
        """
        nodes = [x for x in self.map.keys() if x[-1] == 'A']
        cycle_length = []
        step = 0
        n = len(self.directions)
        terminal = None
        while not terminal:
            terminal = True
            curr_dir = 0 if self.directions[step % n] == 'L' else 1
            for i in range(len(nodes)):
                nodes[i] = self.map[nodes[i]][curr_dir]
                if nodes[i][-1] == 'Z':
                    cycle_length.append(step + 1)
                if len(cycle_length) == len(nodes):
                    return lcm_list(cycle_length)
                if terminal and nodes[i][-1] != 'Z':
                    terminal = False
            step += 1
        return step
    
def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return file.readline(), file.read().splitlines()[1:]

if __name__ == '__main__':
    directions, maps = process_input()

    camel = Network(directions, maps)
    print(camel.follow_map_naive())
    print(camel.multi_path())