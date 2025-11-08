import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from VISHALMUSIC import LOGGER, app, userbot
from VISHALMUSIC.core.call import VISHAL
from VISHALMUSIC.misc import sudo
from VISHALMUSIC.plugins import ALL_MODULES
from VISHALMUSIC.utils.database import get_banned_users, get_gbanned
from VISHALMUSIC.utils.cookie_handler import fetch_and_store_cookies
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("ᴀssɪsᴛᴀɴᴛ sᴇssɪᴏɴ ɴᴏᴛ ғɪʟʟᴇᴅ, ᴘʟᴇᴀsᴇ ғɪʟʟ ᴀ ᴘʏʀᴏɢʀᴀᴍ sᴇssɪᴏɴ...")
        exit()

    # ✅ Try to fetch cookies at startup
    try:
        await fetch_and_store_cookies()
        LOGGER("VISHALMUSIC").info("ʏᴏᴜᴛᴜʙᴇ ᴄᴏᴏᴋɪᴇs ʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅")
    except Exception as e:
        LOGGER("VISHALMUSIC").warning(f"⚠️ ᴄᴏᴏᴋɪᴇ ᴇʀʀᴏʀ: {e}")

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("VISHALMUSIC.plugins" + all_module)

    LOGGER("VISHALMUSIC.plugins").info(" ᴍᴏᴅᴜʟᴇs ʟᴏᴀᴅᴇᴅ...")

    await userbot.start()
    await VISHAL.start()

    try:
        await VISHAL.stream_call("http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4")
    except NoActiveGroupCall:
        LOGGER("VISHALMUSIC").error(
            "ᴘʟᴇᴀsᴇ ᴛᴜʀɴ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴏғ ʏᴏᴜʀ ʟᴏɢ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ.\n\nʙᴏᴛ sᴛᴏᴘᴘᴇᴅ..."
        )
        exit()
    except:
        pass

    await VISHAL.decorators()
    LOGGER("VISHALMUSIC").info(
        "\x41\x6e\x6e\x69\x65\x20\x4d\x75\x73\x69\x63\x20\x52\x6f\x62\x6f\x74\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e\x2e\x2e"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("VISHALMUSIC").info("sᴛᴏᴘᴘɪɴɢ  ᴍᴜsɪᴄ ʙᴏᴛ ...")


if __name__ == "__main__":
    # 🔹 Start the Telegram bot
    asyncio.get_event_loop().run_until_complete(init())

    # 🔹 Keep-Alive Flask Webserver for Render
    from flask import Flask
    import threading
    import os

    app_server = Flask(__name__)

    @app_server.route("/")
    def home():
        return "✅ VishalMusic Bot is Alive and Running!"

    def run():
        port = int(os.getenv("PORT", 8080))
        app_server.run(host="0.0.0.0", port=port)

    threading.Thread(target=run).start()
