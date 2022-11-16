# ▀█▀ █▀▀ █▀▄▀█ █░█ █▀█
# ░█░ ██▄ █░▀░█ █▄█ █▀▄
# ═══════════════════════
# █▀▀ █▀█ █▄▀ █ █▄░█ █▀█ █░█
# ██▄ █▀▄ █░█ █ █░▀█ █▄█ ▀▄▀
# ═════════════════════════════
# meta developer: @netuzb
# meta channel: @umodules

from .. import loader, utils
from asyncio import sleep

@loader.tds
class SekinMod(loader.Module):
	"""Sekin yozish uchun ajoyib modul"""

	strings = {
        "name": "Sekin Yozish"
        }
    
	@loader.owner
	async def sekincmd(self, message):
		"""[buyruq] o`zini yozsa kifoya"""
		text = utils.get_args_raw(message)
		if not text:
			reply = await message.get_reply_message()
			if not reply or not reply.message:
				await message.edit("<b>Habar yozing</b>")
				return
			text = reply.message
		out = ""
		for ch in text:
			out += ch
			if ch not in [" ", "\n"]:
				await message.edit(out+"\u2060")
				await sleep(0.3)
			