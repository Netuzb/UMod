"""
    ███▒███▒██▒██▒█▒░█▒████
    ░█▒░█▒░░█▒█▒█▒█▒░█▒█▒█
    ░█▒░███▒█▒░░█▒████▒█▒░█
    Litsenziya: LLC © N.OA.ZL.QW (qaysi tupoy modul uchun litsenziya oladi? beradi?)
    Taqdim qilingan sana: 03.04.2022 / 20:54
    Taqdim qilingan manzil: https://telegram.me/umodules
"""
__version__ = (1, 0, 0)
# meta developer: @umodules

from .. import loader, utils
from PIL import Image, ImageDraw
from random import randint
from io import BytesIO


@loader.tds
class WhatMod(loader.Module):
	"""Nima-bu - modul suratlarda duch kegan joyiga qizil doirachada belgi chizib beradi

🇺🇿 • Ko'rinishidan oddiy, lekin sizni zeriktirmasligi aniq))
📂 • Modullar bazasi doimo yangilanib boriladi: @umodules"""
	strings = {"name": "Nima-bu #umodules"}
	
	
	async def nimacmd(self, message):
		""".nima <suratga reply qilgan holda>"""
		args = utils.get_args_raw(message)
		scale = int(args) if args and args.isdigit() else 50
		scale = 10 if scale < 0 else scale
		scale = 100 if scale > 100 else scale
		reply = await message.get_reply_message()
		if not reply or not reply.file.mime_type.split("/")[0].lower() == "image":
			await message.edit("<b>🗿 • Rasmga javob tariqasida ishlating!</b>")
			return
		await message.edit("<b>Nima ekan-a bu?</b>")
		im = BytesIO()
		await reply.download_media(im)
		im = Image.open(im)
		w, h = im.size
		f = (min(w,h)//100)*scale
		draw = ImageDraw.Draw(im)
		x, y = randint(0, w-f), randint(0, h-f)
		draw.ellipse((x, y, x+randint(f//2, f), y+randint(f//2, f)), fill=None, outline="red", width=randint(3, 10))
		out = BytesIO()
		out.name = "nima.webp"
		im.save(out)
		out.seek(0)
		await message.delete()
		return await reply.reply(file=out)
	
# modullarni ishlatishni o'rganvol avval, ichini titkilaguncha)))
		
