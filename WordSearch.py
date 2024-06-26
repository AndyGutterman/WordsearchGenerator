import tkinter as tk
from tkinter import messagebox
import random
from Helpers.WordPlacer import WordPlacer  # Assuming you have a WordPlacer module

class WordSearch:
    def __init__(self, size):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.words = []
        self.word_locations = {}
        self.occupied_positions = set()

    def take_words_gui(self, gui_instance):
        spaces_remaining = self.size * self.size

        def handle_input(word):
            nonlocal spaces_remaining
            word = word.strip().upper()
            if word == 'DONE' or spaces_remaining <= 0:
                gui_instance.generate_button.config(state=tk.NORMAL)  # Enable generate button
                gui_instance.output_text.insert(tk.END, "Input complete. Generating word search...\n")
                gui_instance.output_text.see(tk.END)  # Scroll to the end of text widget
                self.place_words()
                self.fill_grid()
                gui_instance.show_word_search(self)
                return
            elif word == 'AUTO':
                self.generate_words(spaces_remaining)
                gui_instance.generate_button.config(state=tk.NORMAL)  # Enable generate button
                gui_instance.output_text.insert(tk.END, "Input complete. Generating word search...\n")
                gui_instance.output_text.see(tk.END)  # Scroll to the end of text widget
                self.place_words()
                self.fill_grid()
                gui_instance.show_word_search(self)
                return

            if len(word) <= self.size and len(word) <= spaces_remaining:
                self.words.append(word)
                spaces_remaining -= len(word)
                gui_instance.output_text.insert(tk.END, f"Entered word: {word}. {spaces_remaining} spaces left\n")
                gui_instance.output_text.see(tk.END)  # Scroll to the end of text widget
                word_entry.delete(0, tk.END)  # Clear the entry widget here
            else:
                messagebox.showerror("Error", "The word you've typed is too large. Please choose another word.")

        gui_instance.generate_button.config(state=tk.DISABLED)  # Disable generate button

        def on_submit():
            word = word_input.get()
            handle_input(word)

        word_entry = tk.Entry(gui_instance)
        word_entry.pack()

        submit_button = tk.Button(gui_instance, text="Submit", command=on_submit)
        submit_button.pack()

        word_input = tk.StringVar()
        word_entry.config(textvariable=word_input)

        gui_instance.output_text.insert(tk.END, f"Spaces remaining: {spaces_remaining}, Max word length: {self.size}\n")

    def generate_words(self, spaces_remaining):
        current_density = (self.size * self.size - spaces_remaining) / (self.size * self.size)
        desired_density = 0.75
        spaces_to_generate = int((desired_density - current_density) * self.size * self.size)

        if spaces_to_generate <= 0:
            return

        min_word_size = 3 if self.size > 3 else 1

        while spaces_to_generate > 0:
            if spaces_to_generate < min_word_size:
                break

            word_length = random.randint(min_word_size, min(self.size, spaces_to_generate, 22))
            word = self.generate_word(word_length)
            self.words.append(word)
            spaces_to_generate -= len(word)

            if spaces_remaining <= 0:
                break

    def generate_word(self, length):
        with open('wordlist.txt', 'r') as f:
            all_words = f.read().splitlines()
            cleaned_words = [word.replace('-', '').replace("'", '').upper() for word in all_words]
            filtered_words = [word for word in cleaned_words if len(word) == length]
            return random.choice(filtered_words) if filtered_words else None

    def place_words(self):
        self.words.sort(key=len, reverse=True)
        big_words_count = sum(1 for word in self.words if len(word) == self.size)
        print(f"Number of words as big as the grid size ({self.size}): {big_words_count}")
        r_big = random.randint(1, 2)
        current_grid_state = [row[:] for row in self.grid]  # Snapshot of current grid state
        try:
            for word in self.words:
                if word in self.word_locations:
                    continue
                letters = list(word)
                placed = False
                while not placed:
                    if (big_words_count >= 1):
                        r = r_big
                    else:
                        r = random.randint(1, 3)
                    if r == 1:
                        placed = WordPlacer.place_vertical(self, letters)
                    elif r == 2:
                        placed = WordPlacer.place_horizontal(self, letters)
                    elif r == 3:
                        placed = WordPlacer.place_diagonal(self, letters)

                if placed:
                    big_words_count -= 1
                    self.word_locations.setdefault(tuple(letters), [])  # Ensure key exists in dict

        except Exception as e:
            print(f"Error occurred during word placement: {e}")
            self.grid = current_grid_state  # Revert to previous grid state

    def fill_grid(self):
        for row in self.grid:
            for i in range(len(row)):
                if row[i] == 0:
                    randchar = chr(random.randint(65, 90))
                    row[i] = randchar

    def show_grid(self):
        print("\n\nWord Search:")
        for row in self.grid:
            print(" ".join(str(element) for element in row))

    def show_wordbank(self):
        for word in self.words:
            print(word)

    def txt_print(self):
        file_name = input("Enter a filename:\n>>> ")
        with open(file_name + ".txt", 'w') as f:
            for row in self.grid:
                f.write('\n')
                for x in row:
                    f.write(' ' + str(x))
            f.write('\n\n')
            f.write('WORDBANK' + '\n')
            for word in self.words:
                f.write(word + '\n')
        print(f"{file_name}.txt created")

    def print_word_locations(self):
        printed_words = set()
        for word in self.words:
            if tuple(word) in self.word_locations and word not in printed_words:
                placements = self.word_locations[tuple(word)]
                for start, direction in placements:
                    try:
                        print(f"{word}: Row/Col {start}, Direction {direction}")
                    except IndexError as e:
                        print(f"Error printing {word}: {e}")
                printed_words.add(word)
            elif word not in printed_words:
                print(f"{word}: Not placed")
                printed_words.add(word)


class WordSearchGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Word Search Generator")

        self.label_size = tk.Label(self, text="Enter size for Word Search:")
        self.label_size.pack()

        self.size_entry = tk.Entry(self)
        self.size_entry.pack()

        self.generate_button = tk.Button(self, text="Generate Word Search", command=self.generate_word_search)
        self.generate_button.pack()

        self.output_text = tk.Text(self, height=10, width=50)
        self.output_text.pack()

    def generate_word_search(self):
        try:
            size = int(self.size_entry.get().strip())
            if size <= 0:
                messagebox.showerror("Error", "Size must be a positive integer.")
                return

            word_search = WordSearch(size)
            word_search.take_words_gui(self)

            # Clear previous output and show current settings
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Type a word in the box below:\n")
            self.output_text.insert(tk.END, f"Spaces remaining: {size * size}\n")
            self.output_text.insert(tk.END, f"Max word length: {size}\n")

        except ValueError:
            messagebox.showerror("Error", "Invalid size. Please enter a valid integer.")

    def show_word_search(self, word_search):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Word Search Grid:\n")
        for row in word_search.grid:
            self.output_text.insert(tk.END, " ".join(map(str, row)) + "\n")

        self.output_text.insert(tk.END, "\nWord Bank:\n")
        for word in word_search.words:
            self.output_text.insert(tk.END, word + "\n")

        self.output_text.config(state=tk.DISABLED)  # Disable editing of the text widget


if __name__ == '__main__':
    app = WordSearchGUI()
    app.mainloop()
