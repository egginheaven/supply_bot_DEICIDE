import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Cog 로드
bot.load_extension('cogs.supply')

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} 보급봇 연결완료!')
    print('------')

bot.run(DISCORD_TOKEN)
