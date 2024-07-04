import tkinter as tk


class InterfaceCreator:
    def __init__(self, root):
        self.root = root

    def initialize_base_UI_elements(self):
        def initialize_menubar():
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

        def initialize_size_elements():
            self.root.size_label_frame = tk.Frame(self.root, pady=10)
            self.root.size_label_frame.pack()
            self.root.size_prompt_label = tk.Label(self.root.size_label_frame, text="Select grid size:")
            self.root.size_prompt_label.pack(side=tk.LEFT, padx=(0, 2))

            def custom_size_elements():
                self.root.size_set_entry = tk.Entry(self.root.size_label_frame, width=10, justify='center')
                self.root.size_set_entry.pack(side=tk.LEFT, padx=(0, 5))
                self.root.size_set_entry.bind("<Return>", self.root.set_size)

                self.root.size_set_button = tk.Button(self.root.size_label_frame, text="Set",
                                                      command=self.root.set_size)
                self.root.size_set_button.pack(side=tk.LEFT, padx=(0, 50))

            def preset_size_buttons():
                small_size = 6
                medium_size = 12
                large_size = 16

                self.root.small_button = tk.Button(
                    self.root.size_label_frame, text="Small",
                    command=lambda size=small_size: self.root.set_preset_size(small_size), state=tk.NORMAL)
                self.root.small_button.pack(side=tk.LEFT, padx=0.25)
                self.root.small_button.bind("<Return>",
                                            lambda event, size=small_size: self.root.set_preset_size(small_size))

                self.root.medium_button = tk.Button(
                    self.root.size_label_frame, text="Medium",
                    command=lambda size=medium_size: self.root.set_preset_size(medium_size), state=tk.NORMAL)
                self.root.medium_button.pack(side=tk.LEFT, padx=0.25)
                self.root.medium_button.bind("<Return>",
                                             lambda event, size=medium_size: self.root.set_preset_size(medium_size))

                self.root.large_button = tk.Button(
                    self.root.size_label_frame, text="Large",
                    command=lambda size=large_size: self.root.set_preset_size(large_size), state=tk.NORMAL)
                self.root.large_button.pack(side=tk.LEFT, padx=0.25)
                self.root.large_button.bind("<Return>",
                                            lambda event, size=large_size: self.root.set_preset_size(large_size))

            custom_size_elements()
            preset_size_buttons()

        initialize_menubar()
        initialize_size_elements()

        output_text_and_fill_indicator_frame = tk.Frame(self.root)
        output_text_and_fill_indicator_frame.pack(pady=(10, 20), padx=20, fill=tk.BOTH, expand=True)
        self.initialize_output_text(output_text_and_fill_indicator_frame)
        self.initialize_scale(output_text_and_fill_indicator_frame)

    def initialize_output_text(self, output_text_and_fill_indicator_frame):
        initial_message = "\n\n\n\nEnter a size to continue"
        self.root.output_text = tk.Text(output_text_and_fill_indicator_frame, height=10, width=40, wrap=tk.WORD)
        self.root.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.root.output_text.tag_configure("center", justify='center')
        self.root.output_text.insert(tk.END, initial_message + "\n", "center")

    def initialize_scale(self, output_text_and_fill_indicator_frame):
        self.root.character_fill_indicator = tk.Scale(
            output_text_and_fill_indicator_frame, from_=1, to=0, orient=tk.VERTICAL)
        self.root.character_fill_indicator.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        self.root.character_fill_indicator.configure(state=tk.DISABLED)


    def initialize_word_entry_buttons(self, word_search_gui):
        button_frame = tk.Frame(self.root)
        button_frame.pack()

        self.root.auto_button = tk.Button(button_frame, text="Auto", fg='green',
                                          command=self.root.auto_generate_words)
        self.root.auto_button.pack(side=tk.LEFT, padx=(10, 10), pady=10)
        self.root.auto_button.bind("<Return>", lambda event: self.root.auto_generate_words())

        self.root.done_button = tk.Button(button_frame, text="Done", fg='green', command=self.root.create)
        self.root.done_button.pack(side=tk.LEFT, padx=(10, 10), pady=10)

        self.root.word_add_entry = tk.Entry(button_frame, justify='center')
        self.root.word_add_entry.insert(0, 'click to enter word')
        self.root.word_add_entry.bind("<FocusIn>", self.root.on_word_entry_focus)
        self.root.word_add_entry.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        self.root.word_add_entry.bind("<Return>", self.root.add_word)

        self.root.word_add_button = tk.Button(button_frame, text="Add Word", command=self.root.add_word)
        self.root.word_add_button.config(state=tk.DISABLED)
        self.root.word_add_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)

