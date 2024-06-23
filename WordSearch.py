import random
from Helpers.WordPlacer import WordPlacer

class WordSearch:
    def __init__(self, size):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.words = []
        self.word_locations = {}

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
        big_words_count = sum(1 for word in self.words if len(word) == self.size)
        print(f"Number of words as big as the grid size ({self.size}): {big_words_count}")
        r_big = random.randint(1, 2);
        attempts = 0
        while attempts < 1:
            words_placed = 0

            current_grid_state = [row[:] for row in self.grid]  # Snapshot of current grid state
            try:
                for word in self.words:
                    if word in self.word_locations:  # Skip already placed words
                        continue
                    letters = list(word)
                    placed = False
                    while not placed:
                        if (big_words_count >= 1):
                            r = r_big;
                        r = random.randint(1, 3)
                        if r == 1:
                            placed = WordPlacer.place_vertical(self, letters)
                        elif r == 2:
                            placed = WordPlacer.place_horizontal(self, letters)
                        elif r == 3:
                            placed = WordPlacer.place_diagonal(self, letters)

                    if placed:
                        words_placed += 1
                        big_words_count -= 1;
                        self.word_locations.setdefault(tuple(letters), [])  # Ensure key exists in dict

                if words_placed == len(self.words):
                    print("Done on attempt no:", attempts)
                    return

            except Exception as e:
                print(f"Error occurred during word placement: {e}")
                self.grid = current_grid_state  # Revert to previous grid state
                attempts += 1

            attempts += 1
            print("New attempt")

        print("Failed to place all words after multiple attempts. Restarting...")

    def fill_grid(self):
        for row in self.grid:
            for i in range(len(row)):
                if row[i] == 0:
                    randchar = chr(random.randint(65, 90))
                    row[i] = randchar

    def show_grid(self):
        print("\n\nWord Search:")
        for row in self.grid:
            print(" ".join(str(element) for element in row))

    def show_wordbank(self):
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
        print(f"{file_name}.txt created")

    def print_word_locations(self):
        printed_words = set()  # To keep track of words already printed
        for word in self.words:
            if tuple(word) in self.word_locations and word not in printed_words:
                placements = self.word_locations[tuple(word)]
                for start, direction in placements:
                    print(f"{word}: Row/Col {start}, Direction {direction}")
                printed_words.add(word)  # Add word to printed set
            elif word not in printed_words:
                print(f"{word}: Not placed")
                printed_words.add(word)  # Add word to printed set


def customize():
    size = abs(int(input("Enter a size for the wordSearch:\n>>> ")))
    if size == 0:
        return WordSearch(size)
    word_search = WordSearch(size)
    word_search.take_words()
    return word_search


if __name__ == '__main__':
    word_search = customize()
    word_search.place_words()
    word_search.fill_grid()
    word_search.show_grid()
    word_search.show_wordbank()
    word_search.txt_print()
