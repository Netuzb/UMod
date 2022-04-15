import io, inspect
from .. import loader, utils


@loader.tds
class ModulesLinkMod(loader.Module):
    """ ModulesLink [mod by #umodules]

🇺🇲 • Retrieves already installed modules' links
🇺🇿 • Oʻrnatilgan modullarning havolalarini osongina olish"""

    strings = {"name": "ModulesLink [mod by #umodules]"}

    async def mlcmd(self, message):
        """🇺🇲 • Metod of sending file in EN language"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "🚫 <b>No args</b>")

        try:
            f = " ".join(
                [
                    x.strings["name"]
                    for x in self.allmodules.modules
                    if args.lower() == x.strings["name"].lower()
                ]
            )
            r = inspect.getmodule(
                next(
                    filter(
                        lambda x: args.lower() == x.strings["name"].lower(),
                        self.allmodules.modules,
                    )
                )
            )

            link = str(r).split("(")[1].split(")")[0]
            if "http" not in link:
                text = f"<b>🇺🇲 • {utils.escape_html(f)}</b>"
            else:
                text = f'🇺🇲 • <b><a href="{link}">Link</a> – {utils.escape_html(f)}</b> <a href="{link}"></a>'

            out = io.BytesIO(r.__loader__.data)
            out.name = f"{f}.py"
            out.seek(0)

            await message.respond(text, file=out)

            if message.out:
                await message.delete()
        except:
            await utils.answer(message, "😔 <b>Module not found</b>")

# ----------------------------------------------------#
# uzbek language mod by @netuzb
# ----------------------------------------------------#

    async def mluzcmd(self, message):
        """🇺🇿 • Modul faylini yuboruvchi metod UZ tilida"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "🚫 <b>Arglar yo'q</b>")

        try:
            f = " ".join(
                [
                    x.strings["name"]
                    for x in self.allmodules.modules
                    if args.lower() == x.strings["name"].lower()
                ]
            )
            r = inspect.getmodule(
                next(
                    filter(
                        lambda x: args.lower() == x.strings["name"].lower(),
                        self.allmodules.modules,
                    )
                )
            )

            link = str(r).split("(")[1].split(")")[0]
            if "http" not in link:
                text = f"<b>🇺🇿 • {utils.escape_html(f)}</b>"
            else:
                text = f'🇺🇿 • <b><a href="{link}">Havola</a> – {utils.escape_html(f)}</b> <a href="{link}"></a>'

            out = io.BytesIO(r.__loader__.data)
            out.name = f"{f}.py"
            out.seek(0)

            await message.respond(text, file=out)

            if message.out:
                await message.delete()
        except:
            await utils.answer(message, "😔 <b>Modul topilmadi</b>")
