import yt_dlp

import discord
from discord.ext import commands
from discord import app_commands

import os

#SERVER CONSTANTS
VOICE_CHANNEL_ID = 1325325286807572572
GUILD_ID = 1325325286371229696

#AUDIO DOWNLOAD CLASS IMPLEMENTATION FOR YTDL
class AudioDL():
    def __init__(self):
        self.ydl = yt_dlp.YoutubeDL({'format': 'bestaudio', 'outtmpl': '%(title)s.mp3', 'playlist_items' : '1'})
        self.video = None
        self.file_path = "Empty.mp3"

    def get_mp3_link(self, link):
        self.cleanup()

        self.video = self.ydl.extract_info(link, download=True)
        #self.file_path = self.ydl.prepare_filename(self.video)
        #print(f"downloaded {self.file_path}")
        for data in os.walk('D:\Python Projects\DiscordBot'):  # where to start searching
            dir_path, folders, files = data

            for f in files:
                if f.lower().endswith('.mp3'):
                    self.file_path = os.path.join(dir_path, f)
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


#DISCORD BOT CLIENT CLASS IMPLEMENTATION
class Client_Bot():
    def __init__(self):
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.intents.members = True
        self.intents.voice_states = True

        self.client = discord.Client(intents=self.intents)

        self.mp3_create = AudioDL()

        self.GENERAL_CHANNEL_ID = VOICE_CHANNEL_ID
        self.GUILD_ID = discord.Object(id=GUILD_ID)

    def get_channel_id(self):
        return self.GENERAL_CHANNEL_ID

    def get_guild_id(self):
        return self.GUILD_ID

    def get_client(self):
        return self.client

    def get_mp3_create(self):
        return self.mp3_create

    def set_audio_file(self, audio_file):
        self.audio_file = audio_file

    def get_audio_file(self):
        return self.audio_file

#MAIN SECTION

client_bot = Client_Bot()

client = client_bot.get_client()
tree = app_commands.CommandTree(client)

MAX_QUERY_LENGTH = 75

#COMMANDS

@client.event
async def on_ready():
    await tree.sync(guild=client_bot.get_guild_id())
    print("Connected to Server")

@tree.command(name="join",description="Ninja Joins the VC", guild=client_bot.get_guild_id())
async def join(interaction):
    await interaction.response.send_message("Connecting...")
    general_channel = client.get_channel(client_bot.get_channel_id())
    await general_channel.connect()

@tree.command(name="disconnect", description="Ninja leaves", guild=client_bot.get_guild_id())
async def disconnect(interaction):
    voice_client = interaction.guild.voice_client

    if voice_client:
        client_bot.get_audio_file().cleanup()
        voice_client.stop()

        await voice_client.disconnect()
        await interaction.response.send_message("Disconnecting")

        client_bot.get_mp3_create().cleanup()
    else:
        await interaction.response.send_message("Not in a Voice Channel")

@tree.command(name="play", description="Ninja Bumps Yo Shit", guild=client_bot.get_guild_id())
async def play(interaction, song_title: str):
    voice_client = interaction.guild.voice_client

    if not voice_client:
        general_channel = client.get_channel(client_bot.get_channel_id())
        await general_channel.connect()
        voice_client = interaction.guild.voice_client

    if len(song_title) < MAX_QUERY_LENGTH:
        await interaction.response.send_message("Playing Song")

        if voice_client.is_playing():
            client_bot.get_audio_file().cleanup()
            voice_client.stop()

        if song_title.__contains__("youtube"):
            client_bot.get_mp3_create().get_mp3_link(song_title)
            print("Already Link")
        else:
            client_bot.get_mp3_create().get_mp3_link('https://music.youtube.com/search?q=' + song_title.replace(" ", "+"))
            print("Converted to Link")

        file_path = client_bot.get_mp3_create().get_file_path()

        client_bot.set_audio_file(discord.FFmpegPCMAudio(file_path))

        voice_client.play(client_bot.get_audio_file())
    else:
        await interaction.response.send_message("Song Title too Long")

@tree.command(name="stop", description="Ninja Stops Playing The Song", guild=client_bot.get_guild_id())
async def stop(interaction):
    voice_client = interaction.guild.voice_client

    if voice_client:
        await interaction.response.send_message("Stopping Audio...")
        client_bot.get_audio_file().cleanup()
        voice_client.stop()
    else:
        await interaction.response.send_message("Not Currently In a Voice Channel")

@tree.command(name="pause", description="Ninja Pauses the Song", guild=client_bot.get_guild_id())
async def pause(interaction):
    voice_client = interaction.guild.voice_client

    if voice_client:
        await interaction.response.send_message("Pausing Audio...")
        voice_client.pause()
    else:
        await interaction.response.send_message("Not Currently In a Voice Channel")

@tree.command(name="resume", description="Ninja Resumes the Song", guild=client_bot.get_guild_id())
async def resume(interaction):
    voice_client = interaction.guild.voice_client

    if voice_client:
        await interaction.response.send_message("Resuming Audio...")
        voice_client.resume()
    else:
        await interaction.response.send_message("Not Currently In a Voice Channel")

#RUN STATEMENT
client.run(os.environ['TOKEN'])