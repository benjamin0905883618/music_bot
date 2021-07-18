# Discord音樂機器人

[![hackmd-github-sync-badge](https://hackmd.io/GHB52IxRT52hWGh_HF-Ylw/badge)](https://hackmd.io/GHB52IxRT52hWGh_HF-Ylw)


### 前置步驟
1. 安裝python, 記得要包含pip
2. Discord帳號

### 申請Discord bot
前往 Discord官網 -> 開發人員 -> Application 可以找到應用程式的介面
建立一個新的應用程式後, 可以看到這個頁面
![](https://i.imgur.com/Qr1DDVH.png)
1. 點入Bot的選項, 可以看到機器人的Token, 點擊 $\mbox{Click to Reveal Token}$可以查看自己機器人的Token, 將Token 儲存下來備用。
2. 點入OAuth2選項, 將$\mbox{Client ID}$的地方也複製下來, 接著利用[這個連結](https://discordapp.com/oauth2/authorize?permissions=301001759&scope=bot&client_id=你的機器人的clientID)把client_id的地方改成你自己的機器人client_id, 就可以將機器人邀請進自己的伺服器了
:::warning
**機器人的Token不能在網路上洩漏, 一旦洩漏Discord官方會自動幫你重新建立, 
到時候就要去自己的程式把Token換掉, 
記得在網路上存程式(如: Github)的時候要把Token刪掉。**
:::

### 讓機器人上線並出入語音頻道
利用Windows上的cmd, 輸入下列指令
```
pip install discord.py
```
如果這行指令輸入時出現錯誤, 例如說pip不是可以call的指令的話, 請重新安裝(Repair也可以)python, 並記得將pip選入安裝的部分。

安裝完後就可以開始寫程式囉~開啟新的檔案來寫吧
```
import discord
from discord.ext import commands

client = commands.Bot(command_prefix = "!")

@client.event
async def ready_on():

    #這裡是機器人上線後預計會執行的程式
    print('目前登入身分', client.user)
    
    #也可以利用指令, 更改機器人目前在玩的遊戲
    game = discord.Game('輸入你想讓機器人顯示的狀態')
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.command()
async def join(ctx):
    
    #這裡的指令會讓機器人進入call他的人所在的語音頻道
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if ctx.author.voice == None:
        await ctx.send("You are not connected to any voice channel")
    elif voice == None:
        voiceChannel = ctx.author.voice.channel
        await voiceChannel.connect()
    else:
        await ctx.send("Already connected to a voice channel")
        
@client.command()
async def leave(ctx):
    
    #離開call他那個伺服器的所在頻道
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("The Bot is not connected to a voice channel")
    else:
        await voice.disconnect()
        
#把你的Token輸入在這邊
client.run("Input Your Token")
```

:::warning
這個步驟中可能會缺一些套件,
在cmd使用 pip install **缺少的套件名稱**
就可以解決
:::

到這裡為止,已經做好了一個機器人, 並且可以隨意進出call他的使用者所在的語音頻道內了。

### 讓機器人播放音樂

**重要 : 這個部分請包含上面的程式共同使用**

```
from pytube import YouTube
import os

def endSong(path):

    #播放完後的步驟, 進行前一首歌刪除, 抓取一首清單內的歌進行播放
    os.remove(path)
    if len(playing_list) != 0:
        voice = discord.utils.get(client.voice_clients)
        url = playing_list[0]
        del playing_list[0]
        
        YouTube(url).streams.first().download()
        for file in os.listdir("./"):
            if file.endswith(".mp4"):
                os.rename(file,"song.mp4")
        
        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="song.mp4"),after = lambda x: endSong("song.mp4"))
playing_list = []
async def play(ctx, url :str = ""):
    
    #取得目前機器人狀態
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    #如果機器人正在播放音樂, 將音樂放入播放清單
    if voice.is_playing():
        playing_list.append(url)
        print(playing_list)
        await ctx.send("insert song into playing_list")
    
    #如果機器人沒在播放, 開始準備要播放的音樂
    else:
    
        #如果還有找到之前已經被播放過的音樂檔, 進行刪除
        song_there = os.path.isfile("song.mp4")
        
        try:
            if song_there:
                os.remove("song.mp4")
        except PermissionError:
            await ctx.send("Wait dor the current playing music to end or use the 'stop' command")
        
        #找尋輸入的Youtube連結, 將目標影片下載下來備用
        YouTube(url).streams.first().download()
        
        #將目標影片改名, 方便找到它
        for file in os.listdir("./"):
            if file.endswith(".mp4"):
                os.rename(file,"song.mp4")
        #找尋要播放的音樂並播放, 結束後依照after部分的程式進行後續步驟
        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="song.mp4"),after = lambda x: endSong("song.mp4"))
```
除了播放之外,一樣重要的便是音樂的操作
1. 音樂暫停
```
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing")
```

2. 音樂繼續
```
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not pause")
```
4. 跳過這首歌
```
@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
```

### 總結
這次實作完的整套Discord機器人, 程式碼只能在自己電腦上執行, 如果要使用必須要執行電腦上的程式才能使用。
如果要利用其他在網路上的雲端平台來Deploy 你的服務的話, 請千萬不要忘記將Token設定成環境變數,並且將client.run的部分改成取得環境變數來啟動。
另外, 如果使用雲端平台來deploy的話, requirement.txt、runtime.txt 跟 Procfile三個文件是必要的, 請務必參考更多資料再進行實作
最後, 這份程式有一些問題, 例如播放清單的部分沒有解決如果多人同時輸入play的問題, 有可能會播放到其他人的清單, 但因為我是寫給自己用的, 這部分我就沒有特別作修正, 如果要給親朋好友使用的話, 記得要在這裡做一些改動。

參考資料 : [Discord版本問題轉換表](https://discordpy.readthedocs.io/en/stable/migrating.html)、[Discord.py 機器人從0到1超詳細教學](https://hackmd.io/@kangjw/Discordpy%E6%A9%9F%E5%99%A8%E4%BA%BA%E5%BE%9E0%E5%88%B01%E8%B6%85%E8%A9%B3%E7%B4%B0%E6%95%99%E5%AD%B8)、[discord.py - Command raised an exception: OpusNotLoaded](https://stackoverflow.com/questions/55919924/discord-py-command-raised-an-exception-opusnotloaded)、[[Python] 如何開發 Discord 機器人並且部屬至 Heroku](https://fightwennote.blogspot.com/2017/10/python-discord-heroku.html)、[Make a Discord Bot with Python (Part 7: Music Bot) | Latest Discord Py Version](https://www.youtube.com/watch?v=ml-5tXRmmFk)