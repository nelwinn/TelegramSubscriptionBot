import os
from dotenv import load_dotenv
from telethon import Button
load_dotenv()

#Authentication details
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
BOT_OWNER = os.getenv("BOT_OWNER")
DATABASE_NAME = os.getenv("DATABASE_NAME")

#Message settings - feel free to edit contents according to your needs.

START_MESSAGE = """
🤖 Hey hey, {}, welcome to (your business name) deal sourcing platform!

Introducing (your business name), your ultimate data-powered platform for discovering unlisted crypto projects and streamlining your sales prospecting process. Our AI-driven technology scours the web to uncover the most innovative startups and cutting-edge technologies before they hit the token market, providing you with a competitive edge in the fast-paced world of investment.

🌐Website: (your website)
📺Socials:(your socials)
Let's get you started!
"""

MENU_BUTTONS = [[Button.text("Subscribe", single_use=True, resize=True)],
                [Button.text("Unsubscribe")],
                [Button.text("Notification Customization")],
                [Button.text("Feedback"), Button.text("Direct Contact")]]

NOTIFICATION_CUSTOMIZATION_OPTIONS = [[Button.text("Edit your details", single_use=True, resize=True)],
                                      [Button.text("Edit Notification Preferences")]]
#when clicking notification customization, show another button to edit their stored details

DASHBOARD_BUTTONS = [[Button.text("Broadcast Message", single_use=True, resize=True)]]
CREATER_ONLY_BUTTONS = [[Button.text("Add admin"), Button.text("Remove admin")],
                        [Button.text("Generate Token")],
                        [Button.text("Generate backend CSV")]]
