from WordSearch import WordSearch
# todo track word location
# todo use word location to make sure words dont get
#  put on top of each other as you will see in runtest3
# todo system to keep track of found words

class TestWordSearch(WordSearch):
    def __init__(self, size, predefined_words):
        super().__init__(size)
        self.words = predefined_words



def run_test():
    size = 10
    predefined_words = ["PYTHON", "JAVA", "RUBY", "CPLUSPLUS", "SWIFT", "JAVASCRIPT"]
    test_word_search = TestWordSearch(size, predefined_words)
    test_word_search.place_words()
    test_word_search.fill_grid()
    test_word_search.show_game()
    # test_word_search.txt_print()

def run_test1():
    size = 5
    predefined_words = ["DOGGY", "FOGGY", "LOG", "COG", "DOG", "POG"]
    test_word_search = TestWordSearch(size, predefined_words)
    test_word_search.place_words()
    test_word_search.fill_grid()
    test_word_search.show_game()

def run_test2():
    size = 5
    predefined_words = ["DOGGY", "DOGGY", "DOGGY", "DOGGY", "DOGGY"]
    test_word_search = TestWordSearch(size, predefined_words)
    test_word_search.place_words()
    test_word_search.fill_grid()
    test_word_search.show_game()


if __name__ == '__main__':
    run_test()
    run_test()
    run_test()
    run_test1()
    run_test1()
    run_test1()
    run_test2()
    run_test2()