import numpy as np
import random

NUM_FIELDS = 40
EREIGNIS = [7, 22, 36]
GEMEINSCHAFT = [2, 17, 33]


def roll_dice():
    first_dice = random.randint(1, 6)
    second_dice = random.randint(1, 6)
    return (first_dice + second_dice, first_dice == second_dice)


def main(dice_rolls, iterations):
    for i in range(iterations):
        board_visited = np.zeros(NUM_FIELDS)
        position = 0
        j = 0
        while j < dice_rolls:
            score, double = roll_dice()
            position += score
            position %= NUM_FIELDS
            board_visited[position] += 1
            if not double:
                j += 1
        print(board_visited)


if __name__ == "__main__":
    main(100, 5)
