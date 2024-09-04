import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import Select, View
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os

# .env 파일의 환경 변수 로드
load_dotenv()

# 환경 변수에서 토큰 가져오기
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 전역 변수 선언
shooting_count = 0
countdown_task = None
channel_id = None  # 메시지를 보낼 채널 ID를 저장하기 위한 변수
game_in_progress = False  # 미니게임 진행 여부를 확인하기 위한 변수

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} 보급봇 연결완료!')
    print('------')

class SupplySelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="포도당 캔디", description="체력을 [20] 회복"),
            discord.SelectOption(label="증폭제", description="보유한 모든 특수효과의 잔여 횟수 +1"),
            discord.SelectOption(label="진정제", description="보유한 모든 특수효과의 잔여 횟수 삭제"),
            discord.SelectOption(label="연막탄", description="직전에 입은 피해량 무효화"),
            discord.SelectOption(label="섬광탄", description="다음 라운드 턴 추가"),
            discord.SelectOption(label="통조림 스튜", description="체력을 [자연회복량] 회복"),
            discord.SelectOption(label="옥수수캔", description="최대 체력까지 회복"),
            discord.SelectOption(label="커피", description="최대 체력을 1회 분량 복구"),
        ]
        super().__init__(placeholder="/보급 커맨드 전송 후 희망하는 아이템을 선택하세요", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        global countdown_task, channel_id, game_in_progress

        # 미니게임이 이미 진행 중이라면 경고 메시지 출력
        if game_in_progress:
            await interaction.response.send_message("⚠️ 현재 보급을 받을 수 없는 상황입니다.", ephemeral=True)
            return

        item = self.values[0]
        result = self.determine_result(item)
        embed = self.create_embed(interaction, item, result)
        await interaction.response.send_message(embed=embed)

        if "비둘기가 날아옵니다" in result:
            # 미니게임 시작
            embed = discord.Embed(
                title="경고!",
                description="10분 내로 10명이 '/사격'을 실행하지 않으면 오늘 받은 아이템이 전부 소멸합니다! 단, 사격한 사람들은 오늘 배급받은 아이템이 소멸됩니다.",
                color=0xFF0000
            )
            await interaction.followup.send(embed=embed)

            # 채널 ID 저장
            channel_id = interaction.channel_id

            # 미니게임 상태 설정
            game_in_progress = True

            # 10분 타이머 시작
            shooting_count = 0
            countdown_task = bot.loop.create_task(self.countdown())

    async def countdown(self):
        global game_in_progress

        # 10분(600초) 대기
        await asyncio.sleep(600)

        global shooting_count, channel_id
        channel = bot.get_channel(channel_id)
        
        if shooting_count < 10:
            embed = discord.Embed(
                title="🕊️헤카텀이 찾아왔습니다!",
                description="오늘 받은 보급품이 전부 소멸합니다.",
                color=0xFF0000
            )
            await channel.send(embed=embed)
        
        # 미니게임 종료
        shooting_count = 0  # 초기화
        channel_id = None  # 채널 ID 초기화
        game_in_progress = False  # 미니게임 상태 초기화


    def determine_result(self, item: str) -> str:
        roll = random.random()
        if item == "포도당 캔디":
            if roll < 0.4:
                return "수령 실패"
            elif roll < 0.9:
                return f"{item} 수령 성공"
            else:
                return f"🕊️멀리서 비둘기가 날아옵니다... 불길한 예감이 듭니다."
        if item == "증폭제":
            if roll < 0.5:
                return "수령 실패"
            elif roll < 0.9:
                return f"{item} 수령 성공"
            else:
                return f"🕊️멀리서 비둘기가 날아옵니다... 불길한 예감이 듭니다."
        if item == "진정제":
            if roll < 0.4:
                return "수령 실패"
            elif roll < 0.9:
                return f"{item} 수령 성공"
            else:
                return f"🕊️멀리서 비둘기가 날아옵니다... 불길한 예감이 듭니다."
        if item == "연막탄":
            if roll < 0.5:
                return "수령 실패"
            elif roll < 0.9:
                return f"{item} 수령 성공"
            else:
                return f"🕊️멀리서 비둘기가 날아옵니다... 불길한 예감이 듭니다."
        if item == "섬광탄":
            if roll < 0.5:
                return "수령 실패"
            elif roll < 0.9:
                return f"{item} 수령 성공"
            else:
                return f"🕊️멀리서 비둘기가 날아옵니다... 불길한 예감이 듭니다."
        if item == "통조림 스튜":
            if roll < 0.5:
                return "수령 실패"
            elif roll < 0.9:
                return f"{item} 수령 성공"
            else:
                return f"🕊️멀리서 비둘기가 날아옵니다... 불길한 예감이 듭니다."
        if item == "옥수수캔":
            if roll < 0.5:
                return "수령 실패"
            elif roll < 0.9:
                return f"{item} 수령 성공"
            else:
                return f"🕊️멀리서 비둘기가 날아옵니다... 불길한 예감이 듭니다."
        if item == "커피":
            if roll < 0.5:
                return "수령 실패"
            elif roll < 0.9:
                return f"{item} 수령 성공"
            else:
                return f"🕊️멀리서 비둘기가 날아옵니다... 불길한 예감이 듭니다."
        else:
            return f"{item} 수령 성공" 

    def create_embed(self, interaction: discord.Interaction, item: str, result: str) -> discord.Embed:
        embed = discord.Embed(title="보급 결과", color=0x00B9C1)
        embed.add_field(name="날짜", value=datetime.now().strftime("%Y-%m-%d"), inline=False)
        embed.add_field(name="이름", value=interaction.user.display_name, inline=False)
        embed.add_field(name="요청", value=item, inline=False)
        embed.add_field(name="보급 안내", value=result, inline=False)
        return embed

class SupplyView(View):
    def __init__(self):
        super().__init__()
        self.add_item(SupplySelect())

@bot.tree.command(name="보급", description='희망하는 아이템을 선택합니다.')
async def 보급(interaction: discord.Interaction):
    global game_in_progress

    # 미니게임이 진행 중이라면 /보급 사용 불가
    if game_in_progress:
        await interaction.response.send_message("⚠️ 현재 보급을 받을 수 없는 상황입니다.", ephemeral=True)
        return

    await interaction.response.send_message("아이템을 선택하세요:", view=SupplyView(), ephemeral=True)

@bot.tree.command(name="사격", description='언젠가 쓸 곳이 있을지도...?')
async def 사격(interaction: discord.Interaction):
    global shooting_count, countdown_task, game_in_progress

    if countdown_task is None:
        await interaction.response.send_message("현재 사격이 필요한 상황이 아닙니다.")
        return

    shooting_count += 1
    await interaction.response.send_message(f"🕊️비둘기가 총에 스쳤습니다. 현재 사격 횟수는 {shooting_count}/10 입니다!")

    if shooting_count >= 10:
        # 사격 횟수가 10에 도달하면 즉시 미니게임 종료
        countdown_task.cancel()  # 카운트다운 작업 취소
        embed = discord.Embed(
            title="🕊️비둘기가 떨어졌습니다!",
            description="다행히 천사가 찾아오지 않았습니다.",
            color=0x00FF00
        )
        shooting_count = 0  # 초기화
        channel = bot.get_channel(channel_id)
        await channel.send(embed=embed)
        channel_id = None  # 채널 ID 초기화
        game_in_progress = False  # 미니게임 상태 초기화

bot.run(DISCORD_TOKEN)