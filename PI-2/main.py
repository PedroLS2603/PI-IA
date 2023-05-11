import discord
import os
import json
from classificador import predict_url
 
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

util = json.load(open("util.json"))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if util["channel_id"] == str(message.channel.id):
        if len(message.attachments) > 0 and str(message.content).startswith("!predict"):
            predicao = predict_url(str(message.attachments[0].url))
            await message.channel.send(f'A imagem pertence à classe **{predicao}**')

client.run(os.getenv('DISCORD-TOKEN'))