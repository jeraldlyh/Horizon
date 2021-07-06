import os
import discord
import pytz
import datetime

from discord.ext import commands
from datetime import timedelta
from dotenv import load_dotenv

from cogs.utils.embed import passembed
from cogs.utils.embed import errorembed
from cogs.utils import logins


extensions = [
        'cogs.classes',
        'cogs.dungeon',
        'cogs.errorhandler',
        'cogs.games', 
        'cogs.general', 
        'cogs.kits',
        'cogs.logs', 
        'cogs.mod', 
        'cogs.profile', 
        'cogs.rank', 
        'cogs.rewards', 
        'cogs.roles',
        'cogs.shop',
        'cogs.tournament',
        'cogs.translation',
        'cogs.usage',
        'cogs.voicechannel'
        ]


bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

def check_me(ctx):
    return ctx.message.author.id == os.getenv("OWNER_ID")

    
# Shutdown of bot
@bot.command()
@commands.check(check_me)
async def shutdown(ctx):
    print('{0} has been shutdown by {1}.'.format(bot.user.name, ctx.message.author))
    pembed = passembed(description='**{0} has been shutdown by {1}**'.format(bot.user.name, ctx.message.author))
    await ctx.send(embed=pembed)
    await bot.logout()
  
    
# Load specific cogs
@bot.command()
@commands.check(check_me)
async def load(ctx, cog: str=None):
    if cog == None:
        eembed = errorembed(description='**Please specify an extension to load.**')
        await ctx.send(embed=eembed)
    else:
        try:
            bot.load_extension('cogs.' + cog.lower())
            pembed = passembed(description='**Successfully loaded extension {0}.**'.format(cog))
            await ctx.send(embed=pembed)
        except Exception as e:
            eembed = errorembed(description='**There was an error loading extension {0}.**'.format(cog))
            await ctx.send(embed=eembed)
            print('Failed to load extension {0} due to {1}'.format(cog, e))

@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return            
            
# Unload specific cogs
@bot.command()
@commands.check(check_me)
async def unload(ctx, cog: str=None):
    if cog == None:
        eembed = errorembed(description='**Please specify an extension to unload.**')
        await ctx.send(embed=eembed)
    else:
        try:
            bot.unload_extension('cogs.' + cog.lower())
            pembed = passembed(description='**Successfully unloaded extension {0}.**'.format(cog))
            await ctx.send(embed=pembed)
        except Exception as e:
            eembed = errorembed(description='**There was an error unloading extension {0}.**'.format(cog))
            await ctx.send(embed=eembed)
            print('Failed to unload extension {0} due to {1}'.format(cog, e))

@unload.error
async def unload_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return 
        
# Reload specific cogs
@bot.command()
@commands.check(check_me)
async def reload(ctx, cog: str=None):
    if cog == None:
        eembed = errorembed(description='**Please specify an extension to reload.**')
        await ctx.send(embed=eembed)
    else:
        try:
            bot.unload_extension('cogs.' + cog.lower())
            bot.load_extension('cogs.' + cog.lower())
            pembed = passembed(description='**Successfully reloaded extension {0}.**'.format(cog))
            await ctx.send(embed=pembed)
        except Exception as e:
            eembed = errorembed(description='**There was an error reloading extension {0}.**'.format(cog))
            await ctx.send(embed=eembed)
            print('Failed to reload extension {0} due to {1}'.format(cog, e))
           
@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return 

# Leaves Server
@bot.command()
@commands.check(check_me)
async def leaveserver(ctx, server: int):
    servertoleave = bot.get_guild(server)
    await servertoleave.leave()
    pembed = passembed(description='**{0} has successfully left the server.**'.format(bot.name))    
    await ctx.send(embed=pembed)
    
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(name='FortniteAsia', type=3))
    time_now = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
    login_time = time_now.strftime('%d-%m-%Y %I:%M %p')
    print("-----------------")
    print('Logged in as {0} at {1}'.format(bot.user.name, login_time))

    
@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None
        
if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print('Loaded {0}'.format(extension))
        except Exception as e:
            raise Exception
            print(e)
            
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))

