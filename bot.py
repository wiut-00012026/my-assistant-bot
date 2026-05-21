mport os
import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json

TOKEN = "8555731522:AAEWv2ZphjR0AVmMPwcRvAW_dCbi--nc7II"

reminders = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men sizning assistant botingizman 🤖\n\nEslatma qo'shish uchun:\n/eslatma 2024-12-25 10:00 Yig'ilish")

async def eslatma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        sana = args[0]
        vaqt = args[1]
        matn = " ".join(args[2:])
        
        vaqt_obj = datetime.strptime(f"{sana} {vaqt}", "%Y-%m-%d %H:%M")
        chat_id = update.message.chat_id
        
        if chat_id not in reminders:
            reminders[chat_id] = []
        reminders[chat_id].append({"vaqt": vaqt_obj, "matn": matn})
        
        await update.message.reply_text(f"✅ Eslatma saqlandi!\n📅 {sana} soat {vaqt}\n📝 {matn}")
    except:
        await update.message.reply_text("❌ Format xato!\nTo'g'ri: /eslatma 2024-12-25 10:00 Yig'ilish")

async def check_reminders(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    for chat_id, reminder_list in reminders.items():
        for reminder in reminder_list[:]:
            if now >= reminder["vaqt"]:
                await context.bot.send_message(chat_id=chat_id, text=f"⏰ Eslatma!\n{reminder['matn']}")
                reminder_list.remove(reminder)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("eslatma", eslatma))
    job_queue = app.job_queue
    job_queue.run_repeating(check_reminders, interval=60)
    app.run_polling()

if name == "main":
    main()
