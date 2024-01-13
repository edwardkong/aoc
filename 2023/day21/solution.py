import os
from collections import deque

class Garden:
    def __init__(self, grid):
        self.grid = grid
        self.h = len(self.grid)
        self.w = len(self.grid[0])
        self.s = self.get_starting_square()

    def get_starting_square(self):
        for r in range(self.h):
            if 'S' in self.grid[r]:
                return r, self.grid[r].index('S')

    def visit_n(self, n, row=None, col=None):
        if row is None or col is None:
            row, col = self.s
        res = set()
        seen = {(row, col)}
        q = deque([(row, col, n)])
        while q:
            r, c, steps = q.popleft()
            if steps % 2 == 0:
                res.add((r, c))
            if steps == 0:
                continue
            for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
                if (not (0 <= nr < self.h) or
                    not (0 <= nc < self.w) or 
                    self.grid[nr][nc] == "#" or 
                    (nr, nc) in seen):
                    continue
                seen.add((nr, nc))
                q.append((nr, nc, steps - 1))
        return len(res)

    def visit_all(self, parity=None):
        seen = set()
        if parity:
            parity_seen = set()
        q = deque([(self.s[0], self.s[1], 1)])
        while q:
            r, c, steps = q.popleft()
            for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
                if (not (0 <= nr < self.h) or not (0 <= nc < self.w) or 
                    self.grid[nr][nc] == "#" or
                    (nr, nc) in seen):
                    continue
                if ((parity == 'odd' and steps % 2 == 1) or
                    (parity == 'even' and steps % 2 == 0)):
                        parity_seen.add((nr, nc))
                seen.add((nr, nc))
                q.append((nr, nc, steps + 1))
        if parity is None:
            return len(seen)
        return len(parity_seen)
    
    def calc_area(self, n):
        l = self.w
        grids = n // l - 1
        r, c = self.s

        def sum_partials(entry, count, steps):
            """
            Sums the squares visited in each type of partially filled grid.
            Args:
                entry (list[int]): The closest point to the center per grid.
                count (int): The amount of each type of grid.
                steps (int): The length travelled into each type of grid.
            Returns:
                int: The total number of squares visited for each type of grid
            """
            return sum(self.visit_n(steps - 1, r, c) for r, c in entry) * count

        # Number of each parity grid
        odd_grids = (grids // 2 * 2 + 1) ** 2
        even_grids = ((grids + 1) // 2 * 2) ** 2

        # Number of squares in each parity grid
        sq_in_odd = self.visit_all(parity='odd')
        sq_in_even = self.visit_all(parity='even')

        odds, evens = odd_grids * sq_in_odd, even_grids * sq_in_even

        # Entry points for corners and edges
        corner_pat = [(l - 1, c), (r, 0), (0, c), (r, l - 1)]
        edge_pat = [(l - 1, 0), (0, 0), (0, l - 1), (l - 1, l - 1)]

        # Get all squares in partially explored grids
        corners = sum_partials(corner_pat, 1, l)
        sm_edge = sum_partials(edge_pat, grids + 1, l // 2)
        lg_edge = sum_partials(edge_pat, grids, l * 3 // 2)

        return odds + evens + corners + sm_edge + lg_edge

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return file.read().splitlines()

if __name__ == '__main__':
    lines = process_input()
    g = Garden(lines)

    print(g.visit_n(64))
    print(g.calc_area(26501365))