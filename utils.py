# utils.py
# -*- coding: utf-8 -*-
import os
import json


def read_file(filename: str) -> str:
    """Reads all the contents of the file, and returns an empty string if the file does not exist or is abnormal. """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return ""
    except Exception as e:
        print(_("[read_file] An error occurred while reading a file: %s") % str(e))
        return ""

def append_text_to_file(text_to_append: str, file_path: str):
    """Add text at the end of the file (with line breaks). If the text is not empty and there is no line break, line breaks will be automatically added."""
    if text_to_append and not text_to_append.startswith('\n'):
        text_to_append = '\n' + text_to_append

    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(text_to_append)
    except IOError as e:
        print(_("[append_text_to_file] An error occurred: %s") % str(e))

def clear_file_content(filename: str):
    """Clear the contents of the specified file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            pass
    except IOError as e:
        print(_("[clear_file_content] Unable to clear the content of file: %s") % str(e))

def save_string_to_txt(content: str, filename: str):
    """Save the string as a txt file (overwrite). """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(_("[save_string_to_txt] An error occurred while saving the file: %s") % str(e))

def save_data_to_json(data: dict, file_path: str) -> bool:
    """Save data to a JSON file. """
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(_("[save_data_to_json] Error saving data to JSON file: %s") % str(e))
        return False

