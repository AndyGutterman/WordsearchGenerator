import random


class WordPlacer:
    @staticmethod
    def place_diagonal(word_search, letters, max_attempts=1000):
        grid = word_search.grid
        size = word_search.size

        attempts = 0
        while attempts < max_attempts:
            row_num = random.randint(0, size - len(letters))
            column_num = random.randint(0, size - len(letters))
            can_place_word = all(grid[row_num + i][column_num + i] in [0, letters[i]] for i in range(len(letters)))

            if can_place_word:
                for i in range(len(letters)):
                    grid[row_num + i][column_num + i] = letters[i]
                return True
            attempts += 1
        return False

    @staticmethod
    def place_horizontal(word_search, letters, max_attempts=1000):
        grid = word_search.grid
        size = word_search.size

        attempts = 0
        while attempts < max_attempts:
            row_num = random.randint(0, size - 1)
            column_num = random.randint(0, size - len(letters))
            can_place_word = all(grid[row_num][column_num + i] in [0, letters[i]] for i in range(len(letters)))
            if can_place_word:
                for i in range(len(letters)):
                    grid[row_num][column_num + i] = letters[i]
                return True
            attempts += 1
        return False

    @staticmethod
    def place_vertical(word_search, letters, max_attempts=1000):
        grid = word_search.grid
        size = word_search.size

        attempts = 0
        while attempts < max_attempts:
            row_num = random.randint(0, size - len(letters))
            column_num = random.randint(0, size - 1)
            can_place_word = all(grid[row_num + i][column_num] in [0, letters[i]] for i in range(len(letters)))

            if can_place_word:
                for i in range(len(letters)):
                    grid[row_num + i][column_num] = letters[i]
                return True
            attempts += 1
        return False
