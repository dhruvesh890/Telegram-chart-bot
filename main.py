import requests import matplotlib.pyplot as plt from io import BytesIO from telegram import Update from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") TWELVE_API_KEY = os.getenv("TWELVE_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("👋 Hello! Send /chart to get the latest price chart.")

async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE): symbol = "EUR/USD" interval = "1min" url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize=30&apikey={TWELVE_API_KEY}"

try:
    response = requests.get(url)
    data = response.json()

    if "values" not in data:
        await update.message.reply_text("❌ Failed to fetch data. Please try again later.")
        return

    timestamps = [entry["datetime"][-5:] for entry in reversed(data["values"])]
    closes = [float(entry["close"]) for entry in reversed(data["values"])]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, closes, marker='o', color='blue')
    plt.xticks(rotation=45)
    plt.title(f'{symbol} - {interval} Chart')
    plt.xlabel('Time')
    plt.ylabel('Close Price')
    plt.grid(True)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    await update.message.reply_photo(photo=buf)
    buf.close()

except Exception as e:
    await update.message.reply_text(f"⚠️ Error: {str(e)}")

if name == 'main': app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(CommandHandler("chart", chart)) app.run_polling()

