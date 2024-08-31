import os
import discord
from discord import Option
from dotenv import load_dotenv
from datetime import datetime
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_IDS = list(map(int, os.getenv('GUILD_IDS').split(',')))
TRACKED_ROLES = list(map(int, os.getenv('TRACKED_ROLES').split(',')))
ROLE_ID_TO_MENTION = int(os.getenv('ROLE_ID_TO_MENTION'))

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = discord.Bot(intents=intents)

def load_phrases(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip().lower() for line in file.readlines() if line.strip()]

WHO_TO_INSULT = load_phrases('who.txt')
HOW_TO_INSULT = load_phrases('how.txt')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(f'Бот подключен к серверу: {guild.name}')

@bot.slash_command(name='my_ckey', description='Укажите ваш сикей в игре.', guild_ids=GUILD_IDS)
async def my_ckey(ctx: discord.ApplicationContext, ckey: Option(str, "Ваш сикей в игре")):
    if not re.match("^[a-zA-Z0-9_]+$", ckey):
        await ctx.respond("Сикей должен содержать только английские буквы, цифры и символ подчеркивания.")
        return

    member = ctx.author
    member_roles = set([role.id for role in member.roles])
    tracked_roles = [role_id for role_id in member_roles if role_id in TRACKED_ROLES]

    if not tracked_roles:
        await ctx.respond("Вы не спонсор.")
        return

    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_record = f"{member.name}, {ckey}, {tracked_roles[0]}, {time_now}\n"

    try:
        with open('discord_sponsors.txt', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    with open('discord_sponsors.txt', 'w') as f:
        updated = False
        for line in lines:
            if line.startswith(f"{member.name},"):
                f.write(new_record)
                updated = True
            else:
                f.write(line)

        if not updated:
            f.write(new_record)

    await ctx.respond(f'Сикей "{ckey}" был установлен для спонсорского магазина в игре.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower().strip().endswith("когда?"):
        await message.reply("Завтра")

    for who in WHO_TO_INSULT:
        for how in HOW_TO_INSULT:
            pattern = r'(?=.*' + re.escape(who) + r')(?=.*' + re.escape(how) + r')'
            if re.search(pattern, message.content.lower()):
                role = message.guild.get_role(ROLE_ID_TO_MENTION)
                if role:
                    await message.reply(f"{role.mention}, сообщение содержит запрещенную фразу: '{who} {how}'!")
                return

bot.run(TOKEN)
