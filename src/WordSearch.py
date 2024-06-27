import random
from src.WordPlacer import WordPlacer  # Assuming WordPlacer is defined elsewhere


class WordSearch:
    def __init__(self, size=None):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.words = []
        self.word_locations = {}
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
        desired_density = 0.75
        spaces_to_generate = int((desired_density - current_density) * self.size * self.size)

        if spaces_to_generate <= 0:
            return

        min_word_size = 3 if self.size > 3 else 1

        while spaces_to_generate > 0:
            if spaces_to_generate < min_word_size:
                break

            word_length = random.randint(min_word_size, min(self.size, spaces_to_generate, 22))
            word = self.generate_word(word_length)
            self.words.append(word)
            spaces_to_generate -= len(word)

            if spaces_remaining <= 0:
                break

    def generate_word(self, length):
        with open('../data/wordlist.txt', 'r') as f:
            all_words = f.read().splitlines()
            cleaned_words = [word.replace('-', '').replace("'", '').upper() for word in all_words]
            filtered_words = [word for word in cleaned_words if len(word) == length]
            return random.choice(filtered_words) if filtered_words else None

    def place_words(self):
        self.words.sort(key=len, reverse=True)
        big_words_count = sum(1 for word in self.words if len(word) == self.size)
        print(f"Number of words as big as the grid size ({self.size}): {big_words_count}")
        r_big = random.randint(1, 2)
        current_grid_state = [row[:] for row in self.grid]  # Snapshot of current grid state

        try:
            for word in self.words:
                if word in self.word_locations:
                    continue
                letters = list(word)
                placed = False
                while not placed:
                    if (big_words_count >= 1):
                        r = r_big
                    else:
                        r = random.randint(1, 3)
                    if r == 1:
                        result = WordPlacer.place_vertical(self, letters)
                        if result:
                            placed, start, end = result
                            self.word_locations[word] = [(start, end, 'vertical')]
                    elif r == 2:
                        result = WordPlacer.place_horizontal(self, letters)
                        if result:
                            placed, start, end = result
                            self.word_locations[word] = [(start, end, 'horizontal')]
                    elif r == 3:
                        result = WordPlacer.place_diagonal(self, letters)
                        if result:
                            placed, start, end = result
                            self.word_locations[word] = [(start, end, 'diagonal')]

                    if placed:
                        big_words_count -= 1

        except Exception as e:
            print(f"Error occurred during word placement: {e}")
            self.grid = current_grid_state

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
        for word in self.words:
            if word in self.word_locations:
                placements = self.word_locations[word]
                for start, end, direction in placements:
                    print(f"{word}: Row/Col {start}, Direction {direction} to {end}")
            else:
                print(f"{word}: Not placed")


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
    #ord_search.print_word_locations()
    word_search.txt_print()
