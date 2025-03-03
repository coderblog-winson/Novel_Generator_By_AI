# ui/main_tab.py
# -*- coding: utf-8 -*-
import customtkinter as ctk
from tkinter import messagebox
from ui.context_menu import TextWidgetContextMenu

def build_main_tab(self):
    """
    The main tab contains the "Content of this Chapter" edit box and output log on the left, as well as the main operation and parameter setting area on the right
    """
    self.main_tab = self.tabview.add(_("Main Functions"))
    self.main_tab.rowconfigure(0, weight=1)
    self.main_tab.columnconfigure(0, weight=1)
    self.main_tab.columnconfigure(1, weight=0)

    self.left_frame = ctk.CTkFrame(self.main_tab)
    self.left_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    self.right_frame = ctk.CTkFrame(self.main_tab)
    self.right_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

    build_left_layout(self)
    build_right_layout(self)

def build_left_layout(self):
    """
    The left area: content of this chapter (editable) + Step process button + Output log (read-only)
    """
    self.left_frame.grid_rowconfigure(0, weight=0)
    self.left_frame.grid_rowconfigure(1, weight=2)
    self.left_frame.grid_rowconfigure(2, weight=0)
    self.left_frame.grid_rowconfigure(3, weight=0)
    self.left_frame.grid_rowconfigure(4, weight=1)
    self.left_frame.columnconfigure(0, weight=1)

    chapter_label = ctk.CTkLabel(self.left_frame, text=_("Contents of this chapter (editable)"), font=("Microsoft YaHei", 12))
    chapter_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")

    # Chapter text editing box
    self.chapter_result = ctk.CTkTextbox(self.left_frame, wrap="word", font=("Microsoft YaHei", 14))
    TextWidgetContextMenu(self.chapter_result)
    self.chapter_result.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))

    # Step Button Area
    self.step_buttons_frame = ctk.CTkFrame(self.left_frame)
    self.step_buttons_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    self.step_buttons_frame.columnconfigure((0, 1, 2, 3), weight=1)

    self.btn_generate_architecture = ctk.CTkButton(
        self.step_buttons_frame,
        text=_("Step1. Generate architecture"),
        command=self.generate_novel_architecture_ui,
        font=("Microsoft YaHei", 12)
    )
    self.btn_generate_architecture.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

    self.btn_generate_directory = ctk.CTkButton(
        self.step_buttons_frame,
        text=_("Step2. Generate outline"),
        command=self.generate_chapter_blueprint_ui,
        font=("Microsoft YaHei", 12)
    )
    self.btn_generate_directory.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

    self.btn_generate_chapter = ctk.CTkButton(
        self.step_buttons_frame,
        text=_("Step3. Generate draft"),
        command=self.generate_chapter_draft_ui,
        font=("Microsoft YaHei", 12)
    )
    self.btn_generate_chapter.grid(row=0, column=2, padx=5, pady=2, sticky="ew")

    self.btn_finalize_chapter = ctk.CTkButton(
        self.step_buttons_frame,
        text=_("Step4. Final chapter"),
        command=self.finalize_chapter_ui,
        font=("Microsoft YaHei", 12)
    )
    self.btn_finalize_chapter.grid(row=0, column=3, padx=5, pady=2, sticky="ew")

    # Log text box
    log_label = ctk.CTkLabel(self.left_frame, text=_("Output log (read-only)"), font=("Microsoft YaHei", 12))
    log_label.grid(row=3, column=0, padx=5, pady=(5, 0), sticky="w")

    self.log_text = ctk.CTkTextbox(self.left_frame, wrap="word", font=("Microsoft YaHei", 12))
    TextWidgetContextMenu(self.log_text)
    self.log_text.grid(row=4, column=0, sticky="nsew", padx=5, pady=(0, 5))
    self.log_text.configure(state="disabled")

def build_right_layout(self):
    """
    The right area: configuration area (tabview) + novel main parameters + optional function buttons
    """
    self.right_frame.grid_rowconfigure(0, weight=0)
    self.right_frame.grid_rowconfigure(1, weight=1)
    self.right_frame.grid_rowconfigure(2, weight=0)
    self.right_frame.columnconfigure(0, weight=1)

    # Configuration area (AI/Embedding)
    self.config_frame = ctk.CTkFrame(self.right_frame, corner_radius=10, border_width=2, border_color="gray")
    self.config_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    self.config_frame.columnconfigure(0, weight=1)
    # The rest will be built in config_tab.py and novel_params_tab.py
