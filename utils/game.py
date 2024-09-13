import discord
import asyncio

# 게임 상태 변수들
shooting_count = 0
countdown_task = None
channel_id = None
_game_in_progress = False

# 미니게임 진행 여부 체크
def game_in_progress():
    return _game_in_progress

# 게임 시작 함수
async def start_game(interaction: discord.Interaction):
    global countdown_task, channel_id, _game_in_progress

    channel_id = interaction.channel_id
    _game_in_progress = True

    embed = discord.Embed(
        title="경고!",
        description="10분 내로 10명이 '/사격'을 실행하지 않으면 오늘 받은 아이템이 전부 소멸합니다!",
        color=0xFF0000
    )
    await interaction.followup.send(embed=embed)

    countdown_task = asyncio.create_task(countdown(interaction))

# 카운트다운 및 게임 종료 로직
async def countdown(interaction: discord.Interaction):
    global _game_in_progress, shooting_count, channel_id

    await asyncio.sleep(600)  # 10분 대기
    channel = interaction.guild.get_channel(channel_id)

    if shooting_count < 10:
        embed = discord.Embed(
            title="🕊️헤카텀이 찾아왔습니다!",
            description="오늘 받은 보급품이 전부 소멸합니다.",
            color=0xFF0000
        )
        await channel.send(embed=embed)

    # 상태 초기화
    shooting_count = 0
    channel_id = None
    _game_in_progress = False

# 사격 명령어 처리 함수
async def shoot_game(interaction: discord.Interaction):
    global shooting_count, countdown_task, _game_in_progress

    if countdown_task is None:
        await interaction.response.send_message("현재 사격이 필요한 상황이 아닙니다.")
        return

    shooting_count += 1
    await interaction.response.send_message(f"🕊️비둘기가 총에 스쳤습니다. 현재 사격 횟수는 {shooting_count}/10 입니다!")

    if shooting_count >= 10:
        countdown_task.cancel()
        channel = interaction.guild.get_channel(channel_id)
        embed = discord.Embed(
            title="🕊️비둘기가 떨어졌습니다!",
            description="다행히 천사가 찾아오지 않았습니다.",
            color=0x00FF00
        )
        await channel.send(embed=embed)

        # 상태 초기화
        shooting_count = 0
        channel_id = None
        _game_in_progress = False
