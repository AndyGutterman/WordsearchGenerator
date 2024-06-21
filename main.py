import random


def takeWords():
    words = []
    spacesRemaining = size * size
    while spacesRemaining > 0:  # Take word from user and add to list, stopping at done
        word = input("Enter a word, 'done' when finished:")
        word = word.upper()  # Convert word to uppercase
        if word == 'DONE' or spacesRemaining < 0:  # Break loop if user is done
            break
        if len(word) <= size & len(word) <= spacesRemaining:  # Ensures word is small enough to fit
            words.append(word)
            spacesRemaining = spacesRemaining - len(word)
            print("You have " + str(spacesRemaining) + "characters left")
        else:
            print("The word you've typed is too large, please choose another word")
    return words


def place_Diagonal(letters, size, wordsearch, max_attempts=1000):
    attempts = 0
    while attempts < max_attempts:
        can_place_word = True
        row_num = random.randint(0, size - len(letters))
        column_num = random.randint(0, size - len(letters))

        for i in range(len(letters)):
            current_char = wordsearch[row_num + i][column_num + i]
            if current_char != 0 and current_char != letters[i]:
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
        intersections = 0

        for i in range(len(letters)):
            current_char = wordsearch[row_num][column_num + i]
            if current_char != 0 and current_char != letters[i]:
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
            current_char = wordsearch[row_num + i][column_num]
            if current_char != 0 and current_char != letters[i]:
                can_place_word = False
                break

        if can_place_word:
            for i in range(len(letters)):
                wordsearch[row_num + i][column_num] = letters[i]
            return True
        attempts += 1
    return False

def placeWords(wordSearch, fullWords):
    size = len(wordSearch)
    fullWords.sort(key=len, reverse=True)  # Sort words by length in descending order

    LimitWords = 0
    for word in fullWords:
        if len(word) == size:
            LimitWords += 1

    if LimitWords > 1:
        print(f"There are {LimitWords} words with length equal to the size of the array.")
        for word in fullWords:
            letters = list(word)
            placed = False
            while not placed:
                r = random.randint(1, 2)
                if r == 1:
                    placed = place_vertical(letters, size, wordSearch)
                    if placed:
                        print(word + " placed vertically")
                elif r == 2:
                    placed = place_horizontal(letters, size, wordSearch)
                    if placed:
                        print(word + " placed horizontally")
    else:
        for word in fullWords:
            letters = list(word)
            placed = False
            while not placed:
                r = random.randint(1, 3)
                if r == 1:
                    placed = place_vertical(letters, size, wordSearch)
                    if placed:
                        print(word + " placed vertically")
                elif r == 2:
                    placed = place_horizontal(letters, size, wordSearch)
                    if placed:
                        print(word + " placed horizontally")
                elif r == 3:
                    placed = place_Diagonal(letters, size, wordSearch)
                    if placed:
                        print(word + " placed diagonally")


def fill_grid(wordSearch):  # Fill spaces with value '0' with random characters
    for row in wordSearch:
        for i in range(len(row)):
            if row[i] == 0:
                randchar = chr(random.randint(65, 90))
                row[i] = randchar


def grid_print(wordSearch):
    print("\n\nWord Search:")
    for row in wordSearch:
        elements_to_print = []
        for element in row:
            if element == "1":
                elements_to_print.append("\033[1;32m" + element + "\033[0m")
            else:
                elements_to_print.append(element)
        row_string = " ".join(str(element) for element in elements_to_print)
        print(row_string)


if __name__ == '__main__':
    size = int(input("Enter a size for the wordSearch:\n>>> "))
    wordSearch = [[0] * size for i in range(size)]
    words = takeWords()
    placeWords(wordSearch, words)
    fill_grid(wordSearch)
    grid_print(wordSearch)
