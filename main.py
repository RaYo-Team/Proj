from pyrogram import Client, filters as ay
from yt_dlp import YoutubeDL
from requests import get
from youtube_search import YoutubeSearch
import os, wget
from pyrogram.types import (
   InlineKeyboardMarkup,
   InlineKeyboardButton,
   InlineQuery,
   InlineQueryResultArticle,
   InputTextMessageContent,
)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
token = os.environ.get("TOKEN")

app = Client("yt", bot_token=token, api_id = api_id, api_hash = api_hash)

Sudo_id = '1390519416'
@app.on_message(ay.command("start"))
async def start(client, message):
   await message.reply_text(
      "๐ ุฃููุงู ุจู ุนุฒูุฒู ุ ๐ค\nโซ๏ธ ูู ุจูุช ุชุญููู ูู Youtube ๐๐ป.\nโซ๏ธ ุงุฑุณู ุฑุงุจุท ุงููุฏูู ูุชุญูููู ุจุตูุบู ููุฏูู ุงู ููู ุตูุชู ุงู ููุฏูู โน๏ธ.\nโซ๏ธ ุงู ุฃุฑุณู ุจุญุซ ุงููุต ููุง ูุซุงู ุจุญุซ ููุชููุจ ๐.",
      reply_markup=InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton("Serรธ โ Bots Service", url=f"https://t.me/SeroBots"),
               InlineKeyboardButton("", url=f"https://t.me/YDDCJ"),
            ]
         ]
      )
   )
   await client.send_message(chat_id=Sudo_id,text=f"ุงูุนุถู : {message.from_user.mention()}\nุถุบุท start ูู ุจูุชู\nุงูุงูุฏู : `{message.from_user.id}`")

@app.on_message(ay.regex(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"))
async def ytdl(client, message):
   await message.reply_text(
      f"ุชู ุงูุญุตูู ุนูู ุจูุงูุงุช ุงูููุฏูู ุจูุฌุงุญ ุฑุงุจุท ุงูููุทุน ุ  {message.text}\n ููู ุชุฑูุฏ ุชุญููู ุงูููุฏูู ุ ๐จ",disable_web_page_preview=True,
      reply_markup=InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton("โข ุชุญููู ุตูุช ๐", callback_data="audio"),
               InlineKeyboardButton("โข ุชุญููู ููุฏูู ๐บ", callback_data="video"),
            ]
         ]
      )
   )

@app.on_callback_query(ay.regex("video"))
async def VideoDownLoad(client, callback_query):
   await callback_query.edit_message_text("โณ")
   try:
      url = callback_query.message.text.split(' : ',1)[1]
      with YoutubeDL(video) as ytdl:
         await callback_query.edit_message_text("โข ุชู ุงุฑุณุงู ุงูุทูุจ ููุชุธุฑ ุงูุงุณุชุฌุงุจู.")
         ytdl_data = ytdl.extract_info(url, download=True)
         video_file = ytdl.prepare_filename(ytdl_data)
   except Exception as e:
      await client.send_message(chat_id=Sudo_id,text=e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text("โข ูุชู ุงูุชุญููู ุนูู ุงูุณูุฑูุฑ ุ ๐ก")
   await client.send_video(
            callback_query.message.chat.id,
            video=video_file,
            duration=int(ytdl_data["duration"]),
            file_name=str(ytdl_data["title"]),
            supports_streaming=True,
            caption=f"[{ytdl_data['title']}]({url})"
        )
   await callback_query.edit_message_text("โข ุชู ุงุฑุณุงู ุงูููุทุน ุจูุฌุงุญ ุ โ")
   os.remove(video_file)

@app.on_callback_query(ay.regex("audio"))
async def AudioDownLoad(client, callback_query):
   await callback_query.edit_message_text("โณ")
   try:
      url = callback_query.message.text.split(' : ',1)[1]
      with YoutubeDL(audio) as ytdl:
         await callback_query.edit_message_text("โข ุชู ุงุฑุณุงู ุงูุทูุจ ููุชุธุฑ ุงูุงุณุชุฌุงุจู.")
         ytdl_data = ytdl.extract_info(url, download=True)
         audio_file = ytdl.prepare_filename(ytdl_data)
         thumb = wget.download(f"https://img.youtube.com/vi/{ytdl_data['id']}/hqdefault.jpg")
   except Exception as e:
      await client.send_message(chat_id=Sudo_id,text=e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text("ูุชู ุงูุชุญููู ุนูู ุงูุณูุฑูุฑ ุ ๐ก")
   await client.send_audio(
      callback_query.message.chat.id,
      audio=audio_file,
      duration=int(ytdl_data["duration"]),
      title=str(ytdl_data["title"]),
      performer=str(ytdl_data["uploader"]),
      file_name=str(ytdl_data["title"]),
      thumb=thumb,
      caption=f"[{ytdl_data['title']}]({url})"
   )
   await callback_query.edit_message_text("โข ุชู ุงุฑุณุงู ุงูููุทุน ุงูุตูุชู ุจูุฌุงุญ ุ โ")
   os.remove(audio_file)
   os.remove(thumb)


@app.on_message(ay.command("ุจุญุซ",None))
async def search(client, message):
    try:
        query = message.text.split(None, 1)[1]
        if not query:
            await message.reply_text("")
            return

        m = await message.reply_text("- ูุชู ุงูุจุญุซ ุงูุชุถุฑ ููููุง ุ ๐")
        results = YoutubeSearch(query, max_results=5).to_dict()
        i = 0
        text = ""
        while i < 5:
            i += 1
            text += f"๐ฌ : {results[i]['title']}\n"
            text += f"๐ค {results[i]['channel']}\n"
            text += f"๐ {results[i]['duration']} - ๐ {results[i]['views']}\n"
            text += f"๐ https://www.youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ููุงู ุงูุจูุช", url="https://t.me/YDDCJ")]]), disable_web_page_preview=True)
    except Exception as e:
        await m.edit(str(e))

@app.on_inline_query()
async def inline(client, query: InlineQuery):
    answers = []
    search_query = query.query.lower().strip().rstrip()

    if search_query == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text="- ุงูุชุจ ุงู ุดู ููุจุญุซ ุนูู ูู ุงูููุชููุจ ุ โน",
            switch_pm_parameter="help",
            cache_time=0,
        )
    else:
        results = YoutubeSearch(search_query).to_dict()
        for result in results:
         answers.append(
               InlineQueryResultArticle(
                  title=result["title"],
                  description="{}, {} views.".format(
                     result["duration"], result["views"]
                  ),
                  input_message_content=InputTextMessageContent(
                     "https://www.youtube.com/watch?v={}".format(result["id"])
                  ),
                  thumb_url=result["thumbnails"][0],
               )
         )
        
        try:
            await query.answer(results=answers, cache_time=0)
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Error: search timed out",
                switch_pm_parameter="",
            )
            
video = {"format": "best","keepvideo": True,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.%(ext)s","quite": True}
audio = {"format": "bestaudio","keepvideo": False,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.mp3","quite": True}

print("Done Start The bot")
app.run()