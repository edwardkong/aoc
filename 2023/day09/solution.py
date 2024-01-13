import os

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

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return [list(map(int, line.split())) 
                for line in file.read().splitlines()]

if __name__ == '__main__':
    lines = process_input()

    print(sum(predict_value(line) for line in lines))
    print(sum(predict_value(line, insert=True) for line in lines))
