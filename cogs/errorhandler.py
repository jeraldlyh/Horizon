import discord
import cogs.utils.checks

from discord.ext import commands
from cogs.utils.embed import (passembed, errorembed)

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()  
    async def on_command_error(self, ctx, error, bypass=False):
        # Do nothing if the command/cog has its own error handler
        if (
            hasattr(ctx.command, "on_error")
            or (ctx.command and hasattr(ctx.cog, f"{ctx.command.cog_name}_error"))
            and not bypass
            ):
            pass

        if isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description=f'Command Usage: ``{ctx.prefix}{ctx.command.name} <{error.param.name}>``')
            await ctx.send(embed=eembed)

        if type(error) == cogs.utils.checks.EconomyChannel:
            lootLake = discord.utils.get(ctx.message.guild.channels, name='loot-lake').mention
            pleasantPark = discord.utils.get(ctx.message.guild.channels, name='pleasant-park').mention
            tiltedTowers = discord.utils.get(ctx.message.guild.channels, name='tilted-towers').mention
            eembed = errorembed(description=f'{ctx.author.mention} Command can only be used in {lootLake}, {pleasantPark}, {tiltedTowers}') 
            return await ctx.send(embed=eembed)

        elif type(error) == cogs.utils.checks.NoDonator:
            titanDonor = discord.utils.get(ctx.message.guild.roles, name='Titan Donator').mention
            mysticDonor = discord.utils.get(ctx.message.guild.roles, name='Mystic Donator').mention
            immortalDonor = discord.utils.get(ctx.message.guild.roles, name='Immortal Donator').mention
            eembed = errorembed(description=f'{ctx.author.mention} Want to be claim this **Supporter** kit? You have to be either a {titanDonor}, {mysticDonor} or {immortalDonor}')
            return await ctx.send(embed=eembed)
        
        elif type(error) == cogs.utils.checks.NotRegistered:
            eembed = errorembed(description=f'{ctx.author.mention} You are currently not registered yet. Kindly type ``.register`` to be registered.')
            return await ctx.send(embed=eembed)

# Adding the cog to main script
def setup(bot):
    bot.add_cog(ErrorHandler(bot))
