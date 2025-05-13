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
menu_keyboard.add("♈ Выбрать знак")

signs_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
sign_buttons = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
for i in range(0, len(sign_buttons), 3):
    signs_keyboard.add(*sign_buttons[i:i+3])

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("✨ Я — Жрица Шёпота.\nЯ расскажу тебе о твоей судьбе. Нажми «♈ Выбрать знак», а затем используй кнопки:", reply_markup=menu_keyboard)

@dp.message_handler(lambda message: message.text == "♈ Выбрать знак")
async def ask_sign(message: types.Message):
    await message.reply("Выбери свой знак зодиака:", reply_markup=signs_keyboard)

@dp.message_handler(lambda message: message.text in signs)
async def save_sign(message: types.Message):
    user_data[message.from_user.id] = message.text
    await message.reply(f"✨ Ты выбрал знак {message.text}. Теперь ты можешь нажимать кнопки и получать магические подсказки.", reply_markup=menu_keyboard)

@dp.message_handler(lambda message: message.text == "🔮 Гороскоп")
async def send_horoscope(message: types.Message):
    user_id = message.from_user.id
    sign = user_data.get(user_id)
    if not sign:
        await message.reply("Ты ещё не открыл знамение. Нажми «♈ Выбрать знак».")
    else:
        await message.reply(f"🔮 Гороскоп для {sign} на сегодня:\n\nТы чувствуешь — и я отвечаю. Сегодня твоя энергия ищет отражение в других. Не спеши. Услышь.")

@dp.message_handler(lambda message: message.text == "🌘 Луна")
async def lunar_whisper(message: types.Message):
    await message.reply("🌘 Сегодня — восьмой лунный день.\nЛуна в Весах. Баланс важнее правды. Дыши глубже.\n\n— Жрица Шёпота")

@dp.message_handler(lambda message: message.text == "🃏 Карта")
async def send_card(message: types.Message):
    cards = {
        "Пламя": "Сегодня ты носишь в себе искру перемен. Не бойся загореться.",
        "Тень": "Ответ не снаружи. Он спрятан в том, от чего ты отворачивался.",
        "Мост": "Кто-то из прошлого думает о тебе. Мост ещё не сгорел.",
        "Лес": "Ты заблудился в мыслях. Истина придёт позже.",
        "Луна": "Ночь откроет знаки. Внимание к снам и случайным словам."
    }
    card = random.choice(list(cards.items()))
    await message.reply(f"🃏 Карта судьбы: *{card[0]}*\n_{card[1]}_\n\n— Жрица Шёпота", parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == "🎲 Игра")
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

daily_whispers = [
    "Сегодня тишина говорит громче слов. Прислушайся к паузам.",
    "Ты почувствуешь толчок. Это знак. Не сопротивляйся переменам.",
    "Невидимые силы уже действуют. Верь своему чутью.",
    "Сегодня день, когда важно не спешить. Ответ идёт.",
    "Пусть шёпот звёзд будет тебе проводником — даже в шуме мира."
]

async def send_whispers_only():
    whisper = random.choice(daily_whispers)
    for user_id in user_data:
        try:
            await bot.send_message(user_id,
                f"🌌 *Шёпот Жрицы:*\n_{whisper}_\n\n— t.me/shepotzvezd_rus",
                parse_mode="Markdown")
        except Exception as e:
            print("Ошибка при отправке шёпота:", e)

async def on_startup(dp):
    scheduler.add_job(send_whispers_only, "cron", hour=9, minute=0, timezone="Europe/Moscow")
    scheduler.start()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
