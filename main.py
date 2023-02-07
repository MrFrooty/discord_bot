import discord
import os 
import asyncio
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = '.', intents = intents)
status = cycle(['you struggle', 'you cry', 'you is joy'])

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.idle, 
                              activity=discord.Activity(
                                type=discord.ActivityType.watching, 
                                name='you struggle')
                             )
    print('bot ready')
    change_status.start()

@tasks.loop(seconds = 10) #create a loop that runs itself after 'x' amount of seconds 
async def change_status():
    await bot.change_presence(activity = discord.Activity(
                                type = discord.ActivityType.watching,
                                name = next(status))
                             )

@bot.event
async def on_raw_reaction_add(payload):
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds) #code allows us to access guild (or the server)
    msg_id = 984945988974301184
    if (payload.message_id == msg_id) and (payload.emoji.name == '🙂'):
        role = discord.utils.get(guild.roles, name = 'admin')
        await payload.member.add_roles(role)

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start('OTgyMDQ1NzQ2ODAxMDE2ODcy.GweyNS.GCw2j4_i6lsqddiA9QT2PRFzQvyIDD6ebigA6k')

asyncio.run(main())
