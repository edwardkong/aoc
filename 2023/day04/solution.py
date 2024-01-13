import os
import re

def num_wins(line: str) -> bool:
    my_nums, winning_nums = re.split(r'[:|]', line)[1:]
    winning_nums = set(winning_nums.split())
    my_nums = set(my_nums.split())
    wins = len(my_nums & winning_nums)
    return wins

def point_value(wins: int) -> int:
    return 2 ** (wins - 1) if wins else 0

def count_cards_won(card_pile: list[str]) -> int:
    cards_won = [1] * len(card_pile)
    for idx, card in enumerate(card_pile):
        wins = num_wins(card)
        for i in range(1, wins + 1):
            cards_won[idx + i] += cards_won[idx]
    return sum(cards_won)

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return file.read().splitlines()

if __name__ == '__main__':
    lines = process_input()

    print(sum(point_value(num_wins(line)) for line in lines))
    print(count_cards_won(lines))