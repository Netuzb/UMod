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
from .. import loader, utils

import requests
import logging
from telethon.tl.types import Message
import io

# requires: urllib requests

logger = logging.getLogger(__name__)


@loader.tds
class CarbonaypiMod(loader.Module):
    """Kodni chiroyli suratga joylash"""

    strings = {
        "name": "CarbonAypi",
        "args": "<b>📖 Hechnima yoʻq...</b>",
        "loading": "<b>📖 Bajarilmoqda...</b>",
        "yoq": "<b>📖 Kod yozishni esdan chiqardingiz.</b>",
    }

    async def client_ready(self, client, db):
        self._client = client

    @loader.unrestricted
    async def carboncmd(self, message: Message) -> None:
        """<kod> - faqat dasturlash tili"""
        args = utils.get_args_raw(message)
        text = utils.get_args_raw(message) 
        if not text:
        	message = await utils.answer(message, self.strings("yoq", message)) and await message.delete()
        
        try:
            code_from_message = (
                await self._client.download_file(message.media)
            ).decode("utf-8")
        except Exception:
            code_from_message = ""

        try:
            reply = await message.get_reply_message()
            code_from_reply = (await self._client.download_file(reply.media)).decode(
                "utf-8"
            )
        except Exception:
            code_from_reply = ""

        args = args or code_from_message or code_from_reply

        message = await utils.answer(message, self.strings("loading", message))
        try:
            message = message[0]
        except Exception:
            pass

        doc = io.BytesIO(
            (
                await utils.run_sync(
                    requests.post,
                    "https://carbonara-42.herokuapp.com/api/cook",
                    json={"code": args},
                )
            ).content
        )
        doc.name = "carbonized.jpg"

        await self._client.send_message(
            utils.get_chat_id(message),
            file=doc,
            force_document=(len(args.splitlines()) > 50),
        )
        await message.delete()
