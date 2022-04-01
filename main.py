import asyncio
import random
import pickle
import sqlite3
import discord
from discord.ext import commands, tasks
from music_cog import Music_Cog
from list_cog import Kicklist
from memory_profiler import memory_usage
print(memory_usage())


intents = discord.Intents.default()

intents.members = True

bot = commands.Bot(command_prefix=['t2 ', 'T2 '], case_insensitive=True, intents=intents)


with open('custom message.pickle', 'rb') as file:
    custom_message = pickle.load(file)

with open('hi message.pickle', 'rb') as file:
    hi_message = pickle.load(file)

with open('custom react.pickle', 'rb') as file:
    custom_react = pickle.load(file)

with open('random message.pickle', 'rb') as file:
    random_message = pickle.load(file)


SALUTAPE = '<:salutape:841439464453832775>'

MONEKY = '<:moneky:672861737120301066>'

HAPEY = '<:hAPEy:728926173907910686>'

WHOPING = '<:WHOPING:786662215377092650>'

DOGGEZ = '<a:doggez:935340410337898516>'

F1 = '<:f1:931279440279924747>'

F2 = '<:f2:931279453810720779>'

FACE = '<:__:807007374963507200>'

TOBY = '<:ttoby:824360560703045685>'

BAGGEZ = '<:bread_monkey:826022442916118528>'

GIMME = '<:gimme:786582737020649502>'

NON_APES = ('hs', 'toby', '<:ttoby:824360560703045685>')

NON_APES_ID = (239021478891356161, 508426328769429506)

APES_TO_PING = (559964322235678721, 595385697305624578, 622608884766605322, 88719283227471872, 631079721840541697, 327210424581881857, 664362978493202433, 234077437598760970, 236863824420929536, 508426328769429506, 563898088390000650, 216707845587075073, 276875973784502272, 163399420015017984, 762380421756878888, 131745461743648768, 330442831967551489, 209424001573978122, 474493846764388362, 217980551058030593, 196721238045884416, 253846404164747264, 183107230160257024, 455231768421990400, 238120502432890880)

REAL_CHANNEL = 870428287418138624

TEST_CHANNEL = 930810301685837864

TEST_CHANNEL_2 = 719661577481093170

CANCEL = ('c', 'cancel')

PEANUT = ('<:peanut:934464589045854268>', '<:peanut1:934464608784236564>', '<:peanut2:934464630036766760>', '<:peanut3:934464803223793664>')

PING_PONG_FAILED_MESSAGE = ('you failed ping pong like ape', 'where pong wtf', 'learn pong ape', 'moek not pong', 'ape mad bc ape (nonponger)')

SQUARE = ':white_square_button:'

PING_PONG_FAILED_MESSAGE = ('you failed ping pong like ape', 'where pong wtf', 'learn pong ape', 'moek not pong', 'ape mad bc ape (nonponger)')

TTT_WRONG_PICK = ('learn how to count tic tac toe board numbers like u spread stickies - try again', 'ape - first line: 123, second: 456, third: 789 no complica')

BYE_MESSAGE = ('see u in q <:jimbo:838930130394284123>', 'bye moek', '<:sleepape:752083069086859295>')

LOOT = ('silver sticky', 'Professional Killstreak Splendid Screen Kit Fabricator', '6+2', 'hat from surplus', 'gas passer', 'nothing(didnt need mission)', '2box')

NHKHNOC_MESSAGE = ('а может ты пидорас ебаный а не бот', 'соси жопу')

in_command = []


@bot.check
async def check_state(ctx):
    return ctx.author.id not in in_command


@bot.before_invoke
async def add_state(ctx):
    in_command.append(ctx.author.id)


@bot.after_invoke
async def remove_state(ctx):
    in_command.remove(ctx.author.id)


def check_perms():
    def check(ctx):
        return ctx.message.author.id in NON_APES_ID
    return commands.check(check)


def cancel_message(message):
    if message.content.lower() in CANCEL:
        return False
    else:
        return True


def ping_player_from_id(user):
    return f'<@{(user)}>'


def test_if_emoji(emoji_to_check):
    return emoji_to_check in [f'<:{emoji.name}:{emoji.id}>' for emoji in bot.emojis]


def test_if_channel(channel_to_check):
    return channel_to_check in [f'<#{channel.id}>' for guild in bot.guilds for channel in guild.text_channels] or channel_to_check in [str(channel.id) for guild in bot.guilds for channel in guild.text_channels]


def test_if_user(user_to_check):
    return user_to_check in [f'<@!{user.id}>' for guild in bot.guilds for user in guild.members] or user_to_check in [str(user.id) for guild in bot.guilds for user in guild.members]


@tasks.loop(hours=1)
async def mal_ping():
    ape_to_ping = random.choice(NON_APES_ID)
    channel = bot.get_channel(TEST_CHANNEL)
    await channel.send(f'{ping_player_from_id(ape_to_ping)} {random.choice(random_message + custom_message.get(ape_to_ping, []) + custom_react.get(ape_to_ping, []))}')


class pingpong_game(commands.Cog):

    def __init__(self, bot, ctx):
        self.bot = bot
        self.channel = ctx.channel
        self.message = None
        self.player_message = None
        self.player_list = []
        self.player_id_list = set({})
        self.bot.loop.create_task(self.setup())
        self.time_left = 60

    async def setup(self):
        self.message = await self.channel.send(f'Ping pong game starting in **60** seconds... React with {WHOPING} to join')
        self.player_message = await self.channel.send('Players registered: ')
        await self.message.add_reaction(WHOPING)
        self.lobby.start()
        self.timer.start()

    def cog_unload(self):
        self.bot.remove_listener(self.on_reaction_add)
        self.bot.remove_listener(self.on_reaction_remove)
        self.lobby.cancel()
        self.timer.cancel()
        self.pingpong.cancel()

    async def on_reaction_add(self, reaction, user):
        if str(reaction.emoji) == WHOPING and reaction.message == self.message and user.id != bot.user.id:
            self.player_list.append(user.mention)
            self.player_id_list.add(user.id)

    async def on_reaction_remove(self, reaction, user):
        if str(reaction.emoji) == WHOPING and reaction.message == self.message and user.id != bot.user.id:
            self.player_list.remove(user.mention)
            self.player_id_list.remove(user.id)

    @tasks.loop(seconds=1)
    async def lobby(self):
        self.player_list_message = ', '.join(self.player_list)
        await self.player_message.edit(content=f'Players registered: {self.player_list_message}')

    @tasks.loop(seconds=5, count=12)
    async def timer(self):
        await self.message.edit(content=f'Ping pong game starting in **{self.time_left}** seconds... React with {WHOPING} to join.')
        self.time_left -= 5

    @timer.before_loop
    async def before_lobby(self):
        self.bot.add_listener(self.on_reaction_add)
        self.bot.add_listener(self.on_reaction_remove)

    @timer.after_loop
    async def after_lobby(self):
        await self.message.edit(content='Ping pong game started. Gl on loot!')
        self.bot.remove_listener(self.on_reaction_add)
        self.bot.remove_listener(self.on_reaction_remove)
        if len(self.player_id_list) > 1:
            self.score = {player: 0 for player in self.player_list}
            self.pingpong.start()
        else:
            bot.remove_cog('pingpong_game')

    @tasks.loop(seconds=1, count=25)
    async def pingpong(self):
        def check(message):
            if message.channel == self.channel and message.author.mention in self.player_list:
                responses.append(message)
                return message.author.mention == pingpong_target and message.content.lower() in ('pong', 'pong.')
            return False
        responses = []
        pingpong_target = random.choice(self.player_list)
        await self.channel.send(f'{pingpong_target} ping')
        try:
            await bot.wait_for('message', check=check, timeout=3)
        except asyncio.TimeoutError:
            message = await self.channel.send(f'{pingpong_target} {random.choice(PING_PONG_FAILED_MESSAGE)}')
            await message.add_reaction(F2)
            self.score[pingpong_target] -= 1
        else:
            message = await self.channel.send(HAPEY)
            await message.add_reaction(F1)
            self.score[pingpong_target] += 1
        finally:
            for response in responses:
                if response.author.mention == pingpong_target:
                    responses.remove(response)
                    continue
                await response.add_reaction(F2)
                self.score[response.author.mention] -= 1

    @pingpong.after_loop
    async def close_game(self):
        def sorting(sort_by_value):
            return sort_by_value[1]
        sorted_score = sorted(self.score.items(), key=sorting)
        for player_score in sorted_score:
            await self.channel.send(f'{player_score[0]}: **{player_score[1]:>5}**')
        bot.remove_cog('pingpong_game')


@bot.event
async def on_ready():
    bot.add_cog(Music_Cog(bot))
    bot.add_cog(Kicklist(bot))
    # bot.add_cog(Kicklist(bot))
    # db = sqlite3.connect('stuff.db')
    # cursor = db.cursor()
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS main(
    #     user_id TEXT,
    #     score_earned TEXT
    #     )
    #     ''')
    print('f4')


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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        pass


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


@bot.command()
async def emojis(ctx):
    for emoji in ctx.guild.emojis:
        print(emoji.name, emoji.id)


@bot.group(invoke_without_command=True, case_insensitive=True)
async def start(ctx, *args):
    pass


@bot.group(invoke_without_command=True, case_insensitive=True)
async def stop(ctx):
    pass


@check_perms()
@start.command()
async def malping(ctx):
    if mal_ping.is_running():
        await ctx.send('already mal pinging apes')
        return
    mal_ping.start()
    await ctx.send('mal pinging apes')


@check_perms()
@start.command()
async def pingpong(ctx):
    if bot.get_cog('pingpong_game'):
        await ctx.send('game already running')
        return
    bot.add_cog(pingpong_game(bot, ctx))


@check_perms()
@stop.command()
async def malping(ctx):
    if not mal_ping.is_running():
        await ctx.send('not yet mal pinging apes')
        return
    mal_ping.cancel()
    await ctx.send('stopped mal pinging apes')


@check_perms()
@stop.command()
async def pingpong(ctx):
    if bot.get_cog('pingpong_game'):
        bot.remove_cog('pingpong_game')
        return
    await ctx.send('no game running')


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


@bot.command()
@check_perms()
async def test(ctx):
    db = sqlite3.connect('stuff.db')
    cursor = db.cursor()
    cursor.execute('SELECT user_id FROM main')
    result = cursor.fetchone()
    await ctx.send(result)
    # if result is None:
    #     sql = ('INSERT INTO main(user_id, score_earned) VALUES(?, ?)')
    #     val = (ctx.author.id, 0)
    #     await ctx.send(ctx.author.id)
    #     await ctx.send(f'User {ctx.author.mention} has been added')
    # elif result is not None:
    #     sql = (f'UPDATE main SET score_earned = ? WHERE user_id = {ctx.author.id}')
    #     result3 = (f'SELECT score_set FROM main WHERE user_id = {ctx.author.id}')
    #     await ctx.send('ok')
    #     # result2 = cursor.fetchone()
    #     # await ctx.send(result2[0])
    #     # old_score = int(result2[0])
    #     # val = (old_score + 1,)
    #     # await ctx.send(f'1 point has been added to {ctx.author.mention}')
    # cursor.execute(sql, result3)
    # db.commit()
    cursor.close()
    db.close()


@bot.command(aliases=['tictactoe', 'tic-tac-toe'])
async def ttt(ctx):
    async def make_board():
        return await ctx.send('{}{}{}\n{}{}{}\n{}{}{}'.format(*board))

    async def get_emoji(ctx, player):
        def check(message):
            return message.channel == ctx.channel and message.author.id == player.id
        await ctx.send('Send an emoji you want to use:')
        try:
            emoji_choice = await bot.wait_for('message', check=check, timeout=30)
            if test_if_emoji(emoji_choice.content):
                return emoji_choice.content
        except asyncio.TimeoutError:
            pass
        if player == challenger_player:
            return ':x:'
        else:
            return ':o:'

    async def opponent():
        def check_opponent(message):
            return message.channel == ctx.channel and message.author.id != ctx.author.id and message.content.lower() in ('join', 'join.') and message.author.id not in in_command
        try:
            opponent = await bot.wait_for('message', check=check_opponent, timeout=120)
            in_command.append(opponent.author.id)
            return opponent.author
        except asyncio.TimeoutError:
            await ctx.send('no one joined, game cancelled')
            return False

    async def gameplay(last_message):
        async def turn(player, last_message):
            def check(message):
                return message.channel == ctx.channel and message.content.isdigit() and 0 < int(message.content) < 10 and message.author.id == player[0].id
            while True:
                next_message = await ctx.send(f'{player[0].mention} pick number (1-9)')
                try:
                    number = await bot.wait_for('message', check=check, timeout=45)
                except asyncio.TimeoutError:
                    await ctx.send('no response, game cancelled')
                    return
                if board[int(number.content) - 1] == SQUARE:
                    board[int(number.content) - 1] = player[1]
                    await last_message.delete()
                    await next_message.edit(content='{}{}{}\n{}{}{}\n{}{}{}'.format(*board))
                    break
                else:
                    await ctx.send(random.choice(TTT_WRONG_PICK))
            if not await check_winner(player[0]):
                return False
            return next_message
        while True:
            last_message = await turn(first_player, last_message)
            if not last_message:
                return
            last_message = await turn(second_player, last_message)
            if not last_message:
                return

    async def check_winner(player):
        async def check_three(spot1, spot2, spot3):
            if board[spot1] == board[spot2] == board[spot3] and board[spot1] != SQUARE:
                return await ctx.send(f'{player.mention} {board[spot1]} wins {random.choice(LOOT)}')
        if await check_three(0, 1, 2):
            return
        if await check_three(3, 4, 5):
            return
        if await check_three(6, 7, 8):
            return
        if await check_three(0, 3, 6):
            return
        if await check_three(1, 4, 7):
            return
        if await check_three(2, 5, 8):
            return
        if await check_three(0, 4, 8):
            return
        if await check_three(2, 4, 6):
            return
        if SQUARE not in board:
            await ctx.send('It\'s a tie!')
            return
        return True

    board = [SQUARE, SQUARE, SQUARE, SQUARE, SQUARE, SQUARE, SQUARE, SQUARE, SQUARE]
    last_message = await make_board()
    challenger_player = ctx.author
    challenger_emoji = await get_emoji(ctx, challenger_player)
    await ctx.send('Type **join** to join:')
    opponent_player = await opponent()
    if not opponent_player:
        return
    opponent_emoji = await get_emoji(ctx, opponent_player)
    first_player, second_player = random.sample([(challenger_player, challenger_emoji), (opponent_player, opponent_emoji)], k=2)
    await gameplay(last_message)
    in_command.remove(opponent_player.id)


bot.run(('OTMwMTE3NTIxMDI4Mjg0NDU2.YdxNcQ.zWECj8ePVa85apxw96Ka2Et8iL0'))
