import discord
from discord.ext import commands
import youtube_dl, ffmpeg
from discord import FFmpegPCMAudio

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix = '.', intents=intents) 

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def join(self, ctx):
        voice_channel = ctx.message.author.voice.channel
        print(ctx.message.author.voice.channel, ctx.voice_client)

        if ctx.author.voice.channel is None:
            await ctx.send('you aint in channel')
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
    
    @commands.command()
    async def play(self,ctx,url):
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format' : 'bestaudio'}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download = False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send('paused')
    
    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send('resumed')

async def setup(bot):
    await bot.add_cog(Music(bot))