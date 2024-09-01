from datetime import datetime

import discord
from discord import Option
from dotenv import load_dotenv
from config import TOKEN, GUILD_IDS, ROLE_ID_TO_MENTION, CKEY_CHANNEL_ID, TRACKED_ROLES, INFO_CHANNEL_ID, SPONSORS_FILE_PATH
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
    try:
        ckey_channel = ctx.guild.get_channel(CKEY_CHANNEL_ID)
        if ckey_channel is None:
            await ctx.respond("Ошибка: указанный канал для команды не найден.", ephemeral=True)
            return

        if ctx.channel.id != CKEY_CHANNEL_ID:
            await ctx.respond(f"Эта команда может использоваться только в канале {ckey_channel.mention}.", ephemeral=True)
            return

        if not re.match("^[a-zA-Z0-9_]+$", ckey):
            await ctx.respond("Сикей должен содержать только английские буквы, цифры или подчеркивания.")
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
            with open(SPONSORS_FILE_PATH, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []

        with open(SPONSORS_FILE_PATH, 'w') as f:
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

    except Exception as e:
        await ctx.respond(f"Произошла ошибка: {e}", ephemeral=True)
        raise

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

@bot.event
async def on_member_update(before, after):
    removed_roles = set(before.roles) - set(after.roles)
    removed_tracked_roles = [role for role in removed_roles if role.id in TRACKED_ROLES]

    if removed_tracked_roles:
        try:
            await after.send(f"Ваша подписка закончилась, так как вы потеряли роль {removed_tracked_roles[0].mention}.")
        except discord.Forbidden:
            info_channel = after.guild.get_channel(INFO_CHANNEL_ID)
            if info_channel:
                await info_channel.send(f"{after.mention}, ваша подписка закончилась.")

        try:
            with open(SPONSORS_FILE_PATH, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []

        with open(SPONSORS_FILE_PATH, 'w') as f:
            for line in lines:
                if not line.startswith(f"{after.name},"):
                    f.write(line)

bot.run(TOKEN)
