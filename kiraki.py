# KOD YAZMAK MÜKEMMEL OLM
import discord
from discord.ext import commands
import random
import asyncio
from discord.ui import Button, View

TOKEN_ENCODED = "TVRJNE9UTXdNVFExTURBeE9EYzROelEyTXcuR2tkUzU0LkxHUzlHYlBheUY0blRwOFFvcThQNllKTVFJNlVuSXVXSkpXb2Q0"
TOKEN = base64.b64decode(TOKEN_ENCODED).decode('utf-8')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='k ', intents=intents, case_insensitive=True)

users_money = {}

def add_money(user_id, amount):
    users_money[user_id] = users_money.get(user_id, 0) + amount

def get_money(user_id):
    return users_money.get(user_id, 0)

@bot.event
async def on_ready():
    print(f'{bot.user.name} hazır! Para kazanma zamanı! 💰')

@bot.command(aliases=['cf', 'coinflip', 'yazitura'])
async def flip(ctx, miktar: int = None):
    user_id = str(ctx.author.id)
    
    if miktar is None:
        embed = discord.Embed(
            title="🎲 Coin Flip Yardım",
            description="**Kullanım:** `k cf [miktar]`\nÖrnek: `k cf 100`",
            color=0x00ff00
        )
        embed.add_field(name="Özellikler", value="- Animasyonlu çevirme\n- Anlık sonuç bildirimi\n- Kazanç hesaplama")
        await ctx.send(embed=embed)
        return
    
    balance = get_money(user_id)
    

    if miktar > balance:
        await ctx.send(f"❌ {ctx.author.mention}, yeterli paran yok! Mevcut bakiyen: {balance} 💰")
        return

    message = await ctx.send(f"🔄 {ctx.author.mention}, para çevriliyor...")
    

    for i in range(3):
        await asyncio.sleep(0.7)
        await message.edit(content=f"🔄 {ctx.author.mention}, para havada... {'🌀'*(i+1)}")
    
 
    result = random.choice(["YAZI", "TURA"])
    coin_image = "https://i.imgur.com/8Km9tLL.png" if result == "YAZI" else "https://i.imgur.com/HMndmJd.png"
    

    if random.random() < 0.495:  # %49.5 kazanma şansı (ev yanı %1)
        add_money(user_id, miktar)
        outcome = f"🎉 Kazandın! +{miktar} 💰"
        color = 0x00ff00
    else:
        add_money(user_id, -miktar)
        outcome = f"😢 Kaybettin! -{miktar} 💰"
        color = 0xff0000
    
  
    embed = discord.Embed(
        title=f"Sonuç: {result}",
        description=f"{outcome}\nYeni bakiyen: {get_money(user_id)} 💰",
        color=color
    )
    embed.set_thumbnail(url=coin_image)
    embed.set_footer(text=f"Oynayan: {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
    
 
    await message.edit(content=None, embed=embed)


@bot.command(aliases=['b'])
async def bakiye(ctx):
    user_id = str(ctx.author.id)
    embed = discord.Embed(
        title="💰 Cüzdan Bilgisi",
        description=f"{ctx.author.mention}, mevcut bakiyen: **{get_money(user_id)}** 💰",
        color=0xffd700
    )
    embed.set_thumbnail(url="https://i.imgur.com/5kyyK1P.png")
    await ctx.send(embed=embed)


@bot.command(aliases=['g', 'gunluk'])
async def daily(ctx):
    user_id = str(ctx.author.id)
    bonus = random.randint(80, 150)
    
 
    msg = await ctx.send(f"🎁 {ctx.author.mention}, günlük ödülün hazırlanıyor...")
    await asyncio.sleep(1.5)
    
    add_money(user_id, bonus)
    embed = discord.Embed(
        title="🎉 Günlük Ödül!",
        description=f"{ctx.author.mention}, **{bonus}** 💰 kazandın!\nYeni bakiyen: **{get_money(user_id)}** 💰",
        color=0x00ff00
    )
    embed.set_thumbnail(url="https://i.imgur.com/5kyyK1P.png")
    await msg.edit(content=None, embed=embed)

bot.run(TOKEN)
