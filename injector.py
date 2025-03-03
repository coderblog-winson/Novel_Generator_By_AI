import builtins
import importlib
import os
from config_manager import load_config


def inject_variables_from_module():
    """
    Inject variables from module to namespace for dynamic load the language module variables
    """
    try:
        loaded_config = load_config('config.json')
        language = loaded_config["other_params"]["language_var"]
        lang_code = "en_US"  
        if language == 'Chinese':
            lang_code = 'zh_CN'
        prompt_module = load_language_module('prompt',lang_code)
        for attr in dir(prompt_module):
            if not attr.startswith('__'):
                setattr(builtins, attr, getattr(prompt_module, attr))
                # print('Injecting prompt variable:', attr)
        
        tooltip_module = load_language_module('tooltips',lang_code)
        for attr in dir(tooltip_module):
            if not attr.startswith('__'):
                setattr(builtins, attr, getattr(tooltip_module, attr))
                # print('Injecting tooltips variable:', attr)
    except:
        pass

def load_language_module(module, lang_code):
    """dynamic load language 

    Args:
        lang_code (_type_): language code (e.g. 'en_US', 'zh_CN')

    Returns:
        _type_: language module
    """
        
    module_name = f'{module}.{lang_code}'
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError as e:
        print(f"Error importing module {module_name}: {e}")
        raise
    