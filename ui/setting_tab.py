# ui/setting_tab.py
# -*- coding: utf-8 -*-
import os
import customtkinter as ctk
from tkinter import messagebox
from ui.generation_handlers import copy_to_clipboard
from utils import FontManager, read_file, save_string_to_txt, clear_file_content
from ui.context_menu import TextWidgetContextMenu

font_manager = FontManager(12) 

def build_setting_tab(self):
    self.setting_tab = self.tabview.add(_("Novel Architecture"))
    self.setting_tab.rowconfigure(0, weight=0)
    self.setting_tab.rowconfigure(1, weight=1)
    self.setting_tab.columnconfigure(0, weight=1)

    load_btn = ctk.CTkButton(self.setting_tab, text=_("Load %s") % "Novel_architecture.txt", command=self.load_novel_architecture, font=("Microsoft YaHei", 12))
    load_btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")    
    
    copy_btn = ctk.CTkButton(
            self.setting_tab,
            text=_("Copy to Clipboard"),
            command=lambda: copy_to_clipboard(self, self.setting_text.get("0.0", "end").strip()),
            font=("Microsoft YaHei", 12)
        )
    copy_btn.grid(row=0, column=0, padx=200, pady=5, sticky="w")
    
    increase_font_btn = ctk.CTkButton(
            self.setting_tab,
            width=30,
            text="+",
            command=lambda: font_manager.increase_font(self.setting_text),
            font=("Microsoft YaHei", 12)
        )
    increase_font_btn.grid(row=0, column=0, padx=380, pady=5, sticky="w")
    
    decrease_font_btn = ctk.CTkButton(
            self.setting_tab,
            width=30,
            text="-",
            command=lambda: font_manager.decrease_font(self.setting_text),
            font=("Microsoft YaHei", 12)
        )
    decrease_font_btn.grid(row=0, column=0, padx=420, pady=5, sticky="w")

    save_btn = ctk.CTkButton(self.setting_tab, text=_("Save Modify"), command=self.save_novel_architecture, font=("Microsoft YaHei", 12))
    save_btn.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    self.setting_text = ctk.CTkTextbox(self.setting_tab, wrap="word", font=("Microsoft YaHei", 12))
    TextWidgetContextMenu(self.setting_text)
    self.setting_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

def load_novel_architecture(self):
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), _("Please set the save file path first"))
        return
    filename = os.path.join(filepath, "Novel_architecture.txt")
    content = read_file(filename)
    self.setting_text.delete("0.0", "end")
    self.setting_text.insert("0.0", content)
    self.log(_("%s content loaded to the editing area.") % "Novel_architecture.txt")

def save_novel_architecture(self):
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), _("Please set the save file path first."))
        return
    content = self.setting_text.get("0.0", "end").strip()
    filename = os.path.join(filepath, "Novel_architecture.txt")
    clear_file_content(filename)
    save_string_to_txt(content, filename)
    self.log(_("Modifications to %s have been saved. ") % "Novel_architecture.txt")
