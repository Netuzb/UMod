# ▀█▀ █▀▀ █▀▄▀█ █░█ █▀█
# ░█░ ██▄ █░▀░█ █▄█ █▀▄
# ═══════════════════════
# █▀▀ █▀█ █▄▀ █ █▄░█ █▀█ █░█
# ██▄ █▀▄ █░█ █ █░▀█ █▄█ ▀▄▀
# ═════════════════════════════
# meta developer: @netuzb
# meta channel: @umodules

__version__ = (3, 6, 13)

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
        """.id va username"""
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
        idmod = (f"<b>🌇 Foydalanuvchi haqida maʼlumotlar:</b>\n\n"
            f"<b>🌉 Ismi:</b> <code>{user.first_name}</code>\n"            
            f"<b>🌉 Familiyasi:</b> <code>{user.last_name}</code>\n"
            f"<b>🌉 User'nomi:</b> <code>@{user.username}</code>\n"
            f"<b>🌉 Raqami:</b> {user.phone}\n"
            f"<b>🌉 ID raqami:</b> <code>{user.id}</code>\n\n"
            f"<b>🏙️ O'chirilgan akkaunt:</b> <code>{user.deleted}</code>\n"
            f"<b>🏙️ Tasdiqlangan akkaunt:</b> <code>{user.verified}</code>\n"
            f"<b>🏙️ Kontaktda mavjudligi:</b> <code>{user.contact}</code>\n\n"
            f"🌆 <b>None</b> = yoʻq, mavjud emas\n"
            f"🌆 <b>False</b> = yolgʻon (yoʻq degandek gap)\n"
            f"🌆 <b>True</b> = toʻgʻri (xa degandek gap)\n\n"
            f"<b>🌉 Foydalanuvchi maʼlumotlari <u>UMod</u></b> orqali qoʻlga kiritdi.\n"
            f"<b>🌉 Qoʻllanma esdan chiqmasin:</b> <code>.id @user</code>"
        )
        await self.inline.form(
                    text = idmod,
                    reply_markup=[
                     [{
       "text": f"🕶️ {user.first_name}", 
       "url": f"https://t.me/{text}"
      }],
      [{
       "text": "🧰 Shaxsiyga", 
       "url": f"https://t.me/{text}"
      },
      {
       "text": f"🆔 ID {user.id}", 
       "url": f"tg://openmessage?user_id={user.id}"
      }],
           ], 
                    ttl=10,
                    message=message,
                )
