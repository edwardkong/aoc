import os

class Universe:
    def __init__(self, map: list[str]):
        self.map = self.expand_universe(map)

    def expand_universe(self, map: list[str]) -> list[str]:
        n_row = len(map)
        n_col = len(map[0])
        new_cols = ['' for _ in range(n_row)]

        for col in range(n_col):
            has_galaxy = any(map[row][col] == '#' for row in range(n_row))
            for row in range(n_row):
                new_cols[row] += map[row][col] * (1 if has_galaxy else 2)

        new_map = []
        for row in range(n_row):
            if '#' not in new_cols[row]:
                new_map.append(new_cols[row])
            new_map.append(new_cols[row])

        return new_map
    
    def expand_universe_wider(self, map: list[str]) -> list[str]:
        n_row = len(map)
        n_col = len(map[0])
        new_cols = [[] for _ in range(n_row)]

        for col in range(n_col):
            has_galaxy = any(map[row][col] == '#' for row in range(n_row))
            for row in range(n_row):
                if map[row][col] == '.':
                        new_cols[row].append(1 if has_galaxy else 1000000)
                else:
                    new_cols[row].append('#')

        new_map = []
        for row in range(n_row):
            if '#' in new_cols[row]:
                new_map.append(new_cols[row])
            else:
                new_map.append(list([x if x == '#' 
                                     else x * 1000000 
                                     for x in new_cols[row]]))

        return new_map
    
    def find_galaxies(self) -> list[(int, int)]:
        map = self.map
        n_row = len(map)
        n_col = len(map[0])
        galaxies = []
        for row in range(n_row):
            for col in range(n_col):
                if map[row][col] == '#':
                    galaxies.append((row, col))
        return galaxies

    def sum_distances(self) -> int:
        galaxies = self.find_galaxies()
        ng = len(galaxies)
        total = 0
        for g in range(ng):
            for d in range(g + 1, ng):
                total += (abs(galaxies[g][0] - galaxies[d][0]) +
                                abs(galaxies[g][1] - galaxies[d][1]))
        return total

    def sum_distances_wider(self) -> int:
        map = self.expand_universe_wider(self.map)
        gxs = self.find_galaxies()
        ng = len(gxs)
        total = 0
        for g in range(ng):
            for d in range(g + 1, ng):
                max_x = max(gxs[g][0], gxs[d][0])
                min_x = min(gxs[g][0], gxs[d][0])
                max_y = max(gxs[g][1], gxs[d][1])
                min_y = min(gxs[g][1], gxs[d][1])
                for i in range(min_x, max_x):
                    col = gxs[g][1]
                    total += 1 if map[i][col] == '#' else map[i][col]
                for j in range(min_y, max_y):
                    row = gxs[g][0]
                    total += 1 if map[row][j] == '#' else map[row][j]
        return total

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return file.read().splitlines()

if __name__ == '__main__':
    lines = process_input()
    uni = Universe(lines)

    print(uni.sum_distances())
    print(uni.sum_distances_wider())