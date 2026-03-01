from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

async def set_main_menu(bot: Bot):
    menu_commands = [
        BotCommand(command = "start", description="Тренировка"),
        BotCommand(command = "help", description="Помощь"),
        BotCommand(command = "top", description="Топ 5 пользователей"),
        BotCommand(command="profile", description="Ваш профиль")
    ]
    await bot.set_my_commands(commands=menu_commands, scope=BotCommandScopeAllPrivateChats())