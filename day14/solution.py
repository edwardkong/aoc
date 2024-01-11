def roll_rocks(board: list[str]) -> list[str]:
    h, w = len(board), len(board[0])
    blockers = [0 for _ in range(h)]
    tilted = [['.' for _ in range(w)] for _ in range(h)]
    load = 0
    for row in range(h):
        for col in range(w):
            if board[row][col] == 'O':
                tilted[blockers[col]][col] = 'O'
                load += (h - blockers[col])
                blockers[col] += 1
            elif board[row][col] == '#':
                tilted[row][col] = '#'
                blockers[col] = row + 1
    return [''.join(x) for x in tilted]

def cycle_rocks(board: list[str]) -> int:
    cache = {}
    i = 0
    while True:
        curr_board = tuple(board)
        if curr_board in cache:
            break
        cache[curr_board] = i
        for _ in range(4):
            board = [''.join(row) for row in zip(*reversed(roll_rocks(board)))]
        i += 1

    start_cycle = cache[curr_board]
    cycles_left = (1000000000 - start_cycle) % (i - start_cycle)
    for _ in range(cycles_left * 4):
        board = [''.join(row) for row in zip(*reversed(roll_rocks(board)))]

    return sum_load(board)

def sum_load(board: list[str]) -> int:
    return sum(board[r].count('O') * (len(board) - r) for r in range(len(board)))

def main_part_one():
    with open('day14/input.txt', 'r') as file:
        lines = file.read().splitlines()
    return sum_load(roll_rocks(lines))

def main_part_two():    
    with open('day14/input.txt', 'r') as file:
        lines = file.read().splitlines()
    return cycle_rocks(lines)

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())
