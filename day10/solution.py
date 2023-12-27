import cProfile
LINKS = {
            '|': ((1, 0), (-1, 0)),
            '-': ((0, 1), (0, -1)),
            'L': ((1, 0), (0, -1), (-1, 0), (0, 1)),
            '7': ((-1, 0), (0, 1), (1, 0), (0, -1)),
            'F': ((-1, 0), (0, -1), (1, 0), (0, 1)),
            'J': ((1, 0), (0, 1), (-1, 0), (0, -1))
        }

class Grid:
    def __init__(self, grid: list[str]):
        self.grid = grid
        self.s, self.s_coord = self.identify_S()
        self.replace_S()
            
    def identify_S(self):
        grid = self.grid
        h = len(grid)
        w = len(grid[0])
        for line in range(h):
            s_idx = grid[line].find('S')
            if s_idx > -1:
                coord = (line, s_idx)
                break
        
        dirs = {(-1, 0): {'|', 'F', '7'}, 
                (0, 1): {'-', 'J', '7'}, 
                (1, 0): {'|', 'J', 'L'}, 
                (0, -1): {'-', 'F', 'L'}
                }
        s = None
        for d in dirs.keys():
            n_line, n_char  = coord[0] + d[0], coord[1] + d[1]
            if 0 <= n_line < h and 0 <= n_char < w:
                if grid[n_line][n_char] in dirs[d]:
                    if not s:
                        s = dirs[tuple(-x for x in d)]
                    else:
                        (s, *_) = s & dirs[tuple(-x for x in d)]
                        break
        return s, coord
    
    def replace_S(self):
        line_num = self.s_coord[0]
        self.grid[line_num] = self.grid[line_num].replace('S', self.s)
    
    def next_square(self, prev_dir, coord):
        sq = self.grid[coord[0]][coord[1]]
        if sq == '|' or sq == '-':
            return tuple(sum(pair) for pair in zip(coord, prev_dir))
        elif prev_dir == LINKS[sq][0]:
            return tuple(sum(pair) for pair in zip(coord, LINKS[sq][3]))
        elif prev_dir == LINKS[sq][1]:
            return tuple(sum(pair) for pair in zip(coord, LINKS[sq][2]))

    def find_loop_opposite(self):
        s = self.s
        pv_cw = pv_ccw = self.s_coord
        cw = self.next_square(LINKS[s][0], pv_cw)
        ccw = self.next_square(LINKS[s][1], pv_ccw)
        steps = 1
        while cw != ccw:
            pv_cw_dir = tuple((x - y for x, y in zip(cw, pv_cw)))
            pv_ccw_dir = tuple((x - y for x, y in zip(ccw, pv_ccw)))

            cw, pv_cw = self.next_square(pv_cw_dir, cw), cw
            ccw, pv_ccw = self.next_square(pv_ccw_dir, ccw), ccw
            steps += 1

            if cw == ccw:
                return steps
            elif cw == pv_ccw:
                return steps - 1
            
    def isolate_loop(self):
        w = len(self.grid[0])
        h = len(self.grid)
        new_grid = [['0'] * w for _ in range(h)]

        s = self.s
        prev_sq = s_coord = self.s_coord
        cur_sq = self.next_square(LINKS[s][0], s_coord)
        while True:
            new_grid[cur_sq[0]][cur_sq[1]] = self.grid[cur_sq[0]][cur_sq[1]]
            if cur_sq == s_coord:
                break
            pv_dir = tuple((x - y for x, y in zip (cur_sq, prev_sq)))
            cur_sq, prev_sq = self.next_square(pv_dir, cur_sq), cur_sq
        return [''.join(line) for line in new_grid]
    
    def calc_interior(self):
        grid = self.isolate_loop()
        area = 0
        for i in grid:
            inside = False
            last = None
            for j in i:
                match j:
                    case '0':
                        if inside:
                            area += 1
                    case '|':
                        inside = not inside
                        last = None
                    case '-':
                        pass
                    case 'F':
                        last = j
                    case 'L':
                        last = j
                    case '7':
                        if last == 'L':
                            inside = not inside
                        last = None
                    case 'J':
                        if last == 'F':
                            inside = not inside
                        last = None
        return area

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