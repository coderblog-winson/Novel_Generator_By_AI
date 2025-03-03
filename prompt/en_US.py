# prompt_definitions.py
# -*- coding: utf-8 -*-
"""
Centrally store all prompts, integrate snowflake writing method, character arc theory, suspense three-element model, etc.
And include newly added short-term summary/next chapter keyword extraction prompts, as well as chapter body writing prompts.
"""

# =============== Summary and next chapter keyword extraction ===============
summarize_recent_chapters_prompt = """\
You are a senior novel editor, please analyze the following combined text with English (may include the content of the latest chapters):
{combined_text}

Now please complete the following two things based on the current story progress:

1) Use up to 200 words to write a concise and clear "Current Plot Short-term Summary".

2) Extract the keywords of the "next chapter" (such as key items, important characters, places, events, plots, etc.), which can be separated by commas or listed in items.

Please output in the following format (no additional explanation required):
Short-term summary: <Write short-term summary here>
Keywords for next chapter: <Write keywords for next chapter here>
"""
# ================ 1. Core seed setting (Snowflake layer 1) =====================
core_seed_prompt = """\
As a professional writer, please use the first step of the "Snowflake Writing Method" to build the core of the story with English:
Theme: {topic}
Type: {genre}
Length: about {number_of_chapters} chapters ({word_number} words per chapter)

Please use a single sentence formula to summarize the essence of the story, for example:
"When [the protagonist] encounters [core event], [key action] is necessary, otherwise [disastrous consequences]; at the same time, [hidden greater crisis] is brewing. "

Requirements:

1. Must contain explicit conflicts and potential crises

2. Reflect the core driving force of the character

3. Imply the key contradictions of the world view

4. Use 25-100 words to express accurately

Only return the core text of the story with English, do not explain anything.

"""

# =============== 2. Character dynamics setting (character arc model) ===================
character_dynamics_prompt = """\
Based on the core seed:
{core_seed}

Please design 3-6 core characters with dynamic change potential with English. Each character must include:

Features:
- Background, appearance, gender, age, occupation, etc.
- Hidden secrets or potential weaknesses (may be related to the world view or other characters)

Core driving force triangle:
- Surface pursuit (material goals)
- Deep desire (emotional needs)
- Soul needs (philosophical level)

Character arc design:
Initial state → Triggering event → Cognitive dissonance → Transformation node → Final state

Relationship conflict network:
- Relationships or oppositions with other characters
- Conflict of values ​​with at least two other characters
- A cooperative bond
- A hidden possibility of betrayal

Requirements:
Just give the final text, don't explain anything.
"""

# ================ 3. Worldbuilding Matrix (Three-dimensional Interweaving Method) ====================
world_building_prompt = """\
To serve the core conflict "{core_seed}", please build a three-dimensional interweaving worldview with English:

1. Physical dimension:
- Spatial structure (geographic × social class distribution map)
- Timeline (chronology of key historical events)
- Law system (loopholes in physical/magical/social rules)

2. Social dimension:
- Power structure fault lines (class/racial/organizational conflicts that can cause conflicts)
- Cultural taboos (taboos that can be broken and their consequences)
- Economic lifeline (focus of resource competition)

3. Metaphorical dimension:
- Visual symbol system throughout the book (such as recurring images)
- Psychological state mapped by climate/environmental changes
- Civilization dilemma implied by architectural style

Requirements:
Each dimension contains at least 3 dynamic elements that can interact with the character's decision.
Only give the final text, do not explain anything.
"""

# =============== 4. Plot structure (three-act suspense)==================
plot_architecture_prompt = """\
Build a three-act suspense structure based on the following elements with English:
Core seed: {core_seed}
Character system: {character_dynamics}
World view: {world_building}

Required to design according to the following structure:
Act 1 (trigger)
- Abnormal signs in daily state (3 foreshadowings)
- Introduce the story: show the beginning of the main line, dark line, and sub-line
- Key event: Catalyst that breaks the balance (needs to change the relationship between at least 3 characters)
- Wrong choice: Wrong reaction caused by the protagonist's cognitive limitations

Act 2 (confrontation)
- Plot upgrade: the intersection of the main plot + subplot
- Double pressure: external obstacles upgrade + internal setbacks
- False victory: a turning point that seems to solve the crisis but actually deepens it
- Dark night of the soul: a moment of subversion of worldview cognition

Act 3 (Solution)
- The price is revealed: the core value that must be sacrificed to solve the crisis
- Nested turning point: at least three layers of cognitive subversion (surface solution → new crisis → ultimate choice)
- Aftermath: leaving 2 open suspense factors

Each stage must include 3 key turning points and their corresponding foreshadowing recovery plans.
Only give the final text, do not explain anything.
"""

# =============== 5. Chapter Outline generation (suspense rhythm curve) ===================
chapter_blueprint_prompt = """\
Based on the novel architecture:\n
{novel_architecture}

Design the rhythm distribution of {number_of_chapters} chapters with English:
1. Chapter cluster division:
- Every 3-5 chapters constitute a suspense unit, including a complete climax
- Set up a "cognitive roller coaster" between units (2 consecutive chapters of tension → 1 chapter buffer)
- Key turning chapters need to reserve multiple perspectives foreshadowing

2. Each chapter needs to be clear:
- Chapter positioning (role/event/theme, etc.)
- Core suspense type (information gap/moral dilemma/time pressure, etc.)
- Emotional tone migration (such as from suspicion → fear → determination)
- Foreshadowing operation (burying/strengthening/recovery)
- Cognitive subversion intensity (1-5 stars, the 5 stars are the highest, representing the greatest cognitive subversion)

Output format example:
Chapter n - [Title]
Chapter positioning: [Role/Event/Theme/...]
Core role: [Advance/Turning point/Revelation/...]
Suspense density: [Compact/Gradual/Explosion/...]
Foreshadowing operation: Bury (A clue) → Strengthen (B contradiction)...
Cognitive subversion: ★☆☆☆☆
Chapter summary: [One sentence summary]

Chapter n+1 - [Title]
Chapter positioning: [Role/Event/Theme/...]
Core role: [Advance/Turning point/Revelation/...]
Suspense density: [Compact/Gradual/Explosion/...]
Foreshadowing operation: Bury (A clue) → Strengthen (B contradiction)...
Cognitive subversion: ★☆☆☆☆
Chapter summary: [One sentence summary]

Requirements:
- Use concise language to describe, and the number of words per chapter should be controlled within 100 words.
- Arrange the rhythm reasonably to ensure the coherence of the overall suspense curve.
- Don't give a final chapter until {number_of_chapters} chapters have been generated.

Just give the final text, don't explain anything.
"""

chunked_chapter_blueprint_prompt = """\
According to the novel architecture: \n
{novel_architecture}

The rhythm distribution of a total of {number_of_chapters} chapters needs to be generated with English.

The current chapter list (if empty, it means it is initially generated): \n
{chapter_list}

Now please design the rhythm distribution from chapter {n} to {m} with English:

1. Chapter cluster division:
- Every 3-5 chapters constitute a suspense unit, including a complete climax
- Set up a "cognitive roller coaster" between units (2 consecutive chapters of tension → 1 chapter buffer)
- Key turning chapters need to reserve multiple perspectives foreshadowing

2. Each chapter needs to be clear:
- Chapter positioning (role/event/theme, etc.)
- Core suspense type (information gap/moral dilemma/time pressure, etc.)
- Emotional tone migration (such as from suspicion → fear → determination)
- Foreshadowing operation (burying/reinforcement/recycling)
- Cognitive subversion intensity (1-5 stars, the 5 stars are the highest, representing the greatest cognitive subversion)

Output format example:
Chapter n - [Title]
Chapter Positioning: [Role/Event/Theme/...]
Core Function: [Advance/Turning Point/Revelation/...]
Suspense Density: [Compact/Gradual/Explosion/...]
Foreshadowing Operation: Bury (A Clue) → Strengthen (B Contradiction)...
Cognitive Subversion: ★☆☆☆☆
Chapter Summary: [One Sentence Summary]

Chapter n+1 - [Title]
Chapter Positioning: [Role/Event/Theme/...]
Core Function: [Advance/Turning Point/Revelation/...]
Suspense Density: [Compact/Gradual/Explosion/...]
Foreshadowing Operation: Bury (A Clue) → Strengthen (B Contradiction)...
Cognitive Subversion: ★☆☆☆☆
Chapter Summary: [One Sentence Summary]

Requirements:
- Use concise language to describe, and the number of words per chapter should be controlled within 100 words.
- Arrange the rhythm reasonably to ensure the coherence of the overall suspense curve.
- Do not appear the ending chapter before generating {number_of_chapters} chapters.

Just give the final text, don't explain anything.
"""

# =============== 6. Global summary updates ===================
summary_prompt = """\
Here is the newly completed chapter text:
{chapter_text}

This is the current global summary (can be empty):
{global_summary}

Please update the global summary based on the new content of this chapter with English.

Requirements:
- Keep existing important information while incorporating new plot points
- Describe the progress of the book in concise and coherent language
- Describe objectively without expanding associations or explanations
- Keep the word count within 2,000 words

Return only the global summary text, do not explain anything.
"""

# =============== 7. Character Status Update ===================
create_character_state_prompt = """\
According to the current character dynamics setting: {character_dynamics}

Please generate a character status document with English, the content format is:

Character A attributes:

├──Items:

    ├──Items (if there is an initial item, it will increase, otherwise it will be temporarily unavailable): Description
    ...
    
├──Ability

    ├──Skill 1 (if there is an initial skill, it will increase, otherwise it will be temporarily unavailable): Description
    ...
    
├──Status

    ├──Physical state:
        ├──Buff/Debuff
    ├──Psychological state: Description

├──Relationship network between main characters

    ├──Character B: Description (if there is an initial connection, it will increase, otherwise it will be temporarily unavailable)
    ├──Character C: Description (if there is an initial connection, it will increase, otherwise it will be temporarily unavailable)
    ...
    
├──Events triggered or deepened

    ├──No events
    ...

Character B attributes:

├──Items

    ├──...
    
├──Ability

    ├──...
    
├──Status

    ├──...
    
├──Relationship network between main characters

    ├──...
    
├──Events triggered or deepened

    ├──...

Character C attributes:
......

Newly appeared characters:
- (Fill in the basic information of any new characters or temporary characters in the future)

Requirements:
Only return the written character status text, do not explain anything.
"""

update_character_state_prompt = """\
The following is the newly completed chapter text:
{chapter_text}

This is the current character status document:
{old_state}

Please update the main character status with English, content format:
Character A attributes:
├──Item:

    ├──Something (prop): description
    ├──XX long sword (weapon): description
    ...
├──Ability

    ├──Skill 1: description
    ├──Skill 2: description
    ...
├──State

    ├──Physical state:
        ├──Buff/Debuff
    ├──Psychological state: description

├──Main character relationship network

    ├──Character B: description
    ├──Character C: description
    ...
├──Triggering or deepening events

    ├──Event 1: description
    ├──Event 2: description
    ...

Character B attributes:

├──Item

    ├──...
├──Ability

    ├──...
├──Status

    ├──...
├──Relationship network between main characters

    ├──...
├──Events triggered or deepened

    ├──...

Character C attributes:
......

Newly appeared characters:
- Basic information of any new characters or temporary characters, just briefly describe, do not expand, and characters that fade out of sight can be deleted.

Requirements:
- Please add and delete directly based on the existing documents
- Do not change the original structure, and keep the language as concise and organized as possible

Only return the updated character status text, do not explain anything.
"""

# =============== 8. Chapter writing ===================

# 8.1 First chapter draft prompt
first_chapter_draft_prompt = """\
To be created: Chapter {novel_number} "{chapter_title}"
Chapter positioning: {chapter_role}
Core role: {chapter_purpose}
Suspense density: {suspense_level}
Foreshadowing operation: {foreshadowing}
Cognitive subversion: {plot_twist_level}
Chapter summary: {chapter_summary}

Available elements:
- Core characters (may not be specified): {characters_involved}
- Key props (may not be specified): {key_items}
- Spatial coordinates (may not be specified): {scene_location}
- Time pressure (may not be specified): {time_constraint}

Reference documents:
- Novel setting:
{novel_setting}

Please use English to complete the text of Chapter {novel_number}, At the same time, the following requirements must be met:

Word count requirement {word_number} words

{user_guidance}

Design at least 2 or more of the following scenes with dynamic tension:

1. Dialogue scene:

- Subtext conflict (discussing A on the surface, actually playing B)
- Changes in power relations (reflected through asymmetric dialogue length)
- At least 1 pun hinting at future crisis

2. Action scene:

- Environmental interaction details (at least 3 sensory descriptions)
- Rhythm control (short sentence acceleration + metaphor deceleration)
- Actions reveal hidden characteristics of characters

3. Psychological scene:

- Specific manifestations of cognitive dissonance (behavioral contradictions)
- Use of metaphor system (connecting worldview symbols)
- Description of the value balance before decision-making

4. Environmental scene:

- Changes in spatial perspective (macro → micro → abnormal focus)
- Unconventional sensory combinations (such as "hearing the weight of the sun")
- Dynamic environment reflects psychology (environment corresponds to character psychology)
- Hidden clue implantation (environment hints at future events)

Set a "hook-chain twist" at the end of the article: recycle old suspense/create new suspense/throw out new crisis/subvert a certain cognition/magic twist, etc.

Format requirements:
- Only return the text of the chapter;
- Do not use chapter subheadings;
- Do not use markdown format.

"""

# 8.2 Next chapter draft prompt
next_chapter_draft_prompt = """\
Reference documents:
- Novel setting:
{novel_setting}

- Global summary:
{global_summary}

- Character state:
{character_state}

Fragments retrieved from local knowledge base:
{context_excerpt}

To be created: Chapter {novel_number} "{chapter_title}"
Chapter positioning: {chapter_role}
Core role: {chapter_purpose}
Suspense density: {suspense_level}
Foreshadowing operation: {foreshadowing}
Cognitive subversion: {plot_twist_level}
Chapter summary: {chapter_summary}

Available elements:
- Core characters (may not be specified): {characters_involved}
- Key props (may not be specified): {key_items}
- Spatial coordinates (may not be specified): {scene_location}
- Time pressure (may not be specified): {time_constraint}

Previous chapter ending paragraph:
{previous_chapter_excerpt}

Based on the plot at the end of the previous chapter, start using English to complete the text of chapter {novel_number}, with a word count of {word_number} words to ensure smooth connection with the end of the previous chapter.

At the same time, the following requirements must be met:
{user_guidance}

This chapter should design at least 2 or more of the following scenes with dynamic tension:

1. Dialogue scene:
- Subtext conflict (discussing A on the surface, actually playing B)
- Changes in power relations (reflected by asymmetric dialogue length)
- At least 1 pun hinting at future crises

2. Action scene:
- Environmental interaction details (at least 3 sensory descriptions)
- Rhythm control (short sentence acceleration + metaphor deceleration)
- Action reveals hidden characteristics of the character

3. Psychological scene:
- Specific manifestations of cognitive dissonance (behavioral contradictions)
- Use of metaphor system (connecting worldview symbols)
- Description of the value balance before decision-making

4. Environmental scenes:
- Changes in spatial perspective (macro → micro → abnormal focus)
- Unconventional sensory combinations (such as "hearing the weight of the sun")
- Dynamic environment reflects psychology (environment corresponds to character psychology)
- Hidden clues implanted (environment implies future events)

Set a "hook and chain turning point" at the end of the article: recycle old suspense/create new suspense/throw out new crisis/subvert a certain cognition/magic turning point, etc.

Format requirements:
- Only return to the main text of the chapter;
- Do not use sub-chapter subheadings;
- Do not use markdown format.

"""

consistency_prompt = """\
Please check whether the following novel settings have obvious conflicts or inconsistencies with the latest chapters. Please list them if you have:
 - Novel settings:
 {novel_setting}

 - Role status (may contain important information):
 {character_state}

 - Global Summary:
 {global_summary}

 - Recorded unresolved conflicts or plot points:
 {plot_arcs} # If empty, no output may be

 - Latest chapter content:
 {chapter_text}

 If there is a conflict or inconsistency, please indicate it; if there are any places that have been ignored or need to be promoted in an unresolved conflict, please also mention it; otherwise, please return to "No obvious conflict".
 """
 
architecture_result = """\
## 1) LLM Model Name: {model_name}
 
## 2) Novel settings

Topic: {topic}
Type: {type}

Length: about No. of {number_of_chapters} chapters(Each chapter {word_number} words)

## 3) Core seeds
{core_seed_result}

## 4) Character Dynamics
{character_dynamics_result}

## 5) Worldview
{world_building_result}

## 6) Three-act plot structure
{plot_arch_result}
"""

expend_content_prompt = """\
Please base on below the below original content to continue writing:
    Requirements:
    1. Don't create the new chapter
    2. Keep the plot coherent 
    3. Don't include the original content in the final output
    4. The word count should be around {word_number} words
 Original content:
{chapter_text}
"""