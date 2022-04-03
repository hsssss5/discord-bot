from utility import *
from responses_emojis_stuff import *
import random
import asyncio


#Можно включить, чтобы бот пинговал админов
@tasks.loop(hours=1)
async def mal_ping():
    ape_to_ping = random.choice(NON_APES_ID)
    channel = bot.get_channel(TEST_CHANNEL)
    await channel.send(f'{ping_player_from_id(ape_to_ping)} {random.choice(random_message + custom_message.get(ape_to_ping, []) + custom_react.get(ape_to_ping, []))}')


#Крестики-нолики в чате с эмодзи на выбор вместо крестика и нолика
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

#Игра основанная на локальной шутке, где бот будет спамить пинги пользователей, которые отреагировали на сообщение о начале игры
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


