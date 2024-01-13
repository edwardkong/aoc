import os
from collections import Counter

def hand_to_hex_val(hand: str, jokers=None) -> int:
    hex_val = 0
    for card in hand:
        if card == 'T':
            hex_val = 0xA | (hex_val << 4)
        elif card == 'J':
            if not jokers:
                hex_val = 0xB | (hex_val << 4)
            else:
                hex_val = 0x1 | (hex_val << 4)
        elif card == 'Q':
            hex_val = 0xC | (hex_val << 4)
        elif card == 'K':
            hex_val = 0xD | (hex_val << 4)
        elif card == 'A':
            hex_val = 0xE | (hex_val << 4)
        else:
            hex_val = int(card) | (hex_val << 4)
    return hex_val

def calc_hand_value(hand: str, jokers=None):
    if jokers and 'J' in hand:
        counter = Counter(hand)
        mc, *mc2 = counter.most_common(2)
        if not mc2:
            new_hand = hand
        elif mc[0] == 'J':
            new_hand = hand.replace('J', mc2[0][0])
        else:
            new_hand = hand.replace('J', mc[0])
    else:
        new_hand = hand
    counter = Counter(new_hand)
    mc, *mc2 = counter.most_common(2)
    mc_v, mc2_v = mc[1], mc2[0][1] if mc2 else 0
    
    hand_value = mc_v
    if mc_v == 2 and mc2_v == 2: hand_value += 1
    if mc_v > 2: hand_value += 1
    if mc_v == 3 and mc2_v == 2: hand_value += 1
    if mc_v > 3: hand_value += 1
    return hand_value << 20 | hand_to_hex_val(hand, jokers)

def order_hands(hands: list[str], jokers=None):
    return sorted(hands, key=lambda x: calc_hand_value(x[0], jokers))

def calc_winnings(hands: list[str], jokers=None):
    s_hands = order_hands(hands, jokers)
    winnings = 0
    for i in range(len(hands)):
        winnings += int(s_hands[i][1]) * (i + 1)
    return winnings

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return [line.split() for line in file.read().splitlines()]

if __name__ == '__main__':
    lines = process_input()

    print(calc_winnings(lines))
    print(calc_winnings(lines, jokers=True))