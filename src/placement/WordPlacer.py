import random

class WordPlacer:
    @staticmethod
    def place_words(word_search):
        word_search.words.sort(key=len, reverse=True)
        max_spaces = word_search.size ** 2
        big_words_count = sum(1 for word in word_search.words if len(word) == word_search.size)
        current_grid_state = [row[:] for row in word_search.grid]
        try:
            for word in word_search.words:
                if word in word_search.word_locations:
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
                    placed = WordPlacer.place(word_search, letters, max_spaces, direction)
                    if placed:
                        big_words_count -= 1
                        word_search.word_locations.setdefault(tuple(letters), [])
                        attempts = 0
                    else:
                        attempts += 1
                if not placed:
                    print(f"Failed to place word '{word}' after {max_attempts} attempts.")

        except Exception as e:
            print(f"Error occurred during word placement: {e}")
            word_search.grid = current_grid_state  # Revert to previous grid state

    @staticmethod
    def place(word_search, letters, max_attempts, direction):
        grid = word_search.grid
        size = word_search.size

        attempts = 0
        while attempts < max_attempts:
            if direction == "diagonal":
                row_num = random.randint(0, size - len(letters))
                column_num = random.randint(0, size - len(letters))
                if WordPlacer.can_place(grid, row_num, column_num, letters, direction):
                    for i in range(len(letters)):
                        grid[row_num + i][column_num + i] = letters[i]
                    start = (row_num, column_num)
            elif direction == "horizontal":
                row_num = random.randint(0, size - 1)
                column_num = random.randint(0, size - len(letters))
                if WordPlacer.can_place(grid, row_num, column_num, letters, direction):
                    for i in range(len(letters)):
                        grid[row_num][column_num + i] = letters[i]
                    start = (row_num, column_num)
            elif direction == "vertical":
                row_num = random.randint(0, size - len(letters))
                column_num = random.randint(0, size - 1)
                if WordPlacer.can_place(grid, row_num, column_num, letters, direction):
                    for i in range(len(letters)):
                        grid[row_num + i][column_num] = letters[i]
                    start = (row_num, column_num)
            else:
                return False  # Invalid direction

            if 'start' in locals():
                if not WordPlacer.check_existing_placement(word_search, letters, start, direction):
                    word_search.word_locations.setdefault(tuple(letters), []).append((start, direction))
                    return True
            attempts += 1

        return False

    @staticmethod
    def can_place(grid, row_num, column_num, letters, direction):
        size = len(letters)
        if direction == "diagonal":
            if row_num + size > len(grid) or column_num + size > len(grid):
                return False
            return all(grid[row_num + i][column_num + i] in [0, letters[i]] for i in range(size))
        elif direction == "horizontal":
            if column_num + size > len(grid[row_num]):
                return False
            return all(grid[row_num][column_num + i] in [0, letters[i]] for i in range(size))
        elif direction == "vertical":
            if row_num + size > len(grid):
                return False
            return all(grid[row_num + i][column_num] in [0, letters[i]] for i in range(size))
        else:
            return False  # Invalid direction

    @staticmethod
    def check_existing_placement(word_search, letters, start, direction):
        if tuple(letters) in word_search.word_locations:
            placements = word_search.word_locations[tuple(letters)]
            for (existing_start, existing_direction) in placements:
                if existing_start == start and existing_direction == direction:
                    return True
        return False
