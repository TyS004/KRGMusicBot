import yt_dlp

import discord
from discord.ext import commands

import os

class AudioDL():
    def __init__(self):
        self.ydl = yt_dlp.YoutubeDL({'format': 'bestaudio', 'outtmpl': '%(title)s.mp3'})
        self.video = None
        self.file_path = ""

    def get_mp3_link(self, link):
        self.cleanup()

        self.video = self.ydl.extract_info(link, download=True)
        self.file_path = self.ydl.prepare_filename(self.video)
        print(f"downloaded {self.file_path}")

        return self.video

    def get_mp3_q(self, q):
        self.cleanup()

        self.video = self.ydl.extract_info(f"ytsearch:{q}", download=True)
        for data in os.walk('D:\Python Projects\DiscordBot'):  # where to start searching
            dir_path, folders, files = data

            for f in files:
                if f.lower().endswith('.mp3'):
                    self.file_path = os.path.join(dir_path, f)
        print(f"downloaded {self.file_path}")

        return self.video

    def get_file_path(self):
        return self.file_path

    def cleanup(self):
        if os.path.exists('D:\Python Projects\DiscordBot\\' + self.file_path):
            os.remove(self.file_path)

class Client_Bot():
    def __init__(self):
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.intents.voice_states = True

        self.GENERAL_CHANNEL_ID = 1325325286807572572

    def create_bot(self):
        return commands.Bot(command_prefix='$', intents=self.intents)

    def get_channel_id(self):
        return self.GENERAL_CHANNEL_ID

client_bot = Client_Bot()
bot = client_bot.create_bot()

@bot.event
async def on_ready():
    print("Bot is up and ready")

@bot.command()
async def connect(ctx):
    await ctx.send("Connecting...")
    general_channel = bot.get_channel(client_bot.get_channel_id())
    await general_channel.connect()

@bot.command()
async def disconnect(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Not in Voice Channel")

@bot.command()
async def play(ctx, args=None):
    if args:
        if ctx.voice_client:
            mp3create = AudioDL()

            song = mp3create.get_mp3_q(args)
            file_path = mp3create.get_file_path()

            audio_file = discord.FFmpegPCMAudio(file_path)

            ctx.voice_client.play(audio_file)

            await ctx.send("Playing " + song['title'])
        else:
            await ctx.send("Not currently in Voice Channel.")
    else:
        await ctx.send("No Song Title")

bot.run(os.environ['TOKEN'])
