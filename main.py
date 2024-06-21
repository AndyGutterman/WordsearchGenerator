from random import random


def fill_grid(wordsearch):  # Fill spaces with value '0' with random characters
    for row in wordsearch:
        for i in range(len(row)):
            if row[i] == 0:
                randchar = chr(random.randint(65, 90))
                row[i] = randchar


if __name__ == '__main__':
    size = 5
    wordsearch = [[0] * size for i in range(size)]
    wordsToFind = ["TOOLS", "FOOL", "COOL"]
