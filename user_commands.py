from datetime import datetime
import discord
from discord import Option
from config import TRACKED_ROLES, CKEY_CHANNEL_ID, SPONSORS_FILE_PATH, CAN_GIVES_ROLES, ROLE_GIVER_CHANNEL, \
    DISPOSABLE_FILE_PATH
import re
from logger import log_user_action


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
        default_color = "#FF0000"
        new_record = f"{member.name}, {ckey}, {tracked_roles[0]}, {time_now}, {default_color}\n"

        # Обновление в SPONSORS_FILE_PATH
        try:
            with open(SPONSORS_FILE_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []

        old_ckey = None
        with open(SPONSORS_FILE_PATH, 'w', encoding='utf-8') as f:
            updated = False
            for line in lines:
                if line.startswith(f"{member.name},"):
                    old_ckey = line.split(', ')[1]
                    f.write(new_record)
                    updated = True
                else:
                    f.write(line)

            if not updated:
                f.write(new_record)

        # Обновление ckey в DISPOSABLE_FILE_PATH, если найден старый
        if old_ckey:
            try:
                with open(DISPOSABLE_FILE_PATH, 'r', encoding='utf-8') as f:
                    disposable_lines = f.readlines()

                updated_disposable_lines = []
                for disposable_line in disposable_lines:
                    parts = disposable_line.strip().split(', ')
                    if len(parts) >= 1 and parts[0] == old_ckey:
                        # Предполагается формат: "ckey, slots, tokens"
                        if len(parts) == 3:
                            updated_disposable_lines.append(f"{ckey}, {parts[1]}, {parts[2]}\n")
                        elif len(parts) == 2:
                            # Если только ckey и слоты, добавляем токены
                            updated_disposable_lines.append(f"{ckey}, {parts[1]}, 0\n")  # Пример: устанавливаем токены как 0
                        else:
                            # Если формат отличается, оставляем без изменений
                            updated_disposable_lines.append(disposable_line)
                    else:
                        updated_disposable_lines.append(disposable_line)

                with open(DISPOSABLE_FILE_PATH, 'w', encoding='utf-8') as f:
                    f.writelines(updated_disposable_lines)

            except FileNotFoundError:
                pass  # Если файла нет, ничего не делаем

        await ctx.respond(f'Сикей "{ckey}" был установлен для спонсорского магазина в игре.')
        log_user_action(f'CKEY command used: {ckey} (default color: {default_color})', member)

    except Exception as e:
        await ctx.respond(f"Произошла ошибка: {e}", ephemeral=True)
        log_user_action(f'Error updating CKEY: {e}', member)
        raise


async def change_my_name_color(ctx: discord.ApplicationContext, color_hex: Option(str, "HEX-код цвета")):
    try:
        ckey_channel = ctx.guild.get_channel(CKEY_CHANNEL_ID)
        if ckey_channel is None:
            await ctx.respond("Ошибка: указанный канал для команды не найден.", ephemeral=True)
            return

        if ctx.channel.id != CKEY_CHANNEL_ID:
            await ctx.respond(f"Эта команда может использоваться только в канале {ckey_channel.mention}.", ephemeral=True)
            return

        # Проверка на корректный формат HEX-кода
        if not re.match(r'^#([A-Fa-f0-9]{6})$', color_hex):
            await ctx.respond("Неверный формат HEX-кода. Используйте формат #RRGGBB.", ephemeral=True)
            return

        member = ctx.author
        member_roles = set([role.id for role in member.roles])
        tracked_roles = [role_id for role_id in member_roles if role_id in TRACKED_ROLES]

        if not tracked_roles:
            await ctx.respond("Вы не спонсор.", ephemeral=True)
            return

        sponsor_record_found = False
        updated_lines = []

        try:
            with open(SPONSORS_FILE_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line in lines:
                if line.startswith(f"{member.name},"):
                    sponsor_record_found = True
                    parts = line.strip().split(', ')
                    if len(parts) == 5:
                        parts[4] = color_hex
                    else:
                        parts.append(color_hex)
                    updated_lines.append(', '.join(parts) + '\n')
                else:
                    updated_lines.append(line)

        except FileNotFoundError:
            await ctx.respond("Файл спонсоров не найден. Пожалуйста, сначала используйте команду /my_ckey.", ephemeral=True)
            return

        if not sponsor_record_found:
            await ctx.respond("Ваша запись не найдена. Пожалуйста, сначала используйте команду /my_ckey.", ephemeral=True)
            return

        with open(SPONSORS_FILE_PATH, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)

        await ctx.respond(f"Цвет вашего имени успешно изменён на {color_hex}.")
        log_user_action(f'Change color command used: {color_hex}', member)

    except Exception as e:
        await ctx.respond(f"Произошла ошибка при изменении цвета имени: {e}", ephemeral=True)
        log_user_action(f'Error changing color: {e}', member)


async def check_permissions_and_find_member_role(ctx, nickname, role_id):
    if ctx.channel.id != ROLE_GIVER_CHANNEL:
        return None, None, "Команда вызвана не в разрешённом канале."

    if ctx.author.name not in CAN_GIVES_ROLES:
        return None, None, "У вас нет прав на выполнение этой команды."

    member = discord.utils.get(ctx.guild.members, name=nickname)
    if member is None:
        return None, None, f"Пользователь с ником {nickname} не найден."

    role = ctx.guild.get_role(int(role_id))
    if role is None:
        return None, None, f"Роль с ID {role_id} не найдена."

    return member, role, None


async def give_role(ctx: discord.ApplicationContext, nickname: Option(str, "Ник пользователя"),
                    role_id: Option(str, "ID роли")):
    member, role, error = await check_permissions_and_find_member_role(ctx, nickname, role_id)

    if error:
        await ctx.respond(error, ephemeral=True)
        log_user_action(f'Give role failed: {error}', ctx.author)
        return

    try:
        await member.add_roles(role)
        await ctx.respond(f"Пользователю {nickname} успешно назначена роль {role.name}.", ephemeral=True)
        log_user_action(f'Role {role.name} given to {nickname}', ctx.author)
    except Exception as e:
        await ctx.respond(f"Произошла ошибка при назначении роли: {e}", ephemeral=True)
        log_user_action(f'Error giving role: {e}', ctx.author)


async def remove_role(ctx: discord.ApplicationContext, nickname: Option(str, "Ник пользователя"),
                      role_id: Option(str, "ID роли")):
    member, role, error = await check_permissions_and_find_member_role(ctx, nickname, role_id)

    if error:
        await ctx.respond(error, ephemeral=True)
        log_user_action(f'Remove role failed: {error}', ctx.author)
        return

    try:
        await member.remove_roles(role)
        await ctx.respond(f"У пользователя {nickname} успешно удалена роль {role.name}.", ephemeral=True)
        log_user_action(f'Role {role.name} removed from {nickname}', ctx.author)
    except Exception as e:
        await ctx.respond(f"Произошла ошибка при удалении роли: {e}", ephemeral=True)
        log_user_action(f'Error removing role: {e}', ctx.author)


async def make_roles_file(ctx: discord.ApplicationContext):
    try:
        if ctx.author.name not in CAN_GIVES_ROLES:
            await ctx.respond("У вас нет прав на выполнение этой команды.", ephemeral=True)
            return

        roles_info = [f"{role.id}: {role.name}" for role in ctx.guild.roles]

        with open("roles_id.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(roles_info))

        await ctx.respond("Файл roles_id.txt успешно создан.", ephemeral=True)
        log_user_action('Make roles file command used', ctx.author)

    except Exception as e:
        await ctx.respond(f"Произошла ошибка при создании файла: {e}", ephemeral=True)
        log_user_action(f'Error creating roles file: {e}', ctx.author)


async def add_disposable(ctx: discord.ApplicationContext, ds_nickname: Option(str, "Дискорд никнейм пользователя"),
                         slots: Option(int, "Количество слотов"), tokens: Option(int, "Количество токенов")):
    try:
        if ctx.author.name not in CAN_GIVES_ROLES:
            await ctx.respond("У вас нет прав на выполнение этой команды.", ephemeral=True)
            return

        # Поиск ckey по ds_nickname в SPONSORS_FILE_PATH
        ckey = None
        with open(SPONSORS_FILE_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.split(', ')[0] == ds_nickname:
                    ckey = line.split(', ')[1]
                    break

        if not ckey:
            await ctx.respond(
                f"Пользователь с дискорд ником '{ds_nickname}' не найден в списке спонсоров. Сначала используйте команду /my_ckey.",
                ephemeral=True)
            return

        # Обновляем или добавляем запись в DISPOSABLE_FILE_PATH
        record_updated = False
        updated_lines = []
        try:
            with open(DISPOSABLE_FILE_PATH, 'r', encoding='utf-8') as f:
                disposable_lines = f.readlines()

            for disposable_line in disposable_lines:
                parts = disposable_line.strip().split(', ')
                if len(parts) >= 1 and parts[0] == ckey:
                    # Если ckey существует, обновляем слоты и токены
                    if len(parts) == 3:
                        updated_lines.append(f"{ckey}, {slots}, {tokens}\n")
                    elif len(parts) == 2:
                        # Если только ckey и слоты, добавляем токены
                        updated_lines.append(f"{ckey}, {slots}, {tokens}\n")
                    else:
                        # Если формат отличается, оставляем без изменений
                        updated_lines.append(disposable_line)
                    record_updated = True
                else:
                    updated_lines.append(disposable_line)

        except FileNotFoundError:
            updated_lines = [f"{ckey}, {slots}, {tokens}\n"]

        # Если ckey не был найден, добавляем новую строку
        if not record_updated:
            updated_lines.append(f"{ckey}, {slots}, {tokens}\n")

        # Перезапись файла с обновлённой информацией
        with open(DISPOSABLE_FILE_PATH, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)

        await ctx.respond(f"Для '{ds_nickname}' ({ckey}) было добавлено/обновлено '{slots}' слотов и '{tokens}' токенов.", ephemeral=True)
        log_user_action(f'Disposable slots/tokens added/updated: {slots} slots, {tokens} tokens to {ckey}', ctx.author)

    except Exception as e:
        await ctx.respond(f"Произошла ошибка при добавлении слотов и токенов: {e}", ephemeral=True)
        log_user_action(f'Error adding disposable slots/tokens: {e}', ctx.author)
