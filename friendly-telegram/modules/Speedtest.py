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
import logging
import speedtest
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class SpeedMod(loader.Module):
    """Speedtest.net orqali tezlikni oʻlchash moduli"""
    strings = {"name": "Speedtest",
               "running": "<b>📖 Speedtest ishga tushmoqda...</b>",
               "results": "<b>📖 Speedtest.ru natijasi eʼlon qilindi:\n📖 Tezlik holati:</b> yuqori",
               "results_download": "<b>📃 Yuklash tezligi:</b> {} MB/S",
               "results_upload": "<b>📃 Yuborish tezligi:</b> {} MB/S",
               "results_ping": "<b>📃 Tezlik sifati:</b> {} MS"}

    async def tezlikcmd(self, message):
        """internet tezligini oʻlchash"""
        await utils.answer(message, self.strings("running", message))
        args = utils.get_args(message)
        servers = []
        for server in args:
            try:
                servers += [int(server)]
            except ValueError:
                logger.warning("server failed")
        results = await utils.run_sync(self.speedtest, servers)
        ret = self.strings("results", message) + "\n\n"
        ret += self.strings("results_download", message).format(round(results["download"] / 2**20, 2)) + "\n"
        ret += self.strings("results_upload", message).format(round(results["upload"] / 2**20, 2)) + "\n"
        ret += self.strings("results_ping", message).format(round(results["ping"], 2)) + "\n"
        await utils.answer(message, ret)

    def speedtest(self, servers):
        speedtester = speedtest.Speedtest()
        speedtester.get_servers(servers)
        speedtester.get_best_server()
        speedtester.download(threads=None)
        speedtester.upload(threads=None)
        return speedtester.results.dict()
