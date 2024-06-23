from WordSearch import WordSearch

class TestWordSearch(WordSearch):
    def __init__(self, size, predefined_words):
        super().__init__(size)
        self.words = predefined_words


def run_test(test_id, size, predefined_words):
    test_word_search = TestWordSearch(size, predefined_words)
    try:
        test_word_search.place_words()
        test_word_search.fill_grid()
        test_word_search.show_grid()
        test_word_search.print_word_locations()
    except Exception as e:
        print(f"Test {test_id} failed with error: {e}")

if __name__ == '__main__':
    tests = [
        ("test1", 10, ["PYTHON", "JAVA", "RUBY", "CPLUSPLUS", "SWIFT", "JAVASCRIPT"]),
        ("test2", 5, ["DOGGY", "FOGGY", "LOG", "COG", "DOG", "POG"]),
        ("test3", 5, ["DOGGY", "DOGGY", "DOGGY", "DOGGY", "DOGGY"]),
        ("test4", 7, ["22222", "11111", "11121", "11111", "123456", "515", "515"]),
        ("test5", 3, ["HELLO", "WORLD", "PYTHON"]),
        ("test6", 4, ["RED", "GREEN", "BLUE", "YELLOW"]),
        ("test7", 6, ["APPLE", "ORANGE", "BANANA", "GRAPE", "PEAR", "KIWI"]),
        ("test8", 2, ["CAR", "BIKE"]),
        ("test9", 5, ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]),
        ("test10", 4, ["SUN", "MOON", "STAR", "PLANET"]),
        ("test11", 0, ["ZERO"]),
        ("test12", -1, ["NEGATIVE"]),
        ("test13", 3, []),
        ("test14", "invalid", ["INVALID"]),
        ("test15", 4, ["VALID", "LIST", "WITH", 12345])
    ]

    for test_id, size, words in tests:
        try:
            run_test(test_id, size, words)
        except Exception as e:
            print(f"Test {test_id} failed with error: {e}")
