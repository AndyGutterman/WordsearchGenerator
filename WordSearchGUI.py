import tkinter as tk
from tkinter import messagebox
from WordSearch import WordSearch
import math


class WordSearchGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Word Search Generator")
        self.word_search = None
        self.label_frame = None
        self.label_size = None
        self.add_word_button = None
        self.size_entry = None
        self.size_button = None
        self.output_text = None
        self.word_entry = None
        self.auto_button = None
        self.done_button = None
        self.grid_frame = None
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

        # Initialize output text here
        self.output_text = tk.Text(self, height=10, width=40, wrap=tk.WORD)
        self.output_text.pack(pady=(10, 20), padx=20)
        self.output_text.tag_configure("center", justify='center')

        initial_message = "\n\n\n\nEnter a size to continue"
        self.output_text.insert(tk.END, initial_message + "\n", "center")

    def set_size(self, event=None):
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

            # Clear previous output
            self.output_text.delete(1.0, tk.END)
            new_message = ("\n\nEnter words below to continue\n\nType 'auto' or 'done' when finished")
            self.output_text.insert(tk.END, new_message + "\n", "center")

        except ValueError:
            messagebox.showerror("Error", "Invalid size. Please enter a valid integer.")

    def take_words_gui(self):
        button_frame = tk.Frame(self)
        button_frame.pack()

        self.size_entry.pack(in_=self.label_frame, side=tk.LEFT, padx=(0, 20))
        self.size_button.pack(in_=self.label_frame, side=tk.LEFT)

        self.auto_button = tk.Button(button_frame, text="Auto", fg='green', command=self.auto_generate_words)
        self.auto_button.pack(side=tk.LEFT, padx=(10, 10), pady=10)
        self.auto_button.bind("<Return>", lambda event: self.auto_generate_words())

        self.done_button = tk.Button(button_frame, text="Done", fg='green', command=self.create)
        self.done_button.pack(side=tk.LEFT, padx=(10, 10), pady=10)

        self.word_entry = tk.Entry(button_frame, justify='center')
        self.word_entry.insert(0, 'click to enter word')
        self.word_entry.bind("<FocusIn>", self.on_word_entry_focus)
        self.word_entry.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        self.word_entry.bind("<Return>", self.add_word)

        self.add_word_button = tk.Button(button_frame, text="Add Word", command=self.add_word)
        self.add_word_button.config(state=tk.DISABLED)
        self.add_word_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)
    def on_word_entry_focus(self, event):
        if self.word_entry.get() == 'click to enter word':
            self.word_entry.delete(0, 'end')
            self.add_word_button.config(state=tk.NORMAL)

    def create(self):
        self.word_search.place_words()
        self.word_search.fill_grid()
        self.show_word_search()
        self.show_wordbank()
        self.word_search.print_word_locations()

    def add_word(self, event=None):
        word = self.word_entry.get().strip().upper()
        if word == 'DONE':
            self.create()
        elif word == 'AUTO':
            self.auto_generate_words()
        elif len(word) <= self.word_search.size and len(word) <= self.word_search.size * self.word_search.size - sum(
                len(w) for w in self.word_search.words):
            self.word_search.words.append(word)
            self.output_text.insert(tk.END, f"Added word: {word}\n", "center")
            remaining_spaces = self.word_search.size * self.word_search.size - sum(
                len(w) for w in self.word_search.words)
            self.output_text.insert(tk.END, f"Spaces remaining: {remaining_spaces}\n", "center")
        else:
            messagebox.showerror("Error", "The word you've typed is too large, please choose another word")
        self.word_entry.delete(0, tk.END)

    def auto_generate_words(self):
        self.auto_button.config(state=tk.DISABLED)
        self.done_button.config(state=tk.DISABLED)
        self.add_word_button.config(state=tk.DISABLED)
        self.word_entry.config(state=tk.DISABLED)
        spaces_remaining = self.word_search.size * self.word_search.size - sum(len(w) for w in self.word_search.words)
        self.word_search.generate_words(spaces_remaining)
        self.create()

    def show_word_search(self):
        if self.grid_frame:
            self.grid_frame.destroy()

        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack()

        # Adjust the size of the grid cells to fit larger grids
        cell_width = 3 if self.word_search.size > 15 else 4
        cell_height = 1 if self.word_search.size > 15 else 2
        font_size = 12 if self.word_search.size > 15 else 16

        for r, row in enumerate(self.word_search.grid):
            for c, letter in enumerate(row):
                label = tk.Label(self.grid_frame, text=letter, borderwidth=0, relief="solid", width=cell_width,
                                 height=cell_height, font=("Helvetica", font_size))
                label.grid(row=r, column=c)
                label.bind("<Button-1>", self.on_label_click)

    def on_label_click(self, event):
        label = event.widget
        letter = label.cget("text")
        messagebox.showinfo("Letter Clicked", f"You clicked on: {letter}")

    def show_wordbank(self):
        self.output_text.delete(1.0, tk.END)
        word_bank = self.word_search.words
        if not word_bank:
            return

        output_width = self.output_text.cget('width')  # Get the width of the output text widget
        word_bank_text = "Word Bank:"
        centered_word_bank_text = word_bank_text.center(output_width)

        self.output_text.insert(tk.END, "\n" + centered_word_bank_text + "\n", "center")

        max_word_length = max(len(word) for word in word_bank)
        max_columns = output_width // (max_word_length + 2)
        num_words = len(word_bank)
        num_rows = math.ceil(num_words / max_columns)

        centered_lines = []
        for row in range(num_rows):
            line = ""
            for col in range(max_columns):
                index = row + col * num_rows
                if index < num_words:
                    word = word_bank[index]
                    line += word.ljust(max_word_length + 2)
            centered_lines.append(line.center(output_width))

        self.output_text.insert(tk.END, "\n".join(centered_lines) + "\n", "center")


if __name__ == '__main__':
    app = WordSearchGUI()
    app.mainloop()
