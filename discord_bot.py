from discord import Intents
from discord.ext import commands
from discord.ui import Button, View
from time import sleep
from dialog_flow import dialog_flow
from cmcApi import fetch_api
import os
import dotenv
dotenv.load_dotenv()

TOKEN = os.getenv("DC_TOKEN")
CHANNEL_ID = 1202305750425141342

bot = commands.Bot(command_prefix='!', intents=Intents.all())
isSent = False

class LinkView(View):
    def __init__(self):
        super().__init__()
        # Add a button with a label and a URL
        self.add_item(Button(label="🌎Website", url="https://www.orangecrypto.com/"))
        self.add_item(Button(label="📜Docs", url="https://docs.orangecrypto.com/"))

@bot.event
async def on_message(message):
    global isSent
    content = str(message.content)
    if not isSent:
        if content.startswith("/orange"):
            inputData = content.removeprefix("/orange")
            inputData = inputData.replace("marketcap", "market cap").replace("totalsupply", "total supply").replace("fullname", "full name")
            tokenName, intent, fulfillmentText = dialog_flow(inputData)
            if intent == "Tradingvolume":
                intent = "Volume"
            if intent == "Totalsupply":
                intent = "TotalSupply"
            if intent == "Marketcapitalization":
                intent = "Capitalization"
            if tokenName:
                if message:
                    try:
                        info = fetch_api(tokenName, intent)
                        if intent=="Price" or intent =="TotalSupply" or intent=="Capitalization" or intent =="Volume":
                            answer = fulfillmentText.replace("{" + f"Asset{intent}" + "}.", str(info)) + " USD."
                        else:
                            answer = fulfillmentText.replace("{" + f"Asset{intent}" + "}.", str(info)) + "."
                        response_text = f"{answer}"
                        isSent = True
                        # await message.channel.send(response_text)
                        certification = "Powered by the Orange Assistant and made by Orange."
                        await message.channel.send(f"{response_text}\n\n{certification}", view=LinkView())
                    except:
                        pass
                else:
                    pass
        else:
            pass
    else:
        isSent = False

if __name__ == "__main__":
    bot.run(TOKEN)
