import os
import logging
import sqlite3

import openpyxl
import telegram
import pandas as pd
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler, MessageHandler,
    filters, CallbackContext,
    Application
)
from dotenv import load_dotenv


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

load_dotenv()
TOKEN = os.getenv('TOKEN')


conn = sqlite3.connect('data.db')
c = conn.cursor()
bot = telegram.Bot(TOKEN)


c.execute('''
    CREATE TABLE IF NOT EXISTS my_table (
        title TEXT DEFAUL None,
        url TEXT DEFAULT None,
        xpath TEXT DEFAULT None
    )
''')
conn.commit()


async def start(update: Update, context: CallbackContext) -> None:
    """
    Создаем функцию для начала работы бота с приветствием
    """
    context.user_data['is_downloading'] = False
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name
    button = KeyboardButton('/download')
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
    await bot.send_message(
        chat_id=chat_id,
        text=f'Привет, {user_name}! Для начала работы нажми кнопку',
        reply_markup=keyboard
    )


async def comand_load(update: Update, context: CallbackContext) -> None:
    """
    Обрабатываем команду download что бы небыло
    возможности загрузить файл пока кнопка не нажата
    """
    chat_id = update.effective_chat.id
    context.user_data['is_downloading'] = True
    await bot.send_message(chat_id=chat_id, text='Загрузите файл Excel')


async def load_document(update: Update, context: CallbackContext) -> None:
    """
    Загрузка документа и проверка на соответствие расширению
    """
    if context.user_data['is_downloading'] is True:
        file = update.message.document
        if not file.file_name.endswith('.xlsx'):
            await update.message.reply_text(
                'Пожалуйста, загрузите файл с расширением .xlsx'
            )
            return
        else:
            file_name = file.file_name.split("/")[-1]
            dock_file = await update.message.document.get_file()
            await dock_file.download_to_drive(file_name)
            wb = openpyxl.load_workbook(file_name)
            sheet = wb.active
            for row in sheet.iter_rows(min_row=2, values_only=True):
                c.execute(
                    "INSERT INTO my_table (title, url, xpath) \
                    VALUES (?, ?, ?)",
                    row
                )

            conn.commit()
            df = pd.read_excel(file_name)
            data_str = df.to_string()
            await update.message.reply_text(
                'Файл успешно сохранен в базе данных.'
            )
            await update.message.reply_text(data_str)
            context.user_data['is_downloading'] = False
            await update.message.reply_text(
                'Для повторной загрузки нажмите кнопку еще раз.'
            )
    else:
        await update.message.reply_text('Вы не нажали кнопку download.')


async def help_command(update: Update, context: CallbackContext) -> None:
    """
    Вызов справки о боте
    """
    text = "Используйте /start для начала работы, бот не принимает(игнорирует)\
        сообщения и сторонние файлы кроме тех которых он ожидает!"
    await update.message.reply_text(text=text)


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("download", comand_load))
    application.add_handler(
        MessageHandler(filters.Document.ALL, load_document)
    )
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    conn.close()


if __name__ == "__main__":
    main()
