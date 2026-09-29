import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "dummy_token")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "Welcome to the AgTech Mandi Bot! 🌾\n"
        "I can help you with real-time prices, profit calculations, and forecasts.\n\n"
        "Try typing something like:\n"
        "District: Nashik, Crop: Onion"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "nashik" in text.lower() and "onion" in text.lower():
        from ml_engine.advisory_agent import generate_advisory
        
        # Mocking incoming data pipeline for Nashik Onion
        farmer_query = text
        crop_quality_data = {"quality_score": 0.85, "defect_grade": "B"}
        spatial_data = {
            "usable_quantity": 20, # quintals
            "spoilage_decay_rate": {"Nashik Local": 0, "Mumbai APMC": 0.5, "Pune Mandi": 0.2},
            "transit_times": {"Nashik Local": 1, "Mumbai APMC": 4, "Pune Mandi": 3},
            "base_prices": {"Nashik Local": 1500, "Mumbai APMC": 2100, "Pune Mandi": 1800},
            "distances": {"Nashik Local": 10, "Mumbai APMC": 160, "Pune Mandi": 210},
            "fuel_rate": 15, # ₹/km
            "tolls": {"Nashik Local": 0, "Mumbai APMC": 400, "Pune Mandi": 250},
            "wages": {"Nashik Local": 200, "Mumbai APMC": 1000, "Pune Mandi": 800}
        }
        
        reply = generate_advisory(
            farmer_query=farmer_query,
            crop_quality_data=crop_quality_data,
            spatial_data=spatial_data,
            local_market_name="Nashik Local"
        )
    else:
        reply = "I couldn't find data for that combination. Please specify 'District: [Name], Crop: [Name]'."
        
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    print("Starting Telegram Bot...")
    application.run_polling()
