import discord
from discord.ui import Button, View
from discord.ext import commands
from discord.utils import get
import sqlite3
from colorama import Back, Fore, Style
import time

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
token = "DiscordBotToken" # 디스코드봇 토큰  넣으세요~

@bot.event
async def on_ready():
    prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print(prfx + '로그인 완료. : ' + Fore.YELLOW + bot.user.name)
    print(prfx + '제작 : By. Amazon Developer Godkong ' + Fore.CYAN)
    print(prfx + 'Running Discord Version : ' + Fore.BLUE + discord.__version__)
    print(prfx + Fore.YELLOW + 'Connect Sqlite3 is Complate')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("AMAZON MAIN SYSTEM 관리"))

@bot.command()
@commands.has_permissions(administrator=True)
async def 사전예약(ctx):
    button1 = Button(label="✨ 사전예약 하기", style=discord.ButtonStyle.green)

    async def button_callback1(interaction):
        role = discord.utils.get(ctx.guild.roles, name="✨ㆍ사전예약자")
        await interaction.user.add_roles(role)

        conn = sqlite3.connect('RESERVATION.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS RESERVATIONS (discord_id TEXT)")
        discord_id = interaction.user.id

        cursor.execute("SELECT * FROM RESERVATIONS WHERE discord_id=?", (discord_id,))
        result = cursor.fetchone()

        if result:
            embed = discord.Embed(title="❌ 사전예약 실패", description=f"{interaction.user.mention}님, 이미 사전예약을 하셨습니다. 중복 사전예약은 불가능합니다.", color=discord.Color.red())
            await interaction.user.send(embed=embed)
        else:
            embed = discord.Embed(title="✅ 사전예약 완료", description=f"{interaction.user.mention}님, 사전예약이 완료되었습니다.", color=discord.Color.green())
            await interaction.user.send(embed=embed)


            cursor.execute("INSERT INTO RESERVATIONS (discord_id) VALUES (?)", (discord_id,))
            conn.commit()

            log_channel = bot.get_channel(1180160421316010124)
            embed = discord.Embed(title="✅ 사전예약 완료", description=f"사전예약이 완료된 사용자 정보입니다.", color=discord.Color.green())
            embed.add_field(name="디스코드 이름", value=interaction.user.mention, inline=False)
            embed.add_field(name="디스코드 아이디", value=interaction.user.id, inline=False)
            embed.add_field(name="커스텀 아이디", value=interaction.user.name, inline=False)
            await log_channel.send(embed=embed)


        conn.close()

    button1.callback = button_callback1

    view = View()
    view.add_item(button1)

    await ctx.send("@everyone", embed=discord.Embed(
        title='AMAZON 사전예약',
        description="**아래에 있는 버튼을 눌러 아마존 사전예약에 참여하세요.**\n\n[ 사전예약 안내사항 ]\n\n- 먼저 사전예약을 하시면 중복 사전예약이 불가능합니다. ( 서버 디코 나갔다 들어와도 불가능. )\n- 인게임에서 사전예약 비콘에서 E키를 눌러 사전예약 보상을 받으실 수 있습니다.\n- 사전예약 비콘은 서버 오픈 후 1주일 뒤에 비활성화됩니다. ( 못 받을 시 본인 책임. )\n- 사전예약을 완료하시면 봇에게 개인DM 으로 알림이 옵니다. 봇에게 알림이 안온다면 개인정보설정 -> 다이렉트 메세지 에서 허용해주세요 !",
        colour=discord.Colour.green()
    ), view=view)
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="❌ 명령어 사용불가!", description=f"** {ctx.author.mention} 님 해당 명령어는 아마존 관리팀, 운영팀만 사용이 가능한 명령어입니다. **", color = discord.Color.dark_red())
        await ctx.send(embed=embed)
        # await ctx.send(f'{ctx.author.mention} **이 명령어는 관리자만 사용할 수 있습니다.**')
    else:
        raise error

bot.run(token)
