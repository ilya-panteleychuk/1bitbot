from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import asyncio
from aiogram.filters import CommandStart
import sqlite3
import smtplib
from email.mime.text import MIMEText


TOKEN = "6868173085:AAEjMWlUHSYAA4AKg2yZdu05wBn-BYKfSm0"  # Токен бота
database_name = 'database.db'

bot = Bot(token=TOKEN)
dp = Dispatcher()
connection = sqlite3.connect(database_name)

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Создать заявку"),
        KeyboardButton(text="Обратный звонок")
    ],
    [
        KeyboardButton(text="Контакты"),
        KeyboardButton(text="FAQ")
    ]
], resize_keyboard=True) # Клавиатура 4 кнопки

# Нажатия на кнопки
async def get_button(message: Message):
    if message.text == "Создать заявку":
        await message.answer("Заявок нет")
    elif message.text == "Обратный звонок":
        await message.answer("Звонка нет")
        await send_email(message.text)
    elif message.text == "Контакты":
        await message.answer('''Линия консультаций: +7 (3812) 332-964 
Круглосуточно omsk@1cbit.ru\n 
г. Омск, ул. Гагарина, д.14, центральный вход, 2 этаж, офис 208, тел. +7 (3812) 320-330
Источник: https://omsk.1cbit.ru/contacts/omsk/omsk/''')
    elif message.text == "FAQ":
        await message.answer("FAQ нет")

# Если есть вернет 1, если нет вернет 0
async def check_user_tg_exists(message: Message):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        user_id INT PRIMARY KEY,
        username VARCHAR(50) NOT NULL
        )
        ''')
    connection.commit()
    user_id = message.from_user.id
    username = message.from_user.username
    # Проверить наличие пользователя в базе данных
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    if result:
        # Пользователь существует в базе данных
        return 1
    else:
        # Пользователя нет в базе данных, добавить его
        cursor.execute("INSERT INTO Users (user_id, username) VALUES (?, ?)",
                       (user_id, username))
        connection.commit()
        return 0

# Передаем сообщение, функция отправляет
async def send_email(message):
    sender = "bit.perw@yandex.ru"
    password = "ojaiaqdykfubxvwi"
    recipient = "cipsevelti@gufum.com"

    server = smtplib.SMTP('smtp.yandex.ru', 587)
    server.ehlo()
    server.starttls()
    server.login(sender, password)
    msg = MIMEText(message)
    server.sendmail(sender, recipient, msg.as_string())

# Проверить есть ли инн в базе
async def check_inn_user():
    pass

async def get_start(message: Message):
    if await check_user_tg_exists(message) == 0:
        await bot.send_message(message.from_user.id, "Спасибо, что зашли!")
    else:
        await bot.send_message(message.from_user.id, "Ты уже был тут", reply_markup=reply_keyboard)


async def start():
    dp.message.register(get_start, CommandStart())
    dp.message.register(get_button)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
