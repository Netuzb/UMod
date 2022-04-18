# <3 title: GeekConfig [geek]
# <3 pic: https://img.icons8.com/external-filled-outline-wichaiwi/64/000000/external-multitasking-generation-z-filled-outline-wichaiwi.png
# <3 desc: Interactive configurator for GeekTG

# scope: inline_content

from .. import loader, utils
from telethon.tl.types import Message
import logging
from typing import Union, List
from aiogram.types import CallbackQuery
import ast

logger = logging.getLogger(__name__)


def chunks(lst: Union[list, tuple, set], n: int) -> List[list]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


blacklist = [
    "Raphielgang Configuration Placeholder",
    "Uniborg configuration placeholder",
    "Logger",
]


@loader.tds
class ConfigMod(loader.Module):
    """Modullarni konfiguratsiya qilish"""

    strings = {
        "name": "Konfiguratsiya",
        "configure": "📖 <b>Bu yerda siz modullarning konfiguratsiyasini sozlashingiz mumkin</b>",
        "configuring_mod": "📖 <b>Mod uchun konfiguratsiya opsiyasini tanlang</b> <code>{}</code>",
        "configuring_option": "📖 <b>Konfiguratsiya opsiyasi </b><code>{}</code><b> mod </b><code>{}</code>\n<i>ℹ️ {}</i>\n\n<b>Standart: </b><code>{}</code>\n\n<b>Hozirgi: </b><code>{}</code>",
        "option_saved": "📖 <b>Konfiguratsiya opsiyasi </b><code>{}</code><b> mod </b><code>{}</code><b> saqlandi!</b>\n<b>Hozirgi: </b><code>{}</code>",
    }

    def get(self, *args) -> dict:
        return self._db.get(self.strings["name"], *args)

    def set(self, *args) -> None:
        return self._db.set(self.strings["name"], *args)

    async def client_ready(self, client, db) -> None:
        self._db = db
        self._client = client
        self._bot_id = (await self.inline.bot.get_me()).id
        self._forms = {}

    @staticmethod
    async def inline__close(call: CallbackQuery) -> None:  # noqa
        await call.delete()

    async def inline__set_config(
        self,
        call: CallbackQuery,
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
    ) -> None:  # noqa
        for module in self.allmodules.modules:
            if module.strings("name") == mod:
                module.config[option] = query
                if query:
                    try:
                        query = ast.literal_eval(query)
                    except (ValueError, SyntaxError):
                        pass
                    self._db.setdefault(module.__module__, {}).setdefault(
                        "__config__", {}
                    )[option] = query
                else:
                    try:
                        del self._db.setdefault(module.__module__, {}).setdefault(
                            "__config__", {}
                        )[option]
                    except KeyError:
                        pass

                self.allmodules.send_config_one(module, self._db, skip_hook=True)
                self._db.save()

        await call.edit(
            self.strings("option_saved").format(mod, option, query),
            reply_markup=[
                [
                    {
                        "text": "👈 Orqaga",
                        "callback": self.inline__configure,
                        "args": (mod,),
                    },
                    {"text": "🚫 Yopish", "callback": self.inline__close},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__configure_option(
        self, call: CallbackQuery, mod: str, config_opt: str
    ) -> None:  # noqa
        for module in self.allmodules.modules:
            if module.strings("name") == mod:
                await call.edit(
                    self.strings("configuring_option").format(
                        utils.escape_html(config_opt),
                        utils.escape_html(mod),
                        utils.escape_html(module.config.getdoc(config_opt)),
                        utils.escape_html(module.config.getdef(config_opt)),
                        utils.escape_html(module.config[config_opt]),
                    ),
                    reply_markup=[
                        [
                            {
                                "text": "✍️ Qiymatni kiriting",
                                "input": "✍️ Ushbu parametr uchun yangi konfiguratsiya qiymatini kiriting",
                                "handler": self.inline__set_config,
                                "args": (mod, config_opt, call.inline_message_id),
                            }
                        ],
                        [
                            {
                                "text": "👈 Orqaga",
                                "callback": self.inline__configure,
                                "args": (mod,),
                            },
                            {"text": "🚫 Yopish", "callback": self.inline__close},
                        ],
                    ],
                )

    async def inline__configure(self, call: CallbackQuery, mod: str) -> None:  # noqa
        btns = []
        for module in self.allmodules.modules:
            if module.strings("name") == mod:
                for param in module.config:
                    btns += [
                        {
                            "text": param,
                            "callback": self.inline__configure_option,
                            "args": (mod, param),
                        }
                    ]

        await call.edit(
            self.strings("configuring_mod").format(utils.escape_html(mod)),
            reply_markup=list(chunks(btns, 2))
            + [
                [
                    {"text": "👈 Orqaga", "callback": self.inline__global_config},
                    {"text": "🚫 Yopish", "callback": self.inline__close},
                ]
            ],
        )

    async def inline__global_config(
        self, call: Union[Message, CallbackQuery]
    ) -> None:  # noqa
        to_config = [
            mod.strings("name")
            for mod in self.allmodules.modules
            if hasattr(mod, "config") and mod.strings("name") not in blacklist
        ]
        kb = []
        for mod_row in chunks(to_config, 3):
            row = [
                {"text": btn, "callback": self.inline__configure, "args": (btn,)}
                for btn in mod_row
            ]
            kb += [row]

        kb += [[{"text": "🚫 Yopish", "callback": self.inline__close}]]

        if isinstance(call, Message):
            await self.inline.form(
                self.strings("configure"), reply_markup=kb, message=call
            )
        else:
            await call.edit(self.strings("configure"), reply_markup=kb)

    async def configcmd(self, message: Message) -> None:
        """Modullarni sozlash"""
        await self.inline__global_config(message)

    async def watcher(self, message: Message) -> None:
        if (
            not getattr(message, "out", False)
            or not getattr(message, "via_bot_id", False)
            or message.via_bot_id != self._bot_id
            or "This message is gonna be deleted..."
            not in getattr(message, "raw_text", "")
        ):
            return

        await message.delete()
