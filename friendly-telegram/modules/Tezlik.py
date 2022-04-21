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
    UMod yoki FTG oʻrnatish qoʻllanmasi: https://t.me/TGraphUz/1620
"""
#meta develope: @umodules
__version__ = (1, 0, 0)
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .. import loader, utils
from datetime import datetime


def register(cb):
	cb(PingerMod())


class PingerMod(loader.Module):
	"""Userbot tezligini o'lchaydigan modul"""

	strings = {'name': 'Tezlik sinash'}

	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []

	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()

	async def pingcmd(self, message):
		"""tezlikni sinash"""
		a = 5
		r = utils.get_args(message)
		if r and r[0].isdigit():
			a = int(r[0])
		ping_msg = []
		ping_data = []
		for _ in range(a):
			start = datetime.now()
			msg = await message.client.send_message("me", "ping")
			end = datetime.now()
			duration = (end - start).microseconds / 1000
			ping_data.append(duration)
			ping_msg.append(msg)
		ping = sum(ping_data) / len(ping_data)
		await message.edit(f"<b>📖 Tezlik: </b> {str(ping)[0:5]} MS")
		for i in ping_msg:
			await i.delete()
