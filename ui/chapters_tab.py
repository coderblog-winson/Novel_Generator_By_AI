# ui/chapters_tab.py
# -*- coding: utf-8 -*-
import os
import customtkinter as ctk
from tkinter import messagebox
from ui.context_menu import TextWidgetContextMenu
from ui.generation_handlers import copy_to_clipboard
from utils import read_file, save_string_to_txt, clear_file_content

def build_chapters_tab(self):
    self.chapters_view_tab = self.tabview.add(_("Chapters Manage"))
    self.chapters_view_tab.rowconfigure(0, weight=0)
    self.chapters_view_tab.rowconfigure(1, weight=1)
    self.chapters_view_tab.columnconfigure(0, weight=1)

    top_frame = ctk.CTkFrame(self.chapters_view_tab)
    top_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    top_frame.columnconfigure(0, weight=0)
    top_frame.columnconfigure(1, weight=0)
    top_frame.columnconfigure(2, weight=0)
    top_frame.columnconfigure(3, weight=0)
    top_frame.columnconfigure(4, weight=1)

    prev_btn = ctk.CTkButton(top_frame, text=_("<< Previous Chapter"), command=self.prev_chapter, font=("Microsoft YaHei", 12))
    prev_btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    next_btn = ctk.CTkButton(top_frame, text=_("Next Chapter >>"), command=self.next_chapter, font=("Microsoft YaHei", 12))
    next_btn.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    self.chapter_select_var = ctk.StringVar(value="")
    self.chapter_select_menu = ctk.CTkOptionMenu(top_frame, values=[], variable=self.chapter_select_var, command=self.on_chapter_selected, font=("Microsoft YaHei", 12))
    self.chapter_select_menu.grid(row=0, column=2, padx=5, pady=5, sticky="w")

    save_btn = ctk.CTkButton(top_frame, text=_("Save Modification"), command=self.save_current_chapter, font=("Microsoft YaHei", 12))
    save_btn.grid(row=0, column=3, padx=5, pady=5, sticky="w")   
    
    copy_btn = ctk.CTkButton(
            top_frame,
            text=_("Copy to Clipboard"),
            command=lambda: copy_to_clipboard(self, self.chapter_view_text.get("0.0", "end").strip()),
            font=("Microsoft YaHei", 12)
        )
    copy_btn.grid(row=0, column=3, padx=200, pady=5, sticky="w")

    refresh_btn = ctk.CTkButton(top_frame, text=_("refresh chapter list"), command=self.refresh_chapters_list, font=("Microsoft YaHei", 12))
    refresh_btn.grid(row=0, column=4, padx=5, pady=5, sticky="e")

    self.chapter_view_text = ctk.CTkTextbox(self.chapters_view_tab, wrap="word", font=("Microsoft YaHei", 12))
    TextWidgetContextMenu(self.chapter_view_text)
    self.chapter_view_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    self.chapters_list = []
    refresh_chapters_list(self)

def refresh_chapters_list(self):
    filepath = self.filepath_var.get().strip()
    chapters_dir = os.path.join(filepath, "chapters")
    if not os.path.exists(chapters_dir):
        self.safe_log(_("The chapters folder has not been found, please make a chapter or check the save path."))
        self.chapter_select_menu.configure(values=[])
        return

    all_files = os.listdir(chapters_dir)
    chapter_nums = []
    for f in all_files:
        if f.startswith("chapter_") and f.endswith(".txt"):
            number_part = f.replace("chapter_", "").replace(".txt", "")
            if number_part.isdigit():
                chapter_nums.append(number_part)
    chapter_nums.sort(key=lambda x: int(x))
    self.chapters_list = chapter_nums
    self.chapter_select_menu.configure(values=self.chapters_list)
    current_selected = self.chapter_select_var.get()
    if current_selected not in self.chapters_list:
        if self.chapters_list:
            self.chapter_select_var.set(self.chapters_list[0])
            load_chapter_content(self, self.chapters_list[0])
        else:
            self.chapter_select_var.set("")
            self.chapter_view_text.delete("0.0", "end")

def on_chapter_selected(self, value):
    load_chapter_content(self, value)

def load_chapter_content(self, chapter_number_str):
    if not chapter_number_str:
        return
    filepath = self.filepath_var.get().strip()
    chapter_file = os.path.join(filepath, "chapters", f"chapter_{chapter_number_str}.txt")
    if not os.path.exists(chapter_file):
        self.safe_log(_("Chapter file %s does not exist!") % chapter_file)
        return
    content = read_file(chapter_file)
    self.chapter_view_text.delete("0.0", "end")
    self.chapter_view_text.insert("0.0", content)
    
def load_chapter_content_only(self, chapter_number_str):
    """
    Only load the chapter content and return it, without updating the UI.
    """
    if not chapter_number_str:
        return
    try:
        filepath = self.filepath_var.get().strip()
        chapter_file = os.path.join(filepath, "chapters", f"chapter_{chapter_number_str}.txt")
        if not os.path.exists(chapter_file):
            return ''
        content = read_file(chapter_file)
        return content
    except Exception as e:
        pass
    return ''

def save_current_chapter(self):
    chapter_number_str = self.chapter_select_var.get()
    if not chapter_number_str:
        messagebox.showwarning(_("Warning"), _("No chapter has been selected and cannot be saved."))
        return
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), _("Please configure the save file path first"))
        return
    chapter_file = os.path.join(filepath, "chapters", f"chapter_{chapter_number_str}.txt")
    content = self.chapter_view_text.get("0.0", "end").strip()
    clear_file_content(chapter_file)
    save_string_to_txt(content, chapter_file)
    self.safe_log(_("Save modifications to chapter %s.") % chapter_number_str)

def prev_chapter(self):
    if not self.chapters_list:
        return
    current = self.chapter_select_var.get()
    if current not in self.chapters_list:
        return
    idx = self.chapters_list.index(current)
    if idx > 0:
        new_idx = idx - 1
        self.chapter_select_var.set(self.chapters_list[new_idx])
        load_chapter_content(self, self.chapters_list[new_idx])
    else:
        messagebox.showinfo(_("Info"), _("It's already the first chapter."))

def next_chapter(self):
    if not self.chapters_list:
        return
    current = self.chapter_select_var.get()
    if current not in self.chapters_list:
        return
    idx = self.chapters_list.index(current)
    if idx < len(self.chapters_list) - 1:
        new_idx = idx + 1
        self.chapter_select_var.set(self.chapters_list[new_idx])
        load_chapter_content(self, self.chapters_list[new_idx])
    else:
        messagebox.showinfo(_("Info"), _("It's already the last chapter."))
