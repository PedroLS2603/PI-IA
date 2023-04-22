import discord
import os
 
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
 
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if len(message.attachments) > 0:
        await message.channel.send('Imagem recebida!')
        
client.run(os.getenv('DISCORD-TOKEN'))