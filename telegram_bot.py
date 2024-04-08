import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
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
from aiAnswer import generateAnswer

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

async def get_gpt4_response(prompt):
    """Placeholder function to get a response from GPT-4.
    
    This function should be replaced with actual code to send a request to the GPT-4 API
    and return the generated response.
    """
    # Example: Simulate getting a response from GPT-4
    answer = generateAnswer(prompt)
    return f"{answer}"

async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    # Generate a response using GPT-4
    response_text = await get_gpt4_response(user_message)
    await update.message.reply_html(response_text)
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Respond according to the 'CryptoInfo' state
    # inputData = update.message.text.strip()
    inputData = update.message.text
    print("inputData", inputData)
    if inputData.startswith("/orange"):
        inputData = update.message.text.removeprefix("/orange")
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
            answer = fulfillmentText.replace("{" + f"Asset{intent}" + "}.", str(info)) + " USD."
        else:
            answer = fulfillmentText.replace("{" + f"Asset{intent}" + "}.", str(info)) + "."
        certification = "Powered by the Orange Assistant and made by Orange."
        response_text = f"{answer}\n\n{certification}"
        button1 = InlineKeyboardButton(text="🌎Website", url="https://www.orangecrypto.com/")
        button2 = InlineKeyboardButton(text="📜Docs", url="https://docs.orangecrypto.com/")

        # Create the keyboard markup with the buttons
        keyboard_markup = InlineKeyboardMarkup([
            [button1, button2], # This is a row with two buttons
        ])
        await update.message.reply_html(response_text, reply_markup=keyboard_markup)
    else:
        pass

async def command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Respond according to the 'CryptoInfo' state
    # inputData = update.message.text.strip()
    inputData = update.message.text
    print("inputData", inputData)
    if inputData.startswith("/orange"):
        inputData = update.message.text.removeprefix("/orange")
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
            answer = fulfillmentText.replace("{" + f"Asset{intent}" + "}.", str(info)) + " USD."
        else:
            answer = fulfillmentText.replace("{" + f"Asset{intent}" + "}.", str(info)) + "."
        certification = "Powered by the Orange Assistant and made by Orange."
        response_text = f"{answer}\n\n{certification}"
        button1 = InlineKeyboardButton(text="🌎Website", url="https://www.orangecrypto.com/")
        button2 = InlineKeyboardButton(text="📜Docs", url="https://docs.orangecrypto.com/")

        # Create the keyboard markup with the buttons
        keyboard_markup = InlineKeyboardMarkup([
            [button1, button2], # This is a row with two buttons
        ])
        await update.message.reply_html(response_text, reply_markup=keyboard_markup)
    else:
        pass

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
    application.add_handler(CommandHandler("orange", command))
    application.add_handler(CommandHandler("gpt", gpt))
    # application.add_handler(CommandHandler("marketcap", command))
    # application.add_handler(CommandHandler("totalsupply", command))
    # application.add_handler(CommandHandler("fullname", command))
    # application.add_handler(CommandHandler("symbol", command))
    # application.add_handler(CommandHandler("volume", command))

    # Run the bot until the user presses Ctrl-C
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
