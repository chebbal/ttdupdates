import logging
import os
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Configuration
BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000/updates")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm the TTD Updates Bot! Use /updates [n] to get the latest info (default 5).")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 **TTD Bot Help**\n\n"
        "Available commands:\n"
        "/start - Wake up the bot\n"
        "/updates - Get latest 5 updates\n"
        "/updates [n] - Get latest 'n' updates (max 20)\n"
        "/help - Show this message"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text, parse_mode='Markdown')


async def get_updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Default limit
        limit = 5
        
        # Check if user provided a limit argument (e.g. /updates 10)
        if context.args and context.args[0].isdigit():
            limit = int(context.args[0])
            # Cap the limit to avoid huge messages if needed, e.g., max 20
            limit = min(limit, 20)

        response = requests.get(BACKEND_URL, timeout=10)
        response.raise_for_status()
        updates = response.json()
        
        if not updates:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No updates found at the moment.")
            return

        # Use the configured limit
        for item in updates[:limit]: 
            msg = f"**Update:**\n{item.get('message', 'No content')}\n"
            if item.get('link'):
                msg += f"\n[Link]({item['link']})"
            
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')
            
    except Exception as e:
        logging.error(f"Error fetching updates: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't reach the updates service right now.")

if __name__ == '__main__':
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_TOKEN environment variable not set.")
        exit(1)
        
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    updates_handler = CommandHandler('updates', get_updates)
    help_handler = CommandHandler('help', help_command)
    
    application.add_handler(start_handler)
    application.add_handler(updates_handler)
    application.add_handler(help_handler)

    
    application.run_polling()
