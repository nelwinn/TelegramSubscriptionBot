import os
from dotenv import load_dotenv
load_dotenv()

#Authentication details
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

#Message settings - feel free to edit contents according to your needs.
START_MESSAGE = """
🤖 Hey hey, {}, welcome to (your business name) deal sourcing platform!

Introducing (your business name), your ultimate data-powered platform for discovering unlisted crypto projects and streamlining your sales prospecting process. Our AI-driven technology scours the web to uncover the most innovative startups and cutting-edge technologies before they hit the token market, providing you with a competitive edge in the fast-paced world of investment.

🌐Website: (your website)
📺Socials:(your socials)
Let's get you started!
"""