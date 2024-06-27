import tkinter as tk
from tkinter import messagebox
from WordSearch import WordSearch
import math

# todo Add reset button
# todo Add text file output

class WordSearchGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Word Search Generator")
        self.word_search = None
        self.label_frame = None
        self.label_size = None
        self.enter_button = None
        self.size_entry = None
        self.size_button = None
        self.output_text = None
        self.word_entry = None
        self.auto_button = None
        self.done_button = None
        self.initialize_gui()

    def initialize_gui(self):
        self.label_frame = tk.Frame(self, pady=10)
        self.label_frame.pack()

        self.label_size = tk.Label(self.label_frame, text="Enter grid size:")
        self.label_size.pack(side=tk.LEFT, padx=(0, 20))

        self.size_entry = tk.Entry(self.label_frame, width=10, justify='center')
        self.size_entry.pack(side=tk.LEFT, padx=(0, 20))
        self.size_entry.bind("<Return>", self.set_size)

        self.size_button = tk.Button(self.label_frame, text="Set", command=self.set_size)
        self.size_button.pack(side=tk.LEFT)

        self.output_text = tk.Text(self, height=10, width=40)  # Initial size
        self.output_text.pack(pady=10)

    def set_size(self):
        try:
            size = int(self.size_entry.get().strip())
            if size <= 0:
                messagebox.showerror("Error", "Size must be a positive integer.")
                return

            # Update size of text widget based on grid size (within limits)
            text_height = min(max(size * 2, 10), 30)
            text_width = min(max(size * 4, 40), 80)
            self.output_text.config(height=text_height, width=text_width)

            self.word_search = WordSearch(size)
            self.take_words_gui()

            # Disable after setting size
            self.size_entry.config(state=tk.DISABLED)
            self.size_button.config(state=tk.DISABLED)

            # Clear prev.  output
            self.output_text.delete(1.0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Invalid size. Please enter a valid integer.")

    def take_words_gui(self):
        self.word_entry = tk.Entry(self, justify='center')
        self.word_entry.insert(0, 'click to enter word')
        self.word_entry.bind("<FocusIn>", lambda args: self.word_entry.delete(0, 'end'))
        self.word_entry.pack()
        self.word_entry.bind("<Return>", self.add_word)  # Bind Enter key to add_word

        self.enter_button = tk.Button(self, text="Add Word", command=self.add_word)
        self.enter_button.pack(pady=6)

        button_frame = tk.Frame(self)
        button_frame.pack(padx=8, pady=10)

        self.auto_button = tk.Button(button_frame, text="Auto", command=self.auto_generate_words)
        self.auto_button.pack(side=tk.LEFT, padx=(0, 10))

        self.done_button = tk.Button(button_frame, text="Done", command=self.create)
        self.done_button.pack(side=tk.LEFT, padx=(10, 0))

    def create(self):
        self.word_search.place_words()
        self.word_search.fill_grid()
        self.show_word_search()
        self.show_wordbank()

    def add_word(self):
        word = self.word_entry.get().strip().upper()
        if word == 'DONE':
            self.create()
        elif word == 'AUTO':
            self.auto_generate_words()
        elif len(word) <= self.word_search.size and len(word) <= self.word_search.size * self.word_search.size - sum(
                len(w) for w in self.word_search.words):
            self.word_search.words.append(word)
            self.output_text.insert(tk.END, f"Added word: {word}\n")
            remaining_spaces = self.word_search.size * self.word_search.size - sum(
                len(w) for w in self.word_search.words)
            self.output_text.insert(tk.END, f"Spaces remaining: {remaining_spaces}\n")
        else:
            messagebox.showerror("Error", "The word you've typed is too large, please choose another word")
        self.word_entry.delete(0, tk.END)

    def auto_generate_words(self):
        self.auto_button.config(state=tk.DISABLED)
        self.done_button.config(state=tk.DISABLED)
        self.enter_button.config(state=tk.DISABLED)
        self.word_entry.config(state=tk.DISABLED)
        spaces_remaining = self.word_search.size * self.word_search.size - sum(len(w) for w in self.word_search.words)
        self.word_search.generate_words(spaces_remaining)
        self.create()

    def show_word_search(self):
        self.output_text.config(state=tk.NORMAL)  # Enable editing to update the text widget
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Word Search Grid:\n\n")
        for row in self.word_search.grid:
            self.output_text.insert(tk.END, " ".join(map(str, row)) + "\n")
            self.output_text.tag_configure("center", justify='center')
            self.output_text.tag_add("center", "1.0", "end")  # Apply center alignment to all text

    def show_wordbank(self):
        self.output_text.insert(tk.END, "\nWord Bank:\n")
        word_bank = self.word_search.words
        if not word_bank:
            return

        max_word_length = max(len(word) for word in word_bank)
        max_columns = self.output_text.cget('width') // (max_word_length + 2)
        num_words = len(word_bank)
        num_rows = math.ceil(num_words / max_columns)

        for row in range(num_rows):
            line = ""
            for col in range(max_columns):
                index = row + col * num_rows
                if index < num_words:
                    word = word_bank[index]
                    line += word.ljust(max_word_length + 2)
            self.output_text.insert(tk.END, line + "\n")
        self.output_text.config(state=tk.DISABLED)


if __name__ == '__main__':
    app = WordSearchGUI()
    app.mainloop()
