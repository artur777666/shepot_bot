from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import random

API_TOKEN = '7577091795:AAEYS5FeQHq1pJoQ1MQDsFHPgindn-t34fI'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()

user_data = {}

signs = [
    "Овен", "Телец", "Близнецы",
    "Рак", "Лев", "Дева",
    "Весы", "Скорпион", "Стрелец",
    "Козерог", "Водолей", "Рыбы"
]

key_markup = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [KeyboardButton(sign) for sign in signs]
for i in range(0, len(buttons), 3):
    key_markup.add(*buttons[i:i+3])

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("✨ Я — Жрица Шёпота. Выбери свой знак, и звёзды заговорят с тобой:", reply_markup=key_markup)

@dp.message_handler(commands=["гороскоп"])
async def send_horoscope(message: types.Message):
    user_id = message.from_user.id
    sign = user_data.get(user_id)
    if not sign:
        await message.reply("Ты ещё не открыл знамение. Выбери знак зодиака ниже.")
    else:
        await message.reply(f"🔮 Гороскоп для {sign} на сегодня:\n\nТы чувствуешь — и я отвечаю. Сегодня твоя энергия ищет отражение в других. Не спеши. Услышь.")

@dp.message_handler(commands=["карта"])
async def send_card(message: types.Message):
    cards = {
        "Пламя": "Сегодня ты носишь в себе искру перемен. Не туши её сомнениями.",
        "Тень": "Ответ не снаружи. Он спрятан в том, от чего ты отворачивался.",
        "Мост": "Кто-то из прошлого думает о тебе. Мост ещё не сгорел.",
        "Лес": "Ты заблудился в мыслях. Истина придёт позже.",
        "Луна": "Ночь откроет знаки. Внимание к снам и случайным словам."
    }
    card = random.choice(list(cards.items()))
    await message.reply(f"🃏 Карта судьбы: *{card[0]}*\n_{card[1]}_\n\n— Жрица Шёпота", parse_mode="Markdown")

@dp.message_handler(commands=["луна"])
async def lunar_whisper(message: types.Message):
    await message.reply("🌘 Сегодня — восьмой лунный день.\nЛуна в Весах. Баланс важнее правды. Дыши глубже.\n\n— Жрица Шёпота")

@dp.message_handler(lambda message: message.text in signs)
async def save_sign(message: types.Message):
    user_data[message.from_user.id] = message.text
    await message.reply(f"✨ Ты выбрал знак {message.text}.\nНапиши /гороскоп, чтобы услышать, что шепчут звёзды.")

async def daily_broadcast():
    for user_id, sign in user_data.items():
        try:
            await bot.send_message(user_id, f"🔮 Гороскоп для {sign} на сегодня:\n\nТы чувствуешь — и я отвечаю. Сегодня твоя энергия ищет отражение в других. Не спеши. Услышь.")
        except Exception:
            continue

async def on_startup(dp):
    scheduler.add_job(daily_broadcast, "cron", hour=9, minute=0)
    scheduler.start()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


@dp.message_handler(commands=["публиковать"])
async def publish_to_channel(message: types.Message):
    if message.from_user.id == message.chat.id:
        await bot.send_message("@shepotzvezd_rus", "🔮 Послание Жрицы:\nСегодня — день интуиции.\nПрислушайся к знакам и не игнорируй случайные совпадения.")
        await message.reply("✅ Послание отправлено в канал.")
