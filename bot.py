
import asyncio
from telethon.tl.types import PeerUser
from telethon import TelegramClient, events, Button
from funcs import *
from config import *

async def main():
    bot = await TelegramClient('botsession', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
    async with bot:
        print('Bot connected.')
        print(await bot.get_me())

        @bot.on(events.NewMessage(func=lambda e:e.is_private, pattern= "/start"))
        async def on_start(event):
            if user_is_active(event.sender.id):
                return show_menu(event)
            await bot.send_message(event.sender.id, "Welcome to bet tips bot! Get started to see daily tips for soccer/basketball sports",
                                   buttons=[[Button.text("Get started")]])
            
        @bot.on(events.NewMessage(pattern="Get Started"))
        async def handle_new_user(event):
            """
            Each questions mentioned below can be edited/deleted/added according to your needs.
            Make sure to update the variable names also to avoid confusion.
            Example: to add a new question, add following lines:
                age = await conv.send_message("Enter your age": )
                age = (await conv.get_response()).text
            Also make sure to add 'age' in the call to store_details function at the end:
                success = await store_details({"user_id": event.sender.id, "age": age,
                                                    .....
                                                    .....
                                                })
            """
            #Ask questions and store them to database
            async with bot.conversation(PeerUser(event.sender.id), timeout=1500) as conv:
                await conv.send_message("Please enter your Name: ")
                name = (await conv.get_response()).text

                await conv.send_message("Please enter your Fund name: ")
                fund_name = (await conv.get_response()).text

                await conv.send_message("Please enter your Fund website: ")
                fund_website = (await conv.get_response()).text

                await conv.send_message("Please enter your Fund size: ")
                fund_size = (await conv.get_response()).text

                await conv.send_message("Please enter your Stage of Invest: ")
                stage_of_invest = (await conv.get_response()).text

                await conv.send_message("Please enter your Preferred deal type (Tokens/Equity): ")
                preferred_deal = (await conv.get_response()).text

                await conv.send_message("Please enter your Check Size: ")
                check_size = (await conv.get_response()).text

                #Call to store_details function
                success = await store_details({"user_id": event.sender.id, "fund_name": fund_name,
                                     "fund_website": fund_website, "fund_size": fund_size,
                                     "stage_of_invest": stage_of_invest, "preferred_deal": preferred_deal,
                                     "check_size": check_size, "name": name})
                if success:
                    await conv.send_message("Your details are successfully stored.",
                                            buttons=[[Button.text("Menu ➡️")]])
                else:
                    await conv.send_message("Something went wrong. Please try again: /start")    
        
        @bot.on(events.NewMessage(pattern="Menu"))
        async def show_menu(event):
            await bot.send_message("Select an option below: ", buttons=MENU_BUTTONS)

        @bot.on(events.NewMessage(pattern="Subscribe"))
        async def subscribe(event):
            async with bot.conversation(event.sender.id, timeout=1500) as conv:
                await conv.send_message("Enter your token for access: ")
                token = (await conv.get_response()).text
                response = await add_subscription(token, event.sender.id)
                await conv.send_message(response, buttons=[[Button.text("Menu ➡️")]])
        @bot.on(events.NewMessage(pattern="Unsubscribe"))
        async def unsubscribe(event):
            await remove_subscription(event.sender.id)
            await bot.send_message(event.sender.id, "Your subscription is removed.",buttons=[[Button.text("Menu ➡️")]])
        await bot.run_until_disconnected()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())