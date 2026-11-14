import os, logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")
client = Groq(api_key=GROQ_KEY)
SYSTEM = "Ты - помощник Kaspi.kz, отвечай коротко на русском, помогаешь с Kaspi Магазин."
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Салам! Kaspi-бот 24/7 готов 🚀 Задай вопрос!")
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"system","content":SYSTEM},{"role":"user","content":update.message.text}], max_tokens=800)
        await update.message.reply_text(r.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()
if __name__ == "__main__":
    main()
