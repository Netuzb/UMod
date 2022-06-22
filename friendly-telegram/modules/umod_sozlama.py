__version__ = (1, 0, 0)
# meta developer: @umodules

import os

import telethon
from telethon.tl.types import Message

from .. import loader, main, utils


@loader.tds
class CoreMod(loader.Module):
    """UMod'ni sozlash boʻlimi"""

    strings = {
        "name": "Umod_sozlamalar",
        "too_many_args": "🚫 <b>Arglar juda ko'p</b>",
        "blacklisted": "✅ <b>Chat {} userbotdan qora roʻyxatga kiritilgan</b>",
        "unblacklisted": "✅ <b>Chat {} userbotdan qora roʻyxatga olib tashlandi</b>",
        "user_blacklisted": "✅ <b>Foydalanuvchi {} userbotdan qora roʻyxatga tushdi</b>",
        "user_unblacklisted": "✅ <b>{} foydalanuvchisi userbotdan qora roʻyxatdan chiqarildi</b>",
        "what_prefix": "<b>🌇 Akasi yangi nuqta simvoli qani?</b>",
        "prefix_incorrect": "🌇 <b>Nuqta oʻrnida simvol tanlanmadi.</b>",
        "prefix_set": "<b>🌇 Yangi nuqta oʻrnida simvol muvaffaqiyatli oʻrnatildi.\n🌉 Yangi nuqta simvoli:</b> <code>{newprefix}help</code> <a href='{oldprefix}'></a>",
        "alias_created": "✅ <b>Taxallus yaratildi. Unga</b> <code>{}</code> orqali kiring",
        "aliases": "<b>Taxalluslar:</b>\n",
        "umod": "<b>Tabriklayman!</b>\n",
        "no_command": "🚫 <b>Buyruq</b> <code>{}</code> <b>mavjud</b>",
        "alias_args": "🚫 <b>Siz buyruq va uning taxallusini berishingiz kerak</b>",
        "delalias_args": "🚫 <b>Taxallus nomi</b>ni ko'rsatishingiz kerak",
        "alias_removed": "✅ <b>Taxallus</b> <code>{}</code> <b>oʻchirildi.",
        "no_alias": "<b>🚫 Taxallus</b> <code>{}</code> <b>mavjud</b>",
        "no_pack": "<b>❓ Qanday tarjima paketini qo'shish kerak?</b>",
        "bad_pack": "<b>✅ Yaroqsiz tarjima paketi belgilandi",
        "trnsl_saved": "<b>✅ Tarjima to'plami qo'shildi</b>",
        "packs_cleared": "<b>✅ Tarjimalar tozalandi</b>",
        "lang_set": "<b>✅ Til o'zgartirildi</b>",
        "db_cleared": "<b>🏙️ Barcha oʻzgarishlar tozalandi!</b>",
        "geek": "🌉 <b>Malades! Sizda ''UMod!''\n🌉 Versiya: <code>2.4.6</code>\n🌉 Soʻngi yangilanish: <code>15.06.2022</code></b>",
        "geek_beta": "🕶 <b>Congrats! You are UMod!</b>\n\n<b>UMod version: {}.{}.{}beta</b>\n<b>Branch: beta</b>\n\n<i>🔮 You're using the unstable branch (<b>beta</b>). You receive fresh but untested updates. Report any bugs to @ftgchatuz</i>",
        "geek_alpha": "🕶 <b>Congrats! You are UMod!</b>\n\n<b>UMod version: {}.{}.{}alpha</b>\n<b>Branch: alpha</b>\n\n<i>🔮 You're using <b><u>very</u></b> unstable branch (<b>alpha</b>). You receive fresh but untested updates. You <b><u>can't ask for help, only report bugs</u></b></i>",
    }

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

    async def blacklistcommon(self, message: Message) -> None:
        args = utils.get_args(message)

        if len(args) > 2:
            await utils.answer(message, self.strings("too_many_args", message))
            return

        chatid = None
        module = None

        if args:
            try:
                chatid = int(args[0])
            except ValueError:
                module = args[0]

        if len(args) == 2:
            module = args[1]

        if chatid is None:
            chatid = utils.get_chat_id(message)

        module = self.allmodules.get_classname(module)
        return f"{str(chatid)}.{module}" if module else chatid

    async def ftgvercmd(self, message: Message) -> None:
        """UMod tekshiruvchi"""

        await self.inline.form(
                    self.strings("geek", message),
                    reply_markup=[
                        [{"text": "🌇 UMod - yuzerbot kanali", "url": "https://t.me/umodules"}],                        
                        [{
       "text": "👇 TREND MODULLARIMIZ", 
       "callback": "umoduz",
      }],
                    [{
       "text": "🍊 Animatsiya", 
       "url": "https://t.me/UModules/144",
      },{
       "text": "❤️ MagicText", 
       "url": "https://t.me/UModules/166",
      }],                     
[{
       "text": "✍️ Typewriter", 
       "url": "https://t.me/UModules/158",
      },{
       "text": "🕋 JumaMuborak", 
       "url": "https://t.me/UModules/159",
      }],                     
[{
       "text": "💖 LoveMagic", 
       "url": "https://t.me/UModules/156",
      },{
       "text": "🥰 LoveEmoji", 
       "url": "https://t.me/UModules/155",
      }],
                    ],
                    ttl=10,
                    message=message,
                )

    async def cmd(self, message: Message) -> None:
        """.blacklist [id]
        Blacklist the bot from operating somewhere"""
        chatid = await self.blacklistcommon(message)

        self._db.set(
            main.__name__,
            "blacklist_chats",
            self._db.get(main.__name__, "blacklist_chats", []) + [chatid],
        )

        await utils.answer(message, self.strings("blacklisted", message).format(chatid))

    async def cmd(self, message: Message) -> None:
        """.unblacklist [id]
        Unblacklist the bot from operating somewhere"""
        chatid = await self.blacklistcommon(message)

        self._db.set(
            main.__name__,
            "blacklist_chats",
            list(
                set(self._db.get(main.__name__, "blacklist_chats", [])) - {chatid}
            ),
        )


        await utils.answer(
            message, self.strings("unblacklisted", message).format(chatid)
        )

    async def getuser(self, message: Message) -> None:
        try:
            return int(utils.get_args(message)[0])
        except (ValueError, IndexError):
            reply = await message.get_reply_message()

            if reply:
                return (await message.get_reply_message()).sender_id

            if message.is_private:
                return message.to_id.user_id

            await utils.answer(message, self.strings("who_to_unblacklist", message))
            return

    async def cmd(self, message: Message) -> None:
        """.blacklistuser [id]
        Prevent this user from running any commands"""
        user = await self.getuser(message)

        self._db.set(
            main.__name__,
            "blacklist_users",
            self._db.get(main.__name__, "blacklist_users", []) + [user],
        )

        await utils.answer(
            message, self.strings("user_blacklisted", message).format(user)
        )

    async def cmd(self, message: Message) -> None:
        """.unblacklistuser [id]
        Allow this user to run permitted commands"""
        user = await self.getuser(message)

        self._db.set(
            main.__name__,
            "blacklist_users",
            list(set(self._db.get(main.__name__, "blacklist_users", [])) - {user}),
        )


        await utils.answer(
            message, self.strings("user_unblacklisted", message).format(user)
        )

    @loader.owner
    async def nuqtacmd(self, message: Message) -> None:
        """nuqtani almashtirish"""
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, self.strings("what_prefix", message))
            return

        if len(args) != 1:
            await utils.answer(message, self.strings("prefix_incorrect", message))

        oldprefix = self._db.get(main.__name__, "command_prefix", ".")
        self._db.set(main.__name__, "command_prefix", args)
        await utils.answer(
            message,
            self.strings("prefix_set", message).format(
                newprefix=utils.escape_html(args[0]),
                oldprefix=utils.escape_html(oldprefix),
            ),
        )

    @loader.owner
    async def cmd(self, message: Message) -> None:
        """Print all your aliases"""
        aliases = self.allmodules.aliases
        string = self.strings("aliases", message)

        string += "\n".join([f"\n{i}: {y}" for i, y in aliases.items()])

        await utils.answer(message, string)

    @loader.owner
    async def cmd(self, message: Message) -> None:
        """Set an alias for a command"""
        args = utils.get_args(message)

        if len(args) != 2:
            await utils.answer(message, self.strings("alias_args", message))
            return

        alias, cmd = args
        ret = self.allmodules.add_alias(alias, cmd)

        if ret:
            self._db.set(
                __name__, "aliases", {**self._db.get(__name__, "aliases"), alias: cmd}
            )
            await utils.answer(
                message,
                self.strings("alias_created", message).format(utils.escape_html(alias)),
            )
        else:
            await utils.answer(
                message,
                self.strings("no_command", message).format(utils.escape_html(cmd)),
            )

    @loader.owner
    async def cmd(self, message: Message) -> None:
        """Remove an alias for a command"""
        args = utils.get_args(message)

        if len(args) != 1:
            await utils.answer(message, self.strings("delalias_args", message))
            return

        alias = args[0]
        ret = self.allmodules.remove_alias(alias)

        if ret:
            current = self._db.get(__name__, "aliases")
            del current[alias]
            self._db.set(__name__, "aliases", current)
            await utils.answer(
                message,
                self.strings("alias_removed", message).format(utils.escape_html(alias)),
            )
        else:
            await utils.answer(
                message,
                self.strings("no_alias", message).format(utils.escape_html(alias)),
            )

    async def cmd(self, message: Message) -> None:
        """Tarjima tilini qoʻshish .tiladd <pack>"""
        args = utils.get_args(message)

        if len(args) != 1:
            await utils.answer(message, self.strings("no_pack", message))
            return

        pack = args[0]
        if str(pack).isdigit():
            pack = int(pack)

        try:
            pack = await self._client.get_entity(pack)
        except ValueError:
            await utils.answer(message, self.strings("bad_pack", message))
            return

        if isinstance(pack, telethon.tl.types.Channel) and not pack.megagroup:
            self._db.setdefault(main.__name__, {}).setdefault("langpacks", []).append(
                pack.id
            )
            self._db.save()
            await utils.answer(message, self.strings("trnsl_saved", message))
        else:
            await utils.answer(message, self.strings("bad_pack", message))

    async def cmd(self, message: Message) -> None:
        """Hamma tillarni oʻchirish"""
        self._db.set(main.__name__, "langpacks", [])
        await utils.answer(message, self.strings("packs_cleared", message))

    async def cmd(self, message: Message) -> None:
        """Tarjimalar uchun ishlatiladigan afzal tilni o'zgartiring
        Tilni afzallik tartibida ISO 639-1 til kodlari roʻyxati boʻsh joy sifatida belgilang (masalan, fr en)
        Parametrlarsiz, hammasi"""
        langs = utils.get_args(message)
        self._db.set(main.__name__, "language", langs)
        await utils.answer(message, self.strings("lang_set", message))

    @loader.owner
    async def tozalashcmd(self, message: Message) -> None:
        """barcha o'zgarishlarni tozalash"""
        self._db.clear()
        self._db.save()
        await utils.answer(message, self.strings("db_cleared", message))

    async def _client_ready2(self, client, db):  # skicpq: PYL-W0613
        ret = {
            alias: cmd
            for alias, cmd in db.get(__name__, "aliases", {}).items()
            if self.allmodules.add_alias(alias, cmd)
        }

        db.set(__name__, "aliases", ret)
