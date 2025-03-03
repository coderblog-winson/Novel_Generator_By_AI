# consistency_checker.py
# -*- coding: utf-8 -*-
from llm_adapters import create_llm_adapter



# ============== Add optional guidance to check "Plot Points/Unresolved Conflicts"==============

def check_consistency(
    novel_setting: str,
    character_state: str,
    global_summary: str,
    chapter_text: str,
    api_key: str,
    base_url: str,
    model_name: str,
    temperature: float = 0.3,
    plot_arcs: str = "",
    interface_format: str = "OpenAI",
    max_tokens: int = 2048,
    timeout: int = 600
) -> str:
    """
    Call the model for simple consistency checks. Extend more prompts or verification rules.
    New: Additional checks will be made for the connection to "unresolved conflicts or plot points" (plot_arcs).
    """
    prompt = consistency_prompt.format(
        novel_setting=novel_setting,
        character_state=character_state,
        global_summary=global_summary,
        plot_arcs=plot_arcs,
        chapter_text=chapter_text
    )

    llm_adapter = create_llm_adapter(
        interface_format=interface_format,
        base_url=base_url,
        model_name=model_name,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout
    )

    # Debug log
    print("\n[ConsistencyChecker] Prompt >>>", prompt)

    response = llm_adapter.invoke(prompt)
    if not response:
        return _("No reply from the review Agent")
    
    # Debug log
    print("[ConsistencyChecker] Response <<<", response)

    return response
