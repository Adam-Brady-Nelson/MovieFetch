import requests
import json
from qbittorrent import Client
import sys
import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='!',intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command(name='ping')
async def ping(ctx):
    await ctx.channel.send("Pong")

@client.command(name='purge')
@commands.has_permissions(administrator=True)
async def purge(ctx):
    amount = 100
    await ctx.channel.send("Purging..... The bot might freeze for a moment while this completes")
    await ctx.channel.purge(limit = amount + 1)  

@client.command(name='get')
async def getFile(ctx, movie):
    try:
        qb = Client('http://127.0.0.1:25565/')
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')
        qb.login(user, password)
        print("Connected to QBittorrent")
    except:
        await ctx.channel.send("Contact Admin")
        print("Could not connect to QBittorrent")
        return

    api_url = os.getenv('API_URL')
    trackers = os.getenv('TRACKERS')
    
    # linkSplit = movie.split("/")
    # code = str(linkSplit[4])
    # ID = code[2:len(code)]
    # print(ID) (Keeping this here incase code no work)
    
    ID = (movie.split("/")[4])[2:len(movie.split("/")[4])]  # (A single line solution for the code above)
    
    payload = {'imdb_id': ID}
    response = requests.get(api_url,params=payload)
    jsonRes = response.json()

    if jsonRes['data']['movie']['id'] == 0:
        await ctx.channel.send("Movie not avaliable")
        return
        
    await ctx.channel.send(jsonRes['data']['movie']['title'] + " - IMDb ID: " + ID)
    print("Getting " + jsonRes['data']['movie']['title'] + " - IMDb ID: " + ID)

    count = 1
    for i in jsonRes['data']['movie']['torrents']:
        qualityDisplay = str(count) + ". " + str(i['quality']) + " - " + str(i['size']) + " - " + str(i['video_codec']) + " - " + str(i['type'])
        await ctx.channel.send(qualityDisplay)
        count+=1
    try:
        await ctx.channel.send("Waiting for response...\nEnter the corresponding number for quality (0 will cancel the operation): ")
        res = await client.wait_for('message', timeout = 60.0)
        qualitySelection = (int(res.content))-1
        
        if (qualitySelection+1) == 0:
            await ctx.channel.send("Operation stopped! File will not download!")
            return
        try:
            hashCode = jsonRes['data']['movie']['torrents'][qualitySelection]['hash']
            magnet = "magnet:?xt=urn:btih:" + hashCode + trackers
            dl_path = os.getenv('SAVEDIR')
            qb.download_from_link(magnet, savepath = dl_path)
            response = "Task started. Please wait at least 15 minutes before trying to watch, EVEN IF THE MOVIE HAS APPEARED ON PLEX!!!!!"
            await ctx.channel.send(response)
        except:
            await ctx.channel.send("That quality does not exist")
            return
    except asyncio.TimeoutError:
        await ctx.channel.send("You did not respond to selecting quality")
        return
client.run(TOKEN)
