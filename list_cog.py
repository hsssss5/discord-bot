import asyncio
import discord
from discord.ext import commands, tasks
import sqlite3


class Kicklist(commands.Cog):

    def __init__(self, bot, dbname="list.db"):
        self.bot = bot
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        
    
    async def add_kicker(self, name, ctx):        
        sql = ('INSERT INTO users(discord_name) VALUES(?)')
        val = (name, )        
        self.conn.execute(sql, val)
        self.conn.commit()
        self.conn.close()
        #await ctx.send('kicker added')
    
    async def add_tag(self, tag, ctx):
        sql = ('INSERT INTO tags(tag) VALUES(?)')
        val = (tag, )        
        self.conn.execute(sql, val)
        self.conn.commit()
        self.conn.close()
        #await ctx.send(new_tag)

    async def get_tags(self, tags):
        c = self.conn.cursor()
        stmt = 'SELECT tag_id FROM tags WHERE tag = (?)' 
        viable_tags = set()
        print(type(viable_tags))
        for tag in tags:
            c.execute(stmt, (tag.strip(), ))
            fetched = c.fetchone()   
            if fetched is not None:         
                viable_tags.update(fetched)    
            print(viable_tags) 
        print(viable_tags)       
        return viable_tags

    async def add_keys(self, tags_id, listing_id):
        c= self.conn.cursor()
        sql = 'INSERT INTO tags_and_listings(tag_id, listing_id) VALUES(?,?)'
        for tag in tags_id:
            c.execute(sql, (tag, listing_id))
        self.conn.commit()
        c.close()

    async def add_kl(self, kicker, ape, comment, final_tags):
        c = self.conn.cursor()
        sql = 'INSERT INTO listings(user_id, link, comment) VALUES(?,?,?)'
        val = (kicker, ape, comment)         
        c.execute(sql, val)
        lastrow = c.lastrowid        
        self.conn.commit()
        c.close()
        await self.add_keys(final_tags, lastrow)        

    async def check_perms_kl(self, kicker):        
        c = self.conn.cursor()        
        stmt = 'SELECT user_id FROM users WHERE discord_name = (?)'            
        c.execute(stmt, (kicker, ))    
        fetched = c.fetchone()   
        if fetched is not None:         
            fetched = fetched[0]  
        return fetched      

    async def show_tags(self):       
        stmt = 'SELECT tag FROM tags'        
        return [x[0] for x in self.conn.execute(stmt)]

    async def show_listings(self, discord_name):        
        stmt = 'SELECT link, comment, tag FROM tags_and_listings INNER JOIN listings ON listings.user_id = (?) AND listings.listing_id = tags_and_listings.listing_id INNER JOIN tags ON tags_and_listings.tag_id = tags.tag_id'        
        return [x[0] for x in self.conn.execute(stmt, (discord_name, ))]



    @commands.command()
    async def kl(self, ctx):
        def check(message):
            return message.channel == ctx.channel and message.author.id == ctx.author.id
        
        await ctx.send('what do u want ape')
        msg = await self.bot.wait_for('message', check=check)        
        if msg.content.lower() == 'add kicker':
            name = msg.author.id
            await self.add_kicker(name, ctx)
            await ctx.send('done')

        elif msg.content.lower() == 'add tag':
            await ctx.send('whats the tag')
            msg = await self.bot.wait_for('message', check=check)  
            tag = msg.content
            await self.add_tag(tag, ctx)
            await ctx.send('done') 

        elif msg.content.lower() == 'add kl':
            kicker = ctx.author.id            
            user_id = await self.check_perms_kl(kicker)
            if not user_id:
                await ctx.send('you adasda')
                return
            await ctx.send('enter the ape') 
            msgape = await self.bot.wait_for('message', check=check)
            ape = msgape.content
            await ctx.send('enter the comment') 
            msgcom = await self.bot.wait_for('message', check=check)
            comment = msgcom.content              
            await ctx.send('enter the tags') 
            msgtags = await self.bot.wait_for('message', check=check)            
            tags = msgtags.content.split(',')
            final_tags = await self.get_tags(tags)
            await self.add_kl(user_id, ape, comment, final_tags)
            await ctx.send('done')
            
        elif msg.content.lower() == 'show tags':            
            items = await self.show_tags()            
            if len(items) != 0:                
                message = '\n'.join(items)
                await ctx.send(message)

        elif msg.content.lower() == 'show listings':  
            discord_name = 1         
            items = await self.show_listings(discord_name)            
            if len(items) != 0:                
                message = '\n'.join(items)
                await ctx.send(message)

        else:
           await ctx.send('something went wrong')


# @bot.command()
# @check_perms()
# async def test(ctx):
#     db = sqlite3.connect('stuff.db')
#     cursor = db.cursor()
#     cursor.execute('SELECT user_id FROM main')
#     result = cursor.fetchone()
#     await ctx.send(result)
#     # if result is None:
#     #     sql = ('INSERT INTO main(user_id, score_earned) VALUES(?, ?)')
#     #     val = (ctx.author.id, 0)
#     #     await ctx.send(ctx.author.id)
#     #     await ctx.send(f'User {ctx.author.mention} has been added')
#     # elif result is not None:
#     #     sql = (f'UPDATE main SET score_earned = ? WHERE user_id = {ctx.author.id}')
#     #     result3 = (f'SELECT score_set FROM main WHERE user_id = {ctx.author.id}')
#     #     await ctx.send('ok')
#     #     # result2 = cursor.fetchone()
#     #     # await ctx.send(result2[0])
#     #     # old_score = int(result2[0])
#     #     # val = (old_score + 1,)
#     #     # await ctx.send(f'1 point has been added to {ctx.author.mention}')
#     # cursor.execute(sql, result3)
#     # db.commit()
#     cursor.close()
#     db.close()