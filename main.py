import yt_dlp

import asyncio

import discord
from discord.ext import commands
from discord import app_commands

import os

GUILD_ID = discord.Object(id=1325325286371229696)

class AudioDL():
    def __init__(self):
        self.ydl = yt_dlp.YoutubeDL({'format': 'bestaudio', 'outtmpl': '%(title)s.mp3'})
        self.video = None
        self.file_path = "Empty.mp3"

    def get_mp3_link(self, link):
        self.cleanup()

        self.video = self.ydl.extract_info(link, download=True)
        self.file_path = self.ydl.prepare_filename(self.video)
        print(f"downloaded {self.file_path}")

        return self.video

    def get_mp3_q(self, q):
        self.cleanup()

        self.video = self.ydl.download(f"ytsearch:{q}")
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
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            print("deleting " + self.file_path)

class Client_Bot():
    def __init__(self):
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.intents.members = True
        self.intents.voice_states = True
        self.client = discord.Client(intents=self.intents)

        self.GENERAL_CHANNEL_ID = 1325325286807572572

    #def create_bot(self):
    #    return commands.Bot(command_prefix='$', intents=self.intents)

    def get_channel_id(self):
        return self.GENERAL_CHANNEL_ID

    def get_client(self):
        return self.client

client_bot = Client_Bot()
#bot = client_bot.create_bot()
client = client_bot.get_client()
tree = app_commands.CommandTree(client)

mp3create = AudioDL()

#JUST USE APPCOMMANDS WITH CLIENT TREE, USE INTERACTION.CTX
@client.event
async def on_ready():
    await tree.sync(guild=GUILD_ID)
    print("Connected to Server")

'''
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.environ['TOKEN'])

'''
@tree.command(name="join",description="Ninja Joins the VC", guild=GUILD_ID)
async def join(interaction):
    await interaction.response.send_message("Connecting...")
    general_channel = client.get_channel(client_bot.get_channel_id())
    await general_channel.connect()


@tree.command(name="disconnect", description="Ninja leaves", guild=GUILD_ID)
async def disconnect(interaction):
    voice_client = interaction.guild.voice_client

    if voice_client:
        voice_client.stop()
        await voice_client.disconnect()
        await interaction.response.send_message("Disconnecting")

        mp3create.cleanup()
    else:
        await interaction.response.send_message("Not in a Voice Channel")

@tree.command(name="play", description="Ninja Bumps Yo Shit", guild=GUILD_ID)
async def play(interaction, song_title: str):
    voice_client = interaction.guild.voice_client

    if not voice_client:
        general_channel = client.get_channel(client_bot.get_channel_id())
        await general_channel.connect()
        voice_client = interaction.guild.voice_client

    if song_title:
        await interaction.response.send_message("Playing Song")
        mp3create.get_mp3_q(song_title)
        file_path = mp3create.get_file_path()

        audio_file = discord.FFmpegPCMAudio(file_path)

        voice_client.play(audio_file)
    else:
        await interaction.response.send_message("No Song Title")


@tree.command(name="stop", description="Ninja Stops Playing The Song", guild=GUILD_ID)
async def stop(interaction):
    voice_client = interaction.guild.voice_client

    if voice_client:
        await interaction.response.send_message("Stopping Audio...")
        voice_client.stop()
    else:
        await interaction.response.send_message("Not Currently In a Voice Channel")

@tree.command(name="pause", description="Ninja Pauses the Song", guild=GUILD_ID)
async def pause(interaction):
    voice_client = interaction.guild.voice_client

    if voice_client:
        await interaction.response.send_message("Pausing Audio...")
        voice_client.pause()
    else:
        await interaction.response.send_message("Not Currently In a Voice Channel")

@tree.command(name="resume", description="Ninja Resumes the Song", guild=GUILD_ID)
async def resume(interaction):
    voice_client = interaction.guild.voice_client

    if voice_client:
        await interaction.response.send_message("Resuming Audio...")
        voice_client.resume()
    else:
        await interaction.response.send_message("Not Currently In a Voice Channel")

client.run(os.environ['TOKEN'])