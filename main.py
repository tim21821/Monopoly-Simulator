import numpy as np
import random


def roll_dice():
    first_dice = random.randint(1, 6)
    second_dice = random.randint(1, 6)
    return (first_dice + second_dice, first_dice == second_dice)


def main(dice_rolls, iterations):
    board_visited = np.zeros(50)
    for i in range(iterations):
        for j in range(dice_rolls):
            score, double = roll_dice()


if __name__ == "__main__":
    main(100, 100)
