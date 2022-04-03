from music_cog import Music_Cog
from list_cog import Kicklist
from responses_emojis_stuff import *
from utility import *
from token import TOKEN


@bot.event
async def on_ready():
    bot.add_cog(Music_Cog(bot))
    bot.add_cog(Kicklist(bot))
    print('f4')

bot.run((TOKEN))
