import discord
from discord.ext import commands
from discord.ui import Select, View
from utils.game import start_game, shoot_game, game_in_progress, shooting_count

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
        if game_in_progress():
            await interaction.response.send_message("⚠️ 현재 보급을 받을 수 없는 상황입니다.", ephemeral=True)
            return

        item = self.values[0]
        result = self.determine_result(item)
        embed = self.create_embed(interaction, item, result)
        await interaction.response.send_message(embed=embed)

        if "비둘기가 날아옵니다" in result:
            await start_game(interaction)

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

# Cog
class Supply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="보급")
    async def 보급(self, interaction: discord.Interaction):
        if game_in_progress():
            await interaction.response.send_message("⚠️ 현재 보급을 받을 수 없는 상황입니다.", ephemeral=True)
            return
        await interaction.response.send_message("아이템을 선택하세요:", view=SupplyView(), ephemeral=True)

    @commands.command(name="사격")
    async def 사격(self, interaction: discord.Interaction):
        await shoot_game(interaction)

# Cog 로드 
async def setup(bot):
    await bot.add_cog(Supply(bot))
