class Universe:
    def __init__(self, map: list[str], wider=False):
        self.map = self.expand_universe(map, wider)

    def expand_universe(self, map: list[str], wider: bool) -> list[str]:
        n_row = len(map)
        n_col = len(map[0])
        new_cols = [[''] for _ in range(n_row)]

        for col in range(n_col):
            has_galaxy = any(map[row][col] == '#' for row in range(n_row))
            for row in range(n_row):
                if wider:
                    if map[row][col] == '.':
                        new_cols[row].append(1 if has_galaxy else 1000000)
                    else:
                        new_cols[row].append(['#'])
                else:
                    new_cols[row].extend([map[row][col]] * (1 if has_galaxy else 2))

        new_map = []
        for row in range(n_row):
            if ['#'] not in new_cols[row]:
                if wider:
                    new_row = [1 if x == ['.']
                               else 100000 * x if x == 1000000 
                               else x for x in new_cols[row]]
                else:
                    new_row = [new_cols[row]] * 2
            else:
                if wider:
                    new_row = [1 if x == '.' else [x] for x in new_cols[row]]
                else:
                    new_row = [new_cols[row]]
            new_map.extend(new_row)

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

def main_part_one():
    with open('day11/input.txt', 'r') as file:
        map = list([line.strip() for line in file.readlines()])
    new_uni = Universe(map)
    return new_uni.sum_distances()


def main_part_two():
    with open('day11/input.txt', 'r') as file:
        pass

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())