import tkinter as tk


def initialize_gui(self):
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
            self.set_size_entry = tk.Entry(self.size_label_frame, width=10, justify='center')
            self.set_size_entry.pack(side=tk.LEFT, padx=(0, 5))
            self.set_size_entry.bind("<Return>", self.set_size)

            self.set_size_button = tk.Button(self.size_label_frame, text="Set", command=self.set_size)
            self.set_size_button.pack(side=tk.LEFT, padx=(0, 50))

        def preset_size_buttons():
            self.small_button = tk.Button(self.size_label_frame, text="Small",
                                          command=lambda: self.set_preset_size(6), state=tk.NORMAL)
            self.small_button.pack(side=tk.LEFT, padx=0.25)
            self.small_button.bind("<Return>", lambda event: self.set_preset_size(6))

            self.medium_button = tk.Button(self.size_label_frame, text="Medium",
                                           command=lambda: self.set_preset_size(12), state=tk.NORMAL)
            self.medium_button.pack(side=tk.LEFT, padx=0.25)
            self.medium_button.bind("<Return>", lambda event: self.set_preset_size(12))

            self.large_button = tk.Button(self.size_label_frame, text="Large",
                                          command=lambda: self.set_preset_size(16), state=tk.NORMAL)
            self.large_button.pack(side=tk.LEFT, padx=0.25)
            self.large_button.bind("<Return>", lambda event: self.set_preset_size(16))

        custom_size_elements()
        preset_size_buttons()

    def initialize_output_and_slider_frame():
        output_text_and_slider_frame = tk.Frame(self)
        output_text_and_slider_frame.pack(pady=(10, 20), padx=20, fill=tk.BOTH, expand=True)

        self.output_text = tk.Text(output_text_and_slider_frame, height=10, width=40, wrap=tk.WORD)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.output_text.tag_configure("center", justify='center')

        initial_message = "\n\n\n\nEnter a size to continue"
        self.output_text.insert(tk.END, initial_message + "\n", "center")
        self.char_slider = tk.Scale(output_text_and_slider_frame, from_=0, to=0, orient=tk.VERTICAL)
        self.char_slider.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        self.char_slider.configure(state=tk.DISABLED)

    initialize_menubar()
    initialize_size_elements()
    initialize_output_and_slider_frame()


def initialize_buttons(self):
    button_frame = tk.Frame(self)
    button_frame.pack()
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


def update_output_text(self, new_content):
    current_content = self.output_text.get(1.0, tk.END)
    if "\n\nEnter words below to continue\n\nType 'auto' or 'done' when finished" in current_content:
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

