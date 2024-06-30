import tkinter as tk
from tkinter import messagebox


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
        text_and_slider_frame = tk.Frame(self)
        text_and_slider_frame.pack(pady=(10, 20), padx=20, fill=tk.BOTH, expand=True)

        self.output_text = tk.Text(text_and_slider_frame, height=10, width=40, wrap=tk.WORD)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.output_text.tag_configure("center", justify='center')

        initial_message = "\n\n\n\nEnter a size to continue"
        self.output_text.insert(tk.END, initial_message + "\n", "center")

        self.char_slider = tk.Scale(text_and_slider_frame, from_=0, to=0, orient=tk.VERTICAL)
        self.char_slider.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        self.char_slider.configure(state=tk.DISABLED)

    initialize_menubar()
    initialize_size_elements()
    initialize_output_and_slider_frame()
