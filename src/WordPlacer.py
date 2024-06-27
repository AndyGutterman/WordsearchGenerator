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

            if WordPlacer.can_place_diagonal(grid, row_num, column_num, letters):
                for i in range(len(letters)):
                    grid[row_num + i][column_num + i] = letters[i]
                start = (row_num, column_num)
                end = (row_num + len(letters) - 1, column_num + len(letters) - 1)
                direction = "diagonal"
                if not WordPlacer.check_existing_placement(word_search, letters, start, direction):
                    word_search.word_locations.setdefault(tuple(letters), []).append((start, end, direction))
                    return True, start, end
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

            if WordPlacer.can_place_horizontal(grid, row_num, column_num, letters):
                for i in range(len(letters)):
                    grid[row_num][column_num + i] = letters[i]
                start = (row_num, column_num)
                end = (row_num, column_num + len(letters) - 1)
                direction = "horizontal"
                if not WordPlacer.check_existing_placement(word_search, letters, start, direction):
                    word_search.word_locations.setdefault(tuple(letters), []).append((start, end, direction))
                    return True, start, end
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

            if WordPlacer.can_place_vertical(grid, row_num, column_num, letters):
                for i in range(len(letters)):
                    grid[row_num + i][column_num] = letters[i]
                start = (row_num, column_num)
                end = (row_num + len(letters) - 1, column_num)
                direction = "vertical"
                if not WordPlacer.check_existing_placement(word_search, letters, start, direction):
                    word_search.word_locations.setdefault(tuple(letters), []).append((start, end, direction))
                    return True, start, end
            attempts += 1
        return False

    @staticmethod
    def can_place_diagonal(grid, row_num, column_num, letters):
        size = len(letters)
        if row_num + size > len(grid) or column_num + size > len(grid):
            return False

        return all(grid[row_num + i][column_num + i] in [0, letters[i]] for i in range(size))

    @staticmethod
    def can_place_horizontal(grid, row_num, column_num, letters):
        size = len(letters)
        if column_num + size > len(grid[row_num]):
            return False

        return all(grid[row_num][column_num + i] in [0, letters[i]] for i in range(size))

    @staticmethod
    def can_place_vertical(grid, row_num, column_num, letters):
        size = len(letters)
        if row_num + size > len(grid):
            return False

        return all(grid[row_num + i][column_num] in [0, letters[i]] for i in range(size))

    @staticmethod
    def check_existing_placement(word_search, letters, start, direction):
        if tuple(letters) in word_search.word_locations:
            placements = word_search.word_locations[tuple(letters)]
            for (existing_start, end, existing_direction) in placements:
                if existing_start == start and existing_direction == direction:
                    return True
        return False
