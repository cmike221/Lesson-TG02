import os
import datetime
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from googletrans import Translator
from gtts import gTTS
from config import TOKEN

API_TOKEN = TOKEN  # Замените на токен вашего бота

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)  # Передача storage в Dispatcher

translator = Translator()

# Убедитесь, что папка /img существует
if not os.path.exists('img'):
    os.makedirs('img')


@dp.message(F.photo)
async def react_photo(message: Message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    await bot.download(message.photo[-1], destination=f'img/Img-{current_time}.jpg')
    await message.reply(f'Фото сохранено {current_time}')

@dp.message(lambda message: message.text.startswith('%'))
async def translate_to_english(message: types.Message):
    text_to_translate = message.text[1:].strip()  # Убираем префикс '%'
    translated_text = translator.translate(text_to_translate, dest='en').text
    await message.reply(translated_text)


@dp.message(lambda message: message.text.startswith('&'))
async def translate_to_speech(message: types.Message):
    text_to_translate = message.text[1:].strip()  # Убираем префикс '&'
    translated_text = translator.translate(text_to_translate, dest='en').text

    # Преобразуем текст в речь
    tts = gTTS(text=translated_text, lang='en')
    tts.save("traning.ogg")
    audio = FSInputFile('traning.ogg')
    await bot.send_voice(message.chat.id, audio)
    os.remove("traning.ogg")


@dp.message(lambda message: not message.text.startswith(('%', '&')))
async def send_help(message: types.Message):
    await message.reply("% - перевод в текст на английском языке\n& - перевод в речь на английском языке\n Сохранение загруженных картинок")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
