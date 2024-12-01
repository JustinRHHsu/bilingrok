import os

def load_prompts(directory, prompt_filename):
    
    filepath = os.path.join(directory, prompt_filename + '.txt')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")
    
    with open(filepath, 'r', encoding='utf-8') as file:
        prompts = file.read()
    
    return prompts
