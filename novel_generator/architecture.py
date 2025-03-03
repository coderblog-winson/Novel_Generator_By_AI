#novel_generator/architecture.py
# -*- coding: utf-8 -*-
"""
The overall architecture generation of novels (Novel_architecture_generate and related helper functions)
"""
import os
import json
import logging
import traceback
from novel_generator.common import invoke_with_cleaning
from llm_adapters import create_llm_adapter
# from injector import (
#     core_seed_prompt,
#     character_dynamics_prompt,
#     world_building_prompt,
#     plot_architecture_prompt,
#     create_character_state_prompt
# )
from utils import clear_file_content, save_string_to_txt


def load_partial_architecture_data(filepath: str) -> dict:
    """
    Read existing phased data from partial_architecture.json under filepath.
    If the file does not exist or cannot be parsed, an empty dict is returned.
    """
    partial_file = os.path.join(filepath, "partial_architecture.json")
    if not os.path.exists(partial_file):
        return {}
    try:
        with open(partial_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        logging.warning(f"Failed to load partial_architecture.json: {e}")
        return {}

def save_partial_architecture_data(filepath: str, data: dict):
    """
    Write phased data to partial_architecture.json.
    """
    partial_file = os.path.join(filepath, "partial_architecture.json")
    try:
        with open(partial_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.warning(f"Failed to save partial_architecture.json: {e}")

def Novel_architecture_generate(
    interface_format: str,
    api_key: str,
    base_url: str,
    llm_model: str,
    topic: str,
    genre: str,
    number_of_chapters: int,
    word_number: int,
    filepath: str,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    timeout: int = 600
) -> None:
    """
    Called in turn:
      1. core_seed_prompt
      2. character_dynamics_prompt
      3. world_building_prompt
      4. plot_architecture_prompt
    If an error is reported in any step in the middle and retry fails multiple times, the generated content will be written to partial_architecture.json and exited;
    You can continue from this step the next time you call it.
    Final output Novel_architecture.txt

    New:
    - After completing the character dynamics setting, use create_character_state_prompt to generate the initial character status table according to the character system.
      and store it in character_state.txt for subsequent maintenance and updates.
    """
    
    os.makedirs(filepath, exist_ok=True)
    partial_data = load_partial_architecture_data(filepath)
    llm_adapter = create_llm_adapter(
        interface_format=interface_format,
        base_url=base_url,
        model_name=llm_model,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout
    )
    # Step1: Core seeds
    if "core_seed_result" not in partial_data:
        logging.info("Step1: Generating core_seed_prompt (Core seeds) ...")
        prompt_core = core_seed_prompt.format(
            topic=topic,
            genre=genre,
            number_of_chapters=number_of_chapters,
            word_number=word_number
        )
        print(prompt_core)
        core_seed_result = invoke_with_cleaning(llm_adapter, prompt_core)
        if not core_seed_result.strip():
            logging.warning("core_seed_prompt generation failed and returned empty.")
            save_partial_architecture_data(filepath, partial_data)
            return
        partial_data["core_seed_result"] = core_seed_result
        save_partial_architecture_data(filepath, partial_data)
    else:
        logging.info("Step1 already done. Skipping...")
    # Step2: Character Dynamics
    if "character_dynamics_result" not in partial_data:
        logging.info("Step2: Generating character_dynamics_prompt ...")
        prompt_character = character_dynamics_prompt.format(core_seed=partial_data["core_seed_result"].strip())
        character_dynamics_result = invoke_with_cleaning(llm_adapter, prompt_character)
        if not character_dynamics_result.strip():
            logging.warning("character_dynamics_prompt generation failed.")
            save_partial_architecture_data(filepath, partial_data)
            return
        partial_data["character_dynamics_result"] = character_dynamics_result
        save_partial_architecture_data(filepath, partial_data)
    else:
        logging.info("Step2 already done. Skipping...")
    # Generate initial role status
    if "character_dynamics_result" in partial_data and "character_state_result" not in partial_data:
        logging.info("Generating initial character state from character dynamics ...")
        prompt_char_state_init = create_character_state_prompt.format(
            character_dynamics=partial_data["character_dynamics_result"].strip()
        )
        character_state_init = invoke_with_cleaning(llm_adapter, prompt_char_state_init)
        if not character_state_init.strip():
            logging.warning("create_character_state_prompt generation failed.")
            save_partial_architecture_data(filepath, partial_data)
            return
        partial_data["character_state_result"] = character_state_init
        character_state_file = os.path.join(filepath, "character_state.txt")
        clear_file_content(character_state_file)
        save_string_to_txt(character_state_init, character_state_file)
        save_partial_architecture_data(filepath, partial_data)
        logging.info("Initial character state created and saved.")
    # Step3: Worldview
    if "world_building_result" not in partial_data:
        logging.info("Step3: Generating world_building_prompt ...")
        prompt_world = world_building_prompt.format(core_seed=partial_data["core_seed_result"].strip())
        world_building_result = invoke_with_cleaning(llm_adapter, prompt_world)
        if not world_building_result.strip():
            logging.warning("world_building_prompt generation failed.")
            save_partial_architecture_data(filepath, partial_data)
            return
        partial_data["world_building_result"] = world_building_result
        save_partial_architecture_data(filepath, partial_data)
    else:
        logging.info("Step3 already done. Skipping...")
    # Step4: Three-act episode
    if "plot_arch_result" not in partial_data:
        logging.info("Step4: Generating plot_architecture_prompt ...")
        prompt_plot = plot_architecture_prompt.format(
            core_seed=partial_data["core_seed_result"].strip(),
            character_dynamics=partial_data["character_dynamics_result"].strip(),
            world_building=partial_data["world_building_result"].strip()
        )
        plot_arch_result = invoke_with_cleaning(llm_adapter, prompt_plot)
        if not plot_arch_result.strip():
            logging.warning("plot_architecture_prompt generation failed.")
            save_partial_architecture_data(filepath, partial_data)
            return
        partial_data["plot_arch_result"] = plot_arch_result
        save_partial_architecture_data(filepath, partial_data)
    else:
        logging.info("Step4 already done. Skipping...")

    core_seed_result = partial_data["core_seed_result"]
    character_dynamics_result = partial_data["character_dynamics_result"]
    world_building_result = partial_data["world_building_result"]
    plot_arch_result = partial_data["plot_arch_result"]

    final_content = architecture_result.format(
        model_name=llm_model,
        topic=topic,
        type=genre,
        number_of_chapters=number_of_chapters,
        word_number=word_number,
        core_seed_result=core_seed_result,
        character_dynamics_result=character_dynamics_result,
        world_building_result=world_building_result,
        plot_arch_result=plot_arch_result)

    arch_file = os.path.join(filepath, "Novel_architecture.txt")
    clear_file_content(arch_file)
    save_string_to_txt(final_content, arch_file)
    logging.info("Novel_architecture.txt has been generated successfully.")

    partial_arch_file = os.path.join(filepath, "partial_architecture.json")
    if os.path.exists(partial_arch_file):
        os.remove(partial_arch_file)
        logging.info("partial_architecture.json removed (all steps completed).")
