import discord
from config import TRACKED_ROLES, INFO_CHANNEL_ID, SPONSORS_FILE_PATH, CKEY_CHANNEL_ID, BOOSTY_ROLE_ID
from logger import log_user_action


async def on_member_update(before, after):
    added_roles = set(after.roles) - set(before.roles)
    added_tracked_roles = [role for role in added_roles if role.id in TRACKED_ROLES]

    if added_tracked_roles:
        role_id = added_tracked_roles[0].id
        try:
            await after.send(f"Спасибо, что подписались на бусти! Теперь вы {added_tracked_roles[0].name}.")
        except discord.Forbidden:
            print(f"Не удалось отправить личное сообщение пользователю {after.name}. Личные сообщения отключены.")

        ckey_channel = after.guild.get_channel(CKEY_CHANNEL_ID)
        if ckey_channel:
            await ckey_channel.send(
                f"Привет, {after.mention}! Ты стал спонсором с доступом к донат-магазину, если хочешь получить доступ к нему в игре - используй команду **/my_ckey**"
            )

        # Добавление роли BOOSTY_ROLE_ID
        boosty_role = after.guild.get_role(BOOSTY_ROLE_ID)
        if boosty_role:
            try:
                await after.add_roles(boosty_role)
                log_user_action(f"BOOSTY_ROLE_ID ({boosty_role.name}) добавлена пользователю {after.name}", after)
            except Exception as e:
                print(f"Не удалось добавить роль BOOSTY_ROLE_ID: {e}")
                log_user_action(f"Ошибка при добавлении BOOSTY_ROLE_ID пользователю {after.name}: {e}", after)

        log_user_action(f"Role added: {role_id}", after)

    removed_roles = set(before.roles) - set(after.roles)
    removed_tracked_roles = [role for role in removed_roles if role.id in TRACKED_ROLES]

    if removed_tracked_roles:
        role_id = removed_tracked_roles[0].id
        try:
            await after.send(
                f"Видимо Ваша подписка на бусти **https://boosty.to/aavikko.ss14** закончилась, так как вы потеряли роль: {removed_tracked_roles[0].name}.")
        except discord.Forbidden:
            info_channel = after.guild.get_channel(INFO_CHANNEL_ID)
            if info_channel:
                await info_channel.send(f"{after.mention}, Ваша подписка закончилась.")

        try:
            with open(SPONSORS_FILE_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []

        with open(SPONSORS_FILE_PATH, 'w', encoding='utf-8') as f:
            for line in lines:
                if not line.startswith(f"{after.name},"):
                    f.write(line)

        # Снятие роли BOOSTY_ROLE_ID
        boosty_role = after.guild.get_role(BOOSTY_ROLE_ID)
        if boosty_role:
            try:
                await after.remove_roles(boosty_role)
                log_user_action(f"BOOSTY_ROLE_ID ({boosty_role.name}) удалена у пользователя {after.name}", after)
            except Exception as e:
                print(f"Не удалось удалить роль BOOSTY_ROLE_ID: {e}")
                log_user_action(f"Ошибка при удалении BOOSTY_ROLE_ID у пользователя {after.name}: {e}", after)

        log_user_action(f"Role removed: {role_id}", after)
