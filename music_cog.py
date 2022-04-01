import asyncio
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


class Music_Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.music_queue = []
        self.ydl_options = {'format': 'bestaudio', 'noplaylist': 'True', 'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}
        self.ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.voice = None
        now_playing = ""
        self.now_playing = now_playing
        self.channel = None
        self.message = None  

    def search_yt(self, query):
        with YoutubeDL(self.ydl_options) as ydl:
            try:
                info = ydl.extract_info('ytsearch:%s' % query, download=False)['entries'][0]
            except:
                return
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    async def player_message(self):   
        print('.')     
        self.message = await self.channel.send(f'**now playing:** \n{self.now_playing}')
        print(self.message)
        await self.message.add_reaction('⏭️')
        self.bot.add_listener(self.on_reaction_add) 

    async def play_music(self):
        def repeat(error):
            next_song = asyncio.run_coroutine_threadsafe(self.play_music(), self.bot.loop)
            next_song.result()
        if self.music_queue:
            if self.voice.channel != self.music_queue[0][1]:
                await self.voice.move_to(self.music_queue[0][1])
            self.now_playing = self.music_queue[0][0]['title']
            m_url = self.music_queue.pop(0)[0]['source']
            await self.player_message()
            self.voice.play(discord.FFmpegPCMAudio(m_url, **self.ffmpeg_options), after=repeat)
            
        else:
            self.now_playing = None
            await self.voice.disconnect()

    async def on_reaction_add(self, reaction, user):
        if str(reaction.emoji) == '⏭️' and reaction.message == self.message and user.id != 930117521028284456:
            if self.voice != "" and self.voice is not None:
                print(self.voice)
                await self.voice.stop()
            else:
                await self.message.send('no music in queue')
                await self.voice.stop()            
            await self.play_music()

    @commands.command()
    async def play(self, ctx, *args):
        voice_channel = ctx.author.voice
        self.channel = ctx.channel  
        if voice_channel is None:
            await ctx.send('join a voice channel first ape')
            return
        voice_channel = voice_channel.channel
        query = ' '.join(args)
        song = self.search_yt(query)
        if not song:
            await ctx.send('try another song ape')
            return
        self.music_queue.append([song, voice_channel])
        await ctx.send('song added to the queue')
        if not self.voice or not self.voice.is_playing() and not self.voice.is_paused():
            self.voice = await self.music_queue[0][1].connect()
            await self.play_music()

    @commands.command(aliases=('q',))
    async def queue(self, ctx):
        if not self.music_queue:
            await ctx.send('nothing in queue moek')
            return
        await ctx.send('\n'.join([song[0]['title'] for song in self.music_queue]))

    @commands.command()
    async def skip(self, ctx):
        if self.voice and self.voice.is_playing() or self.voice.is_paused():
            self.voice.stop()

    @commands.command(aliases=('dc', 'leave', 'disc'))
    async def disconnect(self, ctx):
        if self.voice:
            self.now_playing = None
            await self.voice.disconnect()

    @commands.command()
    async def pause(self, ctx):
        if self.voice and self.voice.is_playing():
            self.voice.pause()

    @commands.command(aliases=('resume',))
    async def unpause(self, ctx):
        if self.voice and self.voice.is_paused():
            self.voice.resume()

    @commands.command(aliases=('np', 'pn'))
    async def playing(self, ctx):
        if self.now_playing:
            await ctx.send(self.now_playing)
