import discord
from discord.ext import commands
import os
import yt_dlp  # <-- This is what you're missing


# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Enable access to message content

# Create the bot with intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I'm your bot 😊")

@bot.command()
async def siddhant(ctx):
    await ctx.send("Madahchod hai siddhant")

@bot.command()
async def join(ctx):
    """Joins the voice channel you're in."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined {channel.name}!")
    else:
        await ctx.send("You must be in a voice channel for me to join!")

@bot.command()
async def leave(ctx):
    """Leaves the voice channel the bot is in."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")

@bot.command()
async def play(ctx, *, search: str):
    vc = ctx.voice_client
    if not vc:
        if ctx.author.voice:
            vc = await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You're not in a voice channel.")
            return

    await ctx.send(f"🔍 Searching for: `{search}`...")

    ydl_opts = {
        'cookiefile': 'cookies.txt',  # <-- Valid cookies file
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search, download=False)
            url = info['entries'][0]['url'] if 'entries' in info else info['url']
            title = info['entries'][0]['title'] if 'entries' in info else info['title']

        source = await discord.FFmpegOpusAudio.from_probe(url, method='fallback')

        vc.stop()  # Stop current audio if any
        vc.play(source)

        await ctx.send(f"🎶 Now playing: **{title}**")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

# Replace with your bot token
bot.run(os.environ["DISCORD_TOKEN"])
