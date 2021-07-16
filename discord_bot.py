import discord
from discord.ext import commands
import asyncio
import os
from pytube import YouTube

client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print("Music Bot is ready")
    game = discord.Game('PUBG是爛東西')
    await client.change_presence(status=discord.Status.idle, activity=game)

#,url_: str
@client.command()
async def join(ctx):    
    voiceChannel = ctx.author.voice.channel
    await voiceChannel.connect()
    
@client.command()
async def play(ctx, url :str = ""):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("The Bot is not connected to a voice channel")
    else:
        song_there = os.path.isfile("song.mp4")
        try:
            if song_there:
                os.remove("song.mp4")
        except PermissionError:
            await ctx.send("Wait dor the current playing music to end or use the 'stop' command")
        
        YouTube(url).streams.first().download()
        
        for file in os.listdir("./"):
            if file.endswith(".mp4"):
                os.rename(file,"song.mp4")
        
        print("finish rename")
        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="song.mp4"))
        print("playing audio")

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("The Bot is not connected to a voice channel")
    else:
        await voice.disconnect()

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not pause")

@client.command()
async def edit_game(ctx,gamename):
    game = discord.Game(gamename)
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.command()
async def command_list(ctx):
    list = '!join: join the voice channel you are\n!leave: leave voice channel\n!play URL_from_YouTube: play the music from youtube\n!pause: pause music\n!resume: resume music\n!edit_game: change the game which the bot will activity\n'
    await ctx.send(list)

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

client.run("ODY1MjUwOTI5MzQzMDcwMjU4.YPBRuQ.3zPBFZEmSTcfK3LtWF_p4bfcT88")
#client.run(os.environ['TOKEN'])
