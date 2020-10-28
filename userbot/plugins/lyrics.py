# credits to @mrconfused (@sandy1709)
import io
import os

import lyricsgenius
from tswift import Song

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP

GENIUS = os.environ.get("GENIUS_API_TOKEN", None)


@bot.on(admin_cmd(outgoing=True, pattern="lyrics ?(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="lyrics ?(.*)"))
async def _(event):
    catevent = await edit_or_reply(event, "Hola... Soy el buscador de letras de canciones....`")
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply.text:
        query = reply.message
    else:
        await catevent.edit("`Lo que se supone que debo encontrar `")
        return
    song = ""
    song = Song.find_song(query)
    if song:
        if song.lyrics:
            reply = song.format()
        else:
            reply = "¡No se pudo encontrar la letra de esa canción! intente con el nombre del artista junto con la canción si aún no funciona intente `.glyrics`"
    else:
        reply = "¡Letra no encontrada! intente con el nombre del artista junto con la canción si aún no funciona intente `.glyrics`"
    if len(reply) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(reply)) as out_file:
            out_file.name = "lyrics.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=query,
                reply_to=reply_to_id,
            )
            await catevent.delete()
    else:
        await catevent.edit(reply)


@bot.on(admin_cmd(outgoing=True, pattern="glyrics ?(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="glyrics ?(.*)"))
async def lyrics(lyric):
    if lyric.pattern_match.group(1):
        query = lyric.pattern_match.group(1)
    else:
        await edit_or_reply(
            lyric,
            "Error: por favor use '-' como divisor de <artista> y <canción> \ejemplo: `.glyrics Alan Walker - Faded`",
        )
        return
    if r"-" not in query:
        await edit_or_reply(
            lyric,
            "Error: por favor use '-' como divisor de <artista> y <canción> \ejemplo: `.glyrics Alan Walker - Faded`",
        )
        return
    if GENIUS is None:
        await edit_or_reply(
            lyric,
            "`¡Proporcione el token de acceso genial a config.py o Heroku Var primero kthxbye!`",
        )
    else:
        genius = lyricsgenius.Genius(GENIUS)
        try:
            args = query.split("-", 1)
            artist = args[0].strip(" ")
            song = args[1].strip(" ")
        except Exception as e:
            await edit_or_reply(lyric, f"Error:\n`{e}`")
            return
    if len(args) < 1:
        await edit_or_reply(lyric, "`Proporciona el nombre del artista y la canción.`")
        return
    catevent = await edit_or_reply(
        lyric, f"`Buscando letras para {artist} - {song}...`"
    )
    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None
    if songs is None:
        await catevent.edit(f"Canción **{artist} - {song}** ¡No encontrada!")
        return
    if len(songs.lyrics) > 4096:
        await catevent.edit("`La letra es demasiado grande, mira el archivo para verlo.`")
        with open("lyrics.txt", "w+") as f:
            f.write(f"Search query: \n{artist} - {song}\n\n{songs.lyrics}")
        await lyric.client.send_file(
            lyric.chat_id,
            "lyrics.txt",
            reply_to=lyric.id,
        )
        os.remove("lyrics.txt")
    else:
        await catevent.edit(
            f"**Consulta de busqueda**: \n`{artist} - {song}`\n\n```{songs.lyrics}```"
        )
    return


CMD_HELP.update(
    {
        "lyrics": "__**PLUGIN NAME :** Lyrics__\
    \n\n📌** CMD ➥** `.lyrics` <aritst name - song nane> or `.lyrics` <song_name>\
    \n**USAGE   ➥  **Searches a song lyrics and sends you if song name doesnt work try along with artisyt name\
    \n\n📌** CMD ➥** `.glyrics <artist name> - <song name>`\
    \n**USAGE   ➥  **Searches a song lyrics and sends you.\
    \n__**Note**__: **-** is neccessary when searching the lyrics to divided artist and song\
    \n\n**Genius lyrics plugin**\
    \nget this value from [Here](https://genius.com/developers)\
    \nAdd var `GENIUS_API_TOKEN` and token value in heroku app settings."
    }
)
