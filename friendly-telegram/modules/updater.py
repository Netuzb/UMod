import asyncio
import atexit
import functools
import logging
import os
import subprocess
import sys
import uuid
import telethon

import git
from git import Repo, GitCommandError
from telethon.tl.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class UpdaterMod(loader.Module):
    """Updates itself"""

    strings = {
        "name": "4.UModYangilash",
        "source": "<b>Manzil mavjud emas</b> <a href='{}'></a>",
        "restarting_caption": "🥷 <b>Baza qayta ishga tushmoqda...</b>",
        "downloading": "🥷 <b>Yangilanish yuklanmoqda...</b>",
        "downloaded": "🥷 <b>Muvaffaqiyatli yuklandi.\n├╴╴╴╴╴╴╴╴╴╴\n└ 👾 Endi</b> <code>.restart</code> <b>qo'llang.</b>",
        "already_updated": "🥷 <b>Muvaffaqiyatli yangilandi!</b>",
        "installing": "🥷 <b>Yangilanish oʻrnatilmoqda...</b>",
        "success": "🥷 <b>Muvaffaqiyatli yakunlandi!\n├╴╴╴╴╴╴╴╴╴╴\n└ 👾 Maʼlumot uchun: <code>.ftgver</code></b>",
        "heroku_warning": "📖 <b>Heroku Api token xatoligi. </b>Update was successful but updates will reset every time the bot restarts.",
        "origin_cfg_doc": "1234567890qweryeiwiskmsmsmsksmsmmsmd?",
        "lavhost": "📖 <b>Odam.</b>\n<i>This message <b>will not</b> be edited after restart is complete!</i>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "GIT_ORIGIN_URL",
            "https://github.com/Netuzb/UMod",
            lambda m: self.strings("origin_cfg_doc", m),
        )

    @loader.owner
    async def restartcmd(self, message: Message) -> None:
        """Qayta ishga tushirish"""
        if os.environ.get("LAVHOST"):
            await utils.answer(message, self.strings("lavhost"))
            await self._client.send_message("@lavhostbot", "/restart")
            return

        msg = (
            await utils.answer(message, self.strings("restarting_caption", message))
        )[0]
        await self.restart_common(msg)

    async def prerestart_common(self, message: Message) -> None:
        logger.debug(f"Self-update. {sys.executable} -m {utils.get_base_dir()}")

        check = str(uuid.uuid4())
        await self._db.set(__name__, "selfupdatecheck", check)
        await asyncio.sleep(3)
        if self._db.get(__name__, "selfupdatecheck", "") != check:
            raise ValueError("An update is already in progress!")
        self._db.set(__name__, "selfupdatechat", utils.get_chat_id(message))
        await self._db.set(__name__, "selfupdatemsg", message.id)

    async def restart_common(self, message: Message) -> None:
        await self.prerestart_common(message)
        atexit.register(functools.partial(restart, *sys.argv[1:]))
        [handler] = logging.getLogger().handlers
        handler.setLevel(logging.CRITICAL)
        for client in self.allclients:
            # Terminate main loop of all running clients
            # Won't work if not all clients are ready
            if client is not message.client:
                await client.disconnect()
        await message.client.disconnect()

    @loader.owner
    async def yangilashcmd(self, message: Message) -> None:
        """Yangilanish yuklash"""
        message = await utils.answer(message, self.strings("downloading", message))
        await self.download_common()
        await utils.answer(message, self.strings("downloaded", message))
        await self.allmodules.commands["restart"](await utils.answer(message, "_"))

    async def download_common(self):
        try:
            repo = Repo(os.path.dirname(utils.get_base_dir()))
            origin = repo.remote("origin")
            r = origin.pull()
            new_commit = repo.head.commit
            for info in r:
                if info.old_commit:
                    for d in new_commit.diff(info.old_commit):
                        if d.b_path == "requirements.txt":
                            return True
            return False
        except git.exc.InvalidGitRepositoryError:
            repo = Repo.init(os.path.dirname(utils.get_base_dir()))
            origin = repo.create_remote("origin", self.config["GIT_ORIGIN_URL"])
            origin.fetch()
            repo.create_head("master", origin.refs.master)
            repo.heads.master.set_tracking_branch(origin.refs.master)
            repo.heads.master.checkout(True)
            return (
                False  # Heroku never needs to install dependencies because we redeploy
            )

    @staticmethod
    def req_common() -> None:
        # Now we have downloaded new code, install requirements
        logger.debug("Installing new requirements...")
        try:
            subprocess.run(  # skipcq: PYL-W1510
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    os.path.join(
                        os.path.dirname(utils.get_base_dir()), "requirements.txt"
                    ),
                    "--user",
                ]
            )

        except subprocess.CalledProcessError:
            logger.exception("Req install failed")

    @loader.owner
    async def cmd(self, message: Message, hard: bool = False) -> None:
        """..."""
        if os.environ.get("LAVHOST"):
            await utils.answer(message, self.strings("lavhost"))
            await self._client.send_message("@lavhostbot", "/update")
            return

        # We don't really care about asyncio at this point, as we are shutting down
        if hard:
            os.system(f"cd {utils.get_base_dir()} && cd .. && git reset --hard HEAD")  # skipcq: BAN-B605

        try:
            try:
                msgs = await utils.answer(message, self.strings("downloading", message))
            except telethon.errors.rpcerrorlist.MessageNotModifiedError:
                pass

            req_update = await self.download_common()

            try:
                message = (
                    await utils.answer(msgs, self.strings("installing", message))
                )[0]
            except telethon.errors.rpcerrorlist.MessageNotModifiedError:
                pass

            if heroku_key := os.environ.get("heroku_api_token"):
                from .. import heroku

                await self.prerestart_common(message)
                heroku.publish(self.allclients, heroku_key)
                # If we pushed, this won't return. If the push failed, we will get thrown at.
                # So this only happens when remote is already up to date (remote is heroku, where we are running)
                self._db.set(__name__, "selfupdatechat", None)
                self._db.set(__name__, "selfupdatemsg", None)

                await utils.answer(message, self.strings("already_updated", message))
            else:
                if req_update:
                    self.req_common()
                await self.restart_common(message)
        except GitCommandError:
            await self.updatecmd(message, True)

    @loader.unrestricted
    async def cmd(self, message: Message) -> None:
        """Links the source code of this project"""
        await utils.answer(
            message,
            self.strings("source", message).format(self.config["GIT_ORIGIN_URL"]),
        )

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()
        self._client = client

        if (
            db.get(__name__, "selfupdatechat") is not None
            and db.get(__name__, "selfupdatemsg") is not None
        ):
            try:
                await self.update_complete(client)
            except Exception:
                logger.exception("Failed to complete update!")

        self._db.set(__name__, "selfupdatechat", None)
        self._db.set(__name__, "selfupdatemsg", None)

    async def update_complete(self, client):
        logger.debug("Self update successful! Edit message")
        heroku_key = os.environ.get("heroku_api_token")
        herokufail = ("DYNO" in os.environ) and (heroku_key is None)

        if herokufail:
            logger.warning("heroku token not set")
            msg = self.strings("heroku_warning")
        else:
            logger.debug("Self update successful! Edit message")
            msg = self.strings("success")

        await client.edit_message(
            self._db.get(__name__, "selfupdatechat"),
            self._db.get(__name__, "selfupdatemsg"),
            msg,
        )


def restart(*argv):
    os.execl(  # skipcq: BAN-B606
        sys.executable,  # skipcq: BAN-B606
        sys.executable,  # skipcq: BAN-B606
        "-m",  # skipcq: BAN-B606
        os.path.relpath(utils.get_base_dir()),  # skipcq: BAN-B606
        *argv,  # skipcq: BAN-B606
    )  # skipcq: BAN-B606
