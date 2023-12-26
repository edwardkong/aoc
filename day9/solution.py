def predict_value(history: list[int], insert=False) -> int:
    diff = []
    if all(item == 0 for item in history):
        return 0
    for i in range(len(history) - 1):
        diff.append(history[i + 1] - history[i])
    if not insert:
        return history[-1] + predict_value(diff)
    else:
        return history[0] - predict_value(diff, insert=True)

def main_part_one():
    r_sum = 0
    with open('day9/input.txt', 'r') as file:
        for line in file:
            seq = [int(x) for x in line.strip().split()]
            r_sum += predict_value(seq)
    return r_sum

def main_part_two():
    r_sum = 0
    with open('day9/input.txt', 'r') as file:
        for line in file:
            seq = [int(x) for x in line.strip().split()]
            r_sum += predict_value(seq, insert=True)
    return r_sum

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())