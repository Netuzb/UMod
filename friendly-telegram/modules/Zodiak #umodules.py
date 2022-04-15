__version__ = (1, 0, 1)
# meta developer: @netuzb

from .. import loader, utils 
from telethon import events 
from telethon.errors.rpcerrorlist import YouBlockedUserError 
from asyncio.exceptions import TimeoutError 
 
def register(cb): 
    cb(ZodiakMod()) 
class ZodiakMod(loader.Module): 
    """Zodiak""" 
    strings = {
               "name": "Zodiak #umodules",
               "eshe": "<b>🤨 • Попробуй еще раз!</b>",
               "chto": "<b>Zodiaklar ro'yhatini olish uchun <code>.royhat</code> deb yozing</b>",
               "oshibka": "<b>😐 • Фига се, ошибка!</b>",
               "udali": "<b>☹️ • Ты забыл активировать! - </b>@zodiakbot"} 

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self._me = await client.get_me()
 
    async def olishcmd(self, message): 
        """olish uchun yuboring""" 
        try:
            text = utils.get_args_raw(message) 
            reply = await message.get_reply_message() 
            olish = "zodiakbot" 
            if not text and not reply: 
                return 
            if text: 
                async with message.client.conversation(olish) as conv: 
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=136873501)) 
                        await message.client.send_message(olish, "📅 Гороскоп на месяц") and await message.delete()
                        response = await response 
                    except YouBlockedUserError: 
                        await message.reply(self.strings("udali", message))
                        return 
                    if not response.text: 
                        await message.edit(self.strings("eshe", message))
                        return
                    await self.client.send_message(message.to_id, response.text)
                    
        except TimeoutError: 
            return await message.edit(self.strings("oshibka", message))
    
    async def zodcmd(self, message): 
        """zodiak nomi""" 
        try:
            text = utils.get_args_raw(message) 
            reply = await message.get_reply_message() 
            zod = "zodiakbot" 
            if not text and not reply: 
                await message.edit(self.strings("chto", message))
                return 
            if text: 
                async with message.client.conversation(zod) as conv: 
                    try: 
                        response = conv.wait_event(events.NewMessage(incoming=True, from_users=136873501)) 
                        await message.client.send_message(zod, text) and await message.delete()
                        response = await response 
                        await self.client.send_message(message.to_id, "Zodiak aktiv boʻldi! Endilikda <b>.olish</b> buyrug'ini ishlating!")
                    except YouBlockedUserError: 
                        await message.reply(self.strings("udali", message))
                        return 
                    if not response.text: 
                        await message.edit(self.strings("eshe", message))
                        return
                    
        except TimeoutError: 
            return await message.edit(self.strings("oshibka", message))
            
    async def qaytacmd(self, message): 
        """• zodiakni o'zgartirish uchun ishlating""" 
        try:
            text = utils.get_args_raw(message)       
            qayta = "zodiakbot"             
            if text: 
                async with message.client.conversation(qayta) as conv: 
                    try:                         
                        await message.client.send_message(qayta, "🌀 Сменить знак") and await message.delete()
                        await self.client.send_message(message.to_id, "<b>Zodiak restart berildi. Endi <code>.zod ♈ Овен</code> yoki Oven oʻrnida hoxlagan bittasini yozing.</b>")
                    except YouBlockedUserError:                         
                        return                     
        except TimeoutError: 
            return await message.edit(self.strings("oshibka", message))