""" 
    ███▒███▒██▒██▒█▒░█▒████
    ░█▒░█▒░░█▒█▒█▒█▒░█▒█▒█
    ░█▒░███▒█▒░░█▒████▒█▒░█
    
    Litsenziya: LLC © N.OA.ZL.QW (qattan olish kere edi?)
    Taqdimot kuni: 12.03.2022 / 23:20
    Taqdimot manzili: https://telegram.me/umodules
"""
__version__ = (1, 3, 9)
# tushunmasang tegma, chunki Python dasturlash tili noyob til
# meta developer: @umodules
# modul qiziqib kirganlar xato qiladi)

from .. import loader, utils 
from telethon import events 
from telethon.errors.rpcerrorlist import YouBlockedUserError 
from asyncio.exceptions import TimeoutError 
 
def register(cb): 
    cb(KarishaMod()) 
 
class KarishaMod(loader.Module): 
    """Ovozlar - sunʼiy intellekt TTS ovozlarining sifatlilari

🇺🇿 • Modulda Karisha va Aleks ovozlari mavjud))
📁 • Modullar bazasi doimo yangilanib boriladi: @UModules""" 
    strings = {
               "name": "Ovozlar #umdoules",
               "yana": "<b>🗿 • Yana urinib koʻrinchi, balkim oʻxshab qolar!</b>",
               "karisha": "<b>🗿 • Buyruqdan keyin soʻz yozish kerak!</b>",
               "xatolik": "<b>🗿 • Xatolik yuz berdi!?</b>",
               "aktivqil": "<b>🗿 • Akasi siz oldin botni aktiv qiling</b> @deepttsbot\n🌟 • <b>Bot adminiga rahmat:</b> @cocuc",
               "aktivqil_alex": "<b>🗿 • Uzr-a akasi, oldin botni aktiv qiling</b> @aleksobot"
               }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self._me = await client.get_me()
 
    async def karishacmd(self, message): 
        """.karisha <yozuv, boʻsh qolmasin>""" 
        try:
            text = utils.get_args_raw(message) 
            reply = await message.get_reply_message() 
            chat = "@deepttsbot" 
            if not text and not reply: 
                await message.edit(self.strings("karisha", message)) 
            if text: 
                async with message.client.conversation(chat) as conv:
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=2134705715))
                        await message.client.send_message(chat, text) and await message.delete()
                        response = await response 
                    except YouBlockedUserError: 
                        await message.reply(self.strings("aktivqil", message))
                        return 
                    if not response.text: 
                        await message.edit(self.strings("yana", message))
                        return
                    await self.client.send_file(message.to_id, response.media, reply_to=reply.id if reply else None)
                    await self.client.delete_dialog(chat)
                    return
        except TimeoutError: 
            return await message.edit(self.strings("xatolik", message))
            
    async def alekscmd(self, message): 
        """.aleks <yozuv, unutmang yozuvni>""" 
        try:
            text = utils.get_args_raw(message) 
            reply = await message.get_reply_message() 
            chat = "@aleksobot" 
            if not text and not reply: 
                await message.edit(self.strings("karisha", message)) 
            if text: 
                async with message.client.conversation(chat) as conv:
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=616484527))
                        await message.client.send_message(chat, text) and await message.delete()
                        response = await response 
                    except YouBlockedUserError: 
                        await message.reply(self.strings("aktivqil_alex", message))
                        return 
                    if not response.text: 
                        await message.edit(self.strings("yana", message))
                        return
                    await self.client.send_file(message.to_id, response.media, reply_to=reply.id if reply else None)
                    await self.client.delete_dialog(chat)
                    return
        except TimeoutError: 
            return await message.edit(self.strings("xatolik", message))
            
    async def blacmd(self, message): 
        """.aleks <yozuv, unutmang yozuvni>""" 
        try:
            text = utils.get_args_raw(message) 
            reply = await message.get_reply_message() 
            chat = "SkyArchivebot" 
            if not text and not reply: 
                await message.edit(self.strings("karisha", message)) 
            if text: 
                async with message.client.conversation(chat) as conv:
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=1584481069))
                        await message.client.send_message(chat, "/bla",) and await message.delete()
                        response = await response 
                    except YouBlockedUserError: 
                        await message.reply(self.strings("aktivqil_alex", message))
                        return 
                    if not response.text: 
                        await message.edit(self.strings("yana", message))
                        return
                    await self.client.send_message(message.to_id, response.text, reply_to=reply.id if reply else None)
                    await self.client.delete_dialog(chat)
                    return
        except TimeoutError: 
            return await message.edit(self.strings("xatolik", message))
     
     async def blacmd(self, message): 
        """.aleks <yozuv, unutmang yozuvni>""" 
        try:
            text = utils.get_args_raw(message) 
            reply = await message.get_reply_message() 
            chat = "SkyArchivebot" 
            if not text and not reply: 
                await message.edit(self.strings("karisha", message)) 
            if text: 
                async with message.client.conversation(chat) as conv:
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=1584481069))
                        await message.client.send_message(chat, "/bla",) and await message.delete()
                        response = await response 
                    except YouBlockedUserError: 
                        await message.reply(self.strings("aktivqil_alex", message))
                        return 
                    if not response.text: 
                        await message.edit(self.strings("yana", message))
                        return
                    await self.client.send_message(message.to_id, response.text, reply_to=reply.id if reply else None)
                    await self.client.delete_dialog(chat)
                    return
        except TimeoutError: 
            return await message.edit(self.strings("xatolik", message))

            #abababbaba anajajajaja ananajanananana