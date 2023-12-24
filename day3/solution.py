from functools import lru_cache

class Reader():
    def __init__(self, text: list[str]):
        self.text = text

    def sum_adjacencies(self) -> int:
        curr_num, symbol_adj = '', False
        r_sum = 0
        text = self.text

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
    
    @lru_cache
    def check_neighbors(self, line_num: int, char_num: int) -> bool:
        text = self.text
        non_symbols = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.')
        num_lines = len(text) - 1
        num_chars = len(text[0]) - 1

        l_start = 0 if line_num == 0 else -1
        l_end = 1 if line_num == num_lines else 2
        c_start = 0 if char_num == 0 else -1
        c_end = 1 if char_num == num_chars else 2

        for i in range(l_start, l_end):
            for j in range(c_start, c_end):
                if text[line_num + i][char_num + j] not in non_symbols:
                    return True
        return False
    
    def gear_ratios() -> int:
        pass


def main_part_one():
    with open('day3/input.txt', 'r') as file:
        lines = [line.strip() for line in file]
    reader = Reader(lines)
    r_sum = reader.sum_adjacencies()
    return r_sum

def main_part_two():
    r_sum = 0
    with open('day3/input.txt', 'r') as file:
        for line in file:
            pass
        #r_sum += optimize_game(line)
    return r_sum

if __name__ == '__main__':
    print(main_part_one())
    #print(main_part_two())