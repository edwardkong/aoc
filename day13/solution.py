
def main_part_one():
    r_sum = 0
    with open('day12/input.txt', 'r') as file:
        for line in file.readlines():
            r_sum += count_arrangements(line.strip())
        return r_sum

def main_part_two():
    r_sum = 0    
    with open('day12/input.txt', 'r') as file:
        for line in file.readlines():
            springs, groups = spring_unpacker(line.strip(), unfold=True)
            r_sum += count_arrangements1(springs, tuple(groups))
            #r_sum += count_arrangements(line, unfold=True)
    
        return r_sum

if __name__ == '__main__':
    #print(main_part_one())
    print(main_part_two())