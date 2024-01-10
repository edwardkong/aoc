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
        """hist = [[{i: 0 for i in range(4)} 
                 for _ in range(self.cols)] 
                 for _ in range(self.rows)]"""
        
        visited = set()

        def dfs1(curr: (int, int), visited: {()}, path_len: int):
            while True:
                if curr == self.end:
                    update_history(visited)
                    return path_len
                
                next_cells = []
                for dx, dy in directions:
                    nx, ny = curr[0] + dx, curr[1] + dy

                    if self.is_valid(nx, ny) and (nx, ny) not in visited:
                        if hist[nx][ny][dirs((dx, dy))] >= path_len + 1:
                            continue
                        next_cells.append((nx, ny, dx, dy))
                        visited[(nx, ny)][dirs((dx, dy))] = path_len + 1


                if len(next_cells) == 1:
                    n = next_cells[0]
                    curr = n[:2]
                    path_len += 1
                    visited[(nx, ny)][dirs((n[2], n[3]))] = path_len
                    continue
                
                max_len = 0
                for nx, ny, dx, dy in next_cells:
                    max_len = max(max_len, dfs((nx, ny), visited.copy(), path_len + 1))
                
                return max_len
            
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
    
    def reduce_edges(self):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        nodes = [self.start, self.end]
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == '#':
                    continue
                dirs = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if self.is_valid(nr, nc):
                        dirs += 1
                if dirs >= 3:
                    nodes.append((r, c))
        
        graph = defaultdict(dict)
        
        for orig_r, orig_c in nodes:
            branches = [(0, orig_r, orig_c)]
            visited = {(orig_r, orig_c)}

            while branches:
                edge_len, r, c = branches.pop()

                if (r, c) != (orig_r, orig_c) and (r, c) in nodes:
                    graph[(orig_r, orig_c)][(r, c)] = edge_len
                    continue

                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if self.is_valid(nr, nc) and (nr, nc) not in visited:
                        branches.append((edge_len + 1, nr, nc))
                        visited.add((nr, nc))
        
        return graph
    
    def navigate_flat1(self):
        graph = self.graph
        visited = set()

        def dfs(curr: (int, int), path_len: int):
            if curr == self.end:
                return path_len
            
            visited.add(curr)
            max_len = 0
            for node in graph[curr]:
                if node not in visited:
                    max_len = max(max_len, dfs(node, path_len + graph[curr][node]))
            visited.remove(curr)
            return max_len
        
        return dfs(self.start, 0)
    
# 5798 too low
# 6286

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

def sol():
    grid = open('day23/input.txt', 'r').read().splitlines()

    start = (0, grid[0].index("."))
    end = (len(grid) - 1, grid[-1].index("."))

    points = [start, end]

    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "#":
                continue
            neighbors = 0
            for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#":
                    neighbors += 1
            if neighbors >= 3:
                points.append((r, c))

    graph = {pt: {} for pt in points}

    for sr, sc in points:
        stack = [(0, sr, sc)]
        seen = {(sr, sc)}

        while stack:
            n, r, c = stack.pop()
            
            if n != 0 and (r, c) in points:
                graph[(sr, sc)][(r, c)] = n
                continue

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#" and (nr, nc) not in seen:
                    stack.append((n + 1, nr, nc))
                    seen.add((nr, nc))

    seen = set()

    def dfs(pt):
        if pt == end:
            return 0

        m = -float("inf")

        seen.add(pt)
        for nx in graph[pt]:
            if nx not in seen:
                m = max(m, dfs(nx) + graph[pt][nx])
        seen.remove(pt)

        return m

    print(dfs(start))

if __name__ == '__main__':
    #print(main_part_one())
    print(main_part_two())