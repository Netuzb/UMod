import io, inspect
from .. import loader, utils


@loader.tds
class ModulesLinkMod(loader.Module):
    """Modulni yuklash"""

    strings = {"name": "Modullar"}

    async def mlcmd(self, message):
        """modul faylini olish"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "📖 <b>Arglar yo'q</b>")

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
                text = f"<b>📖 {utils.escape_html(f)}</b>"
            else:
                text = f'📖 <b>Modul manzili: <a href="{link}">bu yerda</a>\n📖 {utils.escape_html(f)}</b> <a href="{link}"></a>'

            out = io.BytesIO(r.__loader__.data)
            out.name = f"{f}.py"
            out.seek(0)

            await message.respond(text, file=out)

            if message.out:
                await message.delete()
        except:
            await utils.answer(message, "📖 <b>Modul topilmadi</b>")
