import sys
from heapq import heappush, heappop

class Searcher:
    def __init__(self, grid: list[str]):
        self.grid = grid

    def search(self) -> int:
        closed = set()
        open = []
        grid = self.grid
        w, h = len(grid[0]), len(grid)
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
                if d[0] == dy and d[1] == dx:
                    if hist >= 3:
                        continue
                    else:
                        nh = hist + 1
                else:
                    nh = 1
                ny, nx = y + d[0], x + d[1]
                if not (0 <= nx <= end[0]) or not (0 <= ny <= end[1]):
                    continue
                dist = int(grid[ny][nx])
                heappush(open, (r_len + dist, ny, nx, d[0], d[1], nh))
        
        return 0

def main_part_one():
    with open('day17/input.txt', 'r') as file:
        lines = file.read().splitlines()
    city = Searcher(lines)
    return city.search()


def main_part_two():    
    with open('day16/input.txt', 'r') as file:
        lines = file.read().splitlines()
        pass

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())
