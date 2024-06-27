import math
import tkinter as tk
from tkinter import messagebox
from WordSearch import WordSearch

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
        self.grid_window = None
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
            self.size_entry.config(state=tk.DISABLED)
            self.size_button.config(state=tk.DISABLED)

            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)

            text_height = min(max(size * 3, 10), 30)
            text_width = min(max(size * 5, 40), 80)

            self.output_text.config(height=text_height, width=text_width)

            self.word_search = WordSearch(size)
            self.take_words_gui()

            new_message = "\n\nEnter words below to continue\n\nType 'auto' or 'done' when finished"
            self.output_text.insert(tk.END, new_message + "\n", "center")
            self.output_text.config(state=tk.DISABLED)

        except ValueError:
            messagebox.showerror("Error", "Invalid size. Please enter a valid integer.")

    def update_output_text(self, new_content):
        current_content = self.output_text.get(1.0, tk.END)

        if "\n\nEnter words below to continue\n\nType 'auto' or 'done' when finished" in current_content:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)  # Delete initial message
            self.output_text.config(state=tk.DISABLED)
        # New content:
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, new_content + "\n", "center")
        self.output_text.config(state=tk.DISABLED)

    def take_words_gui(self):
        button_frame = tk.Frame(self)
        button_frame.pack()

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
        self.auto_button.config(state=tk.DISABLED)
        self.done_button.config(state=tk.DISABLED)
        self.add_word_button.config(state=tk.DISABLED)
        self.word_entry.config(state=tk.DISABLED)

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
            remaining_spaces = self.word_search.size * self.word_search.size - sum(
                len(w) for w in self.word_search.words)
            self.update_output_text(f"Added {word}, {remaining_spaces} characters left")
        else:
            messagebox.showerror("Error", "The word you've typed is too large, please choose another word")

        self.word_entry.delete(0, tk.END)

    def auto_generate_words(self):
        spaces_remaining = self.word_search.size * self.word_search.size - sum(len(w) for w in self.word_search.words)
        self.word_search.generate_words(spaces_remaining)
        self.create()

    def show_word_search(self):
        if self.grid_frame:
            self.grid_frame.destroy()

        if self.grid_window:
            self.grid_window.destroy()

        if self.word_search.size > 16:
            self.grid_window = tk.Toplevel(self)
            self.grid_window.title("Word Search Grid")
            self.grid_frame = tk.Frame(self.grid_window, padx=20, pady=20)
        else:
            self.grid_frame = tk.Frame(self, padx=20, pady=20)

        self.grid_frame.pack(padx=20, pady=20)

        # Adjust font size based on grid size
        font_size = max(12, 20 - self.word_search.size // 2)

        for r, row in enumerate(self.word_search.grid):
            for c, letter in enumerate(row):
                label = tk.Label(self.grid_frame, text=letter, borderwidth=0, relief="solid", width=4, height=2,
                                 font=("Helvetica", font_size))
                label.grid(row=r, column=c)
                label.bind("<Button-1>", self.on_label_click)

    def on_label_click(self, event):
        label = event.widget
        letter = label.cget("text")
        messagebox.showinfo("Letter Clicked", f"You clicked on: {letter}")

    def show_wordbank(self):
        word_bank = self.word_search.words
        if not word_bank:
            self.update_output_text("Word Bank is empty.")
        else:
            max_word_length = max(len(word) for word in word_bank)
            output_width = self.output_text.cget('width')
            max_columns = output_width // (max_word_length + 2)

            num_rows = math.ceil(len(word_bank) / max_columns)
            text_height = max(num_rows * 1.25, 5)

            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)

            word_bank_text = "Word Bank:\n"
            for i, word in enumerate(word_bank, start=1):
                word_bank_text += f"{word.ljust(max_word_length + 2)}"
                if i % max_columns == 0:
                    word_bank_text += "\n"

            self.output_text.insert(tk.END, word_bank_text + "\n", "center")
            self.output_text.config(height=text_height)
            self.output_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    app = WordSearchGUI()
    app.mainloop()
