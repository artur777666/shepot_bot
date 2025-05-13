from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import random
from datetime import datetime
from pytz import timezone

API_TOKEN = '7577091795:AAH0u0p827vyGmtBOEgw2_zJ7oN9cyUOKZs'
CHANNEL_ID = '@shepotzvezd_rus'

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



menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add("🔮 Гороскоп", "🌘 Луна")
menu_keyboard.add("🃏 Карта", "🎲 Игра")

buttons = [KeyboardButton(sign) for sign in signs]
for i in range(0, len(buttons), 3):
    key_markup.add(*buttons[i:i+3])

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("✨ Я — Жрица Шёпота.\nЯ расскажу тебе о твоей судьбе. Выбери знак и используй кнопки ниже:", reply_markup=menu_keyboard)

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

@dp.message_handler(commands=["публиковать"])
async def publish_to_channel(message: types.Message):
    if message.from_user.id == message.chat.id:
        await bot.send_message(CHANNEL_ID, "🔮 Послание Жрицы:\nСегодня — день интуиции.\nПрислушайся к знакам и не игнорируй случайные совпадения.")

@dp.message_handler(lambda message: message.text in signs)
async def save_sign(message: types.Message):
    user_data[message.from_user.id] = message.text
    await message.reply(f"✨ Ты выбрал знак {message.text}.\nНапиши /гороскоп, чтобы услышать, что шепчут звёзды.")

daily_whispers = [
    "Сегодня тишина говорит громче слов. Прислушайся к паузам.",
    "Ты почувствуешь толчок. Это знак. Не сопротивляйся переменам.",
    "Невидимые силы уже действуют. Верь своему чутью.",
    "Сегодня день, когда важно не спешить. Ответ идёт.",
    "Пусть шёпот звёзд будет тебе проводником — даже в шуме мира."
]

async def scheduled_tasks():
    tz = timezone('Europe/Moscow')
    now = datetime.now(tz)
    whisper = random.choice(daily_whispers)

    try:
            try:
    await bot.send_message(user_id,
        f"🌌 *Шёпот Жрицы:*\\n_{whisper}_\\n\\n— t.me/shepotzvezd_rus",
        parse_mode="Markdown")
except Exception as e:
    print("Ошибка при отправке шёпота:", e)


        print("Ошибка при отправке в канал:", e)

    for user_id in user_data:
        try:
            await bot.send_message(user_id,
                f"🌌 *Шёпот Жрицы:*\n_{whisper}_\n\n— t.me/shepotzvezd_rus",
                parse_mode="Markdown")
        except:
            continue

async def on_startup(dp):
    scheduler.add_job(send_whispers_only, "cron", hour=9, minute=0, timezone="Europe/Moscow")
    scheduler.start()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


@dp.message_handler(commands=["игра"])
async def start_game(message: types.Message):
    await message.reply("🔮 Я разложила 5 карт судьбы перед тобой.\nНапиши число от 1 до 5, чтобы выбрать свою карту...")

@dp.message_handler(lambda message: message.text in ["1", "2", "3", "4", "5"])
async def reveal_card(message: types.Message):
    responses = {
        "1": "Карта 1 — Пламя. Сегодня всё начнётся с искры. Не бойся загореться.",
        "2": "Карта 2 — Тень. Ответ рядом, но он скрыт. Смотри глубже.",
        "3": "Карта 3 — Мост. Что-то из прошлого ждёт твоего шага.",
        "4": "Карта 4 — Лес. Пауза нужна, чтобы услышать зов интуиции.",
        "5": "Карта 5 — Луна. Прислушайся к снам. В них истина."
    }
    await message.reply(f"🌌 {responses[message.text]}\n\n— Жрица Шёпота")

async def send_whispers_only():
    whisper = random.choice(daily_whispers)
    for user_id in user_data:
        try:
            await bot.send_message(user_id,
                f"🌌 *Шёпот Жрицы:*\n_{whisper}_\n\n— t.me/shepotzvezd_rus",
                parse_mode="Markdown")
        except:
            continue

@dp.message_handler(lambda message: message.text == "🔮 Гороскоп")
async def horoscope_button(message: types.Message):
    await send_horoscope(message)

@dp.message_handler(lambda message: message.text == "🌘 Луна")
async def luna_button(message: types.Message):
    await lunar_whisper(message)

@dp.message_handler(lambda message: message.text == "🃏 Карта")
async def card_button(message: types.Message):
    await send_card(message)

@dp.message_handler(lambda message: message.text == "🎲 Игра")
async def game_button(message: types.Message):
    await start_game(message)
