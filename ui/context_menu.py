# ui/context_menu.py
# -*- coding: utf-8 -*-
import tkinter as tk
import customtkinter as ctk

class TextWidgetContextMenu:
    """
    Provides the right-click copy/cut/paste/select all for customtkinter.TextBox or tkinter.Text.
    """
    def __init__(self, widget):
        self.widget = widget
        self.menu = tk.Menu(widget, tearoff=0)
        self.menu.add_command(label="copy", command=self.copy)
        self.menu.add_command(label="paste", command=self.paste)
        self.menu.add_command(label="cut", command=self.cut)
        self.menu.add_separator()
        self.menu.add_command(label="select all", command=self.select_all)
        
        # Binding right-click event
        self.widget.bind("<Button-3>", self.show_menu)
        
    def show_menu(self, event):
        if isinstance(self.widget, ctk.CTkTextbox):
            try:
                self.menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.menu.grab_release()
            
    def copy(self):
        try:
            text = self.widget.get("sel.first", "sel.last")
            self.widget.clipboard_clear()
            self.widget.clipboard_append(text)
        except tk.TclError:
            pass  # Ignore errors when no text is selected

    def paste(self):
        try:
            text = self.widget.clipboard_get()
            self.widget.insert("insert", text)
        except tk.TclError:
            pass  # Ignore errors when clipboard is empty

    def cut(self):
        try:
            text = self.widget.get("sel.first", "sel.last")
            self.widget.delete("sel.first", "sel.last")
            self.widget.clipboard_clear()
            self.widget.clipboard_append(text)
        except tk.TclError:
            pass  # Ignore errors when no text is selected

    def select_all(self):
        self.widget.tag_add("sel", "1.0", "end")
