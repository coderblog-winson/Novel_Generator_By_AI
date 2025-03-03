# main.py
# -*- coding: utf-8 -*-
import customtkinter as ctk
from locale_handler import set_current_language
from ui import NovelGeneratorGUI


def main():
    set_current_language()
    app = ctk.CTk()
    gui = NovelGeneratorGUI(app)
    app.mainloop()

if __name__ == "__main__":
    main()
