import os
import tkinter as tk
from tkinter import filedialog, messagebox
from WordSearch import WordSearch


class FileOutputHandler:
    def __init__(self, parent):
        self.parent = parent

    def load_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            self.parent.hide_customization_elements()

            with open(file_path, 'r') as f:
                lines = f.readlines()
            grid = []
            words = []
            in_wordbank = False

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line == "WORDBANK":
                    in_wordbank = True
                    continue
                if in_wordbank:
                    words.append(line.split(" ")[0])
                else:
                    grid.append(line.split())

            size = len(grid)
            self.parent.adjust_output_text_for_size(self.parent.output_text, size)
            self.parent.word_search = WordSearch(size)
            self.parent.word_search.grid = grid
            self.parent.word_search.words = words
            self.parent.show_word_search()
            self.parent.show_wordbank()
            messagebox.showinfo("File Loaded", f"Word search loaded from {file_path}")

            self.parent.update_size_buttons_state(False)
            self.parent.update_word_buttons_state(False)
            self.parent.filemenu.entryconfig("Save as...", state=tk.DISABLED)

    def save_file(self):
        if not self.parent.word_search:
            messagebox.showerror("Error", "No word search generated yet.")
            return

        initial_dir = os.path.abspath(os.path.dirname(__file__))  # Get current script directory
        file_path = filedialog.asksaveasfilename(
            initialdir=initial_dir,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )

        if file_path:
            with open(file_path, 'w') as f:
                for row in self.parent.word_search.grid:
                    f.write(' '.join(row) + '\n')
                f.write('\nWORDBANK\n')
                for word in self.parent.word_search.words:
                    f.write(word + '\n')

            messagebox.showinfo("File Saved", f"Word search saved as {file_path}")
