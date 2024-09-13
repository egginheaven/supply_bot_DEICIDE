import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# .env 불러오기
load_dotenv()

# 환경 변수에서 토큰 가져오기
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Cog 로드
bot.load_extension('cogs.supply')

# 봇 준비 완료시 호출되는 이벤트
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} 보급봇 연결완료!')
    print('------')

# 봇 실행
bot.run(DISCORD_TOKEN)
