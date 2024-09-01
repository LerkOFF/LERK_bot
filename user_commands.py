from datetime import datetime
import discord
from discord import Option
from config import TRACKED_ROLES, CKEY_CHANNEL_ID, SPONSORS_FILE_PATH
import re

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
