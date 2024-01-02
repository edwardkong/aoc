def energized_tiles(tiles: list[str]):
    splits = []
    seen = set()
    most = 0
    starts = []
    #curr, dir = (0, 0), (0, 1)

    starts.extend([(0, x, 1, 0) for x in range(len(tiles))])
    starts.extend([(len(tiles[0]) - 1, x, -1, 0) for x in range(len(tiles))])
    starts.extend([(x, 0, 0, 1) for x in range(len(tiles[0]))])
    starts.extend([(x, len(tiles) - 1, 0, -1) for x in range(len(tiles[0]))])

    for s in starts:
        curr, dir = (s[0], s[1]), (s[2], s[3])
        splits = []
        seen = set()
        while True:
            if (not (0 <= curr[0] < len(tiles[0])) or 
                not (0 <= curr[1] < len(tiles)) or
                #dir in seen[curr[0]][curr[1]]
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

    #return len({(s[0], s[1]) for s in seen})
    return most


def main_part_one():
    with open('day16/input.txt', 'r') as file:
        lines = file.read().splitlines()
    return energized_tiles(lines)


def main_part_two():    
    with open('day16/input.txt', 'r') as file:
        pass

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())
