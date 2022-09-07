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
      "📑 أهلاً بك عزيزي ؛ 👤\n▫️ في بوت تحميل من Youtube 👋🏻.\n▫️ ارسل رابط الفديو لتحميله بصيغه فيديو او ملف صوتي او فيديو ℹ️.\n▫️ او أرسل بحث النص هنا مثال بحث يوتيوب 📄.",
      reply_markup=InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton("Serø ⁞ Bots Service", url=f"https://t.me/SeroBots"),
               InlineKeyboardButton("", url=f"https://t.me/YDDCJ"),
            ]
         ]
      )
   )
   await client.send_message(chat_id=Sudo_id,text=f"العضو : {message.from_user.mention()}\nضغط start في بوتك\nالايدي : `{message.from_user.id}`")

@app.on_message(ay.regex(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"))
async def ytdl(client, message):
   await message.reply_text(
      f"تم الحصول علي بيانات الفيديو بنجاح رابط المقطع ؛  {message.text}\n كيف تريد تحميل الفيديو ؛ 🖨",disable_web_page_preview=True,
      reply_markup=InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton("• تحميل صوت 🔈", callback_data="audio"),
               InlineKeyboardButton("• تحميل فيديو 📺", callback_data="video"),
            ]
         ]
      )
   )

@app.on_callback_query(ay.regex("video"))
async def VideoDownLoad(client, callback_query):
   await callback_query.edit_message_text("⏳")
   try:
      url = callback_query.message.text.split(' : ',1)[1]
      with YoutubeDL(video) as ytdl:
         await callback_query.edit_message_text("• تم ارسال الطلب ننتظر الاستجابه.")
         ytdl_data = ytdl.extract_info(url, download=True)
         video_file = ytdl.prepare_filename(ytdl_data)
   except Exception as e:
      await client.send_message(chat_id=Sudo_id,text=e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text("• يتم التحميل علي السيرفر ؛ 📡")
   await client.send_video(
            callback_query.message.chat.id,
            video=video_file,
            duration=int(ytdl_data["duration"]),
            file_name=str(ytdl_data["title"]),
            supports_streaming=True,
            caption=f"[{ytdl_data['title']}]({url})"
        )
   await callback_query.edit_message_text("• تم ارسال المقطع بنجاح ؛ ✅")
   os.remove(video_file)

@app.on_callback_query(ay.regex("audio"))
async def AudioDownLoad(client, callback_query):
   await callback_query.edit_message_text("⏳")
   try:
      url = callback_query.message.text.split(' : ',1)[1]
      with YoutubeDL(audio) as ytdl:
         await callback_query.edit_message_text("• تم ارسال الطلب ننتظر الاستجابه.")
         ytdl_data = ytdl.extract_info(url, download=True)
         audio_file = ytdl.prepare_filename(ytdl_data)
         thumb = wget.download(f"https://img.youtube.com/vi/{ytdl_data['id']}/hqdefault.jpg")
   except Exception as e:
      await client.send_message(chat_id=Sudo_id,text=e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text("يتم التحميل علي السيرفر ؛ 📡")
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
   await callback_query.edit_message_text("• تم ارسال المقطع الصوتي بنجاح ؛ ✅")
   os.remove(audio_file)
   os.remove(thumb)


@app.on_message(ay.command("بحث",None))
async def search(client, message):
    try:
        query = message.text.split(None, 1)[1]
        if not query:
            await message.reply_text("")
            return

        m = await message.reply_text("- يتم البحث انتضر قليلا ؛ 🔄")
        results = YoutubeSearch(query, max_results=5).to_dict()
        i = 0
        text = ""
        while i < 5:
            i += 1
            text += f"🎬 : {results[i]['title']}\n"
            text += f"👤 {results[i]['channel']}\n"
            text += f"🕑 {results[i]['duration']} - 👁 {results[i]['views']}\n"
            text += f"🌐 https://www.youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("قناه البوت", url="https://t.me/YDDCJ")]]), disable_web_page_preview=True)
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
            switch_pm_text="- اكتب اي شي للبحث عنه في اليوتيوب ؛ ℹ",
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