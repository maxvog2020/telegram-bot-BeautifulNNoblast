import html
from config import config
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo, KeyboardButton, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.strategy import FSMStrategy
import json
import urllib


TOKEN = config.bot_token.get_secret_value()
CHAT_ID = config.chat_id.get_secret_value()
MODER = config.moder.get_secret_value()
WEB_PREFIX = "https://maxvog2020.github.io/telegram-bot-BeautifulNNoblast/web"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

#########################
async def looking_callback(message: Message, values):
    data = values['json_data']

    type = data['type'].strip()
    description = data['description'].strip()
    price = data['price'].strip()
    address = data['address'].strip()
    contacts = data['contacts'].strip()
    telegram = data['telegram']

    text = f'#ищу_мастера \n\n<em>Тип мастера</em>\n💖 <b>{html.escape(type)}</b>\n\n'

    if address != "":
        text += f'<em>Примерный адрес</em>\n🏩 {html.escape(address)}\n\n'
    if price != "":
        text += f'<em>Ценовой диапазон</em>\n👛 {html.escape(price)}\n\n'
    if description != "":
        text += f'<em>Комментарий</em>\n💬 {html.escape(description)}\n\n'
    if telegram or contacts != "":
        text += f'<em>Контакты</em>\n👤 {html.escape(contacts)}'
    if telegram and contacts != "":
        text += f', '
    if telegram:
        text += get_telegram_ref(message)

    await send_with_images(CHAT_ID, text, [])
    await send_with_images(MODER, text + '\n\n\n<b>By</b> ' + get_telegram_ref(message), [])


async def offer_callback(message: Message, values):
    data = values['json_data']

    type = data['type'].strip()
    description = data['description'].strip()
    price = data['price'].strip()
    address = data['address'].strip()
    contacts = data['contacts'].strip()
    telegram = data['telegram']
    maps = data['maps']

    text = f'#предлагаю_услуги \n\n<em>Тип мастера</em>\n💖 {html.escape(type)}\n\n'

    if address != "" and maps:
        text += f'<em>Адрес</em>\n🏩 {get_address_ref(address)}\n\n'
    if address != "" and not maps:
        text += f'<em>Адрес</em>\n🏩 {html.escape(address)}\n\n'
    if price != "":
        text += f'<em>Цена</em>\n👛 {html.escape(price)}\n\n'
    if description != "":
        text += f'<em>Комментарий</em>\n💬 {html.escape(description)}\n\n'
    if telegram or contacts != "":
        text += f'<em>Контакты</em>\n👤 {html.escape(contacts)}'
    if telegram and contacts != "":
        text += f', '
    if telegram:
        text += get_telegram_ref(message)

    await send_with_images(CHAT_ID, text, values.get('images'))
    await send_with_images(MODER, text + '\n\n\n<b>By</b> ' + get_telegram_ref(message), values.get('images'))


async def rent_callback(message: Message, values):
    data = values['json_data']

    type = data['type'].strip()
    description = data['description'].strip()
    price = data['price'].strip()
    address = data['address'].strip()
    contacts = data['contacts'].strip()
    telegram = data['telegram']

    text = f'#сниму_рабочее_место \n\n<em>Предназначение</em>\n🎀 {html.escape(type)}\n\n'

    if address != "":
        text += f'<em>Примерный адрес</em>\n🏩 {html.escape(address)}\n\n'
    if price != "":
        text += f'<em>Ценовой диапазон</em>\n👛 {html.escape(price)}\n\n'
    if description != "":
        text += f'<em>Комментарий</em>\n💬 {html.escape(description)}\n\n'
    if telegram or contacts != "":
        text += f'<em>Контакты</em>\n👤 {html.escape(contacts)}'
    if telegram and contacts != "":
        text += f', '
    if telegram:
        text += get_telegram_ref(message)

    await send_with_images(CHAT_ID, text, [])
    await send_with_images(MODER, text + '\n\n\n<b>By</b> ' + get_telegram_ref(message), [])
    

async def lease_callback(message: Message, values):
    data = values['json_data']

    type = data['type'].strip()
    description = data['description'].strip()
    price = data['price'].strip()
    address = data['address'].strip()
    contacts = data['contacts'].strip()
    telegram = data['telegram']
    maps = data['maps']

    text = '#сдам_рабочее_место \n\n'

    if address != "" and maps:
        text += f'<em>Адрес</em>\n🏩 {get_address_ref(address)}\n\n'
    if address != "" and not maps:
        text += f'<em>Адрес</em>\n🏩 {html.escape(address)}\n\n'

    if type != "":
        text += f'<em>Для кого</em>\n❤️‍🔥 {html.escape(type)}\n\n'
    if price != "":
        text += f'<em>Цена</em>\n👛 {html.escape(price)}\n\n'
    if description != "":
        text += f'<em>Комментарий</em>\n💬 {html.escape(description)}\n\n'
    if telegram or contacts != "":
        text += f'<em>Контакты</em>\n👤 {html.escape(contacts)}'
    if telegram and contacts != "":
        text += f', '
    if telegram:
        text += get_telegram_ref(message)

    await send_with_images(CHAT_ID, text, values.get('images'))
    await send_with_images(MODER, text + '\n\n\n<b>By</b> ' + get_telegram_ref(message), values.get('images'))
    
async def feedback_callback(message: Message, values):
    data = values['json_data']

    who = data['who'].strip()
    description = data['description'].strip()
    contacts = data['contacts'].strip()
    telegram = data['telegram']

    text = f'#отзыв \n\n<em>Про кого отзыв</em>\n🤔 {html.escape(who)}\n\n'

    if description != "":
        text += f'<em>Комментарий</em>\n💬 {html.escape(description)}\n\n'
    if telegram or contacts != "":
        text += f'<em>Контакты</em>\n👤 {html.escape(contacts)}'
    if telegram and contacts != "":
        text += f', '
    if telegram:
        text += get_telegram_ref(message)

    await send_with_images(CHAT_ID, text, [])
    await send_with_images(MODER, text + '\n\n\n<b>By</b> ' + get_telegram_ref(message), [])

async def model_callback(message: Message, values):
    data = values['json_data']

    type = data['type'].strip()
    description = data['description'].strip()
    address = data['address'].strip()
    contacts = data['contacts'].strip()
    telegram = data['telegram']
    maps = data['maps']

    text = f'#ищу_модель \n\n<em>Тип мастера</em>\n💖 <b>{html.escape(type)}</b>\n\n'

    if address != "" and maps:
        text += f'<em>Адрес</em>\n🏩 {get_address_ref(address)}\n\n'
    if address != "" and not maps:
        text += f'<em>Адрес</em>\n🏩 {html.escape(address)}\n\n'
    if description != "":
        text += f'<em>Комментарий</em>\n💬 {html.escape(description)}\n\n'
    if telegram or contacts != "":
        text += f'<em>Контакты</em>\n👤 {html.escape(contacts)}'
    if telegram and contacts != "":
        text += f', '
    if telegram:
        text += get_telegram_ref(message)

    await send_with_images(CHAT_ID, text, values.get('images'))
    await send_with_images(MODER, text + '\n\n\n<b>By</b> ' + get_telegram_ref(message), values.get('images'))

callbacks = {
    "looking": looking_callback,
    "offer": offer_callback,
    "rent": rent_callback,
    "lease": lease_callback,
    "feedback": feedback_callback,
    "model": model_callback,
}

#########################
def get_telegram_ref(message: Message):
    name = html.escape(message.from_user.full_name)
    return f'<a href="tg://user?id={message.from_user.id}">{name}</a>'

def get_address_ref(str: str):
    str = html.escape(str)
    return f'<a href="https://yandex.com/maps?text={urllib.parse.quote("Нижегородская область, " + str)}">{str}</a>'

async def send_with_images(chat_id, text, images):
    if images == [] or images == None:
        return await bot.send_message(chat_id, text, parse_mode="HTML", disable_web_page_preview=True)

    media = [
        InputMediaPhoto(media=images[0].photo[-1].file_id, caption=text, parse_mode="HTML")
    ]

    for i in range(1, len(images)):
        media.append(InputMediaPhoto(media=images[i].photo[-1].file_id))

    return (await bot.send_media_group(chat_id, media))[0]


async def publish(message: Message, state: FSMContext):
    values = await state.get_data()

    callback = values.get('callback')
    await callback(message, values)

    for pic in values.get('images') or []:
        await pic.delete()
    if values.get('to_delete') != None:
        await values.get('to_delete').delete()
    
    await state.clear()
    message = await message.answer('Опубликовано!')
    await asyncio.sleep(3)
    await message.delete()

@dp.message(F.photo)
async def on_get_photo(message: Message, state: FSMContext):
    values = await state.get_data()
    image_count = int(values.get('image_count')) or 0
    images = values.get('images') or []

    if image_count == 0:
        await message.delete()
        return
    else:
        images.append(message)
        image_count -= 1
        await state.update_data(images=images, image_count=image_count)

    if image_count == 0:
        await publish(message, state)

@dp.message(F.web_app_data)
async def on_get_data(message: Message, state: FSMContext):
    data = message.web_app_data.data

    json_data = json.loads(data)

    callback = callbacks[json_data['callback']]
    image_count = int(json_data.get('image_count') or 0)

    await message.delete()
    await state.update_data(callback=callback, image_count=image_count, json_data=json_data)

    if image_count == 0:
        await publish(message, state)
    else:
        to_delete = await message.answer(f"Приложите фотографии ({image_count} шт.)")
        await state.update_data(to_delete=to_delete)


@dp.callback_query()
async def on_callbacks(callback: CallbackQuery):
    await callback.message.answer("Удалите переписку с этим ботом и начните заново")
    await callback.answer()

@dp.message(Command("start"))
async def on_start(message: Message):
    if message.from_user.id == int(MODER):
        await message.answer("==== Аккаунт модератора ====")
        await message.delete()
        return

    await get_init_message(message)
    await message.delete()

@dp.message(Command(*callbacks))
async def on_command(message: Message):
    await message.delete()
    url = WEB_PREFIX + message.text

    markup = ReplyKeyboardBuilder()
    markup.add(KeyboardButton(text="👉 Перейти в форму", web_app=WebAppInfo(url=url)))

    message = await message.answer(text="Нажмите на кнопку для перехода в форму 👇", reply_markup=markup.as_markup())
    await asyncio.sleep(5)
    await message.delete()

@dp.message()
async def delete_everything_else(message: Message):
    await message.delete()
    message = await get_init_message(message)
    await asyncio.sleep(5)
    await message.delete()

async def get_init_message(message: Message):
    return await message.answer("Для того, чтобы опубликовать объявление, используйте <b>меню</b>!", parse_mode="HTML")

#########################
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
