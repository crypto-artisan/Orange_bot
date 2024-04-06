import logging
from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    PicklePersistence,
    MessageHandler,
    CommandHandler
)
import asyncio
import telegram.ext.filters as filters
from dialog_flow  import dialog_flow
from cmcApi import fetch_api

import os
import dotenv
dotenv.load_dotenv()

# Telegram Info
TOKEN_TELEGRAM = os.getenv("TG_TOKEN")

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '02b9b587-65f6-4ae8-b43f-1556fc862963',
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Respond according to the 'CryptoInfo' state
    inputData = update.message.text.removeprefix("/")
    inputData = inputData.replace("marketcap", "market cap").replace("totalsupply", "total supply").replace("fullname", "full name")
    tokenName, intent, fulfillmentText = dialog_flow(inputData)
    if intent == "Tradingvolume":
        intent = "Volume"
    if intent == "Totalsupply":
        intent = "TotalSupply"
    if intent == "Marketcapitalization":
        intent = "Capitalization"
    info = fetch_api(tokenName, intent)
    if intent=="Price" or intent =="TotalSupply" or intent=="Capitalization" or intent =="Volume":
        answer = fulfillmentText.replace("{" + f"Asset{intent}" + "}", str(info)) + " USD"
    else:
        answer = fulfillmentText.replace("{" + f"Asset{intent}" + "}", str(info))
    response_text = f"{answer}"
    await update.message.reply_text(response_text)

async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Respond according to the 'CryptoInfo' state
    inputData = update.message.text.removeprefix("/")
    inputData = inputData.replace("marketcap", "market cap").replace("totalsupply", "total supply").replace("fullname", "full name")
    tokenName, intent, fulfillmentText = dialog_flow(inputData)
    if intent == "Tradingvolume":
        intent = "Volume"
    if intent == "Totalsupply":
        intent = "TotalSupply"
    if intent == "Marketcapitalization":
        intent = "Capitalization"
    info = fetch_api(tokenName, intent)
    if intent=="Price" or intent =="TotalSupply" or intent=="Capitalization" or intent =="Volume":
        answer = fulfillmentText.replace("{" + f"Asset{intent}" + "}", str(info)) + " USD"
    else:
        answer = fulfillmentText.replace("{" + f"Asset{intent}" + "}", str(info))
    response_text = f"{answer}"
    await update.message.reply_text(response_text)


def main() -> None:
    """Run the bot."""
    # We use persistence to demonstrate how buttons can still work after the bot was restarted
    persistence = PicklePersistence(filepath="arbitrarycallbackdatabot")
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token(TOKEN_TELEGRAM)
        .persistence(persistence)
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(MessageHandler(filters.Text and ~filters.COMMAND, start))
    application.add_handler(CommandHandler("price", command))
    application.add_handler(CommandHandler("marketcap", command))
    application.add_handler(CommandHandler("totalsupply", command))
    application.add_handler(CommandHandler("fullname", command))
    application.add_handler(CommandHandler("symbol", command))
    application.add_handler(CommandHandler("volume", command))

    # Run the bot until the user presses Ctrl-C
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
