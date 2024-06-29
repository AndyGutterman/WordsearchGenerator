import random
import tkinter as tk
from WordSearch import WordSearch
from WordSearchGUI import WordSearchGUI

class TestGUI(WordSearchGUI):
    def __init__(self):
        super().__init__()
        self.word_colors = {}
        self.highlighted_positions = []

    def highlight_all_word_positions_test(self):
        if self.word_search:
            all_positions = []
            for word in self.word_search.words:
                positions = self.word_search.find_word(word)
                if positions:
                    all_positions.extend(positions)
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
            if (row, col) in positions:
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

        self.check_highlighted_tiles()  # Corrected method name

    def assign_word_colors_test(self):
        highlight_colors = ['orange', 'cyan', 'lightgreen', 'lightblue', 'pink', 'green', 'blue', 'red', 'purple', 'violet', 'brown']
        random.shuffle(highlight_colors)

        for i, word in enumerate(self.word_search.words):
            color_index = i % len(highlight_colors)
            self.word_colors[word] = highlight_colors[color_index]

    def main_test(self):
        app = TestGUI()
        app.size_entry.insert(0, "8")
        app.set_size()
        app.auto_generate_words()
        app.highlight_all_word_positions_test()
        app.mainloop()

if __name__ == "__main__":
    TestGUI().main_test()
