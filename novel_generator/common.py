#novel_generator/common.py
# -*- coding: utf-8 -*-
"""
General retry, cleaning, logging tools
"""
import logging
import re
import time
import traceback


def call_with_retry(func, max_retries=3, sleep_time=2, fallback_return=None, **kwargs):
    """
    Common retry mechanism encapsulation.
    :param func: The function to be executed
    :param max_retries: Maximum retries
    :param sleep_time: Number of waiting seconds before retry
    :param fallback_return: Return value if multiple retry still fails
    :param kwargs: named parameters passed to func
    :return: result of func, if it fails, fallback_return will be returned
    """
    for attempt in range(1, max_retries + 1):
        try:
            return func(**kwargs)
        except Exception as e:
            logging.warning(f"[call_with_retry] Attempt {attempt} failed with error: {e}")
            traceback.print_exc()
            if attempt < max_retries:
                time.sleep(sleep_time)
            else:
                logging.error("Max retries reached, returning fallback_return.")
                return fallback_return

def remove_think_tags(text: str) -> str:
    """Remove the content of <think>...</think> package"""
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)

def debug_log(prompt: str, response_content: str):
    logging.info(
        f"\n[#########################################  Prompt  #########################################]\n{prompt}\n"
    )
    logging.info(
        f"\n[######################################### Response #########################################]\n{response_content}\n"
    )

def invoke_with_cleaning(llm_adapter, prompt: str) -> str:
    """
    Call LLM to add retry and clean logic
    If it fails multiple times, an empty string is returned to continue the process, rather than interrupting.
    """
    def _invoke(prompt):
        return llm_adapter.invoke(prompt)

    response = call_with_retry(func=_invoke, max_retries=3, fallback_return="", prompt=prompt)
    if not response:
        logging.warning("No response from model after retry. Return empty.")
        return ""
    cleaned_text = remove_think_tags(response)
    debug_log(prompt, cleaned_text)
    return cleaned_text.strip()
