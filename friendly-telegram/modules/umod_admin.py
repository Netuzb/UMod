# meta pic: https://img.icons8.com/stickers/100/000000/enter-pin.png
# scope: inline

from types import FunctionType
from typing import List, Union
from telethon.tl.types import Message, User, PeerUser
from .. import loader, utils, main, security
from telethon.utils import get_display_name

import logging
import aiogram
from ..security import (
    OWNER,
    SUDO,
    SUPPORT,
    GROUP_OWNER,
    GROUP_ADMIN_ADD_ADMINS,
    GROUP_ADMIN_CHANGE_INFO,
    GROUP_ADMIN_BAN_USERS,
    GROUP_ADMIN_DELETE_MESSAGES,
    GROUP_ADMIN_PIN_MESSAGES,
    GROUP_ADMIN_INVITE_USERS,
    GROUP_ADMIN,
    GROUP_MEMBER,
    PM,
    DEFAULT_PERMISSIONS,
)

logger = logging.getLogger(__name__)


def chunks(lst: list, n: int) -> List[list]:
    return [lst[i : i + n] for i in range(0, len(lst), n)]


@loader.tds
class GeekSecurityMod(loader.Module):
    """Control security settings (geek3.0.8alpha+)"""

    strings = {
        "name": "9.UModAdmin",
        "no_command": "🚫 <b>Buyruq </b><code>{}</code><b> topilmadi!</b>",
        "permissions": "🔐 <b>Bu yerda siz </b><code>{}{}</code> uchun ruxsatlarni sozlashingiz mumkin",
        "close_menu": "🙈 Ushbu menyuni yoping",
        "global": "🔐 <b>Bu yerda siz global chegaralovchi niqobni sozlashingiz mumkin. Agar bu erda ruxsat chiqarib tashlansa, u hamma joyda chiqarib tashlanadi!</b>",
        "owner": "🤴 Egasi",
        "sudo": "🤵 Sudo",
        "support": "💁‍♂️ Qo'llab-quvvatlash",
        "group_owner": "🧛‍♂️ Guruh egasi",
        "group_admin_add_admins": "👨‍💻 Admin (a'zolarni qo'shing)",
        "group_admin_change_info": "👨‍💻 Admin (ma'lumotni o'zgartirish)",
        "group_admin_ban_users": "👨‍💻 Admin (taqiq)",
        "group_admin_delete_messages": "👨‍💻 Admin (xabarlarni o'chirish)",
        "group_admin_pin_messages": "👨‍💻 Admin (pin)",
        "group_admin_invite_users": "👨‍💻 Admin (taklif qiling)",
        "group_admin": "👨‍💻 Admin (har qanday)",
        "group_member": "👥 Guruhda",
        "pm": "🤙 PMda",
        "owner_list": "🤴 <b>Guruhdagi foydalanuvchilar </b><code>egasi</code><b>:</b>\n\n{}",
        "sudo_list": "🤵‍♀️ <b>Guruhdagi foydalanuvchilar </b><code>sudo</code><b>:</b>\n\n{}",
        "support_list": "🙋‍♂️ <b>Guruhdagi foydalanuvchilar </b><code>qo‘llab-quvvatlash</code><b>:</b>\n\n{}",
        "no_owner": "🤴 <b>Guruhda foydalanuvchilar yo'q </b><code>egasi</code>",
        "no_sudo": "🤵‍♀️ <b></b><code>sudo</code> guruhida foydalanuvchilar yo'q",
        "no_support": "🙋‍♂️ <b>Guruhda </b><code>qo‘llab-quvvatlash</code> foydalanuvchilari yo‘q",
        "owner_added": '🤴 <b><a href="tg://user?id={}">{}</a> </b><code>egasi</code> guruhiga qo'shildi',
        "sudo_added": '🤵‍♀️ <b><a href="tg://user?id={}">{}</a> </b><code>sudo</code> guruhiga qo'shildi',
        "support_added": '🙋‍♂️ <b><a href="tg://user?id={}">{}</a> </b><code>qo'llab-quvvatlash</code> guruhiga qo'shildi',
        "owner_removed": '🤴 <b><a href="tg://user?id={}">{}</a> </b><code>egasi</code> guruhidan olib tashlandi',
        "sudo_removed": '🤵‍♀️ <b><a href="tg://user?id={}">{}</a> </b><code>sudo</code> guruhidan olib tashlandi',
        "support_removed": '🙋‍♂️ <b><a href="tg://user?id={}">{}</a> </b><code>qo'llab-quvvatlash</code> guruhidan o'chirildi',
        "no_user": "🚫 <b>Ruxsat berish uchun foydalanuvchini belgilang</b>",
        "not_a_user": "🚫 <b>Belgilangan obyekt foydalanuvchi emas</b>",
        "li": '👾 <b><a href="tg://user?id={}">{}</a></b>',
        "warning": (
            '⚠️ <b>Iltimos, <a href="tg://user?id={}">{}</a> qo‘shmoqchi ekanligingizni tasdiqlang. '
            'guruhlash </b><code>{}</code><b>!\nUshbu harakat shaxsiy ma'lumotlarni ochib berishi va ruxsat berishi mumkin '
            'to'liq yoki qisman bu foydalanuvchiga userbot ruxsati</b>'
        ),
        "cancel": "🚫 Bekor qilish",
        "confirm": "👑 Tasdiqlash",
        "self": "🚫 <b>Siz o'zingizni targ'ib qila olmaysiz/pasaytira olmaysiz!</b>",
        "restart": "<i>🔄 O'zgarishlarni amalga oshirish uchun qayta ishga tushirish talab qilinishi mumkin</i>"
    }

    def get(self, *args) -> dict:
        return self._db.get(self.strings["name"], *args)

    def set(self, *args) -> None:
        return self._db.set(self.strings["name"], *args)

    async def client_ready(self, client, db) -> None:
        self._db = db
        self._client = client
        self.prefix = utils.escape_html(
            (self._db.get(main.__name__, "command_prefix", False) or ".")
        )

        self._me = (await client.get_me()).id
        self._is_geek = hasattr(self, 'inline')

    async def inline__switch_perm(
        self, call: aiogram.types.CallbackQuery, command: str, group: str, level: bool
    ) -> None:
        cmd = self.allmodules.commands[command]
        mask = self._db.get(security.__name__, "masks", {}).get(
            f"{cmd.__module__}.{cmd.__name__}",
            getattr(cmd, "security", security.DEFAULT_PERMISSIONS),
        )

        bit = security.BITMAP[group.upper()]

        if level:
            mask |= bit
        else:
            mask &= ~bit

        masks = self._db.get(security.__name__, "masks", {})
        masks[f"{cmd.__module__}.{cmd.__name__}"] = mask
        self._db.set(security.__name__, "masks", masks)

        await call.answer("Security value set!")
        await call.edit(
            self.strings("permissions").format(self.prefix, command),
            reply_markup=self._build_markup(cmd),
        )

    async def inline__switch_perm_bm(
        self, call: aiogram.types.CallbackQuery, group: str, level: bool
    ) -> None:
        mask = self._db.get(security.__name__, "bounding_mask", DEFAULT_PERMISSIONS)
        bit = security.BITMAP[group.upper()]

        if level:
            mask |= bit
        else:
            mask &= ~bit

        self._db.set(security.__name__, "bounding_mask", mask)

        await call.answer("Bounding mask value set!")
        await call.edit(
            self.strings("global"), reply_markup=self._build_markup_global()
        )

    @staticmethod
    async def inline_close(call: aiogram.types.CallbackQuery) -> None:
        await call.delete()

    def _build_markup(self, command: FunctionType) -> List[List[dict]]:
        perms = self._get_current_perms(command)
        buttons = [
            {
                "text": f"{'✅' agar boshqa darajada bolsa '🚫'} {self.strings[group]}",
                "callback": self.inline__switch_perm,
                "args": (command.__name__[:-3], group, not level),
            }
            for group, level in perms.items()
        ]


        return chunks(buttons, 2) + [
            [{"text": self.strings("close_menu"), "callback": self.inline_close}]
        ]

    def _build_markup_global(self) -> List[List[dict]]:
        perms = self._get_current_bm()
        buttons = [
            {
                "text": f"{'✅' agar boshqa darajada bolsa '🚫'} {self.strings[group]}",
                "callback": self.inline__switch_perm_bm,
                "args": (group, not level),
            }
            for group, level in perms.items()
        ]


        return chunks(buttons, 2) + [
            [{"text": self.strings("close_menu"), "callback": self.inline_close}]
        ]

    def _get_current_bm(self) -> dict:
        return self._perms_map(
            self._db.get(security.__name__, "bounding_mask", DEFAULT_PERMISSIONS)
        )

    @staticmethod
    def _perms_map(perms: int) -> dict:
        return {
            "owner": bool(perms & OWNER),
            "sudo": bool(perms & SUDO),
            "support": bool(perms & SUPPORT),
            "group_owner": bool(perms & GROUP_OWNER),
            "group_admin_add_admins": bool(perms & GROUP_ADMIN_ADD_ADMINS),
            "group_admin_change_info": bool(perms & GROUP_ADMIN_CHANGE_INFO),
            "group_admin_ban_users": bool(perms & GROUP_ADMIN_BAN_USERS),
            "group_admin_delete_messages": bool(perms & GROUP_ADMIN_DELETE_MESSAGES),
            "group_admin_pin_messages": bool(perms & GROUP_ADMIN_PIN_MESSAGES),
            "group_admin_invite_users": bool(perms & GROUP_ADMIN_INVITE_USERS),
            "group_admin": bool(perms & GROUP_ADMIN),
            "group_member": bool(perms & GROUP_MEMBER),
            "pm": bool(perms & PM),
        }

    def _get_current_perms(self, command: FunctionType) -> dict:
        config = self._db.get(security.__name__, "masks", {}).get(
            f"{command.__module__}.{command.__name__}",
            getattr(command, "security", self._client.dispatcher.security._default),  # skipcq: PYL-W0212
        )

        return self._perms_map(config)

    async def cmd(self, message: Message) -> None:
        """[command] - Configure command's security settings"""
        args = utils.get_args_raw(message).lower().strip()
        if args and args not in self.allmodules.commands:
            await utils.answer(message, self.strings("no_command").format(args))
            return

        if not args:
            await self.inline.form(
                self.strings("global"),
                reply_markup=self._build_markup_global(),
                message=message,
                ttl=5 * 60,
            )
            return

        cmd = self.allmodules.commands[args]

        await self.inline.form(
            self.strings("permissions").format(self.prefix, args),
            reply_markup=self._build_markup(cmd),
            message=message,
            ttl=5 * 60,
        )

    async def _resolve_user(self, message: Message) -> None:
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)

        if not args and not reply:
            await utils.answer(message, self.strings("no_user"))
            return

        user = None

        if args:
            try:
                if str(args).isdigit():
                    args = int(args)

                user = await self._client.get_entity(args)
            except Exception:
                pass

        if user is None:
            user = await self._client.get_entity(reply.sender_id)

        if not isinstance(user, (User, PeerUser)):
            await utils.answer(message, self.strings("not_a_user"))
            return

        if user.id == self._me:
            await utils.answer(message, self.strings("self"))
            return

        return user

    async def _add_to_group(
        self,
        message: Union[Message, "aigoram.types.CallbackQuery"],  # noqa: F821
        group: str,
        confirmed: bool = False,
        user: int = None,
    ) -> None:
        if user is None:
            user = await self._resolve_user(message)
            if not user:
                return

        if isinstance(user, int):
            user = await self._client.get_entity(user)

        if self._is_geek and not confirmed:
            await self.inline.form(
                self.strings("warning").format(
                    user.id, utils.escape_html(get_display_name(user)), group
                ),
                message=message,
                ttl=10 * 60,
                reply_markup=[
                    [
                        {
                            "text": self.strings("cancel"),
                            "callback": self.inline_close,
                        },
                        {
                            "text": self.strings("confirm"),
                            "callback": self._add_to_group,
                            "args": (group, True, user.id),
                        },
                    ]
                ],
            )
            return

        self._db.set(
            security.__name__,
            group,
            list(set(self._db.get(security.__name__, group, []) + [user.id])),
        )

        m = self.strings(f"{group}_added").format(
            user.id,
            utils.escape_html(get_display_name(user)),
        )

        if not self._is_geek:
            m += f"\n\n{self.strings('restart')}"

        if isinstance(message, Message):
            await utils.answer(
                message,
                m,
            )
        else:
            await message.edit(m)

    async def _remove_from_group(self, message: Message, group: str) -> None:
        user = await self._resolve_user(message)
        if not user:
            return

        self._db.set(
            security.__name__,
            group,
            list(set(self._db.get(security.__name__, group, [])) - {user.id}),
        )


        m = self.strings(f"{group}_removed").format(
            user.id,
            utils.escape_html(get_display_name(user)),
        )

        if not self._is_geek:
            m += f"\n\n{self.strings('restart')}"

        await utils.answer(
            message,
            m
        )

    async def _list_group(self, message: Message, group: str) -> None:
        _resolved_users = []
        for user in self._db.get(security.__name__, group, []) + ([self._me] if group == "owner" else []):
            try:
                _resolved_users += [await self._client.get_entity(user)]
            except Exception:
                pass

        if _resolved_users:
            await utils.answer(
                message,
                self.strings(f"{group}_list").format(
                    "\n".join(
                        [
                            self.strings("li").format(
                                i.id, utils.escape_html(get_display_name(i))
                            )
                            for i in _resolved_users
                        ]
                    )
                ),
            )
        else:
            await utils.answer(message, self.strings(f"no_{group}"))

    async def cmd(self, message: Message) -> None:
        """<user> - Add user to `sudo`"""
        await self._add_to_group(message, "sudo")

    async def owneraddcmd(self, message: Message) -> None:
        """<user> - Add user to `owner`"""
        await self._add_to_group(message, "owner")

    async def cmd(self, message: Message) -> None:
        """<user> - Add user to `support`"""
        await self._add_to_group(message, "support")

    async def cmd(self, message: Message) -> None:
        """<user> - Remove user from `sudo`"""
        await self._remove_from_group(message, "sudo")

    async def ownerrmcmd(self, message: Message) -> None:
        """<user> - Remove user from `owner`"""
        await self._remove_from_group(message, "owner")

    async def cmd(self, message: Message) -> None:
        """<user> - Remove user from `support`"""
        await self._remove_from_group(message, "support")

    async def cmd(self, message: Message) -> None:
        """List users in `sudo`"""
        await self._list_group(message, "sudo")

    async def ownerlistcmd(self, message: Message) -> None:
        """List users in `owner`"""
        await self._list_group(message, "owner")

    async def cmd(self, message: Message) -> None:
        """List users in `support`"""
        await self._list_group(message, "support")
