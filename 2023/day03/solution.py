import os
from collections import defaultdict

class Reader():
    def __init__(self, text: list[str]):
        self.text = text

    def sum_adjacencies(self) -> int:
        text = self.text
        curr_num, symbol_adj = '', False
        r_sum = 0

        for l_idx, line in enumerate(text):
            for c_idx, char in enumerate(line):
                if char.isdigit():
                    curr_num += char
                    if not symbol_adj:
                        symbol_adj = self.check_neighbors(l_idx, c_idx)
                elif curr_num:
                    if (char == '.' and symbol_adj) or char != '.':
                        r_sum += int(curr_num)
                    curr_num, symbol_adj = '', False
        return r_sum
    
    def check_neighbors(self, line_num: int, char_num: int) -> bool:        
        text = self.text
        symbols = ('@', '#', '$', '%', '&', '*', '+', '=', '-', '/')
        num_lines = len(text) - 1
        num_chars = len(text[0]) - 1

        for i in range(-1, 2):
            for j in range(-1, 2):
                curr_line, curr_char = line_num + i, char_num + j
                if 0 <= curr_line <= num_lines and 0 <= curr_char <= num_chars:
                    if text[curr_line][curr_char] in symbols:
                        return True
        return False
    
    def gen_gear_ratio(self) -> int:
        text = self.text
        curr_num = ''
        gear_adj = False
        gear_index = None, None
        curr_gears = set()
        gears = defaultdict(list)

        for l_idx, line in enumerate(text):
            for c_idx, char in enumerate(line):
                if char.isdigit():
                    curr_num += char
                    gear_index = self.find_gear(l_idx, c_idx)
                    if gear_index != (None, None): 
                        gear_adj = True
                        curr_gears.add(gear_index)
                elif curr_num:
                    if char == '*':
                        curr_gears.add((l_idx, c_idx))
                        gear_adj = True
                    if not char.isdigit() and gear_adj:
                        for gear in curr_gears:
                            gears[gear].append(int(curr_num))
                    curr_num, gear_adj = '', False
                    gear_index = None, None
                    curr_gears = set()

        gear_ratio = 0
        for gear, adj_parts in gears.items():
            if len(adj_parts) == 2:
                gear_ratio += adj_parts[0] * adj_parts[1]

        return gear_ratio
    
    def find_gear(self, line_num: int, char_num: int) -> bool:
        text = self.text
        num_lines = len(text) - 1
        num_chars = len(text[0]) - 1

        for i in range(-1, 2):
            for j in range(-1, 2):
                curr_line, curr_char = line_num + i, char_num + j
                if 0 <= curr_line <= num_lines and 0 <= curr_char <= num_chars:
                    if text[curr_line][curr_char] == '*':
                        return curr_line, curr_char
        return None, None

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return file.read().splitlines()

if __name__ == '__main__':
    lines = process_input()
    r = Reader(lines)

    print(r.sum_adjacencies())
    print(r.gen_gear_ratio())