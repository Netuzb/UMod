#    ████░████░███░███░██░██░████░
#    ░██░░██░░░██░█░██░██░██░███░░
#    ░██░░████░██░░░██░█████░█████
#    ═════════════════════════════════════════
#    ████░████░░██░██░██░███░░██░█████░██░░░██
#    ██░░░███░░░████░░██░██░█░██░██░██░░██░██░
#    ████░█████░██░██░██░██░░███░█████░░░███░░
#    ═════════════════════════════════════════
#    Litsenziya: https://t.me/UModules/112
#    Taqdim qilingan manzil: https://telegram.me/umodules
#    ═════════════════════════════════════════
#    GeekTG yoki FTG oʻrnatish qoʻllanmasi: https://t.me/TGraphUz/1620

from telethon import events
from .. import loader, utils
from asyncio import sleep
from telethon.tl.functions.users import GetFullUserRequest
import random

__version__ = (1, 0, 0)

# meta developer: @netuzb
# meta channel: @umodules

def register(cb):
	cb(HaqiqatMod())
	
class HaqiqatMod(loader.Module):
	"""Haqiqat yoki yolgʻon moduli"""
	
	strings = {
		"name": "Haqiqat",
		"soz_kiriting": "",
		}
		
	async def haqcmd(self, message):
		"""<buyruq> soʻz yoki gap"""
		
		reply = await message.get_reply_message()
		text = utils.get_args_raw(message)
		soz_kiriting = "<b>📖 Iltimos, buyruqdan keyin soʻzni kiriting!</b>"
		haq_natija = ["😑 - YOLGʻON", "😎 - HAQIQAT",]
		haq = [f"{random.choice(haq_natija)}"]
		if not text and not reply:
			await message.edit(soz_kiriting)
		else:
			await message.edit("📖<b> - Haqiqat yoki yolgʻon, hozir bilamiz...\n📖 - \n📖 - \n📖 - </b>")
			await sleep (1.6)
			await message.edit("📖<b> - Haqiqat yoki yolgʻon, hozir bilamiz...\n📖 - Javob qidirilmoqda... \n📖 - \n📖 - </b>")
			await sleep (0.6)
			await message.edit(f"📖<b> - Haqiqat yoki yolgʻon, hozir bilamiz...\n📖 - Javob topildi. ✅\n📖 - Berilgan mavzu: ''{text}'' \n📖 - </b>")
			await sleep (2.0)
			await message.edit(f"📖<b> - Haqiqat yoki yolgʻon, hozir bilamiz...\n📖 - Javob topildi. ✅\n📖 - Berilgan mavzu: ''{text}'' \n📖 - ''{text}'' - {random.choice(haq)}</b>")
			return

	async def инфаcmd(self, message):
		"""<команда> текст или слова"""
		
		reply = await message.get_reply_message()
		text = utils.get_args_raw(message)
		soz_kiriting = "<b>📖 Пожалуйста, введите слово после команды!</b>"
		haq_natija = ["😑 - ЛОЖЬ", "😎 - ПРАВДА",]
		haq = [f"{random.choice(haq_natija)}"]
		if not text and not reply:
			await message.edit(soz_kiriting)
		else:
			await message.edit("📖<b> - Правда или ложь, теперь мы знаем...\n📖 - \n📖 - \n📖 - </b>")
			await sleep (1.6)
			await message.edit("📖<b> - Правда или ложь, теперь мы знаем...\n📖 - Ищу ответ... \n📖 - \n📖 - </b>")
			await sleep (0.6)
			await message.edit(f"📖<b> - Правда или ложь, теперь мы знаем...\n📖 - Ответ был найден. ✅\n📖 - Тема указана: ''{text}'' \n📖 - </b>")
			await sleep (2.0)
			await message.edit(f"📖<b> - Правда или ложь, теперь мы знаем...\n📖 - Ответ был найден. ✅\n📖 - Тема указана: ''{text}'' \n📖 - ''{text}'' - {random.choice(haq)}</b>")
			return
