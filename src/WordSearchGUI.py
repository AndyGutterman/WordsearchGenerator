import math
import os
import tkinter as tk
from tkinter import messagebox, filedialog

from gui_initialization import initialize_gui
from placement.WordPlacer import WordPlacer
from WordSearch import WordSearch


class WordSearchGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.GUI_already_initialized = False
        self.highlighted_labels = []
        self.highlighted_positions = []
        self.title("Word Search Generator")
        self.filemenu = None
        self.word_search = None
        self.size_label_frame = None
        self.size_prompt_label = None
        self.set_size_entry = None
        self.set_size_button = None
        self.small_button = None
        self.medium_button = None
        self.large_button = None
        self.output_text = None
        self.add_word_entry = None
        self.add_word_button = None
        self.auto_button = None
        self.done_button = None
        self.grid_frame = None
        self.grid_window = None
        self.char_slider = None
        initialize_gui(self)


    def set_size(self, event=None):
        try:
            size = int(self.set_size_entry.get().strip())
            if size <= 0:
                messagebox.showerror("Error", "Size must be a positive integer.")
                return
            self.lock_size_buttons()

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

            # Update characters remaining slider properties
            self.char_slider.config(from_=size * size, to=0, length=text_height * 7)
            self.update_slider(0)

        except ValueError:
            messagebox.showerror("Error", "Invalid size. Please enter a valid integer.")

    def set_preset_size(self, preset_size):
        self.set_size_entry.delete(0, tk.END)
        self.set_size_entry.insert(0, str(preset_size))
        self.set_size()

    def load_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
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
            self.word_search = WordSearch(size)
            self.word_search.grid = grid
            self.word_search.words = words
            self.show_word_search()
            self.show_wordbank()
            messagebox.showinfo("File Loaded", f"Word search loaded from {file_path}")
            self.lock_size_buttons()
            self.lock_word_buttons()

    def save_file(self):
        if not self.word_search:
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
                for row in self.word_search.grid:
                    f.write(' '.join(row) + '\n')
                f.write('\nWORDBANK\n')
                for word in self.word_search.words:
                    f.write(word + '\n')

            messagebox.showinfo("File Saved", f"Word search saved as {file_path}")

    def update_slider(self, remaining):
        self.char_slider.config(state=tk.NORMAL)
        self.char_slider.set(remaining)
        self.char_slider.config(state=tk.DISABLED)

    def update_output_text(self, new_content):
        current_content = self.output_text.get(1.0, tk.END)

        if "\n\nEnter words below to continue\n\nType 'auto' or 'done' when finished" in current_content:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.config(state=tk.DISABLED)

        self.output_text.config(state=tk.NORMAL)

        if "word bank" in new_content:
            # Apply strikethrough to parts containing "word bank"
            start_index = 1.0
            while True:
                start_index = self.output_text.search("word bank", start_index, tk.END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len('word bank')}c"
                self.output_text.tag_add("strike", start_index, end_index)
                start_index = end_index

        self.output_text.insert(tk.END, new_content + "\n", "center")
        self.output_text.config(state=tk.DISABLED)

    def initialize_buttons(self, button_frame):
        self.auto_button = tk.Button(button_frame, text="Auto", fg='green', command=self.auto_generate_words)
        self.auto_button.pack(side=tk.LEFT, padx=(10, 10), pady=10)
        self.auto_button.bind("<Return>", lambda event: self.auto_generate_words())

        self.done_button = tk.Button(button_frame, text="Done", fg='green', command=self.create)
        self.done_button.pack(side=tk.LEFT, padx=(10, 10), pady=10)

        self.add_word_entry = tk.Entry(button_frame, justify='center')
        self.add_word_entry.insert(0, 'click to enter word')
        self.add_word_entry.bind("<FocusIn>", self.on_word_entry_focus)
        self.add_word_entry.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        self.add_word_entry.bind("<Return>", self.add_word)

        self.add_word_button = tk.Button(button_frame, text="Add Word", command=self.add_word)
        self.add_word_button.config(state=tk.DISABLED)
        self.add_word_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)

    def take_words_gui(self):
        button_frame = tk.Frame(self)
        button_frame.pack()
        if self.GUI_already_initialized:
            self.unlock_word_buttons()
        else:
            self.initialize_buttons(button_frame)
            self.GUI_already_initialized = True


    def on_word_entry_focus(self, event):
        if self.add_word_entry.get() == 'click to enter word':
            self.add_word_entry.delete(0, 'end')
            self.add_word_button.config(state=tk.NORMAL)

    def lock_size_buttons(self):
        self.set_size_entry.config(state=tk.DISABLED)
        self.set_size_button.config(state=tk.DISABLED)
        self.small_button.config(state=tk.DISABLED)
        self.medium_button.config(state=tk.DISABLED)
        self.large_button.config(state=tk.DISABLED)

    def reset(self):
        self.unlock_size_buttons()
        self.word_search = None
        self.set_size_entry.delete(0, 'end')

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        initial_message = "\n\nEnter a size to continue"
        self.output_text.insert(tk.END, initial_message + "\n", "center")
        self.output_text.config(state=tk.DISABLED)

        if self.add_word_entry:
            self.add_word_entry.delete(0, tk.END)
            self.lock_word_buttons()

        # Reset slider
        self.char_slider.config(state=tk.NORMAL, from_=0, to=0)
        self.char_slider.set(0)
        self.char_slider.config(state=tk.DISABLED)

        # Clear highlighted labels and positions
        for label in self.highlighted_labels:
            label.config(bg='SystemButtonFace')
        self.highlighted_labels = []
        self.highlighted_positions = []

        # Destroy grid components if they exist
        if self.grid_frame:
            self.grid_frame.destroy()
            self.grid_frame = None
        if self.grid_window:
            self.grid_window.destroy()
            self.grid_window = None

    def lock_size_buttons(self):
        self.set_size_entry.config(state=tk.DISABLED)
        self.set_size_button.config(state=tk.DISABLED)
        self.small_button.config(state=tk.DISABLED)
        self.medium_button.config(state=tk.DISABLED)
        self.large_button.config(state=tk.DISABLED)

    def unlock_size_buttons(self):
        self.set_size_entry.config(state=tk.NORMAL)
        self.set_size_button.config(state=tk.NORMAL)
        self.small_button.config(state=tk.NORMAL)
        self.medium_button.config(state=tk.NORMAL)
        self.large_button.config(state=tk.NORMAL)

    def lock_word_buttons(self):
        self.auto_button.config(state=tk.DISABLED)
        self.done_button.config(state=tk.DISABLED)
        self.add_word_button.config(state=tk.DISABLED)
        self.add_word_entry.config(state=tk.DISABLED)

    def unlock_word_buttons(self):
        self.add_word_entry.config(state=tk.NORMAL)
        self.add_word_button.config(state=tk.NORMAL)
        self.auto_button.config(state=tk.NORMAL)
        self.done_button.config(state=tk.NORMAL)

    def create(self):
        self.auto_button.config(state=tk.DISABLED)
        self.done_button.config(state=tk.DISABLED)
        self.add_word_button.config(state=tk.DISABLED)
        self.add_word_entry.config(state=tk.DISABLED)
        self.filemenu.entryconfig("Save as...", state=tk.NORMAL)

        WordPlacer.place_words(self.word_search)
        self.word_search.fill_grid()
        self.show_word_search()
        self.show_wordbank()

    def add_word(self, event=None):
        word = self.add_word_entry.get().strip().upper()

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
            self.update_slider(self.word_search.size ** 2 - remaining_spaces)
            if remaining_spaces <= (1 / 4 * self.word_search.size * self.word_search.size):
                self.update_output_text(f"** Note: Grid nearly full **")
            if remaining_spaces <= (1 / 8 * self.word_search.size * self.word_search.size):
                self.update_output_text(f"** Warning: grid space very low - may not generate **")
            if remaining_spaces <= 0:
                self.create()
        else:
            messagebox.showerror("Error", "The word you've typed is too large, please choose another word")

        self.add_word_entry.delete(0, tk.END)

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

        self.highlight_label(label)
        self.print_highlighted_labels()
        self.check_highlighted_tiles()

    def highlight_label(self, label):
        info = label.grid_info()
        row, col = info['row'], info['column']

        if (row, col) in self.highlighted_positions:
            label.config(bg='SystemButtonFace')
            self.highlighted_positions.remove((row, col))
        else:
            label.config(bg='yellow')
            self.highlighted_positions.append((row, col))

    def print_highlighted_labels(self):
        if self.highlighted_labels:
            print("Highlighted Labels:")
            for label in self.highlighted_labels:
                label_text = label.cget("text")
                info = label.grid_info()
                label_position = (info['row'], info['column'])
                print(f"Label text: {label_text}, Position: {label_position}")

    def check_highlighted_tiles(self):
        found_words = []
        for word in self.word_search.words:
            positions = self.word_search.find_word(word)
            if positions:
                highlighted_positions_set = set(self.highlighted_positions)
                word_positions_set = set(positions)
                if word_positions_set.issubset(highlighted_positions_set):
                    found_words.append(word)
        print("Found words:", found_words)
        self.strike_through_output_text(found_words)

    def print_letter_positions(self):
        if self.word_search:
            print("Letter Positions for Valid Word Locations:")
            for word in self.word_search.words:
                positions = self.word_search.find_word(word)
                if positions:
                    print(f"Word '{word}':")
                    start_position = positions[0]
                    end_position = positions[-1]
                    print(f"  - Start: ({start_position[0]}, {start_position[1]})")
                    print(f"  - End:   ({end_position[0]}, {end_position[1]})")
        else:
            print("No word search initialized yet.")

    def strike_through_output_text(self, found_words):
        # Remove strike-through from all text first
        self.output_text.tag_remove("strike", "1.0", tk.END)

        # Add strike-through only to found words
        for word in found_words:
            start_index = "1.0"
            while True:
                start_index = self.output_text.search(word, start_index, tk.END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(word)}c"
                self.output_text.tag_configure("strike", overstrike=True)
                self.output_text.tag_add("strike", start_index, end_index)
                start_index = end_index

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

        if self.char_slider:
            self.char_slider.pack_forget()

        # Get the found words from check_highlighted_tiles
        found_words = []
        for word in self.word_search.words:
            positions = self.word_search.find_word(word)
            if positions:
                highlighted_positions_set = set(self.highlighted_positions)
                word_positions_set = set(positions)
                if word_positions_set.issubset(highlighted_positions_set):
                    found_words.append(word)
        print("Found words:", found_words)

        # Apply strike-through only to found words
        self.strike_through_output_text(found_words)


def main():
    app = WordSearchGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
