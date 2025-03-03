# ui/novel_params_tab.py
# -*- coding: utf-8 -*-
import customtkinter as ctk
from tkinter import filedialog, messagebox
from locale_handler import set_current_language
from ui.config_tab import save_config_btn
from ui.context_menu import TextWidgetContextMenu

def build_novel_params_area(self, start_row=1):
    
    def on_language_changed(new_value):
        """
        When switching languages, update the current language
        """
        if messagebox.askyesno(_("Confirm Language Change"), _("The app will be restart if you change the language, are you confirm?")):
            save_config_btn(self)
            set_current_language(self.language_var.get(), is_restart=True)
            
    self.params_frame = ctk.CTkScrollableFrame(self.right_frame, orientation="vertical")
    self.params_frame.grid(row=start_row, column=0, sticky="nsew", padx=5, pady=5)
    self.params_frame.columnconfigure(1, weight=1)
    
    # 0) Setup current language
    create_label_with_help_for_novel_params(self, parent=self.params_frame, label_text=_("Language:"), tooltip_key="language", row=0, column=0, font=("Microsoft YaHei", 12), sticky="ne")
    language_dropdown = ctk.CTkOptionMenu(self.params_frame, values=["English", "Chinese"], variable=self.language_var, command=on_language_changed, font=("Microsoft YaHei", 12))
    language_dropdown.grid(row=0, column=1, padx=5, pady=5, columnspan=2, sticky="nsew")

    # 1) Topic
    create_label_with_help_for_novel_params(self, parent=self.params_frame, label_text=_("Topic:"), tooltip_key="topic", row=1, column=0, font=("Microsoft YaHei", 12), sticky="ne")
    self.topic_text = ctk.CTkTextbox(self.params_frame, height=80, wrap="word", font=("Microsoft YaHei", 12))
    TextWidgetContextMenu(self.topic_text)
    self.topic_text.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    if hasattr(self, 'topic_default') and self.topic_default:
        self.topic_text.insert("0.0", self.topic_default)

    # 2) Type
    create_label_with_help_for_novel_params(self, parent=self.params_frame, label_text=_("Type:"), tooltip_key="genre", row=2, column=0, font=("Microsoft YaHei", 12))
    genre_entry = ctk.CTkEntry(self.params_frame, textvariable=self.genre_var, font=("Microsoft YaHei", 12))
    genre_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    # 3) Chapter Number & Word Number per Chapter
    row_for_chapter_and_word = 3
    create_label_with_help_for_novel_params(self, parent=self.params_frame, label_text=_("Chapter counter &\n number of Word per Chapter:"), tooltip_key="num_chapters", row=row_for_chapter_and_word, column=0, font=("Microsoft YaHei", 12))
    chapter_word_frame = ctk.CTkFrame(self.params_frame)
    chapter_word_frame.grid(row=row_for_chapter_and_word, column=1, padx=5, pady=5, sticky="ew")
    chapter_word_frame.columnconfigure((0, 1, 2, 3), weight=0)
    num_chapters_label = ctk.CTkLabel(chapter_word_frame, text=_("Number of Chapter:"), font=("Microsoft YaHei", 12))
    num_chapters_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    num_chapters_entry = ctk.CTkEntry(chapter_word_frame, textvariable=self.num_chapters_var, width=60, font=("Microsoft YaHei", 12))
    num_chapters_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    word_number_label = ctk.CTkLabel(chapter_word_frame, text=_("Number of words per chapter:"), font=("Microsoft YaHei", 12))
    word_number_label.grid(row=1, column=0, padx=(15, 5), pady=5, sticky="e")
    word_number_entry = ctk.CTkEntry(chapter_word_frame, textvariable=self.word_number_var, width=60, font=("Microsoft YaHei", 12))
    word_number_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # 4) Save the path
    row_fp = 4
    create_label_with_help_for_novel_params(self, parent=self.params_frame, label_text=_("Save the path:"), tooltip_key="filepath", row=row_fp, column=0, font=("Microsoft YaHei", 12))
    self.filepath_frame = ctk.CTkFrame(self.params_frame)
    self.filepath_frame.grid(row=row_fp, column=1, padx=5, pady=5, sticky="nsew")
    self.filepath_frame.columnconfigure(0, weight=1)
    filepath_entry = ctk.CTkEntry(self.filepath_frame, textvariable=self.filepath_var, font=("Microsoft YaHei", 12))
    filepath_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    browse_btn = ctk.CTkButton(self.filepath_frame, text=_("Browse..."), command=self.browse_folder, width=60, font=("Microsoft YaHei", 12))
    browse_btn.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    # 5) Chapter number
    row_chap_num = 5
    create_label_with_help_for_novel_params(self, parent=self.params_frame, label_text=_("Chapter number:"), tooltip_key="chapter_num", row=row_chap_num, column=0, font=("Microsoft YaHei", 12))
    chapter_num_entry = ctk.CTkEntry(self.params_frame, textvariable=self.chapter_num_var, width=80, font=("Microsoft YaHei", 12))
    chapter_num_entry.grid(row=row_chap_num, column=1, padx=5, pady=5, sticky="w")

    # 6) Guidance in this chapter
    row_user_guide = 6
    create_label_with_help_for_novel_params(self, parent=self.params_frame, label_text=_("Guidance in this chapter:"), tooltip_key="user_guidance", row=row_user_guide, column=0, font=("Microsoft YaHei", 12), sticky="ne")
    self.user_guide_text = ctk.CTkTextbox(self.params_frame, height=80, wrap="word", font=("Microsoft YaHei", 12))
    TextWidgetContextMenu(self.user_guide_text)
    self.user_guide_text.grid(row=row_user_guide, column=1, padx=5, pady=5, sticky="nsew")
    if hasattr(self, 'user_guidance_default') and self.user_guidance_default:
        self.user_guide_text.insert("0.0", self.user_guidance_default)

    # 7) Optional elements: core characters/key props/space coordinates/time pressure
    row_idx = 7
    create_label_with_help_for_novel_params(self, parent=self.params_frame, label_text=_("Core characters:"), tooltip_key="characters_involved", row=row_idx, column=0, font=("Microsoft YaHei", 12))
    char_inv_entry = ctk.CTkEntry(self.params_frame, textvariable=self.characters_involved_var, font=("Microsoft YaHei", 12))
    char_inv_entry.grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
    row_idx += 1
    create_label_with_help_for_novel_params(self, parent=self.params_frame, label_text=_("Key props:"), tooltip_key="key_items", row=row_idx, column=0, font=("Microsoft YaHei", 12))
    key_items_entry = ctk.CTkEntry(self.params_frame, textvariable=self.key_items_var, font=("Microsoft YaHei", 12))
    key_items_entry.grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
    row_idx += 1
    create_label_with_help_for_novel_params(self, parent=self.params_frame, label_text=_("Space coordinates:"), tooltip_key="scene_location", row=row_idx, column=0, font=("Microsoft YaHei", 12))
    scene_loc_entry = ctk.CTkEntry(self.params_frame, textvariable=self.scene_location_var, font=("Microsoft YaHei", 12))
    scene_loc_entry.grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")
    row_idx += 1
    create_label_with_help_for_novel_params(self, parent=self.params_frame, label_text=_("Time pressure:"), tooltip_key="time_constraint", row=row_idx, column=0, font=("Microsoft YaHei", 12))
    time_const_entry = ctk.CTkEntry(self.params_frame, textvariable=self.time_constraint_var, font=("Microsoft YaHei", 12))
    time_const_entry.grid(row=row_idx, column=1, padx=5, pady=5, sticky="ew")

def build_optional_buttons_area(self, start_row=2):
    self.optional_btn_frame = ctk.CTkFrame(self.right_frame)
    self.optional_btn_frame.grid(row=start_row, column=0, sticky="ew", padx=5, pady=5)
    self.optional_btn_frame.columnconfigure((0, 1, 2, 3), weight=1)

    self.btn_check_consistency = ctk.CTkButton(self.optional_btn_frame, text=_("Consistency review"), command=self.do_consistency_check, font=("Microsoft YaHei", 12))
    self.btn_check_consistency.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    self.btn_import_knowledge = ctk.CTkButton(self.optional_btn_frame, text=_("Import the knowledge base"), command=self.import_knowledge_handler, font=("Microsoft YaHei", 12))
    self.btn_import_knowledge.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    self.btn_clear_vectorstore = ctk.CTkButton(self.optional_btn_frame, text=_("Clear the vector library"), fg_color="red", command=self.clear_vectorstore_handler, font=("Microsoft YaHei", 12))
    self.btn_clear_vectorstore.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    self.plot_arcs_btn = ctk.CTkButton(self.optional_btn_frame, text=_("View the plot points"), command=self.show_plot_arcs_ui, font=("Microsoft YaHei", 12))
    self.plot_arcs_btn.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

def create_label_with_help_for_novel_params(self, parent, label_text, tooltip_key, row, column, font=None, sticky="e", padx=5, pady=5):
    frame = ctk.CTkFrame(parent)
    frame.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    frame.columnconfigure(0, weight=0)
    label = ctk.CTkLabel(frame, text=label_text, font=font)
    label.pack(side="left")  
    btn = ctk.CTkButton(
        frame,
        text=_("?"),
        width=22,
        height=22,
        font=("Microsoft YaHei", 10),
        command=lambda: messagebox.showinfo(_("Parameter description"), tooltips.get(tooltip_key, _("No description yet")))
    )
     
    btn.pack(side="left", padx=3)
    return frame
