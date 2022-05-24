# ▀█▀ █▀▀ █▀▄▀█ █░█ █▀█
# ░█░ ██▄ █░▀░█ █▄█ █▀▄
# ═══════════════════════
# █▀▀ █▀█ █▄▀ █ █▄░█ █▀█ █░█
# ██▄ █▀▄ █░█ █ █░▀█ █▄█ ▀▄▀
# ═════════════════════════════
# meta developer: @netuzb
# meta channel: @umodules

__version__ = (1, 1, 0)

import asyncio
import io
from asyncio import sleep
from os import remove

from telethon import errors, functions
from telethon.errors import (
    BotGroupsBlockedError,
    ChannelPrivateError,
    ChatAdminRequiredError,
    ChatWriteForbiddenError,
    InputUserDeactivatedError,
    MessageTooLongError,
    UserAlreadyParticipantError,
    UserBlockedError,
    UserIdInvalidError,
    UserKickedError,
    UserNotMutualContactError,
    UserPrivacyRestrictedError,
    YouBlockedUserError,
)
from telethon.tl.functions.channels import InviteToChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest, GetCommonChatsRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
)

from .. import loader, utils


@loader.tds
class BluvchiMod(loader.Module):
    """Shaxs haqida maʼlumot beradigan modul"""

    strings = {"name": "Biluvchi"}

    async def client_ready(self, client, db):
        self.db = db

    async def idcmd(self, message):
        """id bilish <reply yoki @user>"""
        text = utils.get_args_raw(message) 
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()        
        if not text and not reply:
        	await message.edit("xato koʻrsatma")
        try:
            if args:            	
                user = await message.client.get_entity(                
                args if not args.isdigit() else int(args))
        except ValueError:           
            user = await message.client.gek_entity(GetFullUserRequest(message.sender_id))
        await message.reply(
            f"<b>🌇 Foydalanuvchi haqida maʼlumotlar:</b>\n\n"
            f"<b>🏙️ Ismi:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"            
            f"<b>🏙️ Familiyasi:</b> <a href='t.me/{user.username}'>{user.last_name}</a>\n"
            f"<b>🌉 User'nomi:</b> @{user.username}\n"
            f"<b>🌉 Raqami:</b> {user.phone}\n"
            f"<b>🌉 ID raqami:</b> <code>{user.id}</code>\n\n"
            f"<b>🏙️ O'chirilgan akkaunt:</b> <code>{user.deleted}</code>\n"
            f"<b>🏙️ Tasdiqlangan akkaunt:</b> <code>{user.verified}</code>\n"
            f"<b>🏙️ Kontaktda mavjudligi:</b> <code>{user.contact}</code>\n\n"
            f"🌆 None = <b>yoʻq, mavjud emas</b>\n"
            f"🌆 False = <b>yolgʻon (yoʻq degandek gap)</b>\n"
            f"🌆 True = <b>toʻgʻri (xa degandek gap)</b>\n\n"
            f"<b>🌉 Qoʻllanma esdan chiqmasin:</b> <code>.id @user</code>"
        )
