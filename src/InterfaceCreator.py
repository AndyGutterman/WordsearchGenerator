import tkinter as tk
from tkinter import messagebox


class InterfaceCreator:
    def __init__(self, root):
        self.size_buttons_labels_frame = None
        self.root = root
        self.word_entry_buttons_frame = None
        self.output_text_and_fill_indicator_frame = None
        self.character_fill_scale = None
        self.character_fill_indicator_label = None
        self.character_fill_indicator_text = tk.StringVar()

    def initialize_base_UI_elements(self):
        self.initialize_menubar()
        self.initialize_size_elements()
        self.output_text_and_fill_indicator_frame = tk.Frame(self.root)
        self.output_text_and_fill_indicator_frame.pack(pady=(10, 20), padx=20, fill=tk.BOTH, expand=True)
        self.initialize_output_text(self.output_text_and_fill_indicator_frame)
        self.initialize_character_fill_indicator(self.output_text_and_fill_indicator_frame)

    def initialize_menubar(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save as...", command=self.root.save_file, state=tk.DISABLED)
        filemenu.add_command(label="Load file", command=self.root.load_file, state=tk.NORMAL)
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Reset", command=self.root.reset, state=tk.NORMAL)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Settings", menu=editmenu)
        self.root.config(menu=menubar)
        self.root.filemenu = filemenu

    def initialize_size_elements(self):
        self.size_buttons_labels_frame = tk.Frame(self.root, pady=10)
        self.size_buttons_labels_frame.pack()
        size_prompt_label = tk.Label(self.size_buttons_labels_frame, text="Select grid size:")
        size_prompt_label.pack(side=tk.LEFT, padx=(0, 2))

        size_set_entry = tk.Entry(self.size_buttons_labels_frame, width=10, justify='center')
        size_set_entry.pack(side=tk.LEFT, padx=(0, 5))
        size_set_entry.bind("<Return>", self.root.set_size)

        size_set_button = tk.Button(self.size_buttons_labels_frame, text="Set", command=self.root.set_size)
        size_set_button.pack(side=tk.LEFT, padx=(0, 50))

        self.root.size_set_entry = size_set_entry
        self.root.size_set_button = size_set_button

        small_button = tk.Button(self.size_buttons_labels_frame, text="Small",
                                 command=lambda: self.root.set_preset_size(6),
                                 state=tk.NORMAL)
        small_button.pack(side=tk.LEFT, padx=0.25)
        medium_button = tk.Button(self.size_buttons_labels_frame, text="Medium",
                                  command=lambda: self.root.set_preset_size(12),
                                  state=tk.NORMAL)
        medium_button.pack(side=tk.LEFT, padx=0.25)
        large_button = tk.Button(self.size_buttons_labels_frame, text="Large",
                                 command=lambda: self.root.set_preset_size(16),
                                 state=tk.NORMAL)
        large_button.pack(side=tk.LEFT, padx=0.25)

        self.root.small_button = small_button
        self.root.medium_button = medium_button
        self.root.large_button = large_button

    def initialize_output_text(self, parent_frame):
        initial_message = "\n\n\n\nEnter a size to continue"
        output_text = tk.Text(parent_frame, height=10, width=40, wrap=tk.WORD)
        output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=0)
        output_text.tag_configure("center", justify='center')
        output_text.insert(tk.END, initial_message + "\n", "center")
        self.root.output_text = output_text

    def initialize_character_fill_indicator(self, parent_frame):
        self.character_fill_indicator_text.set("--")
        self.character_fill_indicator_label = tk.Label(parent_frame, textvariable=self.character_fill_indicator_text)
        self.character_fill_indicator_label.pack(side=tk.RIGHT, anchor='ne', padx=(10, 0))

        self.character_fill_scale = tk.Scale(parent_frame, from_=1, to=0, orient=tk.VERTICAL)
        self.character_fill_scale.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        self.character_fill_scale.config(state=tk.DISABLED)
        self.root.character_fill_scale = self.character_fill_scale

    def initialize_word_entry_buttons(self):
        self.word_entry_buttons_frame = tk.Frame(self.root)
        self.word_entry_buttons_frame.pack()

        auto_button = tk.Button(self.word_entry_buttons_frame, text="Auto", fg='green',
                                command=self.root.auto_generate_words)
        auto_button.pack(side=tk.LEFT, padx=(10, 10), pady=10)
        done_button = tk.Button(self.word_entry_buttons_frame, text="Done", fg='green', command=self.root.create)
        done_button.pack(side=tk.LEFT, padx=(10, 10), pady=10)

        word_add_entry = tk.Entry(self.word_entry_buttons_frame, justify='center')
        word_add_entry.insert(0, 'click to enter word')
        word_add_entry.bind("<FocusIn>", self.root.on_word_entry_focus)
        word_add_entry.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        word_add_entry.bind("<Return>", self.root.add_word)

        word_add_button = tk.Button(self.word_entry_buttons_frame, text="Add Word", command=self.root.add_word)
        word_add_button.config(state=tk.DISABLED)
        word_add_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)

        self.root.auto_button = auto_button
        self.root.done_button = done_button
        self.root.word_add_entry = word_add_entry
        self.root.word_add_button = word_add_button

    def reload_base_elements(self):
        # .pack_forget the following, then re-pack in correct order:
        self.hide_output_text_frame()
        self.hide_word_entry_elements()
        self.show_size_entry_elements()
        self.show_output_text_frame()

    def show_character_fill_indicator(self):
        self.character_fill_scale.pack_forget()
        self.character_fill_indicator_text.set("--")
        self.character_fill_indicator_label.pack(side=tk.RIGHT, anchor='ne', padx=(10, 0))
        self.character_fill_scale.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

    def hide_character_fill_indicator(self):
        if self.character_fill_scale:
            self.character_fill_scale.pack_forget()
        if self.character_fill_indicator_label:
            self.character_fill_indicator_label.pack_forget()

    def hide_output_text_frame(self):
        if self.output_text_and_fill_indicator_frame:
            self.output_text_and_fill_indicator_frame.pack_forget()

    def show_output_text_frame(self):
        if self.output_text_and_fill_indicator_frame:
            self.output_text_and_fill_indicator_frame.pack(pady=(10, 20), padx=20, fill=tk.BOTH, expand=True)

    def hide_size_entry_elements(self):
        if self.size_buttons_labels_frame:
            self.size_buttons_labels_frame.pack_forget()

    def show_size_entry_elements(self):
        if self.size_buttons_labels_frame:
            self.size_buttons_labels_frame.pack()

    def hide_word_entry_elements(self):
        if self.word_entry_buttons_frame:
            self.word_entry_buttons_frame.pack_forget()

    def show_word_entry_elements(self):
        if self.word_entry_buttons_frame:
            self.word_entry_buttons_frame.pack()
