# ▀█▀ █▀▀ █▀▄▀█ █░█ █▀█
# ░█░ ██▄ █░▀░█ █▄█ █▀▄
# ═══════════════════════
# █▀▀ █▀█ █▄▀ █ █▄░█ █▀█ █░█
# ██▄ █▀▄ █░█ █ █░▀█ █▄█ ▀▄▀
# ═════════════════════════════
# meta developer: @netuzb
# meta channel: @umodules

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .. import loader, utils


def register(cb):
	cb(BlackLinesMod())


class BlackLinesMod(loader.Module):
	"""Suratni @BlackLinesBot boti orqali noodatiy holatga aylantiradi"""

	strings = {'name': 'Black Lines'}

	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []

	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()

	async def linecmd(self, message):
		"""[reply rasmga] sifat yuqori boʻlsa vaqti shunchali koʻp boʻladi """
		
		reply = await message.get_reply_message()
		if not reply:
			await message.edit("Suratga reply")
			return
		try:
			photo = reply.media.photo
		except:
			await message.edit("Faqat suratga reply")
			return
		
		args = utils.get_args_raw(message)
				
				
		chat = '@BlackLinesBot'
		await message.edit('@BlackLinesBot <code>Natijani kuting...</code>')
		async with message.client.conversation(chat) as conv:
			try:
				response = conv.wait_event(events.NewMessage(incoming=True, from_users=1051644279))
				await message.client.send_file(chat, photo, caption=args)
				response = await response
			except YouBlockedUserError:
				await message.reply('<code>Botni blokdan chiqaring:</code> @BlackLinesBot')
				return

			await message.delete()
			await message.client.send_file(message.to_id, response.media)
			
