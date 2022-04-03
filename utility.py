import discord
from discord.ext import commands, tasks
import pickle
from responses_emojis_stuff import *

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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        pass

