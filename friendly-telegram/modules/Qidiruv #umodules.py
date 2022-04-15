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
    Taqdim qilingan sana: 12.03.2022 / 12:44
    Taqdim qilingan manzil: https://telegram.me/umodules
    ═════════════════════════════════════════
    GeekTG yoki FTG oʻrnatish qoʻllanmasi: https://t.me/TGraphUz/1620
    Kanallar roʻyhati: @UModules, @TGraphUz
"""
__version__ = (1, 0, 0)
# meta developer: @umodules
from .. import loader, utils 
def register(cb):
	cb(QidiruvMod()) 
	
class QidiruvMod(loader.Module):
	"""Kontent qidirish moduli""" 
	strings = {
               "name": "Qidiruv #umodules", 
               "umodules": "<b>[Qidiruv #umodules]</b> • ",
               "easyapk": "<b>[EasyApk #kanali]</b> • ",
               "uzbekona": "<b>[UZBEKONA #kanali]</b> • ",
               "ftgchatuz": "<b>[Qidiruv #umodules]</b> • ",
               "tgraphuz": "<b>[TGraphUz #kanali]</b> • ",
               "yoq": "Buyruqdan keyin soʻz yozing deb qoʻyibman!?",
               "topilmadi": "Hechnima topilmadi! Buyruqdan keyin faqat bitta soʻz yozishga urinib koʻring!"
               }

	async def tgraphcmd(self, message):
		"""qidirish uchun soʻz yoki raqam"""
		try:
			title = utils.get_args_raw(message)
			if not title:
				await message.edit(self.strings("tgraphuz", message) + self.strings("yoq", message))
			else:
				umods = message.input_chat
				await [i async for i in message.client.iter_messages("tgraphuz", search=title)][0].forward_to(umods)
				await message.delete()
		except:
			await message.edit(self.strings("tgraphuz", message) + self.strings("topilmadi", message))
	async def umodcmd(self, message):
		"""qidirish uchun modul nomi yoki buyrugʻi"""
		try:
			title = utils.get_args_raw(message)
			if not title:
				await message.edit(self.strings("umodules", message) + self.strings("yoq", message))
			else:
				umods = message.input_chat
				await [i async for i in message.client.iter_messages("umodules", search=title)][0].forward_to(umods)
				await message.delete()
		except:
			await message.edit(self.strings("umodules", message) + self.strings("topilmadi", message))
	async def umodgrcmd(self, message):
		"""qidirish uchun soʻz (kirilchada faqat)"""
		try:
			title = utils.get_args_raw(message)
			if not title:
				await message.edit(self.strings("ftgchatuz", message) + self.strings("yoq", message))
			else:
				umods = message.input_chat
				await [i async for i in message.client.iter_messages("ftgchatuz", search=title)][0].forward_to(umods)
				await message.delete()
		except:
			await message.edit(self.strings("ftgchatuz", message) + self.strings("topilmadi", message))
	async def uzbekonacmd(self, message):
		"""qidirish uchun soʻz"""
		try:
			title = utils.get_args_raw(message)
			if not title:
				await message.edit(self.strings("uzbekona", message) + self.strings("yoq", message))
			else:
				umods = message.input_chat
				await [i async for i in message.client.iter_messages("uzbekona", search=title)][0].forward_to(umods)
				await message.delete()
		except:
			await message.edit(self.strings("uzbekona", message) + self.strings("topilmadi", message))
	async def apkcmd(self, message):
		"""dastur yoki oʻyin nomi"""
		try:
			title = utils.get_args_raw(message)
			if not title:
				await message.edit(self.strings("easyapk", message) + self.strings("yoq", message))
			else:
				umods = message.input_chat
				await [i async for i in message.client.iter_messages("easyapk", search=title)][0].forward_to(umods)
				await message.delete()
		except:
			await message.edit(self.strings("easyapk", message) + self.strings("topilmadi", message))

# meta akakakakakakak jaakkakaak uchun quyidagi havolani Termux'da bajaring
# meta Uzbekistan presents 
# Barcha huquqlar himoyalangan!
			