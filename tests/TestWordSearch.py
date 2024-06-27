from src.WordSearch import WordSearch


class TestWordSearch(WordSearch):
    def __init__(self, size, predefined_words=None):
        super().__init__(size)
        if predefined_words:
            self.words = predefined_words




def run_test(test_id, size, predefined_words=None):
    if predefined_words:
        test_word_search = TestWordSearch(size, predefined_words)
    else:
        test_word_search = TestWordSearch(size)
        test_word_search.generate_words(int(0.75 * size * size))

    try:
        test_word_search.place_words()
        test_word_search.fill_grid()
        test_word_search.show_grid()
        test_word_search.print_word_locations()
        return True
    except Exception as e:
        print(f"Test {test_id} failed with error: {e}")
        return False


if __name__ == '__main__':
    tests = [
        (5, ["DOG", "CAT", "MOUSE"]),
        (10, ["PYTHON", "JAVA", "RUBY", "CPLUSPLUS", "SWIFT", "JAVASCRIPT"]),
        (5, ["DOGGY", "FOGGY", "LOG", "COG", "DOG", "POG"]),
        (7, ["22222", "11111", "11121", "11111", "123456", "515", "515"]),
        (6, ["RED", "GREEN", "BLUE", "YELLOW"]),
        (5, ["DOGGY", "DOGGY", "DOGGY", "DOGGY", "DOGGY"]),
    ]


    for i in range(3, 28):
        tests.append((i, None))

    successful_tests = []
    failed_tests = []

    for idx, (size, words) in enumerate(tests, start=1):
        test_id = f"test{idx}"
        try:
            if run_test(test_id, size, words):
                successful_tests.append(test_id)
            else:
                failed_tests.append(test_id)
        except Exception as e:
            print(f"Test {test_id} failed with exception: {e}")
            failed_tests.append(test_id)

    print("\nSummary:")
    print(f"Successful Tests: {successful_tests}")
    print(f"Failed Tests: {failed_tests}")
