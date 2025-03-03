# chapter_blueprint_parser.py
# -*- coding: utf-8 -*-
import re

def parse_chapter_blueprint(blueprint_text: str):
    """
    Parses the entire chapter blueprint text and returns a list, each element is a dict:
    {
      "chapter_number": int,
      "chapter_title": str,
      "chapter_role": str,      # Positioning of this chapter
      "chapter_purpose": str,   # core role
      "suspense_level": str,    # suspense density
      "foreshadowing": str,     # Foreshadowing operation
      "plot_twist_level": str,  # Cognitive subversion
      "chapter_summary": str    # Brief description of this chapter
    }
    """

    # First divide the blank lines to avoid confusion between chapters
    chunks = re.split(r'\n\s*\n', blueprint_text.strip())
    results = []

    # Compatible with whether to wrap chapter titles in square brackets
    # For example:
    # Chapter 1 - Omens under the Purple Aurora
    # or
    # Chapter 1 - [Omen of the Purple Aurora]
    chapter_number_pattern = re.compile(r'^第\s*(\d+)\s*章\s*-\s*\[?(.*?)\]?$')

    role_pattern     = re.compile(r'^本章定位：\s*\[?(.*)\]?$')
    purpose_pattern  = re.compile(r'^核心作用：\s*\[?(.*)\]?$')
    suspense_pattern = re.compile(r'^悬念密度：\s*\[?(.*)\]?$')
    foreshadow_pattern = re.compile(r'^伏笔操作：\s*\[?(.*)\]?$')
    twist_pattern       = re.compile(r'^认知颠覆：\s*\[?(.*)\]?$')
    summary_pattern = re.compile(r'^本章简述：\s*\[?(.*)\]?$')

    for chunk in chunks:
        lines = chunk.strip().splitlines()
        if not lines:
            continue

        chapter_number   = None
        chapter_title    = ""
        chapter_role     = ""
        chapter_purpose  = ""
        suspense_level   = ""
        foreshadowing    = ""
        plot_twist_level = ""
        chapter_summary  = ""

        # First match the first line (or the first few lines), find the chapter number and title
        header_match = chapter_number_pattern.match(lines[0].strip())
        if not header_match:
            # Not in line with the format of "Chapter X - Title", skip
            continue

        chapter_number = int(header_match.group(1))
        chapter_title  = header_match.group(2).strip()

        # Match other fields from the following line
        for line in lines[1:]:
            line_stripped = line.strip()
            if not line_stripped:
                continue

            m_role = role_pattern.match(line_stripped)
            if m_role:
                chapter_role = m_role.group(1).strip()
                continue

            m_purpose = purpose_pattern.match(line_stripped)
            if m_purpose:
                chapter_purpose = m_purpose.group(1).strip()
                continue

            m_suspense = suspense_pattern.match(line_stripped)
            if m_suspense:
                suspense_level = m_suspense.group(1).strip()
                continue

            m_foreshadow = foreshadow_pattern.match(line_stripped)
            if m_foreshadow:
                foreshadowing = m_foreshadow.group(1).strip()
                continue

            m_twist = twist_pattern.match(line_stripped)
            if m_twist:
                plot_twist_level = m_twist.group(1).strip()
                continue

            m_summary = summary_pattern.match(line_stripped)
            if m_summary:
                chapter_summary = m_summary.group(1).strip()
                continue

        results.append({
            "chapter_number": chapter_number,
            "chapter_title": chapter_title,
            "chapter_role": chapter_role,
            "chapter_purpose": chapter_purpose,
            "suspense_level": suspense_level,
            "foreshadowing": foreshadowing,
            "plot_twist_level": plot_twist_level,
            "chapter_summary": chapter_summary
        })

    # Return after sorting by chapter_number
    results.sort(key=lambda x: x["chapter_number"])
    return results


def get_chapter_info_from_blueprint(blueprint_text: str, target_chapter_number: int):
    """
    In the already loaded chapter blueprint text, find the structured information of the corresponding chapter number and return a dict.
    If not found, a default structure is returned.
    """
    all_chapters = parse_chapter_blueprint(blueprint_text)
    for ch in all_chapters:
        if ch["chapter_number"] == target_chapter_number:
            return ch
    # Return by default
    return {
        "chapter_number": target_chapter_number,
        "chapter_title": _("Chapter %d") % target_chapter_number,
        "chapter_role": "",
        "chapter_purpose": "",
        "suspense_level": "",
        "foreshadowing": "",
        "plot_twist_level": "",
        "chapter_summary": ""
    }
