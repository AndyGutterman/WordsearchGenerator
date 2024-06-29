import os
import random
from WordPlacer import WordPlacer

class WordSearch:
    def __init__(self, size=None):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.words = []
        self.word_locations = {}  # Stores word locations
        self.occupied_positions = set()

    def set_size(self, size):
        self.size = size

    def take_words(self):
        spaces_remaining = self.size * self.size

        while spaces_remaining > 0:
            word = input("Enter a word, 'done' if finished, 'auto' to auto-generate remaining:").strip().upper()
            if word == 'DONE' or spaces_remaining <= 0:
                break
            if word == 'AUTO':
                self.generate_words(spaces_remaining)
                break

            if len(word) <= self.size and len(word) <= spaces_remaining:
                self.words.append(word)
                spaces_remaining -= len(word)
                print(f"You have {spaces_remaining} characters left")
            else:
                print("The word you've typed is too large, please choose another word")

    def generate_words(self, spaces_remaining):
        current_density = (self.size * self.size - spaces_remaining) / (self.size * self.size)
        desired_density = 0.5 + 0.25 * (self.size / 30)
        spaces_to_generate = int((desired_density - current_density) * self.size * self.size)

        if spaces_to_generate <= 0:
            return

        # Adjust max word length based on grid size
        max_word_length = min(self.size, 22)

        while spaces_to_generate > 0:
            min_word_size = 3 if self.size >= 3 else (1 if self.size == 1 else 2)
            if spaces_to_generate < min_word_size:
                break

            # Randomly select a word length within the adjusted limits
            word_length = random.randint(min_word_size, min(max_word_length, spaces_to_generate))
            word = self.generate_word(word_length)
            if word:
                self.words.append(word)
                spaces_to_generate -= len(word)

            if spaces_remaining <= 0:
                break

    def generate_word(self, length):
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        wordlist_path = os.path.join(data_dir, 'wordlist.txt')
        try:
            with open(wordlist_path, 'r') as f:
                all_words = f.read().splitlines()
                cleaned_words = [word.replace('-', '').replace("'", '').upper() for word in all_words]
                filtered_words = [word for word in cleaned_words if len(word) == length and word not in self.words]
                return random.choice(filtered_words) if filtered_words else None
        except FileNotFoundError:
            print(f"Error: File '{wordlist_path}' not found.")
            return None

    def place_words(self):
        self.words.sort(key=len, reverse=True)
        max_spaces = self.size ** 2
        big_words_count = sum(1 for word in self.words if len(word) == self.size)
        current_grid_state = [row[:] for row in self.grid]
        try:
            for word in self.words:
                if word in self.word_locations:
                    continue
                letters = list(word)
                placed = False
                attempts = 0
                max_attempts = 1000
                while not placed and attempts < max_attempts:
                    if big_words_count >= 1:
                        r = random.randint(1, 2)
                    else:
                        r = random.randint(1, 4)    # 3 and 4 both diagonal
                    if r == 1:
                        direction = "vertical"
                    elif r == 2:
                        direction = "horizontal"
                    elif r == 3 or r == 4:
                        direction = "diagonal"
                    placed = WordPlacer.place(self, letters, max_spaces, direction)
                    if placed:
                        big_words_count -= 1
                        self.word_locations.setdefault(tuple(letters), [])
                        attempts = 0
                    else:
                        attempts += 1
                if not placed:
                    print(f"Failed to place word '{word}' after {max_attempts} attempts.")

        except Exception as e:
            print(f"Error occurred during word placement: {e}")
            self.grid = current_grid_state  # Revert to previous grid state

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
                if word in self.word_locations:
                    f.write(f"Locations: {self.word_locations[word][0][3]}\n")  # Writing letter positions

        print(f"{file_name}.txt created")

    def print_word_locations(self):
        printed_words = set()
        for word in self.words:
            if tuple(word) in self.word_locations and word not in printed_words:
                placements = self.word_locations[tuple(word)]
                for start, direction in placements:
                    try:
                        print(f"{word}: Row/Col {start}, Direction {direction}")
                    except IndexError as e:
                        print(f"Error printing {word}: {e}")
                printed_words.add(word)
            elif word not in printed_words:
                print(f"{word}: Not placed")
                printed_words.add(word)

    def find_word(self, word):
        word_length = len(word)
        directions = [
            (0, 1),    # horizontal
            (1, 0),    # vertical
            (1, 1),    # diagonal \
            (-1, 1)    # diagonal /
        ]
        found_positions = []
        for row in range(self.size):
            for col in range(self.size):
                for dr, dc in directions:
                    word_end_row = row + (word_length - 1) * dr
                    word_end_col = col + (word_length - 1) * dc

                    # Ensure ending row and column is within bounds
                    if 0 <= word_end_row < self.size and 0 <= word_end_col < self.size:
                        # If all letters match letters in word, add to found_positions list
                        if all(self.grid[row + i * dr][col + i * dc] == word[i] for i in range(word_length)):
                            positions = [(row + i * dr, col + i * dc) for i in range(word_length)]
                            found_positions.extend(positions)

        return found_positions if found_positions else None


def customize():
    size = abs(int(input("Enter a size for the wordSearch:\n>>> ")))
    if size == 0:
        return WordSearch(size)
    wordsearch = WordSearch(size)
    wordsearch.take_words()
    return wordsearch


def main():
    word_search = customize()
    word_search.place_words()
    word_search.fill_grid()
    word_search.show_grid()
    word_search.show_wordbank()
    word_search.txt_print()
    word_search.print_word_locations()

if __name__ == "__main__":
    main()
