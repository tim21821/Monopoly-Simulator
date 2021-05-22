import numpy as np
import random
import pandas as pd

random.seed()

NUM_FIELDS = 40
EREIGNIS = [7, 22, 36]
EREIGNIS_KARTEN = [39, 5, -1, 34, 12, 10, 0, -1, -1, -1, 11, -1, -1, -1, -1, -1]
GEMEINSCHAFT = [2, 17, 33]
GEMEINSCHAFT_KARTEN = [
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    10,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    -1,
    0,
    -1,
]


def roll_dice():
    first_dice = random.randint(1, 6)
    second_dice = random.randint(1, 6)
    return (first_dice + second_dice, first_dice == second_dice)


def simulate(dice_rolls, iterations):
    for i in range(iterations):
        board_visited = np.zeros(NUM_FIELDS).astype("int32")
        position = 0
        j = 0
        ereignis_karten_shuffle = EREIGNIS_KARTEN[:]
        gemeinschaft_karten_shuffle = GEMEINSCHAFT_KARTEN[:]
        random.shuffle(ereignis_karten_shuffle)
        random.shuffle(gemeinschaft_karten_shuffle)
        while j < dice_rolls:
            score, double = roll_dice()
            position += score
            position %= NUM_FIELDS
            board_visited[position] += 1
            if position == 30:
                position = 10
                board_visited[position] += 1
            elif position in EREIGNIS:
                card = ereignis_karten_shuffle.pop()
                if card >= 0:
                    position = card
                    board_visited[position] += 1
                if len(ereignis_karten_shuffle) == 0:
                    ereignis_karten_shuffle = EREIGNIS_KARTEN[:]
                    random.shuffle(ereignis_karten_shuffle)
            elif position in GEMEINSCHAFT:
                card = gemeinschaft_karten_shuffle.pop()
                if card >= 0:
                    position = card
                    board_visited[position] += 1
                if len(gemeinschaft_karten_shuffle) == 0:
                    gemeinschaft_karten_shuffle = GEMEINSCHAFT_KARTEN[:]
                    random.shuffle(gemeinschaft_karten_shuffle)

            if not double:
                j += 1
        csv = pd.read_csv("ergebnisse.csv")
        csv[f"Lauf {i+1}"] = board_visited
        csv.to_csv("ergebnisse.csv", index=False)


if __name__ == "__main__":
    simulate(100, 5)
    print("run finished!")
