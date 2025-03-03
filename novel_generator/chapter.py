# novel_generator/chapter.py
# -*- coding: utf-8 -*-
"""
Generate and obtain historical chapter texts, short-term summary, etc.
"""
import os
import logging
from nltk import download
from llm_adapters import create_llm_adapter
# from injector import first_chapter_draft_prompt, next_chapter_draft_prompt, summarize_recent_chapters_prompt
from chapter_directory_parser import get_chapter_info_from_blueprint
from novel_generator.common import invoke_with_cleaning
from utils import read_file, clear_file_content, save_string_to_txt
from novel_generator.vectorstore_utils import get_relevant_context_from_vector_store


def get_last_n_chapters_text(chapters_dir: str, current_chapter_num: int, n: int = 3) -> list:
    """
    Get the text content of the most recent n chapters from the directory chapters_dir and return to the text list.
    """
    texts = []
    start_chap = max(1, current_chapter_num - n)
    for c in range(start_chap, current_chapter_num):
        chap_file = os.path.join(chapters_dir, f"chapter_{c}.txt")
        if os.path.exists(chap_file):
            text = read_file(chap_file).strip()
            texts.append(text)
        else:
            texts.append("")
    return texts

def summarize_recent_chapters(
    interface_format: str,
    api_key: str,
    base_url: str,
    model_name: str,
    temperature: float,
    max_tokens: int,
    chapters_text_list: list,
    timeout: int = 600
) -> tuple:
    """
    Generate (short_summary, next_chapter_keywords)
    If parsing fails, return (merge text, "")
    """
    combined_text = "\n".join(chapters_text_list).strip()
    if not combined_text:
        return ("", "")
    llm_adapter = create_llm_adapter(
        interface_format=interface_format,
        base_url=base_url,
        model_name=model_name,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout
    )
    prompt = summarize_recent_chapters_prompt.format(combined_text=combined_text)
    response_text = invoke_with_cleaning(llm_adapter, prompt)
    short_summary = ""
    next_chapter_keywords = ""
    for line in response_text.splitlines():
        line = line.strip()
        if line.startswith("Short-term summary:"):
            short_summary = line.replace("短期摘要:", "").strip()
        elif line.startswith("Next chapter keywords:"):
            next_chapter_keywords = line.replace("Next chapter keywords:", "").strip()
    if not short_summary and not next_chapter_keywords:
        short_summary = response_text
    return (short_summary, next_chapter_keywords)

def build_chapter_prompt(
    api_key: str,
    base_url: str,
    model_name: str,
    filepath: str,
    novel_number: int,
    word_number: int,
    temperature: float,
    user_guidance: str,
    characters_involved: str,
    key_items: str,
    scene_location: str,
    time_constraint: str,
    embedding_api_key: str,
    embedding_url: str,
    embedding_interface_format: str,
    embedding_model_name: str,
    embedding_retrieval_k: int = 2,
    interface_format: str = "openai",
    max_tokens: int = 2048,
    timeout: int = 600
) -> str:
    """
    Constructs the request prompt word for the current chapter, without calling LLM, and only returns the constructed prompt word string.
    """
    arch_file = os.path.join(filepath, "Novel_architecture.txt")
    novel_architecture_text = read_file(arch_file)
    directory_file = os.path.join(filepath, "Novel_outline.txt")
    blueprint_text = read_file(directory_file)
    global_summary_file = os.path.join(filepath, "global_summary.txt")
    global_summary_text = read_file(global_summary_file)
    character_state_file = os.path.join(filepath, "character_state.txt")
    character_state_text = read_file(character_state_file)
    
    chapter_info = get_chapter_info_from_blueprint(blueprint_text, novel_number)
    chapter_title = chapter_info["chapter_title"]
    chapter_role = chapter_info["chapter_role"]
    chapter_purpose = chapter_info["chapter_purpose"]
    suspense_level = chapter_info["suspense_level"]
    foreshadowing = chapter_info["foreshadowing"]
    plot_twist_level = chapter_info["plot_twist_level"]
    chapter_summary = chapter_info["chapter_summary"]

    chapters_dir = os.path.join(filepath, "chapters")
    os.makedirs(chapters_dir, exist_ok=True)

    if novel_number == 1:
        prompt_text = first_chapter_draft_prompt.format(
            novel_number=novel_number,
            word_number=word_number,
            chapter_title=chapter_title,
            chapter_role=chapter_role,
            chapter_purpose=chapter_purpose,
            suspense_level=suspense_level,
            foreshadowing=foreshadowing,
            plot_twist_level=plot_twist_level,
            chapter_summary=chapter_summary,
            characters_involved=characters_involved,
            key_items=key_items,
            scene_location=scene_location,
            time_constraint=time_constraint,
            user_guidance=user_guidance,
            novel_setting=novel_architecture_text
        )
    else:
        recent_3_texts = get_last_n_chapters_text(chapters_dir, novel_number, n=3)
        short_summary, next_chapter_keywords = summarize_recent_chapters(
            interface_format=interface_format,
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            chapters_text_list=recent_3_texts,
            timeout=timeout
        )
        previous_chapter_excerpt = ""
        for text_block in reversed(recent_3_texts):
            if text_block.strip():
                if len(text_block) > 1500:
                    previous_chapter_excerpt = text_block[-1500:]
                else:
                    previous_chapter_excerpt = text_block
                break
        from embedding_adapters import create_embedding_adapter  # Avoid circular dependencies
        embedding_adapter = create_embedding_adapter(
            embedding_interface_format,
            embedding_api_key,
            embedding_url,
            embedding_model_name
        )
        retrieval_query = short_summary + " " + next_chapter_keywords
        relevant_context = get_relevant_context_from_vector_store(
            embedding_adapter=embedding_adapter,
            query=retrieval_query,
            filepath=filepath,
            k=embedding_retrieval_k
        )
        if not relevant_context.strip():
            relevant_context = "(No context retrieved)"
        prompt_text = next_chapter_draft_prompt.format(
            novel_number=novel_number,
            word_number=word_number,
            chapter_title=chapter_title,
            chapter_role=chapter_role,
            chapter_purpose=chapter_purpose,
            suspense_level=suspense_level,
            foreshadowing=foreshadowing,
            plot_twist_level=plot_twist_level,
            chapter_summary=chapter_summary,
            characters_involved=characters_involved,
            key_items=key_items,
            scene_location=scene_location,
            time_constraint=time_constraint,
            user_guidance=user_guidance,
            novel_setting=novel_architecture_text,
            global_summary=global_summary_text,
            character_state=character_state_text,
            context_excerpt=relevant_context,
            previous_chapter_excerpt=previous_chapter_excerpt
        )
    return prompt_text

def generate_chapter_draft(
    api_key: str,
    base_url: str,
    model_name: str,
    filepath: str,
    novel_number: int,
    word_number: int,
    temperature: float,
    user_guidance: str,
    characters_involved: str,
    key_items: str,
    scene_location: str,
    time_constraint: str,
    embedding_api_key: str,
    embedding_url: str,
    embedding_interface_format: str,
    embedding_model_name: str,
    embedding_retrieval_k: int = 2,
    interface_format: str = "openai",
    max_tokens: int = 2048,
    timeout: int = 600,
    custom_prompt_text: str = None  # Added new parameters. If not None, use the prompt word edited by the user.
) -> str:
    """
   Judging whether it is the first chapter based on novel_number.
    - If it is the first chapter, use first_chapter_draft_prompt
    - Otherwise use next_chapter_draft_prompt
    If custom_prompt_text is provided, this is used as a prompt word for generation.
    Finally, the generated text will be saved in chapters/chapter_{novel_number}.txt.
    """
    # Construct the prompt word: If the user provides the edited prompt word, use it; otherwise, construct the default prompt word
    if custom_prompt_text is None:
        prompt_text = build_chapter_prompt(
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            filepath=filepath,
            novel_number=novel_number,
            word_number=word_number,
            temperature=temperature,
            user_guidance=user_guidance,
            characters_involved=characters_involved,
            key_items=key_items,
            scene_location=scene_location,
            time_constraint=time_constraint,
            embedding_api_key=embedding_api_key,
            embedding_url=embedding_url,
            embedding_interface_format=embedding_interface_format,
            embedding_model_name=embedding_model_name,
            embedding_retrieval_k=embedding_retrieval_k,
            interface_format=interface_format,
            max_tokens=max_tokens,
            timeout=timeout
        )
    else:
        prompt_text = custom_prompt_text

    chapters_dir = os.path.join(filepath, "chapters")
    os.makedirs(chapters_dir, exist_ok=True)

    llm_adapter = create_llm_adapter(
        interface_format=interface_format,
        base_url=base_url,
        model_name=model_name,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout
    )

    chapter_content = invoke_with_cleaning(llm_adapter, prompt_text)
    if not chapter_content.strip():
        logging.warning("Generated chapter draft is empty.")
    chapter_file = os.path.join(chapters_dir, f"chapter_{novel_number}.txt")
    clear_file_content(chapter_file)
    save_string_to_txt(chapter_content, chapter_file)
    logging.info(f"[Draft] Chapter {novel_number} generated as a draft.")
    return chapter_content
