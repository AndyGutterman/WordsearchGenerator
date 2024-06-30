import tkinter as tk
from tkinter import messagebox


def initialize_base_UI_elements(self):
    def initialize_menubar():
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save as...", command=self.save_file, state=tk.DISABLED)
        filemenu.add_command(label="Load file", command=self.load_file, state=tk.NORMAL)
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Reset", command=self.reset, state=tk.NORMAL)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Settings", menu=editmenu)
        self.config(menu=menubar)

        self.filemenu = filemenu

    def initialize_size_elements():
        self.size_label_frame = tk.Frame(self, pady=10)
        self.size_label_frame.pack()
        self.size_prompt_label = tk.Label(self.size_label_frame, text="Select grid size:")
        self.size_prompt_label.pack(side=tk.LEFT, padx=(0, 2))

        def custom_size_elements():
            self.size_set_entry = tk.Entry(self.size_label_frame, width=10, justify='center')
            self.size_set_entry.pack(side=tk.LEFT, padx=(0, 5))
            self.size_set_entry.bind("<Return>", self.set_size)

            self.size_set_button = tk.Button(self.size_label_frame, text="Set", command=self.set_size)
            self.size_set_button.pack(side=tk.LEFT, padx=(0, 50))

        def preset_size_buttons():
            small_size = 6
            medium_size = 12
            large_size = 16

            self.small_button = tk.Button(
                self.size_label_frame, text="Small",
                command=lambda size=small_size: self.set_preset_size(small_size), state=tk.NORMAL)
            self.small_button.pack(side=tk.LEFT, padx=0.25)
            self.small_button.bind("<Return>", lambda event, size=small_size: self.set_preset_size(6))

            self.medium_button = tk.Button(
                self.size_label_frame, text="Medium",
                command=lambda size=medium_size: self.set_preset_size(medium_size), state=tk.NORMAL)
            self.medium_button.pack(side=tk.LEFT, padx=0.25)
            self.medium_button.bind("<Return>", lambda event, size=medium_size: self.set_preset_size(2))

            self.large_button = tk.Button(
                self.size_label_frame, text="Large",
                command=lambda size=large_size: self.set_preset_size(large_size), state=tk.NORMAL)
            self.large_button.pack(side=tk.LEFT, padx=0.25)
            self.large_button.bind("<Return>", lambda event, size=large_size: self.set_preset_size(16))

        custom_size_elements()
        preset_size_buttons()

    def initialize_output_text_and_fill_indicator_frame():
        output_text_and_fill_indicator_frame = tk.Frame(self)
        output_text_and_fill_indicator_frame.pack(pady=(10, 20), padx=20, fill=tk.BOTH, expand=True)

        self.output_text = tk.Text(output_text_and_fill_indicator_frame, height=10, width=40, wrap=tk.WORD)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.output_text.tag_configure("center", justify='center')

        initial_message = "\n\n\n\nEnter a size to continue"
        self.output_text.insert(tk.END, initial_message + "\n", "center")
        self.character_fill_indicator = tk.Scale(
            output_text_and_fill_indicator_frame, from_=1, to=0, orient=tk.VERTICAL)
        self.character_fill_indicator.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        self.character_fill_indicator.configure(state=tk.DISABLED)

    initialize_menubar()
    initialize_size_elements()
    initialize_output_text_and_fill_indicator_frame()


def get_size_from_entry(entry_widget):
    size_str = entry_widget.get().strip()
    try:
        size = int(size_str)
        if size <= 0:
            messagebox.showerror("Error", "Size must be a positive integer.")
            return None
        return size
    except ValueError:
        messagebox.showerror("Error", "Invalid size. Please enter a valid integer.")
        return None


def adjust_output_text_for_size(output_text_widget, size):
    text_height = min(max(size * 3, 10), 30)
    text_width = min(max(size * 5, 40), 80)
    output_text_widget.config(height=text_height, width=text_width)
    initial_message = "\n\nEnter words below to continue\n\nType 'auto' or 'done' when finished"
    output_text_widget.insert(tk.END, initial_message + "\n", "center")
    output_text_widget.config(state=tk.DISABLED)


def initialize_word_entry_buttons(self):
    button_frame = tk.Frame(self)
    button_frame.pack()
    self.auto_button = tk.Button(button_frame, text="Auto", fg='green', command=self.auto_generate_words)
    self.auto_button.pack(side=tk.LEFT, padx=(10, 10), pady=10)
    self.auto_button.bind("<Return>", lambda event: self.auto_generate_words())

    self.done_button = tk.Button(button_frame, text="Done", fg='green', command=self.create)
    self.done_button.pack(side=tk.LEFT, padx=(10, 10), pady=10)

    self.word_add_entry = tk.Entry(button_frame, justify='center')
    self.word_add_entry.insert(0, 'click to enter word')
    self.word_add_entry.bind("<FocusIn>", self.on_word_entry_focus)
    self.word_add_entry.pack(side=tk.LEFT, padx=(10, 5), pady=10)
    self.word_add_entry.bind("<Return>", self.add_word)

    self.word_add_button = tk.Button(button_frame, text="Add Word", command=self.add_word)
    self.word_add_button.config(state=tk.DISABLED)
    self.word_add_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)
