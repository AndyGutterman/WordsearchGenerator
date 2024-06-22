import random
from WordPlacer import WordPlacer


class WordSearch:
    def __init__(self, size):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.words = []

    def take_words(self):
        spaces_remaining = self.size * self.size

        while spaces_remaining > 0:
            word = input("Enter a word, 'done' when finished: ").upper()

            if word == 'DONE' or spaces_remaining < 0:
                break
            if len(word) <= self.size and len(word) <= spaces_remaining:
                self.words.append(word)
                spaces_remaining -= len(word)
                print(f"You have {spaces_remaining} characters left")
            else:
                print("The word you've typed is too large, please choose another word")

    def place_words(self):
        self.words.sort(key=len, reverse=True)

        attempts = 0
        while attempts < 1000:
            words_placed = 0
            if attempts > 0:
                self.grid = [[0] * self.size for _ in range(self.size)]

            limit_r = random.randint(1, 2)
            limit_words = sum(1 for word in self.words if len(word) == self.size)
            if limit_words > 1:
                print(f"There are {limit_words} words with length equal to the size of the array.")
            try:
                for word in self.words:
                    letters = list(word)
                    placed = False
                    while not placed:
                        if (limit_words > 1):
                            r = limit_r
                            limit_words -= 1
                        else:
                            r = random.randint(1, 3)
                        if r == 1:
                            placed = WordPlacer.place_vertical(self.grid, letters, self.size)
                            if placed:
                                print(word + " placed vertically")
                                words_placed += 1
                        elif r == 2:
                            placed = WordPlacer.place_horizontal(self.grid, letters, self.size)
                            if placed:
                                print(word + " placed horizontally")
                                words_placed += 1
                        elif r == 3:
                            placed = WordPlacer.place_diagonal(self.grid, letters, self.size)
                            if placed:
                                print(word + " placed diagonally")
                                words_placed += 1
                        if placed:
                            break

                if words_placed == len(self.words):
                    print("Done on attempt no:", attempts)
                    return

            except Exception as e:
                print(f"Error occurred during word placement: {e}")

            attempts += 1
            print("New attempt")

        print("Failed to place all words after multiple attempts. Restarting...")

    def fill_grid(self):
        for row in self.grid:
            for i in range(len(row)):
                if row[i] == 0:
                    randchar = chr(random.randint(65, 90))
                    row[i] = randchar

    def show_game(self):
        print("\n\nWord Search:")
        for row in self.grid:
            print(" ".join(str(element) for element in row))
        for word in self.words:
            print(word)

    def txt_print(self):
        file_name = input("Enter a filename:\n>>> ")
        with open(file_name + ".txt", 'w') as f:
            for row in self.grid:
                f.write('\n')
                for x in row:
                    f.write(' ' + str(x))
            f.write('\n\n')
            f.write('WORDBANK' + '\n')
            for word in self.words:
                f.write(word + '\n')
        print(file_name + ".txt created")


def customize():
    size = int(input("Enter a size for the wordSearch:\n>>> "))
    word_search = WordSearch(size)
    word_search.take_words()
    return word_search


if __name__ == '__main__':
    word_search = customize()
    word_search.place_words()
    word_search.fill_grid()
    word_search.show_game()
    word_search.txt_print()
