import os

def load_prompts(prompt_filename):
    directory = os.path.dirname(__file__)
    filepath = os.path.join(directory, prompt_filename + '.txt')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")
    
    with open(filepath, 'r', encoding='utf-8') as file:
        prompts = file.read()
    
    return prompts
