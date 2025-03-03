# handle multiple languages in the codebase
import builtins
import gettext
import importlib
import os
import sys

from config_manager import load_config
            
def set_current_language(language = None, is_restart=False):
    """
    Set the current language for the system
    """
    # Load the language configuration from the config file
    if language is None:
        try:
            loaded_config = load_config('config.json')
            language = loaded_config["other_params"]["language_var"]
        except:
            pass
    
    if language is None:
        language = 'English'
        
    local_dir = os.path.join(os.path.dirname(__file__), 'locale')
    domain = "messages"
    lang_code = "en_US"  
    if language == 'Chinese':
        lang_code = 'zh_CN'

    print(f"Setting language to {lang_code}")
    translate = gettext.translation(domain, local_dir, languages=[lang_code], fallback=True)
    # translate = Translations.load(f'locale/{lang_code}/LC_MESSAGES', domain=domain)
    translate.install()
    builtins._ = translate.gettext
    
    # Automatically restart the application after changing the language
    if is_restart:
        os.execv(sys.executable, ['python'] + sys.argv)
  
