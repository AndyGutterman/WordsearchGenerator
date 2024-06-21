import random

def fill_grid(wordsearch):  # Fill spaces with value '0' with random characters
    for row in wordsearch:
        for i in range(len(row)):
            if row[i] == 0:
                randchar = chr(random.randint(65, 90))
                row[i] = randchar

def grid_print(wordsearch):
    print("\n\nWord Search:")
    for row in wordsearch:
        elements_to_print = []
        for element in row:
            if element == "1":
                elements_to_print.append("\033[1;32m" + element + "\033[0m")
            else:
                elements_to_print.append(element)
        row_string = " ".join(str(element) for element in elements_to_print)
        print(row_string)

def place_Diagonal(letters, size, wordsearch, max_attempts=1000):
    attempts = 0
    while attempts < max_attempts:
        can_place_word = True
        row_num = random.randint(0, size - len(letters))
        column_num = random.randint(0, size - len(letters))

        for i in range(len(letters)):
            if wordsearch[row_num + i][column_num + i] not in (0, letters[i]):
                can_place_word = False
                break

        if can_place_word:
            for i in range(len(letters)):
                wordsearch[row_num + i][column_num + i] = letters[i]
            return True
        attempts += 1
    return False

def place_horizontal(letters, size, wordsearch, max_attempts=1000):
    attempts = 0
    while attempts < max_attempts:
        can_place_word = True
        row_num = random.randint(0, size - 1)
        column_num = random.randint(0, size - len(letters))

        for i in range(len(letters)):
            if wordsearch[row_num][column_num + i] not in (0, letters[i]):
                can_place_word = False
                break

        if can_place_word:
            for i in range(len(letters)):
                wordsearch[row_num][column_num + i] = letters[i]
            return True
        attempts += 1
    return False

def place_vertical(letters, size, wordsearch, max_attempts=1000):
    attempts = 0
    while attempts < max_attempts:
        can_place_word = True
        row_num = random.randint(0, size - len(letters))
        column_num = random.randint(0, size - 1)

        for i in range(len(letters)):
            if wordsearch[row_num + i][column_num] not in (0, letters[i]):
                can_place_word = False
                break

        if can_place_word:
            for i in range(len(letters)):
                wordsearch[row_num + i][column_num] = letters[i]
            return True
        attempts += 1
    return False

def placeWords(wordsearch, words):
    size = len(wordsearch)
    words.sort(key=len, reverse=True)  # Sort words by length in descending order

    LimitWords = 0
    for word in words:
        if len(word) == size:
            LimitWords += 1

    if LimitWords > 1:
        print(f"There are {LimitWords} words with length equal to the size of the array.")
        for word in words:
            letters = list(word)
            placed = False
            while not placed:
                r = random.randint(1, 2)
                if r == 1:
                    placed = place_vertical(letters, size, wordsearch)
                    if placed:
                        print(word + " placed vertically")
                elif r == 2:
                    placed = place_horizontal(letters, size, wordsearch)
                    if placed:
                        print(word + " placed horizontally")
    else:
        for word in words:
            letters = list(word)
            placed = False
            while not placed:
                r = random.randint(1, 3)
                if r == 1:
                    placed = place_vertical(letters, size, wordsearch)
                    if placed:
                        print(word + " placed vertically")
                elif r == 2:
                    placed = place_horizontal(letters, size, wordsearch)
                    if placed:
                        print(word + " placed horizontally")
                elif r == 3:
                    placed = place_Diagonal(letters, size, wordsearch)
                    if placed:
                        print(word + " placed diagonally")

if __name__ == '__main__':
    size = 5
    wordsearch = [[0] * size for i in range(size)]
    words = ["TOOLS", "FOOLS", "COOL"]

    placeWords(wordsearch, words)
    fill_grid(wordsearch)
    grid_print(wordsearch)
