# config_manager.py
# -*- coding: utf-8 -*-
import json
import os
import threading
from llm_adapters import create_llm_adapter
from embedding_adapters import create_embedding_adapter

def load_config(config_file: str) -> dict:
    """Load the configuration from the specified config_file and return an empty dictionary if it does not exist. """
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_config(config_data: dict, config_file: str) -> bool:
    """Save config_data into config_file, return True/False to indicate whether it is successful. """
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)
        return True
    except:
        return False

def test_llm_config(interface_format, api_key, base_url, model_name, temperature, max_tokens, timeout, log_func, handle_exception_func):
    """Test whether the current LLM configuration is available"""
    def task():
        try:            
            log_func(_("Start testing LLM configuration..."))
            llm_adapter = create_llm_adapter(
                interface_format=interface_format,
                base_url=base_url,
                model_name=model_name,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout
            )

            test_prompt = "Please reply 'OK'"
            response = llm_adapter.invoke(test_prompt)
            if response:
                log_func(_("✅ LLM configuration test succeeded!"))
                log_func(f"Test Reply: {response}")
            else:
                log_func(_("❌ LLM configuration test failed: no response was obtained"))
        except Exception as e:
            log_func(_("❌ LLM configuration test error: %s") % str(e))
            handle_exception_func("An error occurred while testing LLM configuration")

    threading.Thread(target=task, daemon=True).start()

def test_embedding_config(api_key, base_url, interface_format, model_name, log_func, handle_exception_func):
    """Test whether the current Embedding configuration is available"""
    def task():
        try:
            log_func(_("Start testing the Embedding configuration..."))
            embedding_adapter = create_embedding_adapter(
                interface_format=interface_format,
                api_key=api_key,
                base_url=base_url,
                model_name=model_name
            )

            test_text = "Test text"
            embeddings = embedding_adapter.embed_query(test_text)
            if embeddings and len(embeddings) > 0:
                log_func(_("✅ Embedding configuration test succeeded!"))
                log_func(f"The generated vector dimension: {len(embeddings)}")
            else:
                log_func(_("❌ Embedding configuration test failed: vector not obtained"))
        except Exception as e:
            log_func(_("❌ Embedding configuration test error: %s") % str(e))
            handle_exception_func("An error occurred while testing Embedding configuration")

    threading.Thread(target=task, daemon=True).start()
    
def load_chapter_param(key: str, default_value):
    """Load the chapter parameter (other_params) from the configuration file"""
    config_data = load_config('config.json')
    params = config_data.get('other_params', {})
    return params.get(key, default_value)