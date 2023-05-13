import discord
import os
import json
from classificador import predict_url
from command import help 

 
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
        if str(message.content).startswith("!predict") and message:
            if len(message.attachments) == 0:
                await message.channel.send("Não há imagem para classificar!") 
                return
            elif len(message.attachments) > 1:
                await message.channel.send("Este comando só utiliza **uma** imagem!") 
                return
            elif str(message.attachments[0].url).split(".")[-1] not in util["image_format"]:
                await message.channel.send("Arquivo inválido!") 
                return
            predicao = predict_url(str(message.attachments[0].url))
            await message.channel.send(f'A imagem pertence à classe **{predicao}**')

        if str(message.content).startswith("!help"):
            await message.channel.send(help())    

client.run(os.getenv('DISCORD-TOKEN'))