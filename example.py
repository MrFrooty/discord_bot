import discord
import random
from discord.ui import Button, View
from discord.ext import commands
import sys, traceback

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix = '.', intents=intents) 

class MyButton(Button):
    def __init__(self):
        super().__init__(label='click me', style = discord.ButtonStyle.green)

    async def callback(self, interaction):
        self.disabled = True
        await interaction.response.edit_message(content = 'clicked')
        await interaction.followup.send('complete')
        print(self, self.disabled)
        
class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @commands.Cog.listener() #listener is same as bot.event decorator, events
    async def on_command_error(self,ctx, error):
        if isinstance(error, commands.CommandNotFound): #handle missing argument errors 
            await ctx.send('do !help idiot')
        else:
             print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
             traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command()
    async def hello(self, ctx):
        button = MyButton()

        view = View()
        view.add_item(button)
        await ctx.send('bye', view = view)

    @commands.command() #commands
    async def ping(self, ctx): #ctx stands for context 
        print(bot.ws.ping)
        await ctx.send(f'pong bitch, you have {round(bot.latency * 1000)} ms') #f string, information inside the {} is going to be outputted following the first string

    @commands.command(alias=['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ['yes',
                    'no',
                    'maybe']
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount:int): #default amount is set to 5
        await ctx.channel.purge(limit=amount+1) 

    '''@clear.error() #this is function specific, meaning it'll only run when clear meets an error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument): #handle missing argument errors 
            await ctx.send('put in the number of messages you want to delete')'''

    def is_me(ctx):
        return ctx.author.id == 367430509107871745
    
    @commands.command()
    @commands.check(is_me) #create special checks for functions/users
    async def special(self, ctx):
        #if ctx.author.id == 367430509107871745: you can use this too
            await ctx.send(f'{ctx.author} is special')

async def setup(bot):
    await bot.add_cog(Test(bot))
