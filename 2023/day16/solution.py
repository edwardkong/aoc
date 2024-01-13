import os

def energized_tiles(tiles: list[str], start=None):
    splits = []
    seen = set()
    most = 0
    starts = []
    if start is None:
        starts.append((0, 0, 1, 0))
    else:
        # Optimization possible by storing paths between objects/walls
        starts.extend(
            [(0, x, 1, 0) for x in range(len(tiles))] +
            [(len(tiles[0]) - 1, x, -1, 0) for x in range(len(tiles))] +
            [(x, 0, 0, 1) for x in range(len(tiles[0]))] +
            [(x, len(tiles) - 1, 0, -1) for x in range(len(tiles[0]))]
        )

    for s in starts:
        curr, dir = (s[0], s[1]), (s[2], s[3])
        splits = []
        seen = set()
        while True:
            if (not (0 <= curr[0] < len(tiles[0])) or 
                not (0 <= curr[1] < len(tiles)) or
                (curr[0], curr[1], dir[0], dir[1]) in seen):
                if not splits:
                    break
                curr, dir = splits.pop()

            seen.add((curr[0], curr[1], dir[0], dir[1]))
            sq = tiles[curr[1]][curr[0]]

            if sq == '\\':
                dir = (dir[1], dir[0])
            elif sq == '/':
                dir = (-dir[1], -dir[0])
            elif sq == '|':
                if dir[0]:
                    splits.append((curr, (0, dir[0])))
                    dir = (0, -dir[0])
            elif sq == '-':
                if dir[1]:
                    splits.append((curr, (dir[1], 0)))
                    dir = (-dir[1], 0)
            
            curr = tuple(c + d for c, d in zip(curr, dir))
        most = max(most, len({(s[0], s[1]) for s in seen}))

    return most

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return file.read().splitlines()

if __name__ == '__main__':
    lines = process_input()

    print(energized_tiles(lines))
    print(energized_tiles(lines, start=True))