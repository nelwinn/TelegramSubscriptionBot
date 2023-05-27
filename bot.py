
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
            if await user_is_active(event.sender.id):
                return await show_menu(event)
            await bot.send_message(event.sender.id, START_MESSAGE,
                                   buttons=[[Button.text("Get Started", resize=True)]])
            
        @bot.on(events.NewMessage(pattern="Get Started"))
        async def handle_new_user(event, existing_user=False):
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

                await conv.send_message("Please enter your Preferred deal type (Tokens/Equity): ",
                                        buttons=[[Button.text("Tokens", single_use=True, resize=True)],
                                                 [Button.text("Equity")]])
                preferred_deal = (await conv.get_response()).text
                if not preferred_deal in ("Equity", "Tokens"):
                    return await conv.send_message("Preferred deal type must be either 'Tokens' or 'Equity'.\n\nTry again /start")
                
                await conv.send_message("Please enter your Check Size: ")
                check_size = (await conv.get_response()).text

                #Call to store_details function
                success = await store_details({"user_id": event.sender.id, "fund_name": fund_name,
                                     "fund_website": fund_website, "fund_size": fund_size,
                                     "stage_of_invest": stage_of_invest, "preferred_deal": preferred_deal,
                                     "check_size": check_size, "name": name}, existing_user=existing_user)
                if success:
                    await conv.send_message("Your details are successfully stored.",
                                            buttons=[[Button.text("Menu ➡️")]])
                else:
                    await conv.send_message("Something went wrong. Please try again: /start")    
        
        @bot.on(events.NewMessage(pattern="Menu"))
        async def show_menu(event):
            await bot.send_message(event.sender.id, "Select an option below: ", buttons=MENU_BUTTONS)

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
        
        @bot.on(events.NewMessage(pattern="Notification Customization"))
        async def notification_customisation(event):
            await bot.send_message(event.sender.id, "Select an option below: ",buttons=NOTIFICATION_CUSTOMIZATION_OPTIONS)

        @bot.on(events.NewMessage(pattern="Edit your details"))
        async def edit_user_details(event):
            await handle_new_user(event, existing_user=True)

        @bot.on(events.NewMessage(pattern="Edit Notification Preferences"))
        async def edit_preferences(event):
            async with bot.conversation(event.sender.id, timeout=1500) as conv:
                await conv.send_message("Enter the number of notifications you would like to receive daily: ")
                num = (await conv.get_response()).text
                if not num.isdigit():
                    await update_notif_preferences(event.sender.id, num)
                    await conv.send_message("Succesfully updated your preferences.")
        
        @bot.on(events.NewMessage(pattern="/dashboard"))
        async def admin_dashboard(event):
            admins = [x['username'] for x in await get_all_admins()]
            if not event.sender.username in admins:
                if (not event.sender.id in admins):
                    return await event.reply("Not authorized")
            buttons = CREATER_ONLY_BUTTONS + DASHBOARD_BUTTONS if event.sender.username == BOT_OWNER else DASHBOARD_BUTTONS
            await bot.send_message(event.sender.id, "Welcome to Admin dashboard.", buttons=buttons)

        @bot.on(events.NewMessage(pattern="Broadcast Message"))
        async def broadcast_message(event):
            async with bot.conversation(event.sender.id) as conv:
                await conv.send_message("Send the exact message to be broadcasted (It can be any type of telegram message): ")
                message = await conv.get_response()
                await conv.send_message("Sure to send the above message to all users?",
                                        buttons=[[Button.text("Yes", resize=True), Button.text("No")]])
                if (await conv.get_response()).text == "Yes":
                    users = [x['user_id'] for x in await get_all_users()]
                    for user in users:
                        try:
                            await bot.send_message(PeerUser(int(user)), message)
                        except:
                            print("Could not message", user)
        @bot.on(events.NewMessage(pattern="Generate Token"))
        async def gen_token(event):
            #Add feature to specify expiry time
            token = await generate_new_token()
            await event.reply(token)
        await bot.run_until_disconnected()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())