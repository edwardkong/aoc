import re

def num_wins(line:str) -> bool:
    my_nums, winning_nums = re.split(r'[:|]', line)[1:]
    winning_nums = set(winning_nums.split())
    my_nums = set(my_nums.split())
    wins = len(my_nums & winning_nums)
    return wins

def count_cards_won(card_pile: list[str]) -> int:
    cards_won = [1] * len(card_pile)
    for idx, card in enumerate(card_pile):
        wins = num_wins(card)
        for i in range(1, wins + 1):
            cards_won[idx + i] += cards_won[idx]
    return sum(cards_won)

def main_part_one():
    r_sum = 0
    with open('day4/input.txt', 'r') as file:
        for line in file:
            wins = num_wins(line)
            r_sum += (2 ** (wins - 1) if wins else 0)
    return r_sum

def main_part_two():
    with open('day4/input.txt', 'r') as file:
        lines = [line.strip() for line in file]
        r_sum = count_cards_won(lines)
    return r_sum

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())