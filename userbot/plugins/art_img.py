"""
Created by @Jisan7509
plugin for Cat_Userbot
☝☝☝
You remove this, you gay.
"""

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import ALIVE_NAME, CMD_HELP

from ..utils import admin_cmd, edit_or_reply, sudo_cmd

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
USERNAME = str(Config.LIVE_USERNAME) if Config.LIVE_USERNAME else "@Jisan7509"


@bot.on(admin_cmd("ascii ?(.*)"))
@bot.on(sudo_cmd(pattern="ascii ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "```Responder a cualquier mensaje de usuario.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "```Responder al archivo```")
        return
    chat = "@asciiart_bot"
    reply_message.sender
    if reply_message.sender.bot:
        await edit_or_reply(event, "```Responder al actual mensaje del usuario.```")
        return
    kakashi = await edit_or_reply(event, "```Espere, creando código ASCII...```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=164766745)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await kakashi.edit(
                "```Por favor inicie el bot @asciiart_bot e intente otra vez.```"
            )
            return
        if response.text.startswith("Forward"):
            await kakashi.edit(
                "```¿Puede deshabilitar la configuración de privacidad hacia adelante para siempre?```"
            )
        else:
            await kakashi.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
                caption=f"**➥ Imagen Tipo :** ASCII Arte\n**➥ Subido por:** [{DEFAULTUSER}]({USERNAME})",
            )
            await event.client.send_read_acknowledge(conv.chat_id)


@borg.on(admin_cmd(pattern="line ?(.*)"))
@bot.on(sudo_cmd(pattern="line ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "```Responder a cualquier mensaje de usuario.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "```Responder al archivo```")
        return
    chat = "@Lines50Bot"
    reply_message.sender
    if reply_message.sender.bot:
        await edit_or_reply(event, "```Responder al actual mensaje del usuario.```")
        return
    kakashi = await edit_or_reply(event, "```Procesando```")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(reply_message)
            await conv.get_response()
            pic = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await kakashi.edit(
                "```Por favor, inicie el bot @Lines50Bot e intente de nuevo.```"
            )
            return
        await kakashi.delete()
        await event.client.send_file(
            event.chat_id,
            pic,
            caption=f"**➥ Imagen Tipo :** LINE Arte \n**➥ Subido por:** [{DEFAULTUSER}]({USERNAME})",
        )


CMD_HELP.update(
    {
        "art_img": "__**PLUGIN NAME :** Art Image__\
      \n\n📌** CMD ➥** `.ascii` reply to any image file:\
      \n**USAGE   ➥  **Makes an image ascii style, try out your own.\
      \n\n📌** CMD ➥** `.line` reply to any image file:\
      \n**USAGE   ➥  **Makes an image line style.\ "
    }
)
