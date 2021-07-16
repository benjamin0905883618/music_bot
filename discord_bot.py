import discord
import asyncio
import os

print(os.environ['TOKEN'])

client = discord.Client()

@client.event
async def on_ready():

    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("--------------------------------")

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await message.channel.send('Calculating message...')
        async for log in discord.abc.Messageable.history(message.channel, limit = 100):
            if log.author == message.author:
                counter += 1
                output = "You have " + str(counter) + " message"
                await tmp.edit(content=output)
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await message.channel.send('Done Sleeping')

client.run(os.environ['TOKEN'])
