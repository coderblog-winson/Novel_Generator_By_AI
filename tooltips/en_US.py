# tooltips.py
# -*- coding: utf-8 -*-

tooltips = {
    "api_key": "Fill in your API Key here. If you use the official OpenAI interface, please get it at https://platform.openai.com/account/api-keys. ",
    "base_url": "The interface address of the model. If you use OpenAI official: https://api.openai.com/v1. If you use Ollama local deployment, it is similar to http://localhost:11434/v1. If you call the Gemini model, you do not need to fill in it.",
    "interface_format":"Specify LLM interface compatible format, optional DeepSeek, OpenAI, Ollama, ML Studio, Gemini, etc.\n\nNote: "+
                        "OpenAI compatibility refers to any interface that can be requested through this standard, not only the api.openai.com interface\n"+
                        "For example, the Ollama interface format is also compatible with OpenAI, and you can use it directly without modification\n"+
                        "The ML Studio interface format is also the same as the OpenAI interface format.",
    "model_name":"The model name to be used, such as deepseek-reasoner, gpt-4o, etc. If it is Ollama, please fill in the local model name you have downloaded.",
    "temperature": "The randomness of generated text. The larger the value, the divergence, and the smaller the rigorous.",
    "max_tokens":"Limit the maximum number of tokens generated in a single time. The range is 1~100000. Please fill in the appropriate value according to the model context and requirements.\n"+
                    "The following are the maximum values ​​for some common models:\n"+
                    "o1:100,000\n"+
                    "o1-mini: 65,536\n"+
                    "gpt-4o:16384\n"+
                    "gpt-4o-mini:16384\n"+
                    "deepseek-reasoner:8192\n"+
                    "deepseek-chat:4096\n",
    "timeout": "The timeout of the calling model, in seconds. After this time, the model will automatically stop running.",
    "embedding_api_key": "The API Key required when calling the Embedding model.",
    "embedding_interface_format": "Embedding model interface style, such as OpenAI or Ollama.",
    "embedding_url": "Embedding model interface address.",
    "embedding_model_name": "Embedding model name, such as text-embedding-ada-002.",
    "embedding_retrieval_k": "The number of Top-K results returned when vector searching.",
    "topic": "A description of the general theme or main story background of the novel.",
    "genre": "The subject types of novels, such as fantasy, urban, science fiction, etc.",
    "num_chapters": "Total number of chapters expected in the novel.",
    "word_number": "Target word count for each chapter.",
    "filepath": "The root directory path of the generated file storage. All txt files, vector libraries, etc. are placed in this directory.",
    "chapter_num": "The chapter number currently being processed, used to generate draft or finalize operations.",
    "user_guidance": "Some additional instructions or writing guidance provided for this chapter.",
    "characters_involved": "This chapter needs to focus on describing or affecting the plot.",
    "key_items": "Important props, clues or items that appear in this chapter.",
    "scene_location": "Description of the main location or scene in this chapter.",
    "time_constraint": "The time pressure or time limit settings involved in the plot of this chapter.",
    "language": "The language that generates text, such as Chinese, English, etc.",
}
