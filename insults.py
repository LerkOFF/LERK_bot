import re
import os

def load_phrases(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip().lower() for line in file.readlines() if line.strip()]

def check_insults(message, who_to_insult, how_to_insult):
    message_content = message.content.lower()
    for who in who_to_insult:
        for how in how_to_insult:
            pattern = r'(?=.*' + re.escape(who) + r')(?=.*' + re.escape(how) + r')'
            if re.search(pattern, message_content):
                return True
    return False
