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
    
    def navigate_flat(self):
        def dfs(curr: (int, int), path_len: int):
            if curr == self.end:
                return path_len
            visited.add(curr)
            mx = 0
            for node in graph[curr]:
                if node not in visited:
                    mx = max(mx, dfs(node, path_len + graph[curr][node]))
            visited.remove(curr)
            return mx
        
        graph = self.graph
        visited = set()
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
    return h.navigate_flat()

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())