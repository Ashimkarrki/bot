import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import redis
from dotenv import load_dotenv
load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
# host=os.getenv("DEV_HOST")
host=os.getenv("PROD_HOST")


r = redis.Redis(host=host, port=6379, db=0)
# 1269865645

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r.sadd("users",str(update.effective_chat.id))
    await update.message.reply_text("Welcome to news-pasa.\nYou have been successfully added as a member.\nNews updates will be delivered to you regularly.")

async def anyMessage(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You will be provided with news for ervery 10min.\n You can deactivate this service with /cancel and activate with /start.\n ")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You will receive news updates every 10 minutes.\nTo deactivate this service, use the command` /cancel`.\nTo reactivate it, use `/start`.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r.srem("users",str(update.effective_chat.id))
    await update.message.reply_text("Service deactivated.\nYou will no longer receive any further messages.")




def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help",help))
    app.add_handler(CommandHandler("cancel",cancel))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anyMessage))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
    
