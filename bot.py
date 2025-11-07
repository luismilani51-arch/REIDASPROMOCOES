from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from bs4 import BeautifulSoup

TOKEN = "8412456444:AAG5fLXAr18Do6c4KMIjDdPX5xLqBw_G0wc" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Olá! Envie um link da Shopee que eu gero o anúncio pra você.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "shopee" not in url:
        await update.message.reply_text("⚠️ Envie um link válido da Shopee.")
        return
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        title = soup.find("title").text.strip().split("|")[0]
        price_tag = soup.find("meta", {"property": "product:price:amount"})
        price = price_tag["content"] if price_tag else "Preço não disponível"

        message = f"🛍️ {title}\n💲 Preço: R$ {price}\n🔗 [Compre aqui]({url})"
        await update.message.reply_text(message, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.run_polling()
