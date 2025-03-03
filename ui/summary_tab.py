# ui/summary_tab.py
# -*- coding: utf-8 -*-
import os
import customtkinter as ctk
from tkinter import messagebox
from ui.generation_handlers import copy_to_clipboard
from utils import read_file, save_string_to_txt, clear_file_content
from ui.context_menu import TextWidgetContextMenu

def build_summary_tab(self):
    self.summary_tab = self.tabview.add(_("Global Summary"))
    self.summary_tab.rowconfigure(0, weight=0)
    self.summary_tab.rowconfigure(1, weight=1)
    self.summary_tab.columnconfigure(0, weight=1)

    load_btn = ctk.CTkButton(self.summary_tab, text=_("Load %s") % "global_summary.txt", command=self.load_global_summary, font=("Microsoft YaHei", 12))
    load_btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")   
    
    copy_btn = ctk.CTkButton(
            self.summary_tab,
            text=_("Copy to Clipboard"),
            command=lambda: copy_to_clipboard(self, self.summary_text.get("0.0", "end").strip()),
            font=("Microsoft YaHei", 12)
        )
    copy_btn.grid(row=0, column=0, padx=200, pady=5, sticky="w")

    save_btn = ctk.CTkButton(self.summary_tab, text="Save Modify", command=self.save_global_summary, font=("Microsoft YaHei", 12))
    save_btn.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    self.summary_text = ctk.CTkTextbox(self.summary_tab, wrap="word", font=("Microsoft YaHei", 12))
    TextWidgetContextMenu(self.summary_text)
    self.summary_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

def load_global_summary(self):
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), _("Please set the save file path first"))
        return
    filename = os.path.join(filepath, "global_summary.txt")
    content = read_file(filename)
    self.summary_text.delete("0.0", "end")
    self.summary_text.insert("0.0", content)
    self.log(_("Loaded %s into the editing area.") % "global_summary.txt")

def save_global_summary(self):
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), _("Please set the save file path first"))
        return
    content = self.summary_text.get("0.0", "end").strip()
    filename = os.path.join(filepath, "global_summary.txt")
    clear_file_content(filename)
    save_string_to_txt(content, filename)
    self.log(_("Saved modifications to %s.") % "global_summary.txt")
