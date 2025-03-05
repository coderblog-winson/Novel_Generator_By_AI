# ui/generation_handlers.py
# -*- coding: utf-8 -*-
import os
import re
import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import traceback
import pyperclip
from utils import FontManager, read_file, save_string_to_txt, clear_file_content
from novel_generator import (
    Novel_architecture_generate,
    Chapter_blueprint_generate,
    generate_chapter_draft,
    finalize_chapter,
    import_knowledge_file,
    clear_vector_store,
    enrich_chapter_text
)
from novel_generator.consistency_checker import check_consistency

font_manager = FontManager(12) 

def generate_novel_architecture_ui(self):
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), _("Please select the save file path first"))
        return

    def task():
        self.disable_button_safe(self.btn_generate_architecture)
        try:
            interface_format = self.interface_format_var.get().strip()
            api_key = self.api_key_var.get().strip()
            base_url = self.base_url_var.get().strip()
            model_name = self.model_name_var.get().strip()
            temperature = self.temperature_var.get()
            max_tokens = self.max_tokens_var.get()
            timeout_val = self.safe_get_int(self.timeout_var, 600)

            topic = self.topic_text.get("0.0", "end").strip()
            genre = self.genre_var.get().strip()
            num_chapters = self.safe_get_int(self.num_chapters_var, 10)
            word_number = self.safe_get_int(self.word_number_var, 3000)

            self.safe_log(_("Start to generate novel architecture..."))
            Novel_architecture_generate(
                interface_format=interface_format,
                api_key=api_key,
                base_url=base_url,
                llm_model=model_name,
                topic=topic,
                genre=genre,
                number_of_chapters=num_chapters,
                word_number=word_number,
                filepath=filepath,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout_val
            )
            self.safe_log(_("✅ The novel architecture is generated. Please view or edit it in the 'Novel Architecture' tab."))
        except Exception:
            self.handle_exception(_("An error occurred while generating the novel architecture"))
        finally:
            self.enable_button_safe(self.btn_generate_architecture)
    threading.Thread(target=task, daemon=True).start()

def generate_chapter_blueprint_ui(self):
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), "Please select the save file path first")
        return

    def task():
        self.disable_button_safe(self.btn_generate_directory)
        try:
            interface_format = self.interface_format_var.get().strip()
            api_key = self.api_key_var.get().strip()
            base_url = self.base_url_var.get().strip()
            model_name = self.model_name_var.get().strip()
            number_of_chapters = self.safe_get_int(self.num_chapters_var, 10)
            temperature = self.temperature_var.get()
            max_tokens = self.max_tokens_var.get()
            timeout_val = self.safe_get_int(self.timeout_var, 600)

            self.safe_log(_("Start generating chapter blueprints..."))
            Chapter_blueprint_generate(
                interface_format=interface_format,
                api_key=api_key,
                base_url=base_url,
                llm_model=model_name,
                number_of_chapters=number_of_chapters,
                filepath=filepath,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout_val
            )
            self.safe_log(_("✅ Chapter blueprint generation is completed. Please view or edit it in the 'Chapter Blueprint' tab. "))
        except Exception:
            self.handle_exception(_("An error occurred while generating chapter blueprints"))
        finally:
            self.enable_button_safe(self.btn_generate_directory)
    threading.Thread(target=task, daemon=True).start()

def generate_chapter_draft_ui(self):
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), _("Please configure the save file path first."))
        return

    def task():
        self.disable_button_safe(self.btn_generate_chapter)
        try:
            interface_format = self.interface_format_var.get().strip()
            api_key = self.api_key_var.get().strip()
            base_url = self.base_url_var.get().strip()
            model_name = self.model_name_var.get().strip()
            temperature = self.temperature_var.get()
            max_tokens = self.max_tokens_var.get()
            timeout_val = self.safe_get_int(self.timeout_var, 600)

            chap_num = self.safe_get_int(self.chapter_num_var, 1)
            word_number = self.safe_get_int(self.word_number_var, 3000)
            user_guidance = self.user_guide_text.get("0.0", "end").strip()

            char_inv = self.characters_involved_var.get().strip()
            key_items = self.key_items_var.get().strip()
            scene_loc = self.scene_location_var.get().strip()
            time_constr = self.time_constraint_var.get().strip()

            embedding_api_key = self.embedding_api_key_var.get().strip()
            embedding_url = self.embedding_url_var.get().strip()
            embedding_interface_format = self.embedding_interface_format_var.get().strip()
            embedding_model_name = self.embedding_model_name_var.get().strip()
            embedding_k = self.safe_get_int(self.embedding_retrieval_k_var, 4)

            self.safe_log(_("Generate the draft of the chapter %d: Prepare to generate the request prompt word...") % chap_num)

            # Call the newly added build_chapter_prompt function to construct the initial prompt word
            from novel_generator.chapter import build_chapter_prompt
            prompt_text = build_chapter_prompt(
                api_key=api_key,
                base_url=base_url,
                model_name=model_name,
                filepath=filepath,
                novel_number=chap_num,
                word_number=word_number,
                temperature=temperature,
                user_guidance=user_guidance,
                characters_involved=char_inv,
                key_items=key_items,
                scene_location=scene_loc,
                time_constraint=time_constr,
                embedding_api_key=embedding_api_key,
                embedding_url=embedding_url,
                embedding_interface_format=embedding_interface_format,
                embedding_model_name=embedding_model_name,
                embedding_retrieval_k=embedding_k,
                interface_format=interface_format,
                max_tokens=max_tokens,
                timeout=timeout_val
            )

            # The editable prompt word dialog box pops up, waiting for the user to confirm or cancel
            result = {"prompt": None}
            event = threading.Event()

            def create_dialog():
                dialog = ctk.CTkToplevel(self.master)
                dialog.title(_("Current chapter request prompt word (editable)"))
                dialog.geometry("650x800")
                text_box = ctk.CTkTextbox(dialog, wrap="word", font=("Microsoft YaHei", 12))
                text_box.pack(fill="both", expand=True, padx=10, pady=10)
                text_box.insert("0.0", prompt_text)
                button_frame = ctk.CTkFrame(dialog)
                button_frame.pack(pady=10)
                def on_confirm():
                    result["prompt"] = text_box.get("1.0", "end").strip()
                    dialog.destroy()
                    event.set()
                def on_cancel():
                    result["prompt"] = None
                    dialog.destroy()
                    event.set()
                btn_confirm = ctk.CTkButton(button_frame, text=_("Confirm use"), font=("Microsoft YaHei", 12), command=on_confirm)
                btn_confirm.pack(side="left", padx=10)
                btn_cancel = ctk.CTkButton(button_frame, text=_("Cancel request"), font=("Microsoft YaHei", 12), command=on_cancel)
                btn_cancel.pack(side="left", padx=10)
                
                increase_font_btn = ctk.CTkButton(
                        button_frame,
                        width=30,
                        text="+",
                        command=lambda: font_manager.increase_font(text_box),
                        font=("Microsoft YaHei", 12)
                    )
                increase_font_btn.pack(side="left", padx=10)
                
                decrease_font_btn = ctk.CTkButton(
                        button_frame,
                        width=30,
                        text="-",
                        command=lambda: font_manager.decrease_font(text_box),
                        font=("Microsoft YaHei", 12)
                    )
                decrease_font_btn.pack(side="left", padx=10)
    
                # If the user directly closes the pop-up window, call on_cancel to process
                dialog.protocol("WM_DELETE_WINDOW", on_cancel)
                dialog.grab_set()
            self.master.after(0, create_dialog)
            event.wait()  # Wait for the user to complete
            edited_prompt = result["prompt"]
            if edited_prompt is None:
                self.safe_log(_("❌ The user canceled the draft generation request."))
                return

            self.safe_log(_("Start generating chapter drafts..."))
            from novel_generator.chapter import generate_chapter_draft
            draft_text = generate_chapter_draft(
                api_key=api_key,
                base_url=base_url,
                model_name=model_name,
                filepath=filepath,
                novel_number=chap_num,
                word_number=word_number,
                temperature=temperature,
                user_guidance=user_guidance,
                characters_involved=char_inv,
                key_items=key_items,
                scene_location=scene_loc,
                time_constraint=time_constr,
                embedding_api_key=embedding_api_key,
                embedding_url=embedding_url,
                embedding_interface_format=embedding_interface_format,
                embedding_model_name=embedding_model_name,
                embedding_retrieval_k=embedding_k,
                interface_format=interface_format,
                max_tokens=max_tokens,
                timeout=timeout_val,
                custom_prompt_text=edited_prompt  # Use user edited prompt words
            )
            if draft_text:
                self.safe_log(_("✅ The draft of the chapter %d was generated. Please view or edit on the left. ") % chap_num)
                self.master.after(0, lambda: self.show_chapter_in_textbox(draft_text))
            else:
                self.safe_log(_("⚠️ The draft of this chapter failed to be generated or there was no content."))
        except Exception:
            self.handle_exception(_("An error occurred while generating a chapter draft"))
        finally:
            self.enable_button_safe(self.btn_generate_chapter)
    threading.Thread(target=task, daemon=True).start()

def finalize_chapter_ui(self):
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), _("Please configure the save file path first."))
        return

    def task():
        self.disable_button_safe(self.btn_finalize_chapter)
        try:
            interface_format = self.interface_format_var.get().strip()
            api_key = self.api_key_var.get().strip()
            base_url = self.base_url_var.get().strip()
            model_name = self.model_name_var.get().strip()
            temperature = self.temperature_var.get()
            max_tokens = self.max_tokens_var.get()
            timeout_val = self.safe_get_int(self.timeout_var, 600)

            embedding_api_key = self.embedding_api_key_var.get().strip()
            embedding_url = self.embedding_url_var.get().strip()
            embedding_interface_format = self.embedding_interface_format_var.get().strip()
            embedding_model_name = self.embedding_model_name_var.get().strip()

            chap_num = self.safe_get_int(self.chapter_num_var, 1)
            word_number = self.safe_get_int(self.word_number_var, 3000)

            self.safe_log(_("Start finalizing Chapter %d...") % chap_num)

            chapters_dir = os.path.join(filepath, "chapters")
            os.makedirs(chapters_dir, exist_ok=True)
            chapter_file = os.path.join(chapters_dir, f"chapter_{chap_num}.txt")

            edited_text = self.chapter_result.get("0.0", "end").strip()
            
            word_counter = count_chinese_and_english(edited_text)
            self.safe_log(_("Current chapter words count is: %d ") % word_counter)

            #If the word count is less than 80%, ask if it is expanded
            need_to_expand = False
            if word_counter < 0.8 * word_number:
                ask = messagebox.askyesno(_("Insufficient word count"), _("The current chapter word count %d is lower than 80%% of the target word count (%d). Do you want to try to expand it?") % (word_counter, word_number))
                if ask:
                    self.safe_log(_("Expanding chapter content..."))
                    enriched = enrich_chapter_text(
                        chapter_text=edited_text,
                        word_number=word_number,
                        api_key=api_key,
                        base_url=base_url,
                        model_name=model_name,
                        temperature=temperature,
                        interface_format=interface_format,
                        max_tokens=max_tokens,
                        timeout=timeout_val
                    )
                    # expend the content and append to the existing content
                    edited_text = edited_text + '\n\r' + enriched
                    self.master.after(0, lambda: self.chapter_result.delete("0.0", "end"))
                    self.master.after(0, lambda: self.chapter_result.insert("0.0", edited_text))
                    clear_file_content(chapter_file)
                    save_string_to_txt(edited_text, chapter_file)
                    word_counter = count_chinese_and_english(edited_text)
                    self.safe_log(_("✅ Chapter %d has been expended, the current word count is %d, you can do it again if still not enough the word count.") % (chap_num, word_counter))
                    need_to_expand = True
                else:
                    need_to_expand = False
            else:
                need_to_expand = False
                
            if need_to_expand == False:
                finalize_chapter(
                    novel_number=chap_num,
                    word_number=word_number,
                    api_key=api_key,
                    base_url=base_url,
                    model_name=model_name,
                    temperature=temperature,
                    filepath=filepath,
                    embedding_api_key=embedding_api_key,
                    embedding_url=embedding_url,
                    embedding_interface_format=embedding_interface_format,
                    embedding_model_name=embedding_model_name,
                    interface_format=interface_format,
                    max_tokens=max_tokens,
                    timeout=timeout_val
                )
                self.safe_log(_("✅ Chapter %d is finalized (global summary, character status, vector library has been updated). ") % chap_num)

                final_text = read_file(chapter_file)
                self.master.after(0, lambda: self.show_chapter_in_textbox(final_text))
        except Exception:
            self.handle_exception(_("An error occurred while finalizing the chapter"))
        finally:
            self.enable_button_safe(self.btn_finalize_chapter)
    threading.Thread(target=task, daemon=True).start()

def do_consistency_check(self):
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), _("Please configure the save file path first."))
        return

    def task():
        self.disable_button_safe(self.btn_check_consistency)
        try:
            api_key = self.api_key_var.get().strip()
            base_url = self.base_url_var.get().strip()
            model_name = self.model_name_var.get().strip()
            temperature = self.temperature_var.get()
            interface_format = self.interface_format_var.get()
            max_tokens = self.max_tokens_var.get()
            timeout = self.timeout_var.get()

            chap_num = self.safe_get_int(self.chapter_num_var, 1)
            chap_file = os.path.join(filepath, "chapters", f"chapter_{chap_num}.txt")
            chapter_text = read_file(chap_file)

            if not chapter_text.strip():
                self.safe_log(_("⚠️ The current chapter file is empty or does not exist and cannot be reviewed. "))
                return

            self.safe_log(_("Begin consistent review..."))
            result = check_consistency(
                novel_setting="",
                character_state=read_file(os.path.join(filepath, "character_state.txt")),
                global_summary=read_file(os.path.join(filepath, "global_summary.txt")),
                chapter_text=chapter_text,
                api_key=api_key,
                base_url=base_url,
                model_name=model_name,
                temperature=temperature,
                interface_format=interface_format,
                max_tokens=max_tokens,
                timeout=timeout,
                plot_arcs=""
            )
            self.safe_log(_("Review results:"))
            self.safe_log(result)
        except Exception:
            self.handle_exception(_("An error occurred during review"))
        finally:
            self.enable_button_safe(self.btn_check_consistency)
    threading.Thread(target=task, daemon=True).start()

def import_knowledge_handler(self):
    selected_file = tk.filedialog.askopenfilename(
        title=_("Select the knowledge base file to import"),
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if selected_file:
        def task():
            self.disable_button_safe(self.btn_import_knowledge)
            try:
                emb_api_key = self.embedding_api_key_var.get().strip()
                emb_url = self.embedding_url_var.get().strip()
                emb_format = self.embedding_interface_format_var.get().strip()
                emb_model = self.embedding_model_name_var.get().strip()

                self.safe_log(_("Start importing knowledge base files: %s") % selected_file)
                import_knowledge_file(
                    embedding_api_key=emb_api_key,
                    embedding_url=emb_url,
                    embedding_interface_format=emb_format,
                    embedding_model_name=emb_model,
                    file_path=selected_file,
                    filepath=self.filepath_var.get().strip()
                )
                self.safe_log(_("✅ The knowledge base file import is completed."))
            except Exception:
                self.handle_exception(_("An error occurred while importing the knowledge base"))
            finally:
                self.enable_button_safe(self.btn_import_knowledge)
        threading.Thread(target=task, daemon=True).start()

def clear_vectorstore_handler(self):
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), _("Please configure the save file path first."))
        return

    first_confirm = messagebox.askyesno(_("Warning"), _("Are you sure you want to clear the local vector library? This operation is not restored!"))
    if first_confirm:
        second_confirm = messagebox.askyesno(_("Confirmation"), _("Are you sure you really want to delete all vector data? This operation is not recoverable!"))
        if second_confirm:
            if clear_vector_store(filepath):
                self.log(_("The vector library has been cleared."))
            else:
                self.log(_("The vector library cannot be cleared. Please manually delete the vectorstore folder under %s after closing the program. ") % filepath)

def show_plot_arcs_ui(self):
    filepath = self.filepath_var.get().strip()
    if not filepath:
        messagebox.showwarning(_("Warning"), _("Please set the save file path in the main Tab first"))
        return

    plot_arcs_file = os.path.join(filepath, "plot_arcs.txt")
    if not os.path.exists(plot_arcs_file):
        messagebox.showinfo(_("Plot points"), _("No plot points or conflict records have been generated yet. "))
        return

    arcs_text = read_file(plot_arcs_file).strip()
    if not arcs_text:
        arcs_text=_("There are currently no recorded plot points or conflicts.")

    top = ctk.CTkToplevel(self.master)
    top.title(_("Plot points/unresolved conflict"))
    top.geometry("600x400")
    text_area = ctk.CTkTextbox(top, wrap="word", font=("Microsoft YaHei", 12))
    text_area.pack(fill="both", expand=True, padx=10, pady=10)
    text_area.insert("0.0", arcs_text)
    text_area.configure(state="disabled")
    
def count_chinese_and_english(text):
    """
    Calculate the number of Chinese characters and English words in text
    """
    # Calculate Chinese characters
    chinese_count = len([char for char in text if '\u4e00' <= char <= '\u9fff'])
    
    # Calculate English words
    english_words = re.findall(r'\b[a-zA-Z]+\b', text)
    english_word_count = len(english_words)

    # Returns the total number of Chinese characters and English words
    return chinese_count + english_word_count

def copy_to_clipboard(self, content):
    try:            
        pyperclip.copy(content)
        # self.log(_("Content has been copied to clipboard successfully!"))
        messagebox.showinfo(_("Info"), _("Content has been copied to clipboard successfully!"))
    except Exception as e:
        self.log(_("Failed to copy content to clipboard: %s") % e)
