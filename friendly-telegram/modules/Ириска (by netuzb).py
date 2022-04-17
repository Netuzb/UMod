__version__ = (1, 0, 1)
# meta developer: @netuzb
# Все права защищены и управляются Темуром Эркиновым(@netuzb).
# Обратите внимание, что вы будете нести ответственность за любые изменения, внесенные в этот модуль. 

from .. import loader, utils 
from telethon import events 
from telethon.errors.rpcerrorlist import YouBlockedUserError 
from asyncio.exceptions import TimeoutError 
 
def register(cb): 
    cb(iriskaMod()) 
 
class iriskaMod(loader.Module): 
    """ Ириска: Создатель: @netuzb

🇺🇿 • Админ узбек!)
🇷🇺 • Модуль должен был написан на узбекском языке. Но Ириска не говорит по-узбекски. Именно поэтому модуль на русском языке.""" 
    strings = {
               "name": "Ириска #umodules",
               "eshe": "<b>🤨 • Попробуй еще раз!</b>",
               "chto": "<b>😑 • Давай только с текстом?</b>",
               "oshibka": "<b>😐 • Фига се, ошибка!</b>",
               "udali": "<b>☹️ • Ты забыл активировать! - </b>@iris_cm_bot"} 

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self._me = await client.get_me()
 
    async def инфаcmd(self, message): 
        """😚 • Выдает вероятность инфы""" 
        try:
            text = utils.get_args_raw(message) 
            reply = await message.get_reply_message() 
            chat = "@iris_cm_bot" 
            if not text and not reply: 
                await message.edit(self.strings("chto", message))
                return 
            if text: 
                async with message.client.conversation(chat) as conv: 
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=707693258)) 
                        await message.client.send_message(chat, "!Инфа " + text) 
                        response = await response 
                    except YouBlockedUserError: 
                        await message.reply(self.strings("udali", message))
                        return 
                    if not response.text: 
                        await message.edit(self.strings("eshe", message))
                        return
                    await self.client.send_message(message.to_id, response.text)
                    await self.client.delete_dialog(chat) 
        except TimeoutError: 
            return await message.edit(self.strings("oshibka", message))
            
# -----------------------------------------------------------#
# The creator of this module is @netuzb 
# -----------------------------------------------------------#

    async def выбериcmd(self, message): 
        """🤔 • Выбирает межди <text> или <text>""" 
        try:
            text = utils.get_args_raw(message) 
            reply = await message.get_reply_message() 
            chat = "@iris_cm_bot" 
            if not text and not reply: 
                await message.edit(self.strings("chto", message))
                return 
            if text: 
                async with message.client.conversation(chat) as conv: 
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=707693258)) 
                        await message.client.send_message(chat, "!Выбери " + text) 
                        response = await response 
                    except YouBlockedUserError: 
                        await message.reply(self.strings("udali", message))
                        return 
                    if not response.text: 
                        await message.edit(self.strings("eshe", message))
                        return
                    await self.client.send_message(message.to_id, response.text)
                    await self.client.delete_dialog(chat) 
        except TimeoutError: 
            return await message.edit(self.strings("oshibka", message))

# -----------------------------------------------------------#
# The creator of this module is @netuzb 
# -----------------------------------------------------------#

    async def данетcmd(self, message): 
        """🤨 • Выбирает <да> или <нет>""" 
        try:
            text = utils.get_args_raw(message) 
            reply = await message.get_reply_message() 
            chat = "@iris_cm_bot" 
            if not text and not reply: 
                await message.edit(self.strings("chto", message))
                return 
            if text: 
                async with message.client.conversation(chat) as conv: 
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=707693258)) 
                        await message.client.send_message(chat, "!Данет " + text) 
                        response = await response 
                    except YouBlockedUserError: 
                        await message.reply(self.strings("udali", message))
                        return 
                    if not response.text: 
                        await message.edit(self.strings("eshe", message))
                        return
                    await self.client.send_message(message.to_id, response.text)
                    await self.client.delete_dialog(chat) 
        except TimeoutError: 
            return await message.edit(self.strings("oshibka", message))

# -----------------------------------------------------------#
# The creator of this module is @netuzb 
# -----------------------------------------------------------#

    async def погодаcmd(self, message): 
        """🥶 • Выдает погоду на указанный город""" 
        try:
            text = utils.get_args_raw(message) 
            reply = await message.get_reply_message() 
            chat = "@iris_cm_bot" 
            if not text and not reply: 
                await message.edit(self.strings("chto", message))
                return 
            if text: 
                async with message.client.conversation(chat) as conv: 
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=707693258)) 
                        await message.client.send_message(chat, "!Погода " + text) and await message.delete()
                        response = await response 
                    except YouBlockedUserError: 
                        await message.reply(self.strings("udali", message))
                        return 
                    if not response.text: 
                        await message.edit(self.strings("eshe", message))
                        return
                    await self.client.send_message(message.to_id, response.text)
                    await self.client.delete_dialog(chat) 
        except TimeoutError: 
            return await message.edit(self.strings("oshibka", message))

# -----------------------------------------------------------#
# The creator of this module is @netuzb 
# -----------------------------------------------------------#

    async def рандомcmd(self, message): 
        """🤓 • Выпадает рандомная цифра <цифр до бесконечности>""" 
        try:
            text = utils.get_args_raw(message) 
            reply = await message.get_reply_message() 
            chat = "@iris_cm_bot" 
            if not text and not reply: 
                await message.edit(self.strings("chto", message))
                return 
            if text: 
                async with message.client.conversation(chat) as conv: 
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=707693258)) 
                        await message.client.send_message(chat, "!Рандом " + text) 
                        response = await response 
                    except YouBlockedUserError: 
                        await message.reply(self.strings("udali", message))
                        return 
                    if not response.text: 
                        await message.edit(self.strings("eshe", message))
                        return
                    await self.client.send_message(message.to_id, response.text)
                    await self.client.delete_dialog(chat) 
        except TimeoutError: 
            return await message.edit(self.strings("oshibka", message))
