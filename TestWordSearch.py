from WordSearch import WordSearch


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



if __name__ == '__main__':
    run_test()
    run_test()
    run_test()
    run_test()
    run_test()
    run_test1()
    run_test1()
    run_test1()
    run_test1()
    run_test1()