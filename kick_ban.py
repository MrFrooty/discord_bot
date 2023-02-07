import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix = '.', intents = intents) 

class Kick_ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command() #an asterisk is used to pass a variable number of arguments to a function
    async def kick(self, ctx, member : discord.Member, *, reason=None): #using having 'member' called as an object by discord.Member
        await member.kick(reason=reason)
        await ctx.send(f'kicked {member.mention}')

    @commands.command() 
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
        
        if((user.name, user.discriminator) == (member_name, member_discriminator)):
           await ctx.guild.unban(user) 
           await ctx.send(f'unbanned {user.mention}')
           return
    
    @commands.command() 
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason=None): 
        await member.ban(reason=reason)
        await ctx.send(f'banned {member.mention}')
    
async def setup(bot):
    await bot.add_cog(Kick_ban(bot))