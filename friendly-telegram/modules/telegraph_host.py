# ▀█▀ █▀▀ █▀▄▀█ █░█ █▀█
# ░█░ ██▄ █░▀░█ █▄█ █▀▄
# ═══════════════════════
# █▀▀ █▀█ █▄▀ █ █▄░█ █▀█ █░█
# ██▄ █▀▄ █░█ █ █░▀█ █▄█ ▀▄▀
# ═════════════════════════════
# meta developer: @netuzb
# meta channel: @umodules

__version__ = (1, 0, 0)

from .. import loader, utils
import asyncio
import requests
from telethon.tl.types import DocumentAttributeFilename

def register(cb):
 cb(TelegraphMod())

class TelegraphMod(loader.Module):
	"""telegra.ph hostiga rasm/video/gif yuklash"""
	strings = {
               "name": "telegraph",
               "reply": "🏙️ <b>Mediaga javob tariqasida...</b>"}

	def __init__(self):
		self.name = self.strings['name']
		
	async def ph_qollanmacmd(self, message):
		"""qoʻllanma"""
		
		qollanma = """<b>
🌇 Qoʻllanma: <code>Telegraph host</code>

🌉 - Kerakli, yuklamoqchi boʻlgan rasm/gif/video topasiz, aniqlaysiz. Va shu media'ga javoban <code>.ph</code> buyrugʻini yozib yuborasiz.
🌉 - Buyruqdan keyin darrov "Nega qotib qoldi?" degan savolga berilmang.
🌉 - Modul tezligi media hajmiga bogʻliq.

🌇 Qisqacha namuna:
🌉 <a href="https://te.legra.ph/file/763e3cb894fb1566723ec.mp4">Videoni koʻrish</a></b>"""
		await message.edit(qollanma)
		return
		
	
	async def phcmd(self, message):
			"""javob tariqasida: rasm/video/gif"""
			if message.is_reply:
				reply_message = await message.get_reply_message()
				data = await check_media(reply_message)
				if isinstance(data, bool):
					await message.edit(self.strings("reply", message))
					return
			else:
				await message.edit(self.strings("reply", message))
				return
					
				
			file = await message.client.download_media(data, bytes)
			path = requests.post('https://te.legra.ph/upload', files={'file': ('file', file, None)}).json()
			try:
				link = 'https://te.legra.ph'+path[0]['src']
			except KeyError:
				link = path["error"]
			await message.edit("<b>🌇 Havola tayyor.\n🌉 Yuklangan host: https://te.legra.ph\n🌉 Yuklangan manzilga havola:\n🏙️ "+link+"</b>")
				
			
async def check_media(reply_message):
	if reply_message and reply_message.media:
		if reply_message.photo:
			data = reply_message.photo
		elif reply_message.document:
			if DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in reply_message.media.document.attributes:
				return False
			if reply_message.audio or reply_message.voice:
				return False
			data = reply_message.media.document
		else:
			return False
	else:
		return False
	if not data or data is None:
		return False
	else:
		return data
		
		
		
