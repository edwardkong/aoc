def main_part_one():
    with open('day10/input.txt', 'r') as file:
        grid = list([line.strip() for line in file.readlines()])
    new_grid = Grid(grid)
    return new_grid.find_loop_opposite()


def main_part_two():
    with open('day10/input.txt', 'r') as file:
        grid = list([line.strip() for line in file.readlines()])
    new_grid = Grid(grid)
    return new_grid.calc_interior()

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())