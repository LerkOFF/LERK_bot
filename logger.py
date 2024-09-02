from config import LOG_FILE_PATH
from datetime import datetime


def log_user_action(action, user):
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] User: {user}, Action: {action}\n"

        with open(LOG_FILE_PATH, 'a') as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(f"Ошибка при логировании действия: {e}")
