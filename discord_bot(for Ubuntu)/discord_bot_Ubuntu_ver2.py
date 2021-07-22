import discord
from discord.ext import commands
import asyncio
import os
from youtube_dl import YoutubeDL

client = commands.Bot(command_prefix = "!")
playing_list = []

def download_song(url, play = True):
    result = YoutubeDL({'format':'bestaudio'}).extract_info(url,download=False)
    if play == True:
        if 'entries' in result:
            url = result['entries'][0]['webpage_url']
            for i in range(1,len(result)):
                playing_list.append(result['entries'][i]['webpage_url'])
            length = len(result['entries'])
        else:
            url = result['webpage_url']
            length = 1
        download_opts = {'format':'bestaudio',
                   'external_downloader':'aria2c',
                   'external_downloader_args':'-x 16 -s 16 -k 1M',}
        YoutubeDL(download_opts).download([url])
        return "Insert " + str(length) + " song(s) into playing list"
    else:
        if 'entries' in result:
            url = result['entries'][0]['webpage_url']
            for i in range(len(result)):
                playing_list.append(result['entries'][i]['webpage_url'])
            length = len(result['entries'])
        else:
            url = result['webpage_url']
            length = 1
        return "Insert " + str(length) + " song(s) into playing list"
    
    return "Insert " + str(length) + " song(s) into playing list"
def endSong(path):
    os.remove(path)
    if len(playing_list) != 0:
        voice = discord.utils.get(client.voice_clients)
        url = playing_list[0]
        del playing_list[0]
        
        download_song(url)
        
        for file in os.listdir("./"):
            if file.endswith(".webm"):
                os.rename(file,"song.webm")
        
        voice.play(discord.FFmpegPCMAudio("song.webm"),after = lambda x: endSong("song.webm"))

@client.event
async def on_ready():
    print("Music Bot is ready")
    game = discord.Game('Ubuntu 18.04')
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.command()
async def join(ctx):    
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if ctx.author.voice == None:
        await ctx.send("You are not connected to any voice channel")
    elif voice == None:
        voiceChannel = ctx.author.voice.channel
        await voiceChannel.connect()
    else:
        await ctx.send("Already connected to a voice channel")
@client.command()
async def play(ctx, url :str = ""):
    try:
        voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
        if voice == None:
            await ctx.send("You are not connected to any voice channel")
        elif voice.is_playing():
            await ctx.send(download_song(url,False))
        else:
            await ctx.send(download_song(url))
            for file in os.listdir("./"):
                if file.endswith("webm"):
                    os.rename(file,"song.webm")
            voice.play(discord.FFmpegPCMAudio("song.webm"), after = lambda x: endSong("song.webm"))
            await ctx.send("Start playing")
    except Exception as e:
        await ctx.send(e)
@client.command()
async def del_al(ctx):
    length = len(playing_list)
    playing_list = []
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send("Delete " + str(length) +  " songs from playing list")

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("The Bot is not connected to any voice channel")
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
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

client.run("Token")
