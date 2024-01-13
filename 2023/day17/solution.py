import os
from heapq import heappush, heappop

class Searcher:
    def __init__(self, grid: list[str]):
        self.grid = grid

    def search(self, ultra=False) -> int:
        grid = self.grid
        w, h = len(grid[0]), len(grid)
        closed = set()
        open = []
        start, end = (0, 0), (w - 1, h - 1)

        heappush(open, (0, start[0], start[1], 0, 0, 0))
        while open:
            r_len, y, x, dy, dx, hist = heappop(open)
            if y == end[1] and x == end[0]:
                return r_len
            
            key = (y, x, dy, dx, hist)
            if key in closed:
                continue
            closed.add(key)

            for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if d == (-dy, -dx):
                    continue
                same_dir = d == (dy, dx)
                if ultra:
                    if ((0 < hist < 4 and not same_dir) 
                        or (hist >= 10 and same_dir)):
                        continue
                    nh = hist + 1 if same_dir else 1
                else:
                    if hist >= 3 and same_dir:
                        continue
                    nh = hist + 1 if same_dir else 1

                ny, nx = y + d[0], x + d[1]
                if not (0 <= nx <= end[0]) or not (0 <= ny <= end[1]):
                    continue
                dist = int(grid[ny][nx])
                heappush(open, (r_len + dist, ny, nx, d[0], d[1], nh))

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return file.read().splitlines()

if __name__ == '__main__':
    lines = process_input()

    city = Searcher(lines)
    print(city.search())
    print(city.search(ultra=True))