import discord
from config import TRACKED_ROLES, INFO_CHANNEL_ID, SPONSORS_FILE_PATH, CKEY_CHANNEL_ID
from logger import log_user_action  # Импортируем функцию логирования


async def on_member_update(before, after):
    added_roles = set(after.roles) - set(before.roles)
    added_tracked_roles = [role for role in added_roles if role.id in TRACKED_ROLES]

    if added_tracked_roles:
        role_name = added_tracked_roles[0].name
        try:
            await after.send(f"Спасибо, что подписались на бусти! Теперь вы {role_name}.")
        except discord.Forbidden:
            print(f"Не удалось отправить личное сообщение пользователю {after.name}. Личные сообщения отключены.")

        ckey_channel = after.guild.get_channel(CKEY_CHANNEL_ID)
        if ckey_channel:
            await ckey_channel.send(
                f"Привет, {after.mention}! Ты стал спонсором. Если хочешь получить доступ к донат-магазину в игре - используй команду **/my_ckey**"
            )
        log_user_action(f"Role added: {role_name}", after)

    removed_roles = set(before.roles) - set(after.roles)
    removed_tracked_roles = [role for role in removed_roles if role.id in TRACKED_ROLES]

    if removed_tracked_roles:
        role_name = removed_tracked_roles[0].name
        try:
            await after.send(
                f"Видимо Ваша подписка на бусти **https://boosty.to/aavikko.ss14** закончилась, так как вы потеряли роль: {role_name}.")
        except discord.Forbidden:
            info_channel = after.guild.get_channel(INFO_CHANNEL_ID)
            if info_channel:
                await info_channel.send(f"{after.mention}, Ваша подписка закончилась.")

        try:
            with open(SPONSORS_FILE_PATH, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []

        with open(SPONSORS_FILE_PATH, 'w') as f:
            for line in lines:
                if not line.startswith(f"{after.name},"):
                    f.write(line)

        log_user_action(f"Role removed: {role_name}", after)
