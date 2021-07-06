import asyncio
import discord
import datetime
import pytz
import random
import colorsys
import os
from discord.ext import commands

from cogs.utils.embed import passembed
from cogs.utils.embed import errorembed


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.case = {}
    
    def check_me(ctx):
        return ctx.message.author.id == os.getenv("OWNER_ID")
    
    # Purge message
    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def purge(self, ctx, amount=100):
        amount = int(amount)
        await ctx.channel.purge(limit=amount+1)
        pembed = passembed(description='{0} messages have been deleted.'.format(amount))
        await ctx.send(embed=pembed, delete_after=25)
        
    @purge.error
    async def purge_error(self, ctx, error):    
        if isinstance(error, commands.CheckFailure):
            return
    
    # Ban command
    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def ban(self, ctx, user: discord.Member, *, reason: str=None):
        if reason is None:
            reason = 'no reason'
        await user.ban(reason=reason)
        pembed = passembed(description='{0} has been banned by {1} due to {2}.'.format(user, ctx.message.author, reason))
        await ctx.send(embed=pembed)
        # Logging
        for channel in ctx.guild.channels:
            if channel.name == 'mod-logs':
                guild_id = ctx.message.guild.id
                if guild_id in self.case:
                    self.case[guild_id]+=1
                    embed=discord.Embed(color=discord.Color.red())
                    embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                    embed.set_author(name='Case #{0} | Ban | {1}'.format(int(self.case.get(guild_id)), user), icon_url=user.avatar_url)
                    embed.add_field(name='User',value='{0}'.format(user.mention), inline=True)
                    embed.add_field(name='Moderator',value='{0}'.format(ctx.message.author.mention), inline=True)
                    embed.add_field(name='Reason', value='{0}'.format(reason), inline=True)
                    embed.set_footer(text='ID: {0}'.format(user.id))
                    await channel.send(embed=embed)
                else:
                    self.case[guild_id]=0
                    self.case[guild_id]+=1
                    print(self.case)
                    embed=discord.Embed(color=discord.Color.red())
                    embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                    embed.set_author(name='Case #{0} | Ban | {1}'.format(int(self.case.get(guild_id)), user), icon_url=user.avatar_url)
                    embed.add_field(name='User',value='{0}'.format(user.mention), inline=True)
                    embed.add_field(name='Moderator',value='{0}'.format(ctx.message.author.mention), inline=True)
                    embed.add_field(name='Reason', value='{0}'.format(reason), inline=True)
                    embed.set_footer(text='ID: {0}'.format(user.id))
                    await channel.send(embed=embed)
                    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Please indicate the User you wish to ban.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.BadArgument):
            eembed = errorembed(description='Invalid User. Please tag the User you wish to ban.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.CheckFailure):
            return

    # Force ban command
    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def forceban(self, ctx, id: int, *, reason: str=None):
        if reason is None:
            reason = 'no reason'
        try:
            limitedUser = await self.bot.fetch_user(id)
            pembed = passembed(description='{0} has been banned by {1} due to {2}.'.format(user, ctx.message.author, reason))
            await ctx.send(embed=pembed)
            
        except Exception as e:
            if 'Unknown User' in str(e):
                eembed = errorembed(description='User ID could not be found. Please input a valid User ID.')
                await ctx.send(embed=eembed)

    @forceban.error
    async def forceban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Please indicate the User you wish to force ban.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.BadArgument):
            eembed = errorembed(description='User ID is invalid. Please input a valid User ID.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.CheckFailure):
            return 
        
    # Unban command
    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def unban(self, ctx, id: int):
        try:
            banuser = await self.bot.fetch_user(id)
            await ctx.guild.unban(banuser)
            pembed = passembed(description='{0} has been unbanned by {1} due to {2}.'.format(banuser, ctx.message.author, reason))
            await ctx.send(embed=pembed)
        except Exception as e:
            if 'Unknown Ban' in str(e):
                eembed = errorembed(description='{0} {1} is not banned in the server. Please check again.'.format(ctx.message.author.mention, banuser))
                await ctx.send(embed=eembed)
            elif 'Unknown User' in str(e):
                eembed = errorembed(description='User ID could not be found. Please input a valid User ID.')
                await ctx.send(embed=eembed)
        # Logging
        for channel in ctx.guild.channels:
            if channel.name == 'mod-logs':
                guild_id = ctx.message.guild.id
                if guild_id in self.case:
                    self.case[guild_id]+=1
                    print(self.case)
                    embed=discord.Embed(color=discord.Color.red())
                    embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                    embed.set_author(name='Case #{0} | Unban | {1}'.format(int(self.case.get(guild_id)), banuser), icon_url=banuser.avatar_url)
                    embed.add_field(name='User',value='{0}'.format(banuser.mention), inline=True)
                    embed.add_field(name='Moderator',value='{0}'.format(ctx.message.author.mention), inline=True)
                    embed.set_footer(text='ID: {0}'.format(banuser.id))
                    await channel.send(embed=embed)
                else:
                    self.case[guild_id]=0
                    self.case[guild_id]+=1
                    print(self.case)
                    embed=discord.Embed(color=discord.Color.red())
                    embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                    embed.set_author(name='Case #{0} | Unban | {1}'.format(int(self.case.get(guild_id)), banuser), icon_url=banuser.avatar_url)
                    embed.add_field(name='User',value='{0}'.format(banuser.mention), inline=True)
                    embed.add_field(name='Moderator',value='{0}'.format(ctx.message.author.mention), inline=True)
                    embed.set_footer(text='ID: {0}'.format(banuser.id))
                    await channel.send(embed=embed)
        
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Please indicate the User ID you wish to unban.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.BadArgument):
            eembed = errorembed(description='User ID is either not banned or invalid/not found. Please input a valid User ID.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.CheckFailure):
            return
       
           
    # Mute command
    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def mute(self, ctx, user: discord.Member, reason: str=None, time: int=5):
        # If not specified, defaulted as 5 minutes.
        secs = time * 60
        if reason is None:
            reason = 'no reason'
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, overwrite=discord.PermissionOverwrite(send_messages=False))
            elif isinstance(channel, discord.VoiceChannel):
                await ctx.channel.set_permissions(user, overwrite=discord.PermissionOverwrite(connect=False))
        pembed = passembed(description='{0} has been muted for {1} minutes due to {2}.'.format(user, time, reason))
        await ctx.send(embed=pembed)
        # Logging
        for channel in ctx.guild.channels:
            if channel.name == 'mod-logs':
                guild_id = ctx.message.guild.id
                if guild_id in self.case:
                    self.case[guild_id]+=1
                    print(self.case)
                    embed=discord.Embed(color=discord.Color.red())
                    embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                    embed.set_author(name='Case #{0} | Mute | {1}'.format(int(self.case.get(guild_id)), user.name), icon_url=user.avatar_url)
                    embed.add_field(name='User',value='{0}'.format(user.mention), inline=True)
                    embed.add_field(name='Moderator',value='{0}'.format(ctx.message.author.mention), inline=True)
                    embed.add_field(name='Length', value='{0} mins'.format(time), inline=True)
                    embed.add_field(name='Reason', value='{0}'.format(reason), inline=True)                    
                    embed.set_footer(text='ID: {0}'.format(user.id))
                    await channel.send(embed=embed)
                else:
                    self.case[guild_id]=0
                    self.case[guild_id]+=1
                    print(self.case)
                    embed=discord.Embed(color=discord.Color.red())
                    embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                    case = self.case.get(guild_id)
                    embed.set_author(name='Case #{0} | Mute | {1}'.format(int(self.case.get(guild_id)), user.name), icon_url=user.avatar_url)
                    embed.add_field(name='User',value='{0}'.format(user.mention), inline=True)
                    embed.add_field(name='Moderator',value='{0}'.format(ctx.message.author.mention), inline=True)
                    embed.add_field(name='Length', value='{0} mins'.format(time), inline=True)
                    embed.add_field(name='Reason', value='{0}'.format(reason), inline=True)
                    embed.set_footer(text='ID: {0}'.format(user.id))
                    await channel.send(embed=embed)
        await asyncio.sleep(secs)
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, overwrite=None)
            elif isinstance(channel, discord.VoiceChannel):
                await ctx.channel.set_permissions(user, overwrite=None)
        pembed = passembed(description='{0} has been unmuted in the server.'.format(user))
        await ctx.send(embed=pembed)
        # Logging
        for channel in ctx.guild.channels:
            if channel.name == 'mod-logs':
                guild_id = ctx.message.guild.id
                if guild_id in self.case:
                    self.case[guild_id]+=1
                    print(self.case)
                    embed=discord.Embed(color=discord.Color.red())
                    embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                    embed.set_author(name='Case #{0} | Unmute | {1}'.format(int(self.case.get(guild_id)), user.name), icon_url=user.avatar_url)
                    embed.add_field(name='User',value='{0}'.format(user.mention), inline=True)
                    embed.add_field(name='Moderator',value='{0}'.format(self.bot.user.mention), inline=True)
                    embed.add_field(name='Reason', value='timeout', inline=True)
                    embed.set_footer(text='ID: {0}'.format(user.id))
                    await channel.send(embed=embed)
                else:
                    self.case[guild_id]=0
                    self.case[guild_id]+=1
                    print(self.case)
                    embed=discord.Embed(color=discord.Color.red())
                    embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                    case = self.case.get(guild_id)
                    embed.set_author(name='Case #{0} | Unmute | {1}'.format(int(self.case.get(guild_id)), user.name), icon_url=user.avatar_url)
                    embed.add_field(name='User',value='{0}'.format(user.mention), inline=True)
                    embed.add_field(name='Moderator',value='{0}'.format(self.bot.user.mention), inline=True)
                    embed.add_field(name='Reason', value='timeout', inline=True)
                    embed.set_footer(text='ID: {0}'.format(user.id))
                    await channel.send(embed=embed)
        
    @mute.error
    async def mute_error(self, ctx, error):    
        if isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Please indicate the user you wish to mute.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.BadArgument):
            eembed = errorembed(description='User could not be found. Please tag a valid User.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.CheckFailure):
            return
            
    # Unmute command
    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def unmute(self, ctx, user: discord.Member, reason: str=None):
        if reason is None:
            reason = 'no reason'
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=None)
            elif isinstance(channel, discord.VoiceChannel):
                await ctx.channel.set_permissions(user, connect=None)
        pembed = passembed(description='{0} has been unmuted in the server.'.format(user))
        await ctx.send(embed=pembed)
        # Logging
        for channel in ctx.guild.channels:
            if channel.name == 'mod-logs':
                guild_id = ctx.message.guild.id
                if guild_id in self.case:
                    self.case[guild_id]+=1
                    print(self.case)
                    embed=discord.Embed(color=discord.Color.red())
                    embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                    embed.set_author(name='Case #{0} | Unmute | {1}'.format(int(self.case.get(guild_id)), user.name), icon_url=user.avatar_url)
                    embed.add_field(name='User',value='{0}'.format(user.mention), inline=True)
                    embed.add_field(name='Moderator',value='{0}'.format(ctx.message.author.mention), inline=True)
                    embed.add_field(name='Reason', value='{0}'.format(reason), inline=True)
                    embed.set_footer(text='ID: {0}'.format(user.id))
                    await channel.send(embed=embed)
                else:
                    self.case[guild_id]=0
                    self.case[guild_id]+=1
                    print(self.case)
                    embed=discord.Embed(color=discord.Color.red())
                    embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                    case = self.case.get(guild_id)
                    embed.set_author(name='Case #{0} | Unmute | {1}'.format(int(self.case.get(guild_id)), user.name), icon_url=user.avatar_url)
                    embed.add_field(name='User',value='{0}'.format(user.mention), inline=True)
                    embed.add_field(name='Moderator',value='{0}'.format(ctx.message.author.mention), inline=True)
                    embed.add_field(name='Reason', value='{0}'.format(reason), inline=True)
                    embed.set_footer(text='ID: {0}'.format(user.id))
                    await channel.send(embed=embed)
        
    @unmute.error
    async def unmute_error(self, ctx, error):    
        if isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Please indicate the user you wish to unmute.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.BadArgument):
            eembed = errorembed(description='User could not be found. Please tag a valid User.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.CheckFailure):
            return
            
    # Announce command
    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def announce(self, ctx, channel: discord.TextChannel, *,message: str):
        await channel.send(message)
    
    @announce.error
    async def announce_error(self, ctx, error):    
        if isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Please specify text channel in the command.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.BadArgument):
            eembed = errorembed(description='Channel could not be found in the server. Please specify the correct text channel.')
            return await ctx.send(embed=eembed)
        elif 'message is a required argument' in str(error):
            eembed = errorembed(description='Please indicate your message in the command.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.CheckFailure):
            return

    # Embed announce command
    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def emannounce(self, ctx, channel: discord.TextChannel, *, message: str):
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed=discord.Embed(description="{0}".format(message), color=discord.Color((r << 16) + (g << 8) + b), icon_url=self.bot.user.avatar_url)
        #embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
        #embed.set_footer(text='Announced by {0}'.format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await channel.send(embed=embed)

    @emannounce.error
    async def emannounce_error(self, ctx, error):    
        if isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Please specify text channel in the command.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.BadArgument):
            eembed = errorembed(description='Channel could not be found. Please specify the correct text channel.')
            return await ctx.send(embed=eembed)
        elif 'message is a required argument' in str(error):
            eembed = errorembed(description='Please indicate your message in the command.')
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.CheckFailure):
            return
        
    # Set watching status
    @commands.command()
    @commands.check(check_me)
    async def watching(self, ctx, *name: str):
        type = discord.ActivityType.watching
        activity = discord.Activity(name=name, type=type)
        await self.bot.change_presence(activity=activity)
        pembed = passembed(description='Status has been updated.')
        await ctx.send(embed=pembed, delete_after=5)
    
   #@watching.error
   #async def watching_error(self, ctx, error):  
   #    if isinstance(error, commands.CheckFailure):
   #        return
    
    # Resets status of bot
    @commands.command()
    @commands.check(check_me)
    async def reset(self, ctx):
        await self.bot.change_presence(activity=discord.Activity(name=f'{str(len(bot.users))} users in FortniteAsia', type=2))
        pembed = passembed(description='Status has been reseted.')
        await ctx.send(embed=pembed, delete_after=5)
        
    @reset.error
    async def reset_error(self, ctx, error):  
        if isinstance(error, commands.CheckFailure):
            return
    
    # Lock command
    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def lock(self, ctx, channelname: discord.TextChannel=None):
        overwrite = discord.PermissionOverwrite(send_messages=False)
        # Can be used without specifying channel name
        if channelname is None:
            await ctx.message.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            pembed = passembed(description='{0} has been locked by {1}.'.format(ctx.channel.mention, ctx.message.author))
            await ctx.send(embed=pembed)
        else:
            await channelname.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            pembed = passembed(description='{0} has been locked by {1}.'.format(channelname.mention, ctx.message.author))
            await ctx.send(embed=pembed)
    
    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return 
    
    # Unlock command
    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def unlock(self, ctx, channelname: discord.TextChannel=None):
        overwrite = discord.PermissionOverwrite(send_messages=True)
        # Can be used without specifying channel name
        if channelname is None:
            await ctx.message.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            pembed = passembed(description='{0} has been unlocked by {1}.'.format(ctx.channel.mention, ctx.message.author))
            await ctx.send(embed=pembed)
        else:
            await channelname.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            pembed = passembed(description='{0} has been unlocked by {1}.'.format(channelname.mention, ctx.message.author))
            await ctx.send(embed=pembed)
    
    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return 
    
    
# Adding the cog to main script
def setup(bot):
    bot.add_cog(Mod(bot))
