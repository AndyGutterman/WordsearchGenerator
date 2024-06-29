import random
import tkinter as tk
from WordSearch import WordSearch
from WordSearchGUI import WordSearchGUI

class TestGUI(WordSearchGUI):
    def __init__(self, grid_size):
        super().__init__()
        self.grid_size = grid_size
        self.word_colors = {}
        self.highlighted_positions = []
        self.found_words = []

    def highlight_all_word_positions_test(self):
        if self.word_search:
            self.found_words = []
            all_positions = []
            for word in self.word_search.words:
                positions = self.word_search.find_word(word)
                if positions:
                    all_positions.extend(positions)
                    self.found_words.append(word)
            self.assign_word_colors_test()

            def highlight_next_test(index=0):
                if index < len(all_positions):
                    row, col = all_positions[index]
                    label = self.grid_frame.grid_slaves(row=row, column=col)[0]
                    self.highlight_label_test(label, automated=True)
                    self.after(45, lambda idx=index + 1: highlight_next_test(idx))
                else:
                    self.check_highlighted_tiles()

            highlight_next_test()

    def get_word_at_position_test(self, row, col):
        for word in self.word_search.words:
            positions = self.word_search.find_word(word)
            if positions and (row, col) in positions:
                return word
        return None

    def highlight_label_test(self, label, automated=False):
        info = label.grid_info()
        row, col = info['row'], info['column']

        word = self.get_word_at_position_test(row, col)
        if word:
            word_color = self.word_colors.get(word, 'yellow')
            label.config(bg=word_color)

            if not automated:
                if (row, col) in self.highlighted_positions:
                    label.config(bg='SystemButtonFace')
                    self.highlighted_positions.remove((row, col))
                else:
                    label.config(bg=word_color)
                    self.highlighted_positions.append((row, col))
            else:
                self.highlighted_positions.append((row, col))

            label.bind("<Button-1>", lambda event, l=label: self.toggle_highlight_test(event, l))
        else:
            label.config(bg='SystemButtonFace')

    def toggle_highlight_test(self, event, label):
        info = label.grid_info()
        row, col = info['row'], info['column']

        if (row, col) in self.highlighted_positions:
            label.config(bg='SystemButtonFace')
            self.highlighted_positions.remove((row, col))
        else:
            label.config(bg='yellow')
            self.highlighted_positions.append((row, col))

        self.check_highlighted_tiles()

    def assign_word_colors_test(self):
        highlight_colors = ['orange', 'cyan', 'lightgreen', 'lightblue', 'pink', 'green', 'blue', 'red', 'purple', 'violet', 'brown']
        random.shuffle(highlight_colors)

        for i, word in enumerate(self.word_search.words):
            color_index = i % len(highlight_colors)
            self.word_colors[word] = highlight_colors[color_index]

    def main_test(self):
        self.size_entry.insert(0, str(self.grid_size))
        self.set_size()
        self.auto_generate_words()
        self.highlight_all_word_positions_test()
        self.uncheck_random_word()
        self.mainloop()

    def uncheck_random_word(self):
        if self.found_words:
            word_to_uncheck = random.choice(self.found_words)
            positions = self.word_search.find_word(word_to_uncheck)
            if positions:
                for pos in positions:
                    row, col = pos
                    label = self.grid_frame.grid_slaves(row=row, column=col)[0]
                    self.toggle_highlight_test(None, label)
                print(f"Unchecked word: {word_to_uncheck}")

def run_test(test_id, size, words):
    try:
        gui = TestGUI(size)
        gui.main_test()
        return gui.found_words == []
    except Exception as e:
        print(f"Test {test_id} failed with exception: {e}")
        return False

if __name__ == "__main__":
    tests = [(size, None) for size in range(3, 28)]
    successful_tests = []
    failed_tests = []

    for idx, (size, words) in enumerate(tests, start=1):
        test_id = f"test{idx}"
        if run_test(test_id, size, words):
            successful_tests.append(test_id)
        else:
            failed_tests.append(test_id)

    print("\nSummary:")
    print(f"Successful Tests: {successful_tests}")
    print(f"Failed Tests: {failed_tests}")
