from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from collect_data import collect_data
from config import *
import time
import json

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


def show_data():
    with open('result.json') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
               f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
               f'{hbold("Цена: ")}${item.get("item_price")}🔥'

        time.sleep(SLEEP_COUNT)

        yield card


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['🔪 Ножи', '🥊 Перчатки', '🔫 Снайперские винтовки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите категорию', reply_markup=keyboard)


@dp.message_handler(Text(equals='🔪 Ножи'))
async def get_discount_knives(message: types.Message):
    await message.answer('Пожалуйста, подождите...')

    collect_data(KNIFE_ID)

    for card in show_data():
        await message.answer(card)


@dp.message_handler(Text(equals='🥊 Перчатки'))
async def get_discount_knives(message: types.Message):
    await message.answer('Пожалуйста, подождите...')

    collect_data(GLOVES_ID)

    for card in show_data():
        await message.answer(card)


@dp.message_handler(Text(equals='🔫 Снайперские винтовки'))
async def get_discount_guns(message: types.Message):
    await message.answer('Пожалуйста, подождите...')

    collect_data(SNIPER_GUN_ID)

    for card in show_data():
        await message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()