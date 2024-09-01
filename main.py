import discord
from dotenv import load_dotenv
from config import TOKEN, GUILD_IDS, ROLE_ID_TO_MENTION
from insults import check_insults, load_phrases
from user_commands import my_ckey
from role_events import on_member_update
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


bot.slash_command(name='my_ckey', description='Укажите ваш сикей в игре.', guild_ids=GUILD_IDS)(my_ckey)


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


bot.event(on_member_update)

bot.run(TOKEN)
