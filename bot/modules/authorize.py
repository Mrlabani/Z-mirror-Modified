#!/usr/bin/env python3
from pyrogram.filters import command
from pyrogram.handlers import MessageHandler
import asyncio
from bot import DATABASE_URL, bot, user_data
from bot.helper.ext_utils.bot_utils import update_user_ldata
from bot.helper.ext_utils.db_handler import DbManager
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage


async def authorize(_, message):
    sticker_message = await message.reply_sticker("CAACAgQAAxkBAAIBTWdUfA9uNcFCC8fFRDMRoZaHicRaAAIZDQACdmcgUfTj7QQtmo08NgQ")
    await asyncio.sleep(2)
    await sticker_message.delete()
    msg = message.text.split()
    if len(msg) > 1:
        id_ = int(msg[1].strip())
    elif reply_to := message.reply_to_message:
        id_ = reply_to.from_user.id
    else:
        id_ = message.chat.id
    if id_ in user_data and user_data[id_].get('is_auth'):
        msg = 'Already Authorized!'
    else:
        update_user_ldata(id_, 'is_auth', True)
        if DATABASE_URL:
            await DbManager().update_user_data(id_)
        msg = 'Authorized Successfully!'
    await sendMessage(message, msg)


async def unauthorize(_, message):
    msg = message.text.split()
    if len(msg) > 1:
        id_ = int(msg[1].strip())
    elif reply_to := message.reply_to_message:
        id_ = reply_to.from_user.id
    else:
        id_ = message.chat.id
    if id_ not in user_data or user_data[id_].get('is_auth'):
        update_user_ldata(id_, 'is_auth', False)
        if DATABASE_URL:
            await DbManager().update_user_data(id_)
        msg = 'Unauthorized Successfully!'
    else:
        msg = 'Already Unauthorized!'
    await sendMessage(message, msg)


async def addSudo(_, message):
    id_ = ""
    msg = message.text.split()
    if len(msg) > 1:
        id_ = int(msg[1].strip())
    elif reply_to := message.reply_to_message:
        id_ = reply_to.from_user.id
    if id_:
        if id_ in user_data and user_data[id_].get('is_sudo'):
            msg = 'Already Sudo!'
        else:
            update_user_ldata(id_, 'is_sudo', True)
            if DATABASE_URL:
                await DbManager().update_user_data(id_)
            msg = 'Promoted as Sudo.'
    else:
        msg = "Give ID or Reply To message of whom you want to Promote."
    await sendMessage(message, msg)


async def removeSudo(_, message):
    id_ = ""
    msg = message.text.split()
    if len(msg) > 1:
        id_ = int(msg[1].strip())
    elif reply_to := message.reply_to_message:
        id_ = reply_to.from_user.id
    if id_ and id_ not in user_data or user_data[id_].get('is_sudo'):
        update_user_ldata(id_, 'is_sudo', False)
        if DATABASE_URL:
            await DbManager().update_user_data(id_)
        msg = 'Demoted!'
    else:
        msg = "Give ID or Reply To message of whom you want to remove from Sudo"
    await sendMessage(message, msg)

bot.add_handler(MessageHandler(authorize, filters=command(
    BotCommands.AuthorizeCommand) & CustomFilters.sudo))
bot.add_handler(MessageHandler(unauthorize, filters=command(
    BotCommands.UnAuthorizeCommand) & CustomFilters.sudo))
bot.add_handler(MessageHandler(addSudo, filters=command(
    BotCommands.AddSudoCommand) & CustomFilters.sudo))
bot.add_handler(MessageHandler(removeSudo, filters=command(
    BotCommands.RmSudoCommand) & CustomFilters.sudo))
