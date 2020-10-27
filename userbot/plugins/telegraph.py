# telegraph utils for catuserbot

import os
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import ALIVE_NAME, BOTLOG, BOTLOG_CHATID, CMD_HELP

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
USERNAME = str(Config.LIVE_USERNAME) if Config.LIVE_USERNAME else "@DKzippO"

telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


@borg.on(admin_cmd(pattern="telegraph (media|text) ?(.*)"))
@borg.on(sudo_cmd(pattern="telegraph (media|text) ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    catevent = await edit_or_reply(event, "`procesando........`")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if BOTLOG:
        await borg.send_message(
            BOTLOG_CHATID,
            "Se creó una nueva cuenta de Telegraph {} para la sesión actual. \n**No le dé esta URL a nadie, ¡incluso si dice que es de Telegram!**".format(
                auth_url
            ),
        )
    optional_title = event.pattern_match.group(2)
    if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str == "media":
            downloaded_file_name = await borg.download_media(
                r_message, Config.TMP_DOWNLOAD_DIRECTORY
            )
            end = datetime.now()
            ms = (end - start).seconds
            await catevent.edit(
                "Descargado a {} en {} segundos.".format(downloaded_file_name, ms),
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await catevent.edit("**Error : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                media_urls = upload_file(downloaded_file_name)
                jisan = "https://telegra.ph{}".format(media_urls[0])
                os.remove(downloaded_file_name)
                await catevent.edit(
                    f"**__➥ Subido a :-__ [Telegraph]**({jisan})\
                    \n__**➥ Subido en {ms + ms_two} segundos .**__\n__**➥ Subido por :-**__ [{DEFAULTUSER}]({USERNAME})",
                    link_preview=True,
                )
        elif input_str == "text":
            user_object = await borg.get_entity(r_message.from_id)
            title_of_page = user_object.first_name  # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            if optional_title:
                title_of_page = optional_title
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await borg.download_media(
                    r_message, Config.TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(title_of_page, html_content=page_content)
            end = datetime.now()
            ms = (end - start).seconds
            cat = f"https://telegra.ph/{response['path']}"
            await catevent.edit(
                f"**__➥ Pegado a :-__ [Telegraph]**({cat})\
                \n__**➥ Pegado en {ms} segundos .**__",
                link_preview=True,
            )
    else:
        await catevent.edit(
            "`Responde a un mensaje para obtener un enlace telegra.ph permanente. (Inspired by @DKzippO)`",
        )


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


CMD_HELP.update(
    {
        "telegraph": "__**PLUGIN NAME :** Telegraph__\
     \n\n📌** CMD ➥** `.telegraph media`\
     \n**USAGE   ➥  **Responda a cualquier imagen o video para subirlo a Telegraph (el video debe tener menos de 5mb)\
     \n\n📌** CMD ➥** `.telegraph text`\
     \n**USAGE   ➥  **Responda a cualquier archivo de texto o cualquier mensaje para pegarlo en telegraph\
    "
    }
)
