from datetime import datetime
import discord
from discord import Option
from config import TRACKED_ROLES, CKEY_CHANNEL_ID, SPONSORS_FILE_PATH, CAN_GIVES_ROLES, ROLE_GIVER_CHANNEL
import re
from logger import log_user_action


async def my_ckey(ctx: discord.ApplicationContext, ckey: Option(str, "Ваш сикей в игре")):
    try:
        ckey_channel = ctx.guild.get_channel(CKEY_CHANNEL_ID)
        if ckey_channel is None:
            await ctx.respond("Ошибка: указанный канал для команды не найден.", ephemeral=True)
            return

        if ctx.channel.id != CKEY_CHANNEL_ID:
            await ctx.respond(f"Эта команда может использоваться только в канале {ckey_channel.mention}.",
                              ephemeral=True)
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
        log_user_action(f'CKEY command used: {ckey}', member)

    except Exception as e:
        await ctx.respond(f"Произошла ошибка: {e}", ephemeral=True)
        raise


async def check_permissions_and_find_member_role(ctx, nickname, role_id):
    if ctx.channel.id != ROLE_GIVER_CHANNEL:
        return None, None, "Команда вызвана не в разрешённом канале."

    if ctx.author.name not in CAN_GIVES_ROLES:
        return None, None, "У вас нет прав на выполнение этой команды."

    member = discord.utils.get(ctx.guild.members, name=nickname)
    if member is None:
        return None, None, f"Пользователь с ником {nickname} не найден."

    # Поиск роли по ID
    role = ctx.guild.get_role(int(role_id))
    if role is None:
        return None, None, f"Роль с ID {role_id} не найдена."

    return member, role, None

async def give_role(ctx: discord.ApplicationContext, nickname: Option(str, "Ник пользователя"), role_id: Option(str, "ID роли")):
    member, role, error = await check_permissions_and_find_member_role(ctx, nickname, role_id)

    if error:
        await ctx.respond(error, ephemeral=True)
        return

    try:
        await member.add_roles(role)
        await ctx.respond(f"Пользователю {nickname} успешно назначена роль {role.name}.", ephemeral=True)
    except Exception as e:
        await ctx.respond(f"Произошла ошибка при назначении роли: {e}", ephemeral=True)

async def remove_role(ctx: discord.ApplicationContext, nickname: Option(str, "Ник пользователя"), role_id: Option(str, "ID роли")):
    member, role, error = await check_permissions_and_find_member_role(ctx, nickname, role_id)

    if error:
        await ctx.respond(error, ephemeral=True)
        return

    try:
        await member.remove_roles(role)
        await ctx.respond(f"У пользователя {nickname} успешно удалена роль {role.name}.", ephemeral=True)
    except Exception as e:
        await ctx.respond(f"Произошла ошибка при удалении роли: {e}", ephemeral=True)


async def make_roles_file(ctx: discord.ApplicationContext):
    try:
        if ctx.author.name not in CAN_GIVES_ROLES:
            await ctx.respond("У вас нет прав на выполнение этой команды.", ephemeral=True)
            return

        roles_info = [f"{role.id}: {role.name}" for role in ctx.guild.roles]

        with open("roles_id.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(roles_info))

        await ctx.respond("Файл roles_id.txt успешно создан.", ephemeral=True)

    except Exception as e:
        await ctx.respond(f"Произошла ошибка при создании файла: {e}", ephemeral=True)

