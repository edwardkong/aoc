import os
import re
from sympy import symbols, solve

class Hail:
    def __init__(self, stones):
        self.stones = stones # (x, y, z, dx, dy, dz)

    @staticmethod
    def intersect(lower, upper, p1, p2):
        p1_x, p1_y, p2_x, p2_y = p1[0], p1[1], p2[0], p2[1]
        p1_vx, p1_vy, p2_vx, p2_vy = p1[2], p1[3], p2[2], p2[3]

        # Standard form ax + by + c = 0
        p1_a, p1_b = p1_vy, -p1_vx
        p2_a, p2_b = p2_vy, -p2_vx
        p1_c = p1_a * p1_x + p1_b * p1_y
        p2_c = p2_a * p2_x + p2_b * p2_y

        if p1_a * p2_b == p1_b * p2_a:
            return 0
        
        determinant = p1_a * p2_b - p2_a * p1_b
        x_intersect = (p1_c * p2_b - p2_c * p1_b) / determinant
        y_intersect = (p2_c * p1_a - p1_c * p2_a) / determinant

        if lower <= x_intersect <= upper and lower <= y_intersect <= upper:
            if ((x_intersect - p1_x) * p1_vx >= 0 and
                (y_intersect - p1_y) * p1_vy >= 0 and
                (x_intersect - p2_x) * p2_vx >= 0 and
                (y_intersect - p2_y) * p2_vy >= 0):
                return 1
        return 0

    def compare_pairs(self, lower, upper):
        pairs = 0
        for a in range(len(self.stones) - 1):
            for b in range(a + 1, len(self.stones)):
                ax, ay, _, avx, avy, _ = self.stones[a]
                bx, by, _, bvx, bvy, _ = self.stones[b]
                pairs += Hail.intersect(lower, upper, (ax, ay, avx, avy), 
                                        (bx, by, bvx, bvy))
        return pairs
        
    def solve_eqs(self):
        equations = []
        x1, y1, z1, vx1, vy1, vz1 = symbols('x1, y1, z1, vx1, vy1, vz1')
        for x, y, z, vx, vy, vz in self.stones:
            equations.extend([(x1 - x) * (vy - vy1) - (y1 - y) * (vx - vx1),
                              (y1 - y) * (vz - vz1) - (z1 - z) * (vy - vy1)])
        solution = [sol for sol in solve(equations) 
                    if all(v.is_real and v.is_integer for v in sol.values())]
        assert len(solution) == 1, 'No solution'
        return solution[0][x1] + solution[0][y1] + solution[0][z1]

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return [list(map(int, re.split(r'[,@]+', x))) 
                 for x in file.read().splitlines()]

if __name__ == '__main__':
    lines = process_input()
    h = Hail(lines)

    print(h.compare_pairs(200000000000000, 400000000000000))
    print(h.solve_eqs())
