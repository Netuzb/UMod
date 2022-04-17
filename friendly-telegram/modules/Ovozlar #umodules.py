"""
    ████░████░███░███░██░██░████░
    ░██░░██░░░██░█░██░██░██░███░░
    ░██░░████░██░░░██░█████░█████
    ═════════════════════════════════════════
    ████░████░░██░██░██░███░░██░█████░██░░░██
    ██░░░███░░░████░░██░██░█░██░██░██░░██░██░
    ████░█████░██░██░██░██░░███░█████░░░███░░
    ═════════════════════════════════════════
    Litsenziya: LLC © N.OA.ZL.QW (qaysi tupoy modul uchun litsenziya oladi? beradi?)
    Taqdim qilingan manzil: https://telegram.me/umodules
    ═════════════════════════════════════════
    GeekTG yoki FTG oʻrnatish qoʻllanmasi: https://t.me/TGraphUz/1620
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
    """Ovozlar - sunʼiy intellekt TTS ovozlarining sifatlilari""" 
    strings = {
               "name": "Ovozlar",
               "yana": "<b>🗿 • Yana urinib koʻringchi, balkim oʻxshab qolar!</b>",
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
        """<yozuv, boʻsh qolmasin>""" 
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
        """<yozuv, unutmang yozuvni>""" 
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
            
    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self._me = await client.get_me()
