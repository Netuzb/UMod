# ▀█▀ █▀▀ █▀▄▀█ █░█ █▀█
# ░█░ ██▄ █░▀░█ █▄█ █▀▄
# ═══════════════════════
# █▀▀ █▀█ █▄▀ █ █▄░█ █▀█ █░█
# ██▄ █▀▄ █░█ █ █░▀█ █▄█ ▀▄▀
# ═════════════════════════════
# meta developer: @netuzb
# meta channel: @umodules

import os
from .. import loader, utils
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest, GetFullChatRequest
from telethon.tl.types import MessageActionChannelMigrateFrom, ChannelParticipantsAdmins, UserStatusOnline
from telethon.errors import (ChannelInvalidError, ChannelPrivateError, ChannelPublicGroupNaError)
from datetime import datetime
from math import sqrt


def register(cb):
    cb(ChatinfoMod())

class ChatinfoMod(loader.Module):
    """Показывает информацию о чате."""
    strings = {'name': 'ChatInfo'}

    async def chatinfocmd(self, chatinfo):
        """Chat haqida umumiy ma`lumot olish"""
        if chatinfo.chat:
            await chatinfo.edit("<b>Saralanmoqda...</b>")
            chat = await get_chatinfo(chatinfo)
            caption = await fetch_info(chat, chatinfo)
            try:
                await chatinfo.client.send_message(chat.full_chat.id, str(caption), file=await chatinfo.client.download_profile_photo(chat.full_chat.id, "chatphoto.jpg"))
            except Exception:
                await chatinfo.edit(f"<b>Xatolik yuzaga keldi.</b>")
            await chatinfo.delete()
        else:
            await chatinfo.edit("<b>Bu guruh emas!</b>")


async def get_chatinfo(event):
    chat = utils.get_args_raw(event)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChannelRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("<b>Haqiqiy kanal/guruh</b>")
            return None
        except ChannelPrivateError:
            await event.reply("<b>Bu guruh yoki kanal xususiy sanaladi.</b>")
            return None
        except ChannelPublicGroupNaError:
            await event.reply("<b>Bu guruh yoki kanal mavjud emas.</b>")
            return None
        except:
            chat = event.input_chat
            chat_info = await event.client(GetFullChannelRequest(chat))
            return chat_info
    return chat_info


async def fetch_info(chat, event):
    chat_obj_info = await event.client.get_entity(chat.full_chat.id)
    chat_title = chat_obj_info.title
    try:
        msg_info = await event.client(
            GetHistoryRequest(peer=chat_obj_info.id, offset_id=0, offset_date=datetime(2010, 1, 1),
                              add_offset=-1, limit=1, max_id=0, min_id=0, hash=0))
    except Exception:
        msg_info = None
        await event.edit("<b>Tushunrsiz xatolik yuzaga keldi.</b>")
    first_msg_valid = True if msg_info and msg_info.messages and msg_info.messages[0].id == 1 else False
    creator_valid = True if first_msg_valid and msg_info.users else False
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = msg_info.users[0].first_name if creator_valid and msg_info.users[0].first_name is not None else "O`chirilgan hisob"
    creator_username = msg_info.users[0].username if creator_valid and msg_info.users[0].username is not None else None
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = msg_info.messages[0].action.title if first_msg_valid and type(msg_info.messages[0].action) is MessageActionChannelMigrateFrom and msg_info.messages[0].action.title != chat_title else None
    description = chat.full_chat.about
    members = chat.full_chat.participants_count if hasattr(chat.full_chat, "participants_count") else chat_obj_info.participants_count
    admins = chat.full_chat.admins_count if hasattr(chat.full_chat, "admins_count") else None
    banned_users = chat.full_chat.kicked_count if hasattr(chat.full_chat, "kicked_count") else None
    restrcited_users = chat.full_chat.banned_count if hasattr(chat.full_chat, "banned_count") else None
    users_online = 0
    async for i in event.client.iter_participants(event.chat_id):
        if isinstance(i.status, UserStatusOnline):
            users_online = users_online + 1
    group_stickers = chat.full_chat.stickerset.title if hasattr(chat.full_chat, "stickerset") and chat.full_chat.stickerset else None
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = chat.full_chat.read_inbox_max_id if hasattr(chat.full_chat, "read_inbox_max_id") else None
    messages_sent_alt = chat.full_chat.read_outbox_max_id if hasattr(chat.full_chat, "read_outbox_max_id") else None
    username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
    bots_list = chat.full_chat.bot_info
    bots = 0
    slowmode = "Ha" if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled else "Yo`q"
    slowmode_time = chat.full_chat.slowmode_seconds if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled else None
    restricted = "Ha" if hasattr(chat_obj_info, "restricted") and chat_obj_info.restricted else "Yo`q"
    verified = "Ha" if hasattr(chat_obj_info, "verified") and chat_obj_info.verified else "Yo`q"
    username = "@{}".format(username) if username else None
    creator_username = "@{}".format(creator_username) if creator_username else None

    if admins is None:
        try:
            participants_admins = await event.client(
                GetParticipantsRequest(channel=chat.full_chat.id, filter=ChannelParticipantsAdmins(),
                                       offset=0, limit=0, hash=0))
            admins = participants_admins.count if participants_admins else None
        except Exception:
            await event.edit("<b>Ko`limagan xatolik yuzaga keldi.</b>")
    if bots_list:
        for bot in bots_list:
            bots += 1

    caption = "<b>Guruh Bo`yicha Umumiy Ma`lumot:</b>\n\n"
    caption += f"<b>ID:</b> {chat_obj_info.id}\n"
    if chat_title is not None:
        caption += f"<b>Guruh nomi:</b> {chat_title}\n"
    if former_title is not None:
        caption += f"<b>Eski nomi:</b> {former_title}\n"
    if username is not None:
        caption += f"<b>Guruh turi:</b> Ommaviy\n"
        caption += f"<b>Havola:</b> {username}\n"
    else:
        caption += f"<b>Guruh turi:</b> Xususiy\n"
    if creator_username is not None:
        caption += f"<b>Hissa solgan:</b> <code>{creator_username}</code>\n"
    elif creator_valid:
        caption += f"<b>Hissa qo`shgan:</b> <code><a href=\"tg://user?id={creator_id}\">{creator_firstname}</a></code>\n"
    if created is not None:
        caption += f"<b>Yaratgan:</b> {created.date().strftime('%b %d, %Y')} - {created.time()}\n"
    else:
        caption += f"<b>Yaratuvchhi:</b> {chat_obj_info.date.date().strftime('%b %d, %Y')} - {chat_obj_info.date.time()}\n"
    if messages_viewable is not None:
        caption += f"<b>Ko`rinimli habarlar:</b> {messages_viewable}\n"
    if messages_sent:
        caption += f"<b>Umumiy yozishmalar:</b> {messages_sent}\n"
    elif messages_sent_alt:
        caption += f"<b>Umumiy habarlar:</b> {messages_sent_alt}\n"
    if members is not None:
        caption += f"<b>Foydalanuvchilar:</b> {members}\n"
    if admins is not None:
        caption += f"<b>Adminlar:</b> {admins}\n"
    if bots_list:
        caption += f"<b>Botlar:</b> {bots}\n"
    if users_online:
        caption += f"<b>Hozir onlayn:</b> {users_online}\n"
    if restrcited_users is not None:
        caption += f"<b>Vazifasi cheklangan foydalanuvchilar:</b> {restrcited_users}\n"
    if banned_users is not None:
        caption += f"<b>Bloklangan foydalanuvchilar:</b> {banned_users}\n"
    if group_stickers is not None:
        caption += f"<b>Guruh stikeri:</b> <a href=\"t.me/addstickers/{chat.full_chat.stickerset.short_name}\">{group_stickers}</a>\n"
    caption += "\n"
    caption += f"<b>Sloumod:</b> {slowmode}"
    if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled:
        caption += f", {slowmode_time} sekund\n"
    else:
        caption += "\n"
    caption += f"<b>Cheklanganligi:</b> {restricted}\n"
    if chat_obj_info.restricted:
        caption += f"> Platforma: {chat_obj_info.restriction_reason[0].platform}\n"
        caption += f"> Sabab: {chat_obj_info.restriction_reason[0].reason}\n"
        caption += f"> Tekst: {chat_obj_info.restriction_reason[0].text}\n\n"
    else:
        caption += ""
    if hasattr(chat_obj_info, "scam") and chat_obj_info.scam:
        caption += "<b>Havfli</b>: да\n\n"
    if hasattr(chat_obj_info, "verified"):
        caption += f"<b>Tasdiqlash belgisi:</b> {verified}\n\n"
    if description:
        caption += f"<b>Poddekst:</b> \n\n<code>{description}</code>\n"
    return caption
