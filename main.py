from datetime import datetime

import discord
from discord import Option
from dotenv import load_dotenv
from config import TOKEN, GUILD_IDS, ROLE_ID_TO_MENTION, TRACKED_ROLES
from insults import check_insults, load_phrases
import re

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = discord.Bot(intents=intents)

WHO_TO_INSULT = load_phrases('phrases/who.txt')
HOW_TO_INSULT = load_phrases('phrases/how.txt')

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

    if re.search(r'\bкогда\b(?!\-|\w)', message.content.lower()):
        await message.reply("Завтра")

    if check_insults(message, WHO_TO_INSULT, HOW_TO_INSULT):
        role = message.guild.get_role(ROLE_ID_TO_MENTION)
        if role:
            await message.reply(f"{role.mention}, сообщение содержит запрещенную фразу!")

bot.run(TOKEN)
