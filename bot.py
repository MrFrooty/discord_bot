import discord
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True


client = commands.Bot(command_prefix = '.', intents=intents)

@client.event
async def on_ready():
    print('ready')

@client.command()
async def ping(ctx):
    await ctx.send(f'pong bitch, you have {round(client.latency * 1000)} ms')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['yes',
                 'no',
                 'maybe']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount) 
    
client.run('OTgyMDQ1NzQ2ODAxMDE2ODcy.Gv5bXP.mnSG_o2Gg0GjMCPPkI3_eiuG8Wpls34BisBxQY')
