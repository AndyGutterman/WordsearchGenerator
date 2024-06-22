from WordSearch import WordSearch
# todo track word location
# todo use word location to make sure words dont get
#  put on top of each other as you will see in runtest3
# todo system to keep track of found words

class TestWordSearch(WordSearch):
    def __init__(self, size, predefined_words):
        super().__init__(size)
        self.words = predefined_words



def run_test(size, predefined_words):
    test_word_search = TestWordSearch(size, predefined_words)
    test_word_search.place_words()
    test_word_search.fill_grid()
    test_word_search.show_game()

if __name__ == '__main__':
    tests = [
        (10, ["PYTHON", "JAVA", "RUBY", "CPLUSPLUS", "SWIFT", "JAVASCRIPT"]),
        (5, ["DOGGY", "FOGGY", "LOG", "COG", "DOG", "POG"]),
        (5, ["DOGGY", "DOGGY", "DOGGY", "DOGGY", "DOGGY"])
    ]

    for size, words in tests:
        run_test(size, words)