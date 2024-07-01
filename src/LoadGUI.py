import tkinter as tk


def initialize_base_UI_elements(word_search_gui):
    def initialize_menubar():
        menubar = tk.Menu(word_search_gui)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save as...", command=word_search_gui.save_file, state=tk.DISABLED)
        filemenu.add_command(label="Load file", command=word_search_gui.load_file, state=tk.NORMAL)
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Reset", command=word_search_gui.reset, state=tk.NORMAL)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Settings", menu=editmenu)
        word_search_gui.config(menu=menubar)

        word_search_gui.filemenu = filemenu

    def initialize_size_elements():
        word_search_gui.size_label_frame = tk.Frame(word_search_gui, pady=10)
        word_search_gui.size_label_frame.pack()
        word_search_gui.size_prompt_label = tk.Label(word_search_gui.size_label_frame, text="Select grid size:")
        word_search_gui.size_prompt_label.pack(side=tk.LEFT, padx=(0, 2))

        def custom_size_elements():
            word_search_gui.size_set_entry = tk.Entry(word_search_gui.size_label_frame, width=10, justify='center')
            word_search_gui.size_set_entry.pack(side=tk.LEFT, padx=(0, 5))
            word_search_gui.size_set_entry.bind("<Return>", word_search_gui.set_size)

            word_search_gui.size_set_button = tk.Button(word_search_gui.size_label_frame, text="Set",
                                                        command=word_search_gui.set_size)
            word_search_gui.size_set_button.pack(side=tk.LEFT, padx=(0, 50))

        def preset_size_buttons():
            small_size = 6
            medium_size = 12
            large_size = 16

            word_search_gui.small_button = tk.Button(
                word_search_gui.size_label_frame, text="Small",
                command=lambda size=small_size: word_search_gui.set_preset_size(small_size), state=tk.NORMAL)
            word_search_gui.small_button.pack(side=tk.LEFT, padx=0.25)
            word_search_gui.small_button.bind("<Return>",
                                              lambda event, size=small_size: word_search_gui.set_preset_size(6))

            word_search_gui.medium_button = tk.Button(
                word_search_gui.size_label_frame, text="Medium",
                command=lambda size=medium_size: word_search_gui.set_preset_size(medium_size), state=tk.NORMAL)
            word_search_gui.medium_button.pack(side=tk.LEFT, padx=0.25)
            word_search_gui.medium_button.bind("<Return>",
                                               lambda event, size=medium_size: word_search_gui.set_preset_size(2))

            word_search_gui.large_button = tk.Button(
                word_search_gui.size_label_frame, text="Large",
                command=lambda size=large_size: word_search_gui.set_preset_size(large_size), state=tk.NORMAL)
            word_search_gui.large_button.pack(side=tk.LEFT, padx=0.25)
            word_search_gui.large_button.bind("<Return>",
                                              lambda event, size=large_size: word_search_gui.set_preset_size(16))

        custom_size_elements()
        preset_size_buttons()

    initialize_menubar()
    initialize_size_elements()
    output_text_and_fill_indicator_frame = tk.Frame(word_search_gui)
    output_text_and_fill_indicator_frame.pack(pady=(10, 20), padx=20, fill=tk.BOTH, expand=True)
    initialize_output_text(word_search_gui, output_text_and_fill_indicator_frame)
    initialize_scale(word_search_gui, output_text_and_fill_indicator_frame)


def initialize_output_text(word_search_gui, output_text_and_fill_indicator_frame):
    initial_message = "\n\n\n\nEnter a size to continue"
    word_search_gui.output_text = tk.Text(output_text_and_fill_indicator_frame, height=10, width=40, wrap=tk.WORD)
    word_search_gui.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
    word_search_gui.output_text.tag_configure("center", justify='center')
    word_search_gui.output_text.insert(tk.END, initial_message + "\n", "center")


def initialize_scale(word_search_gui, output_text_and_fill_indicator_frame):
    word_search_gui.character_fill_indicator = tk.Scale(
        output_text_and_fill_indicator_frame, from_=1, to=0, orient=tk.VERTICAL)
    word_search_gui.character_fill_indicator.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
    word_search_gui.character_fill_indicator.configure(state=tk.DISABLED)


def adjust_output_text_for_size(output_text_widget, size):
    initial_message = "\n\nEnter words below to continue\n\nType 'auto' or 'done' when finished"
    output_text_widget.config(state=tk.NORMAL)
    output_text_widget.delete(1.0, tk.END)

    text_height = min(max(size * 3, 10), 30)
    text_width = min(max(size * 5, 40), 80)
    output_text_widget.config(height=text_height, width=text_width)
    output_text_widget.insert(tk.END, initial_message + "\n", "center")
    output_text_widget.config(state=tk.DISABLED)


def initialize_word_entry_buttons(word_search_gui):
    button_frame = tk.Frame(word_search_gui)
    button_frame.pack()

    word_search_gui.auto_button = tk.Button(button_frame, text="Auto", fg='green',
                                            command=word_search_gui.auto_generate_words)
    word_search_gui.auto_button.pack(side=tk.LEFT, padx=(10, 10), pady=10)
    word_search_gui.auto_button.bind("<Return>", lambda event: word_search_gui.auto_generate_words())

    word_search_gui.done_button = tk.Button(button_frame, text="Done", fg='green', command=word_search_gui.create)
    word_search_gui.done_button.pack(side=tk.LEFT, padx=(10, 10), pady=10)

    word_search_gui.word_add_entry = tk.Entry(button_frame, justify='center')
    word_search_gui.word_add_entry.insert(0, 'click to enter word')
    word_search_gui.word_add_entry.bind("<FocusIn>", word_search_gui.on_word_entry_focus)
    word_search_gui.word_add_entry.pack(side=tk.LEFT, padx=(10, 5), pady=10)
    word_search_gui.word_add_entry.bind("<Return>", word_search_gui.add_word)

    word_search_gui.word_add_button = tk.Button(button_frame, text="Add Word", command=word_search_gui.add_word)
    word_search_gui.word_add_button.config(state=tk.DISABLED)
    word_search_gui.word_add_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)
