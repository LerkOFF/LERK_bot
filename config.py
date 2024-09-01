import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_IDS = list(map(int, os.getenv('GUILD_IDS').split(',')))
TRACKED_ROLES = list(map(int, os.getenv('TRACKED_ROLES').split(',')))
ROLE_ID_TO_MENTION = int(os.getenv('ROLE_ID_TO_MENTION'))
CKEY_CHANNEL_ID = int(os.getenv('CKEY_CHANNEL_ID'))
