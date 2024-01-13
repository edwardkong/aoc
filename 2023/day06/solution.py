import os

def boat_race(times: list[int], dists: list[int]):
    result = 1
    for i in range(len(times)):
        result *= ways_to_win(times[i], dists[i])
    return result

def ways_to_win(time: int, dist: int) -> int:
    wins = 0
    for i in range(time):
        speed = i
        move_time = time - i
        if speed * move_time > dist:
            wins += 1
    return wins

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        times = file.readline().split(':')[1].split()
        dists = file.readline().split(':')[1].split()
        time, dist = int(''.join(times)), int(''.join(dists))
        return list(map(int, times)), list(map(int, dists)), time, dist

if __name__ == '__main__':
    times, dists, time, dist = process_input()

    print(boat_race(times, dists))
    print(ways_to_win(time, dist))