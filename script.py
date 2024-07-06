from telegram import Bot
import asyncio
import os
from dotenv import load_dotenv
import requests

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TOKEN_MERCADO_LIVRE = os.environ.get('TOKEN_MERCADO_LIVRE')
CHAT_ID = os.environ.get('CHAT_ID')
bot = Bot(token=TELEGRAM_BOT_TOKEN)

PRODUCTS_TO_SEARCH = [
    {
      "product": "rtx 3070",
      "max-price": 1600,
      "min-price": 1000,
      "avoid": ["3070m", "com defeito", "tem defeito", "sem video"]
    }
  ]


async def send_message_telegram(message: str):
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML', disable_web_page_preview=True)


async def start_is_bot_online():
    while True:
        await send_message_telegram('Bot is online')
        await asyncio.sleep(60 * 60 * 3)


async def start_search_product():
    while True:
        await run()
        await asyncio.sleep(60 * 5)


async def run():


  for product in PRODUCTS_TO_SEARCH:
    response = requests.get('https://api.mercadolibre.com/sites/MLB/search', params={
      "q": product["product"],
      "price": f'{product["min-price"]}-{product["max-price"]}'
    },
                            headers={
                              'Authorization': f'Bearer Token {TOKEN_MERCADO_LIVRE}'
                            })
    

    for item in response.json()["results"]:
      title = item["title"]
      price = item["price"]
      link = item["permalink"]
      
      names_product = [str(attribute["value_name"]) for attribute in item["attributes"]]

      second_filter_product = any(product["product"].lower() in name.lower()  for name in names_product)

      contains_substring_to_avoid = any(word_to_avoid.lower() in title.lower() for word_to_avoid in product["avoid"])
      
      if second_filter_product and not contains_substring_to_avoid and item["accepts_mercadopago"] and item["currency_id"] == "BRL":
        message = f"""
        <b>{title}</b> for <b>{price}</b>, <a href="{link}">Click to redirect</a>
        """
        await send_message_telegram(message)
      
    await asyncio.sleep(5)
    

async def main():
    task1 = asyncio.create_task(start_is_bot_online())
    task2 = asyncio.create_task(start_search_product())
    await asyncio.gather(task1, task2)


if __name__ == "__main__":
  asyncio.run(main())
    
    

  


