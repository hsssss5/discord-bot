from utility import *
import random
from responses_emojis_stuff import *
import asyncio

#Просто набор ответов на возможные сообщения боту

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    if ctx.author.id in in_command:
        return
    if random.randrange(30) == 1:
        await ctx.add_reaction(random.choice(custom_react.get(ctx.author.id, [MONEKY])))
    if ctx.content.lower() == 't2':
        await ctx.channel.send(random.choice(random_message + custom_message.get(ctx.author.id, []) + custom_react.get(ctx.author.id, [])))
        return
    if ctx.content.lower() in ('t2 fuck you', 't2 fuck off'):
        await ctx.channel.send(FACE)
        return
    if ctx.author.id == 366545173364080657:
        await ctx.channel.send(random.choice(NHKHNOC_MESSAGE))
    if 'ttoby' in ctx.content.lower() and ctx.content.lower().startswith('t2'):
        await ctx.channel.send(TOBY)
        return
    if ctx.content.lower() == 't2 help':
        if ctx.author.id in NON_APES_ID:
            await ctx.channel.send(SALUTAPE)
            return
        else:
            await ctx.channel.send('baggezbot (NOT HELPING)')
            return
    if ctx.content.lower().startswith('t2 is ape'):
        if any(check_who in ctx.content.lower() for check_who in NON_APES):
            await ctx.channel.send('no')
            return
        else:
            await ctx.channel.send('yes')
            return
    if bot.user.mentioned_in(ctx):
        if ctx.author.id in NON_APES_ID:
            await ctx.channel.send(f'{ctx.author.mention} ready to harass baggez')
            return
        else:
            await ctx.channel.send(f'{ctx.author.mention} wat u want ape')
            return
    await bot.process_commands(ctx)

@bot.command(aliases=['hello', 'hey'])
async def hi(ctx):
    await ctx.send(random.choice(hi_message))

@bot.command(aliases=['goodbye'])
async def bye(ctx):
    await ctx.send(random.choice(BYE_MESSAGE))

@bot.command()
async def baggez(ctx):
    await ctx.send(BAGGEZ)

@bot.command()
async def doggez(ctx):
    await ctx.send(DOGGEZ)


#Локальная шутка

@bot.command()
async def ping(ctx):
    def check(message):
        return message.channel == ctx.channel and message.author.id == ctx.author.id
    await ctx.send('pong')
    while True:
        try:
            message = await bot.wait_for('message', check=check, timeout=30)
            if 'hapey' in message.content.lower():
                return
            else:
                await ctx.send(f'this is not hapey {FACE}')
                await ctx.send('you WILL hapey the pong')
        except asyncio.TimeoutError:
            await ctx.send(f'{ctx.author.mention} hapey the pong ape {FACE}')


#Бот повторяет твоё сообщение на любом сервере и канале с возможностью пингануть пользователя

@check_perms()
@bot.command()
async def repeat(ctx):
    def check(message):
        return message.channel == ctx.channel and message.author.id == ctx.author.id

    async def send_message(message, channel, user=''):
        if not channel.isdigit():
            channel = channel[2:-1]
        if user and user.isdigit():
            user = bot.get_user(int(user)).mention
        channel = bot.get_channel(int(channel))
        await channel.send(user + ' ' + message)
    await ctx.send(f'{GIMME} message **or** {GIMME} message, channel, user (optional)')
    repeat_message = await bot.wait_for('message', check=check)
    test_message = repeat_message.content.replace(' ', '').split(',')
    if len(test_message) > 1:
        if test_if_channel(test_message[-2]) and test_if_user(test_message[-1]):
            channel, user = test_message[-2], test_message[-1]
            message = repeat_message.content[:repeat_message.content.find(test_message[-2])].strip()[:-1]
            await send_message(message, channel, user)
            return
        if test_if_channel(test_message[-1]):
            channel = test_message[-1]
            message = repeat_message.content[:repeat_message.content.find(test_message[-1])].strip()[:-1]
            await send_message(message, channel)
            return
    await ctx.send(f'{GIMME} channel')
    channel = await bot.wait_for('message', check=check)
    if test_if_channel(channel.content):
        await ctx.send(f'{GIMME} user or ignore')
        try:
            user = await bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await send_message(repeat_message, channel.content)
            return
        if not test_if_user(user.content):
            await send_message(repeat_message.content, channel.content)
            return
        await send_message(repeat_message.content, channel.content, user.content)
        return
    await ctx.send('learn how to write moek')


#Для работы с пиклами

@check_perms()
@bot.command()
async def add(ctx, *where_to_add):
    def check(message):
        return message.channel == ctx.channel and message.author.id == ctx.author.id
    where_to_add = ' '.join(list(where_to_add))
    if not where_to_add:
        await ctx.send('wat u want to add to ape')
        message = await bot.wait_for('message', check=check)
        where_to_add = message.content
    if where_to_add == 'hi message':
        await ctx.send('enter new hi message moek')
        message = await bot.wait_for('message', check=check)
        what_to_add = message.content
        await ctx.send(f'are you sure you want to add {what_to_add}? f1 or f2')
        message = await bot.wait_for('message', check=check)
        if message.content.lower() == 'f1':
            hi_message.append(what_to_add)
            with open('hi message.pickle', 'wb') as file:
                pickle.dump(hi_message, file)
            await ctx.send(':white_check_mark:')
            return
        else:
            await ctx.send('kol for f2 :monkey:')
            return
    elif where_to_add == 'random message':
        await ctx.send('enter new random message moek')
        message = await bot.wait_for('message', check=check)
        what_to_add = message.content
        await ctx.send(f'are you sure you want to add {what_to_add}? f1 or f2')
        message = await bot.wait_for('message', check=check)
        if message.content.lower() == 'f1':
            random_message.append(what_to_add)
            with open('random message.pickle', 'wb') as file:
                pickle.dump(random_message, file)
            await ctx.send(':white_check_mark:')
            return
        else:
            await ctx.send('kol for f2 :monkey:')
            return
    elif where_to_add == 'custom message':
        await ctx.send('do you want to **ping** or just send me an **id**')
        id_or_ping = await bot.wait_for('message', check=check)
        if id_or_ping.content.lower() == 'id':
            await ctx.send(f'id it is {GIMME}')
            message = await bot.wait_for('message', check=check)
            if test_if_user(message.content) and message.content.isdigit() and int(message.content) != bot.user.id:
                ape = int(message.content)
            else:
                await ctx.send('try again ape')
                return
        elif id_or_ping.content.lower() == 'ping':
            await ctx.send('ping the ape')
            message = await bot.wait_for('message', check=check)
            if not len(message.mentions) == 1 or bot.user.mentioned_in(message):
                await ctx.send('try again ape')
                return
            ape = message.mentions[0].id
        else:
            await ctx.send('try again ape')
            return
        await ctx.send('enter new custom message moek')
        message = await bot.wait_for('message', check=check)
        what_to_add = message.content
        await ctx.send(f'are you sure you want to add {what_to_add}? f1 or f2')
        message = await bot.wait_for('message', check=check)
        if message.content.lower() == 'f1':
            custom_message[ape] = custom_message.get(ape, []) + [what_to_add]
            with open('custom message.pickle', 'wb') as file:
                pickle.dump(custom_message, file)
            await ctx.send(':white_check_mark:')
        else:
            await ctx.send(f'kol for f2 {MONEKY}')
            return
    elif where_to_add == 'custom react':
        await ctx.send('do you want to **ping** or just send me an **id**')
        id_or_ping = await bot.wait_for('message', check=check)
        if id_or_ping.content.lower() == 'id':
            await ctx.send(f'id it is {GIMME}')
            message = await bot.wait_for('message', check=check)
            if test_if_user(message.content) and message.content.isdigit() and int(message.content) != bot.user.id:
                ape = int(message.content)
            else:
                await ctx.send('try again ape')
                return
        elif id_or_ping.content.lower() == 'ping':
            await ctx.send('ping the ape')
            message = await bot.wait_for('message', check=check)
            if not len(message.mentions) == 1 or bot.user.mentioned_in(message):
                await ctx.send('try again ape')
                return
            ape = message.mentions[0].id
        else:
            await ctx.send('try again ape')
            return
        await ctx.send('enter new custom react moek')
        message = await bot.wait_for('message', check=check)
        what_to_add = message.content
        try:
            await message.add_reaction(message.content)
        except (discord.NotFound, discord.InvalidArgument):
            await ctx.send('try again ape')
            return
        await ctx.send(f'are you sure you want to add {what_to_add}? f1 or f2')
        message = await bot.wait_for('message', check=check)
        if message.content.lower() == 'f1':
            custom_react[ape] = custom_react.get(ape, []) + [what_to_add]
            with open('custom react.pickle', 'wb') as file:
                pickle.dump(custom_react, file)
            await ctx.send(':white_check_mark:')
            return
        else:
            await ctx.send('kol for f2 :monkey:')
            return
    else:
        await ctx.send('invalid entry ape')


#Создаёт сообщение-голосование

@bot.command()
async def vote(ctx):
    def check(message):
        return message.channel == ctx.channel and message.author == ctx.author
    await ctx.send('who are we kicking?')
    message = await bot.wait_for('message', check=check)
    if not cancel_message(message):
        await ctx.send('cancelled')
        return
    await ctx.send(f'{message.author.mention} wants to call a vote:')
    bot_message = await ctx.send(message.content)
    await bot_message.add_reaction(F1)
    await bot_message.add_reaction(F2)