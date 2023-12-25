def boat_race(times: list[int], dists: list[int]):
    result = 1
    for i in range(len(times)):
        result *= ways_to_win(times[i], dists[i])
    return result

def ways_to_win(time: int, dist: int) -> int:
    wins = 0
    for i in range(time):
        speed = charge_time = i
        move_time = time - i
        if speed * move_time > dist:
            wins += 1
    return wins
        
def main_part_one():
    with open('day6/input.txt', 'r') as file:
        times = [int(x) for x in file.readline().split(':')[1].split()]
        dists = [int(x) for x in file.readline().split(':')[1].split()]
    return boat_race(times, dists)    


def main_part_two():
    with open('day6/input.txt', 'r') as file:
        time = int(file.readline().split(':')[1].replace(' ', ''))
        dist = int(file.readline().split(':')[1].replace(' ', ''))
    return ways_to_win(time, dist)

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())