from collections import defaultdict



class Hike:
    def __init__(self, grid):
        self.grid = grid
        self.rows, self.cols = len(grid), len(grid[0])
        self.start = (0, grid[0].index('.'))
        self.end = (len(grid) - 1, grid[-1].index('.'))
        self.graph = self.reduce_edges()

    def is_valid(self, row, col):
        return (0 <= row < self.rows and
                0 <= col < self.cols and
                self.grid[row][col] != '#')

    def navigate_slopes(self):
        directions = {'^': [(-1, 0)],
                    '>': [(0, 1)],
                    'v': [(1, 0)],
                    '<': [(0, -1)],
                    '.': [(-1, 0), (0, 1), (1, 0), (0, -1)]}


        def dfs(curr: (int, int), visited: {(int, int)}, path_len: int):
            while True:
                if curr == self.end:
                    return path_len
                visited.add(curr)
                next_cells = []
                for d in directions[self.grid[curr[0]][curr[1]]]:
                    dx, dy = curr[0] + d[0], curr[1] + d[1]
                    if self.is_valid(dx, dy) and (dx, dy) not in visited:
                        next_cells.append((dx, dy))

                if len(next_cells) == 1:
                    curr = next_cells[0]
                    path_len += 1
                    continue
                
                max_len = 0
                for cell in next_cells:
                    max_len = max(max_len, dfs(cell, visited.copy(), path_len + 1))
                
                return max_len
            
        return dfs(self.start, set(), 0)
    
    def navigate_flat(self):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        hist = defaultdict(dict)        
        visited = set()
            
        def dfs(curr: (int, int), path_len: int):
            while True:
                if curr == self.end:
                    return path_len
                
                visited.add(curr)
                next_cells = []
                for dx, dy in directions:
                    nx, ny = curr[0] + dx, curr[1] + dy

                    if self.is_valid(nx, ny) and (nx, ny) not in visited:
                        next_cells.append((nx, ny, dx, dy))

                if len(next_cells) == 1:
                    curr = next_cells[0][:2]
                    path_len += 1
                    continue
                
                max_len = 0
                for nx, ny, dx, dy in next_cells:
                    if hist[(nx, ny)].get((dx, dy), 0) >= path_len + 1:
                        continue
                    max_len = max(max_len, r:= dfs((nx, ny), path_len + 1))
                    if r:
                        hist[(nx, ny)][(dx, dy)] = max(hist[nx, ny].get((dx, dy), 0), path_len + 1)
                visited.remove(curr)
                
                return max_len
        
        return dfs(self.start, 0)

def main_part_one():
    with open('day23/input.txt', 'r') as file:
        lines = file.read().splitlines()
    h = Hike(lines)
    return h.navigate_slopes()

def main_part_two():    
    with open('day23/input.txt', 'r') as file:
        lines = file.read().splitlines()
    h = Hike(lines)
    return h.navigate_flat1()

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())