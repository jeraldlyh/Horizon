import discord
import datetime
import pytz
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_guild_channel_create(self, create_channel):
        try:
            guild = create_channel.guild
            for channel in guild.channels:
                if channel.name == 'mod-logs':
                    embed=discord.Embed(color=discord.Color.green())
                    embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                    embed.set_author(name='Channel Created | {0}'.format(guild.name), icon_url=guild.icon_url)
                    embed.add_field(name='Channel Name',value='#{0}'.format(create_channel.name))
                    embed.set_footer(text='ID: {0}'.format(create_channel.id))
                    await channel.send(embed=embed)
        except:
            pass
    
    @commands.Cog.listener()    
    async def on_guild_channel_delete(self, delete_channel):
        try:
            guild = delete_channel.guild
            for channel in guild.channels:
                if channel.name == 'mod-logs':
                    embed=discord.Embed(color=discord.Color.red())
                    embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                    embed.set_author(name='Channel Deleted | {0}'.format(guild.name), icon_url=guild.icon_url)
                    embed.add_field(name='Channel Name',value='#{0}'.format(delete_channel.name))
                    embed.set_footer(text='ID: {0}'.format(delete_channel.id))
                    await channel.send(embed=embed)
        except:
            pass
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:    
            if message.author.bot: #== self.bot.user:
                return
            if message.channel.name == 'scrim-codes':
                return
            user = message.author
            for channel in message.guild.channels:
                if channel.name == 'mod-logs':
                    embed=discord.Embed(color=discord.Color.red())
                    embed.timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                    embed.set_author(name='Message Deleted | {0}'.format(user), icon_url=user.avatar_url)
                    embed.add_field(name='Channel',value='{0}'.format(message.channel.mention), inline=False)
                    embed.add_field(name='Message',value='\u200b{0}'.format(message.content), inline=False)
                    embed.set_footer(text='ID: {0}'.format(user.id))
                    await channel.send(embed=embed)
        except:
            pass
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            # Ignores if before and after message is the same
            if before.content == after.content:
                return
            # Ignores if before author is the bot
            if before.author == self.bot.user:
                return
            else:
                user = before.author
                for channel in user.guild.channels:
                    if channel.name == 'mod-logs':
                        long_before = (before.content[:250] + '...') if len(before.content) > 258 else before.content
                        long_after = (after.content[:250] + '...') if len(after.content) > 258 else after.content
                        embed=discord.Embed(color=0xf02c2c, timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')))
                        embed.set_author(name='Message Edited | {0}'.format(user), icon_url=user.avatar_url)
                        embed.add_field(name='Channel',value='{0}'.format(before.channel.mention), inline=False)
                        embed.add_field(name='Before', value=long_before, inline=False)
                        embed.add_field(name='After', value=long_after, inline=False)
                        embed.set_footer(text='ID: {0}'.format(user.id))
                        await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()    
    async def on_member_update(self, before, after):
        try:
            user = before
            # Nickname change
            if before.nick != after.nick:
                embed = discord.Embed(colour=0x9fee71)
                embed.timestamp = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                embed.set_author(name='Nickname Changed | {0}'.format(user), icon_url=user.avatar_url)
                embed.add_field(name='Before', value=before.nick, inline=False)
                embed.add_field(name='After', value=after.nick, inline=False)
                embed.set_footer(text='ID: {0}'.format(user.id))
                channel = discord.utils.get(user.guild.channels, name='mod-logs')
                await channel.send(embed=embed)
                
            # Username change
            if before.name != after.name:
                embed = discord.Embed(colour=0x9fee71)
                embed.timestamp = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
                embed.set_author(name='Username Changed | {0}'.format(user), icon_url=user.avatar_url)
                embed.add_field(name='Before', value=str(before), inline=False)
                embed.add_field(name='After', value=str(after), inline=False)
                embed.set_footer(text='ID: {0}'.format(user.id))
                channel = discord.utils.get(user.guild.channels, name='mod-logs')
                await channel.send(embed=embed)
        except:
            pass
    
    @commands.Cog.listener()    
    async def on_guild_role_create(self, role):
        try:
            server = role.guild
            for channel in server.channels:
                if channel.name == 'mod-logs':
                    embed=discord.Embed(color=discord.Color.green(), timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')))
                    embed.set_author(name='Role Created | {0}'.format(server.name), icon_url=server.icon_url)
                    embed.add_field(name='Role Name',value='{0}'.format(role.name), inline=False)
                    embed.add_field(name='Role Colour',value='{0}'.format(role.colour), inline=False)
                    embed.set_footer(text='ID: {0}'.format(role.id))
                    await channel.send(embed=embed)
        except:
            pass
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        try:
            server = role.guild
            for channel in server.channels:
                if channel.name == 'mod-logs':
                    embed=discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')))
                    embed.set_author(name='Role Deleted | {0}'.format(server.name), icon_url=server.icon_url)
                    embed.add_field(name='Role Name',value='{0}'.format(role.name), inline=False)
                    embed.add_field(name='Role Colour',value='{0}'.format(role.colour), inline=False)
                    embed.set_footer(text='ID: {0}'.format(role.id))
                    await channel.send(embed=embed)
        except:
            pass
        
    #@commands.Cog.listener()
    #async def on_message(self, message):
    #    if message.content.startswith('.'):
    #        await message.delete()
        
        
        # Tracks every single messages
        #channel = message.channel
        #author = message.author
        #content = message.clean_content
        #if author != self.bot.user and not author.bot:
        #    try:
        #        logs = discord.utils.get(author.guild.channels, name="mod-logs")
        #        await logs.send("`#{}` **{}**: {}".format(channel, author, content))
        #        await self.bot.process_commands(message)
        #    except Exception as e:
        #        print(e)
        
# Adding the cog to main script
def setup(bot):
    bot.add_cog(Logs(bot))   
