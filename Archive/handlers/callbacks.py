from aiogram import Router, F
import asyncio
from aiogram.filters import Command
from aiogram import types, Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
from datetime import datetime
import aiosqlite
from aiogram.types import CallbackQuery
from database.get_message import edit_message
from database.save_message import *
from config import *
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from API.music import *
from modules.save_data import quote, unquote

router = Router()

bot = Bot(
     token=TOKEN,
     default=DefaultBotProperties(
         parse_mode=ParseMode.HTML))



BOT_USER = "t.me/a999km_muz_bot"

BOT_LINK = "@a999km_muz_bot"

def pagination(
    tracks_list,
    type,
    page=0,
    search=None
):
    if search is not None:
        type = type + "_" + quote(search)
        print(type)
    print(tracks_list)
    tracks_list = list(tracks_list)

    builder = InlineKeyboardBuilder()
    start_offset = page * 9
    end_offset = start_offset + 9
    print(tracks_list[start_offset:end_offset])
    count = 0
    for elem in tracks_list[start_offset:end_offset]:
        count += 1
        if type.startswith("popular"):
            music_id = elem.track["id"]
      
            title = elem.track["title"]
            artist = elem.track["artists"][0]["name"]
        else:
            music_id = elem["id"]
            title = elem["title"]
            artist = elem["artists"][0]["name"]

        builder.row(
            types.InlineKeyboardButton(
                text=f"• {title} - {artist}",
                callback_data=f"music_{music_id}"
            )
        )
    count_pages = len(tracks_list) // 9


    if count < 9:
        builder.row(
            types.InlineKeyboardButton(
                text="←",
                callback_data=f"up_{page - 1}_{type}"
            ),
            types.InlineKeyboardButton(
                text=f"{page + 1}/{count_pages + 1}",
                callback_data="empty"
            ),
            types.InlineKeyboardButton(
                text="•",
                callback_data="empty"
            )
        )
    elif page > 0:
        builder.row(
            types.InlineKeyboardButton(
                text="←",
                callback_data=f"up_{page - 1}_{type}"
            ),
            types.InlineKeyboardButton(
                text=f"{page + 1}/{count_pages + 1}",
                callback_data="empty"
            ),
            types.InlineKeyboardButton(
                text="→",
                callback_data=f"up_{page + 1}_{type}"
            )
        )

    if page <= 0:
        builder.row(
            types.InlineKeyboardButton(
                text="•",
                callback_data="empty"
            ),
            types.InlineKeyboardButton(
                text=f"{page + 1}/{count_pages + 1}",
                callback_data="empty"
            ),
            types.InlineKeyboardButton(
                text="→",
                callback_data=f"up_{page + 1}_{type}"
            )
        )

    
    return builder.as_markup()


@router.callback_query(F.data.startswith("up"))
async def page(
    callback: CallbackQuery
):
    
    split = callback.data.split("_")
    page = split[1]
    type = split[2]
    tracks_list = None
    query = None
    if type == "search":
        query = unquote(split[3])
        query = query.split("+")
        query = " ".join(query)
        category = query
        tracks_list = search_music(query)
        
    elif type == "popular":
        tracks_list = get_popular()
        category = "ПОПУЛЯРНЫЕ"
    elif type == "new":
        category = "НОВИНКИ"
        tracks_list = get_new()
        

    await edit_message(
        text=category,
        chat_id=callback.message.chat.id,
        reply_markup=pagination(
            tracks_list=tracks_list,
            type=type,
            page=int(page),
            search=query
        )
    )

@router.callback_query(F.data == "popular")
async def popular_music(
    callback: CallbackQuery
):

    result = get_popular()

    send_message = await bot.send_message(
        chat_id=callback.message.chat.id,
        text="ПОПУЛЯРНОЕ",
        reply_markup=pagination(
            tracks_list=result, 
            type="popular"
        )
    )
    await save_message(chat_id=callback.message.chat.id, message_id=send_message.message_id)

@router.callback_query(F.data == "new")
async def new_tracks(
    callback: CallbackQuery
):
    result = get_new()
    markup = pagination(
        tracks_list=result, 
        type="new"
    )

    send_message = await bot.send_message(
        chat_id=callback.message.chat.id,
        text="НОВИНКИ",
        reply_markup=markup
    )
    await save_message(chat_id=callback.message.chat.id, message_id=send_message.message_id)



@router.message()
async def searching(
    message: types.Message
):
    check_member = True
    member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
    if member.status == "left":
        check_member = False
    if not check_member:
        url = InlineKeyboardBuilder()
        url.button(
           text="✅Подписаться",
           url=CHANNEL_LINK
        )
        url.button(
            text="✅Подписаться",
            url="https://t.me/m3ka3"
        )

        url.button(
           text="✅Я подписался!",
           
callback_data="check_subscription"
        )
	
        await message.answer("🕸️Вы не подписаны на каналы, подпишитесь, чтоб пользоваться функциями бота!", reply_markup=url.as_markup())
        return
    search = message.text
    if len(search) < 3:
        await message.answer(
            text="Название музыки должно быть не менее трех букв."
        )
        return
    result = search_music(query=search)
    markup = pagination(
        tracks_list=result, 
        type="search",
        search=search
    )

    send_message = await bot.send_message(
        chat_id=message.chat.id,
        text=search,
        reply_markup=markup
    )
    await save_message(chat_id=message.chat.id, message_id=send_message.message_id)



    
@router.callback_query(F.data.startswith("music_"))
async def get_music(
	callback: CallbackQuery
):
	music_id = callback.data.split("_")[1]
	
	result = download_track(music_id)
	file = FSInputFile(result)
	await callback.message.answer_audio(
		audio=file,
		caption=f"<a href='{BOT_LINK}'>Скачано ботом {BOT_USER}</a>",
		performer="a999muz",
		title=result.split("/")[1]
	)
	



# Обработчик проверки
@router.callback_query(F.data == "check_subscription")
async def check_sub(callback: types.CallbackQuery):

    user_id = callback.from_user.id
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ["member", "administrator", "creator"]:
            await callback.message.answer("Вы можете пользоваться ботом.")
            return
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return None

        # Если не подписан - отправляем сообщение с кнопкой
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text=BUTTON_TEXT,
            url=f"{CHANNEL_LINK}")]  # Юзернейм канала
        ])

    markup.add(types.InlineKeyboardButton(
    text="Я подписался!",
    callback_data="check_subscription")
)


    await callback.message.answer(
            text=SUBSCRIBE_TEXT,
            reply_markup=markup,
            parse_mode="HTML"
        )

        # Прерываем дальнейшую обработку
    return

	