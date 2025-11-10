import asyncio
import importlib
import os
from threading import Thread

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

    LOGGER("VISHALMUSIC.plugins").info("ᴍᴏᴅᴜʟᴇs ʟᴏᴀᴅᴇᴅ...")

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
    LOGGER("VISHALMUSIC").info("✅ Vishal music Bot Started Successfully!")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("VISHALMUSIC").info("sᴛᴏᴘᴘɪɴɢ ᴍᴜsɪᴄ ʙᴏᴛ ...")


# ----------------------🔹 Render Flask Keepalive 🔹----------------------

from flask import Flask

def run_flask():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "VISHALMUSIC Bot Running Successfully ✅"

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# ----------------------------------------------------------------------

if __name__ == "__main__":
    keep_alive()  # 🔥 start tiny Flask server for Render
    asyncio.get_event_loop().run_until_complete(init())
