# ▀█▀ █▀▀ █▀▄▀█ █░█ █▀█
# ░█░ ██▄ █░▀░█ █▄█ █▀▄
# ═══════════════════════
# █▀▀ █▀█ █▄▀ █ █▄░█ █▀█ █░█
# ██▄ █▀▄ █░█ █ █░▀█ █▄█ ▀▄▀
# ═════════════════════════
# meta developer: @netuzb
# meta channel: @umodules

__version__ = (1, 0, 0)

from .. import loader, utils  
import logging
from requests import post
import io


logger = logging.getLogger(__name__)


@loader.tds
class OrnatgichMod(loader.Module):
    """Modul fayliga reply holatda yozing va u sizga o'rnatish kerak boʻlgan modulni toʻgʻridan-toʻgʻri havolasini yartib beradi!"""

    strings = {
               "name": "Umod_auto",
               "yukla": "🌇 <b>Havola yaratilmoqda...</b>",
               "javob": "🏙️ <b>Modul fayliga javob tariqasida yozing!</b>"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.sudo
    async def ornatishcmd(self, message):
        """modul fayliga reply holatda"""
    
        await message.edit(self.strings("yukla", message))
        reply = await message.get_reply_message()
        if not reply:
            await message.edit(self.strings("javob", message))
            return
        media = reply.media
        if not media:
            file = io.BytesIO(bytes(reply.raw_text, "utf-8"))
            file.name = "txt.txt"
        else:
            file = io.BytesIO(await self.client.download_file(media))
            file.name = reply.file.name or reply.file.id + reply.file.ext
        try:
            x0at = post("https://x0.at", files={"file": file})
        except ConnectionError as e:
            await message.edit(ste(e))
            return
        url = x0at.text
        output = f'<b>🌇 Havola tayyor!\n🌉 Havola: <code>{url}</code>🏙️ Modul uchun:</b> <code>.dlmod {url}</code><b>🏙️ <b>Baza: @umoduz</b>'
        await message.edit(output)
        
