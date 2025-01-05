import os

import discord
from discord.ext import commands

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

intents = discord.Intents.default()

intents.message_content = True
intents.voice_states = True

GENERAL_CHANNEL_ID = 1325325286807572572

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print("Bot is up and ready")

@bot.command()
async def connect(ctx):
    await ctx.send("Connecting...")
    general_channel = bot.get_channel(GENERAL_CHANNEL_ID)
    await general_channel.connect()

@bot.command()
async def disconnect(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Not currently in Voice Channel.")

@bot.command()
async def play(ctx):
    if ctx.voice_client:
        audio_file = discord.FFmpegPCMAudio("20 (Instrumental).mp3")
        await ctx.voice_client.play(audio_file)
    else:
        await ctx.send("Not currently in Voice Channel.")

bot.run(os.environ['TOKEN'])
