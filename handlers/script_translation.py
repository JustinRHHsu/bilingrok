import os
import json


def load_translations(native_lang):
    translations_path = os.path.join('config', 'translations', f'{native_lang}.json')
    with open(translations_path, 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations