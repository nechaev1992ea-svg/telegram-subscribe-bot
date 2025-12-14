import os
from aiogram import Bot, Dispatcher, executor, types

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@dom2nechaeva"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    member = await bot.get_chat_member(CHANNEL, msg.from_user.id)

    if member.status in ["member", "administrator", "creator"]:
        await msg.answer("🎁 Держи файл:")
        await msg.answer_document(open("gift.pdf", "rb"))
    else:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("Подписаться", url="https://t.me/dom2nechaeva"))
        kb.add(types.InlineKeyboardButton("Проверить", callback_data="check"))
        await msg.answer("Подпишись на канал:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "check")
async def check(call: types.CallbackQuery):
    member = await bot.get_chat_member(CHANNEL, call.from_user.id)
    if member.status in ["member", "administrator", "creator"]:
        await call.message.answer("🎁 Вот твой файл:")
        await call.message.answer_document(open("gift.pdf", "rb"))
    else:
        await call.answer("Ты ещё не подписан", show_alert=True)

executor.start_polling(dp)
