import numpy as np
import random
import pandas as pd
from numba import njit
from tqdm import tqdm

random.seed()

NUM_FIELDS = 40
EREIGNIS = np.array([7, 22, 36])
EREIGNIS_KARTEN = np.array(
    [39, 5, -1, 34, 12, 10, 0, -1, -1, -1, 11, -1, -1, -1, -1, -1]
)
GEMEINSCHAFT = np.array([2, 17, 33])
GEMEINSCHAFT_KARTEN = np.array(
    [
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
)
FELDER = np.array(
    [
        "Los",
        "Badstraße",
        "Gemeinschaft 1",
        "Turmstraße",
        "Einkommenssteuer",
        "Südbahnhof",
        "Chausseestraße",
        "Ereignis 1",
        "Elisenstraße",
        "Poststraße",
        "Gefängnis",
        "Seestraße",
        "Elektrizitätswerk",
        "Hafenstraße",
        "Neue Straße",
        "Westbahnhof",
        "Münchner Straße",
        "Gemeinschaft 2",
        "Wiener Straße",
        "Berliner Straße",
        "Frei Parken",
        "Theaterstraße",
        "Ereignis 2",
        "Museumstraße",
        "Opernplatz",
        "Nordbahnhof",
        "Lessingstraße",
        "Schillerstraße",
        "Wasserwerk",
        "Goethestraße",
        "Gehe in Gefängnis",
        "Rathausplatz",
        "Hauptstraße",
        "Gemeinschaft 3",
        "Bahnhofstraße",
        "Hauptbahnhof",
        "Ereignis 3",
        "Parkstraße",
        "Zusatzsteuer",
        "Schlossallee",
    ]
)


def main(dice_rolls, iterations):
    @njit
    def roll_dice():
        first_dice = random.randint(1, 6)
        second_dice = random.randint(1, 6)
        return (first_dice + second_dice, first_dice == second_dice)

    @njit
    def simulation(dice_rolls):
        board_visited = np.zeros(NUM_FIELDS).astype(np.int32)
        position = 0
        j = 0

        # Karten mischen
        ereignis_karten_shuffle = EREIGNIS_KARTEN.copy()
        gemeinschaft_karten_shuffle = GEMEINSCHAFT_KARTEN.copy()
        np.random.shuffle(ereignis_karten_shuffle)
        np.random.shuffle(gemeinschaft_karten_shuffle)
        while j < dice_rolls:
            score, double = roll_dice()
            position += score
            position %= NUM_FIELDS
            board_visited[position] += 1

            # "Gehen Sie in das Gefängnis"
            if position == 30:
                position = 10
                board_visited[position] += 1

            # Ereigniskarte ziehen
            elif position in EREIGNIS:
                card, ereignis_karten_shuffle = (
                    ereignis_karten_shuffle[-1],
                    ereignis_karten_shuffle[:-1],
                )
                # Karte, die für Bewegung sorgt
                if card >= 0:
                    position = card
                    board_visited[position] += 1
                # Wenn Deck leer, neu mischen
                if len(ereignis_karten_shuffle) == 0:
                    ereignis_karten_shuffle = EREIGNIS_KARTEN.copy()
                    np.random.shuffle(ereignis_karten_shuffle)

            # Gemeinschaftkarte ziehen
            elif position in GEMEINSCHAFT:
                card, gemeinschaft_karten_shuffle = (
                    gemeinschaft_karten_shuffle[-1],
                    gemeinschaft_karten_shuffle[:-1],
                )
                # Karte, die für Bewegung sorgt
                if card >= 0:
                    position = card
                    board_visited[position] += 1
                # Wenn Deck leer, neu mischen
                if len(gemeinschaft_karten_shuffle) == 0:
                    gemeinschaft_karten_shuffle = GEMEINSCHAFT_KARTEN.copy()
                    np.random.shuffle(gemeinschaft_karten_shuffle)

            # Nächste Runde, wenn kein Pasch geworfen wurde
            if not double:
                j += 1
        return board_visited

    data = pd.DataFrame({"Straße": FELDER})
    for i in tqdm(range(iterations)):
        data[f"Lauf {i+1}"] = simulation(dice_rolls)
    data.to_csv("ergebnisse.csv", index=False)


if __name__ == "__main__":
    main(150, 50_000)
