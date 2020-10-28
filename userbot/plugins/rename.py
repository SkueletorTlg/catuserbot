import asyncio
import os
import time
from datetime import datetime

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import progress

thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "thumb_image.jpg"


@borg.on(admin_cmd(pattern="rename (.*)"))
@borg.on(sudo_cmd(pattern="rename (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    catevent = await edit_or_reply(
        event,
        "`Cambio de nombre en proceso 🙄🙇‍♂️🙇‍♂️🙇‍♀️ Puede llevar algo de tiempo si el tamaño del archivo es grande...`",
    )
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        c_time = time.time()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await event.client.download_media(
            reply_message,
            downloaded_file_name,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, catevent, c_time, "Intentado descargar", file_name)
            ),
        )
        end = datetime.now()
        ms = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            await catevent.edit(
                f"**Archivo descargado en {ms} segundos.**\n**Localización del archivo : **`{downloaded_file_name}`"
            )
        else:
            await catevent.edit("Se produjo un error\n {}".format(input_str))
    else:
        await catevent.edit(
            "**Syntax : ** `.rename file.name` como respuesta a un archivo de Telegram"
        )


@borg.on(admin_cmd(pattern="rnup (.*)"))
@borg.on(sudo_cmd(pattern="rnup (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    catevent = await edit_or_reply(
        event,
        "`Cambiar el nombre y subir en proceso 🙄🙇‍♂️🙇‍♂️🙇‍♀️ Puede llevar algo de tiempo si el tamaño del archivo es grande.`",
    )
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        c_time = time.time()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await borg.download_media(
            reply_message,
            downloaded_file_name,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, catevent, c_time, "Intentado descargar", file_name)
            ),
        )
        end = datetime.now()
        ms_one = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            c_time = time.time()
            caat = await event.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                reply_to=event.message.id,
                thumb=thumb,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d, t, event, c_time, "Intentando subir", downloaded_file_name
                    )
                ),
            )
            end_two = datetime.now()
            os.remove(downloaded_file_name)
            ms_two = (end_two - end).seconds
            await catevent.edit(
                f"`Archivo descargado en {ms_one} segundos.`\n`Subido en {ms_two} segundos.`"
            )
            await asyncio.sleep(3)
            await catevent.delete()
        else:
            await catevent.edit("Archivo no encontrado {}".format(input_str))
    else:
        await catevent.edit(
            "**Syntax : **`.rnupload file.name` as reply to a Telegram media"
        )
