import discord
from config import TRACKED_ROLES, INFO_CHANNEL_ID, SPONSORS_FILE_PATH, CKEY_CHANNEL_ID

async def on_member_update(before, after):
    added_roles = set(after.roles) - set(before.roles)
    added_tracked_roles = [role for role in added_roles if role.id in TRACKED_ROLES]

    if added_tracked_roles:
        ckey_channel = after.guild.get_channel(CKEY_CHANNEL_ID)
        if ckey_channel:
            await ckey_channel.send(
                f"Привет, {after.mention}! Ты стал спонсором. Если хочешь получить доступ к донат-магазину в игре - используй команду `/my_ckey`."
            )

    removed_roles = set(before.roles) - set(after.roles)
    removed_tracked_roles = [role for role in removed_roles if role.id in TRACKED_ROLES]

    if removed_tracked_roles:
        info_channel = after.guild.get_channel(INFO_CHANNEL_ID)
        if info_channel:
            await info_channel.send(f"{after.mention}, ваша подписка на бусти закончилась.")

        try:
            with open(SPONSORS_FILE_PATH, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []

        with open(SPONSORS_FILE_PATH, 'w') as f:
            for line in lines:
                if not line.startswith(f"{after.name},"):
                    f.write(line)
