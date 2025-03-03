# ui/directory_tab.py
# -*- coding: utf-8 -*-
import os
import customtkinter as ctk
from tkinter import messagebox
from ui.context_menu import TextWidgetContextMenu
from utils import read_file, save_string_to_txt, clear_file_content

def build_directory_tab(self):
    self.directory_tab = self.tabview.add(_("Chapter Blueprint"))
    self.directory_tab.rowconfigure(0, weight=0)
    self.directory_tab.rowconfigure(1, weight=1)
    self.directory_tab.columnconfigure(0, weight=1)

    load_btn = ctk.CTkButton(self.directory_tab, text=_("Load %s") % "Novel_outline.txt", command=self.load_chapter_blueprint, font=("Microsoft YaHei", 12))
    load_btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    save_btn = ctk.CTkButton(self.directory_tab, text=_("Save Modify"), command=self.save_chapter_blueprint, font=("Microsoft YaHei", 12))
    save_btn.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    self.directory_text = ctk.CTkTextbox(self.directory_tab, wrap="word", font=("Microsoft YaHei", 12))
    TextWidgetContextMenu(self.directory_text)
    self.directory_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

def load_chapter_blueprint(self):
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), _("Please set the save file path first"))
        return
    filename = os.path.join(filepath, "Novel_outline.txt")
    content = read_file(filename)
    self.directory_text.delete("0.0", "end")
    self.directory_text.insert("0.0", content)
    self.log(_("Novel_outline.txt content has been loaded to the editing area. "))

def save_chapter_blueprint(self):
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), _("Please set the save file path first"))
        return
    content = self.directory_text.get("0.0", "end").strip()
    filename = os.path.join(filepath, "Novel_outline.txt")
    clear_file_content(filename)
    save_string_to_txt(content, filename)
    self.log(_("Saved modifications to Novel_outline.txt."))
