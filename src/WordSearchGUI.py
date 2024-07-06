import math
import tkinter as tk
from tkinter import messagebox

from FileOutputHandler import FileOutputHandler
from InterfaceCreator import InterfaceCreator
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
        self.size_prompt_label = None
        self.size_set_entry = None
        self.size_set_button = None
        self.small_button = None
        self.medium_button = None
        self.large_button = None
        self.output_text = None
        self.word_add_entry = None
        self.word_add_button = None
        self.auto_button = None
        self.done_button = None
        self.grid_frame = None
        self.grid_window = None
        self.character_fill_indicator_label = None
        self.character_fill_scale = None
        self.file_handler = FileOutputHandler(self)
        self.interface_creator = InterfaceCreator(self)
        self.interface_creator.initialize_base_UI_elements()

    def set_size(self, event=None, preset_size=None):
        try:
            if preset_size is None:
                size = self.get_size_from_entry()
                if size is None:
                    return
            else:
                size = preset_size

            self.update_size_buttons_state(False)
            self.initialize_word_search(size)
            self.character_fill_scale.config(from_=size * size, to=0, length=self.output_text.cget("height") * 7)
            self.update_character_fill_indicator(0)
            self.update_character_fill_label(size)
            self.update_word_buttons_state(True)

            self.adjust_output_text_for_size(self.output_text, size)

        except ValueError:
            messagebox.showerror("Error", "Invalid size. Please enter a valid integer.")

    def get_size_from_entry(self):
        size_str = self.size_set_entry.get().strip()
        try:
            size = int(size_str)
            if size <= 0:
                messagebox.showerror("Error", "Size must be a positive integer.")
                return None
            return size
        except ValueError:
            messagebox.showerror("Error", "Invalid size. Please enter a valid integer.")
            return None

    def set_preset_size(self, preset_size):
        self.size_set_entry.config(state=tk.NORMAL)
        self.size_set_entry.delete(0, tk.END)
        self.size_set_entry.insert(0, str(preset_size))
        self.set_size(preset_size=preset_size)
        self.size_set_entry.config(state=tk.DISABLED)

    def initialize_word_search(self, size):
        self.word_search = WordSearch(size)
        self.update_word_entry_buttons()

    def update_word_entry_buttons(self):
        if self.GUI_already_initialized:
            self.update_word_buttons_state(True)
            self.interface_creator.show_word_entry_elements()
        else:
            self.interface_creator.initialize_word_entry_buttons()
            self.GUI_already_initialized = True

    def update_size_buttons_state(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.size_set_entry.config(state=state)
        self.size_set_button.config(state=state)
        self.small_button.config(state=state)
        self.medium_button.config(state=state)
        self.large_button.config(state=state)

    def update_word_buttons_state(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.auto_button.config(state=state)
        self.done_button.config(state=state)
        self.word_add_button.config(state=state)
        self.word_add_entry.config(state=state)

    def update_save_filemenu_state(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.filemenu.entryconfig("Save as...", state=state)

    def load_file(self):
        self.file_handler.load_file()

    def save_file(self):
        self.file_handler.save_file()

    def update_character_fill_indicator(self, remaining):
        self.character_fill_scale.config(state=tk.NORMAL)
        self.character_fill_scale.set(remaining)
        self.character_fill_scale.config(state=tk.DISABLED)

    def update_character_fill_label(self, size):
        max_characters = size * size
        self.interface_creator.character_fill_indicator_text.set(f"{max_characters}")

    def on_word_entry_focus(self, event):
        if self.word_add_entry.get() == 'click to enter word':
            self.word_add_entry.delete(0, 'end')
            self.word_add_button.config(state=tk.NORMAL)

    def reset(self):
        self.word_search = None
        self.filemenu.entryconfig("Save as...", state=tk.DISABLED)
        self.interface_creator.reload_base_elements()
        self.interface_creator.show_character_fill_indicator()
        self.update_size_buttons_state(True)
        self.size_set_entry.delete(0, 'end')
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        initial_message = "\n\nEnter a size to continue"
        self.output_text.insert(tk.END, initial_message + "\n", "center")
        self.output_text.config(state=tk.DISABLED)

        if self.word_add_entry:
            self.word_add_entry.delete(0, tk.END)
            self.update_word_buttons_state(False)

        if self.character_fill_scale:
            self.character_fill_scale.config(state=tk.NORMAL, from_=1, to=0)
            self.character_fill_scale.set(0)

        self.interface_creator.show_character_fill_indicator()

        for label in self.highlighted_labels:
            label.config(bg='SystemButtonFace')
        self.highlighted_labels = []
        self.highlighted_positions = []

        if self.grid_frame:
            self.grid_frame.destroy()
            self.grid_frame = None
        if self.grid_window:
            self.grid_window.destroy()
            self.grid_window = None

    def add_word(self, event=None):
        word = self.word_add_entry.get().strip().upper()
        if word == 'DONE':
            self.create()
        elif word == 'AUTO':
            self.auto_generate_words()
        elif len(word) <= self.word_search.size and len(word) <= self.word_search.size * self.word_search.size - sum(
                len(w) for w in self.word_search.words):
            self.word_search.words.append(word)
            remaining_spaces = self.word_search.size * self.word_search.size - sum(
                len(w) for w in self.word_search.words)
            confirmation_message = f"Added {word}, {remaining_spaces} characters left"
            self.update_output_text(confirmation_message)
            self.update_character_fill_indicator(self.word_search.size ** 2 - remaining_spaces)
            if remaining_spaces <= (1 / 4 * self.word_search.size * self.word_search.size):
                grid_near_full_warning = f"** Note: Grid nearly full **"
                self.update_output_text(grid_near_full_warning)
            if remaining_spaces <= (1 / 8 * self.word_search.size * self.word_search.size):
                grid_critically_full_warning = f"** Warning: grid space very low - may not generate **"
                self.update_output_text(grid_critically_full_warning)
            if remaining_spaces <= 0:
                self.create()
        else:
            messagebox.showerror("Error", "The word you've typed is too large, please choose another word")

        self.word_add_entry.delete(0, tk.END)

    def auto_generate_words(self):
        spaces_remaining = self.word_search.size * self.word_search.size - sum(len(w) for w in self.word_search.words)
        self.word_search.generate_words(spaces_remaining)
        self.create()

    def create(self):
        self.interface_creator.hide_word_entry_elements()
        self.interface_creator.hide_size_entry_elements()
        self.interface_creator.hide_character_fill_indicator()

        self.update_word_buttons_state(False)
        self.update_size_buttons_state(False)
        self.update_save_filemenu_state(True)
        WordPlacer.place_words(self.word_search)
        self.word_search.fill_grid()
        self.show_word_search()
        self.show_wordbank()
        self.track_found_words()

    def show_word_search(self):
        if self.grid_frame:
            self.grid_frame.destroy()
        if self.grid_window:
            self.grid_window.destroy()

        if self.word_search.size > 16:
            self.grid_window = tk.Toplevel(self)
            self.grid_window.title("Word Search Grid")
            self.grid_frame = tk.Frame(self.grid_window, padx=0, pady=0)
        else:
            self.grid_frame = tk.Frame(self, padx=2, pady=2)

        if self.word_search.size == 15:
            font_size = 20
        elif self.word_search.size < 15:
            font_size = 20
        else:
            font_size = 14

        for r, row in enumerate(self.word_search.grid):
            for c, letter in enumerate(row):
                label = tk.Label(self.grid_frame, text=letter, width=2, height=1, padx=1, pady=1,
                                 font=("Helvetica", font_size))
                label.grid(row=r, column=c)
                label.bind("<Button-1>", self.on_label_click)

        self.grid_frame.pack()

    def update_output_text(self, new_content):
        current_content = self.output_text.get(1.0, tk.END)
        word_entry_message = "\n\nEnter words below to continue\n\nType 'auto' or 'done' when finished"
        if word_entry_message in current_content:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.config(state=tk.DISABLED)

        self.output_text.config(state=tk.NORMAL)

        if "word bank" in new_content:
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

    @staticmethod
    def adjust_output_text_for_size(output_text_widget, size):
        initial_message = "\n\nEnter words below to continue\n\nType 'auto' or 'done' when finished"
        output_text_widget.config(state=tk.NORMAL)
        output_text_widget.delete(1.0, tk.END)

        text_height = min(max(size * 3, 10), 30)
        text_width = min(max(size * 5, 40), 80)
        output_text_widget.config(height=text_height, width=text_width)
        output_text_widget.insert(tk.END, initial_message + "\n", "center")
        output_text_widget.config(state=tk.DISABLED)

    def show_wordbank(self):
        self.output_text.config(state=tk.NORMAL)
        word_bank = self.word_search.words
        if not word_bank:
            empty_wordbank_message = "Word Bank is empty."
            self.update_output_text(empty_wordbank_message)
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

            self.update_output_text(word_bank_text)
            self.output_text.config(height=text_height)
            self.output_text.config(state=tk.DISABLED)

    def track_found_words(self):
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

    def on_label_click(self, event):
        label = event.widget

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
                label_position = (info['row'], 'column')
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


def main():
    app = WordSearchGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
