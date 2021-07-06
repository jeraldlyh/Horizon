import asyncio
import discord
import os

from discord.ext import commands


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):       
        guild = self.bot.get_guild(os.getenv("SERVER_ID"))
        welcomeChannel = discord.utils.get(guild.channels, name='welcome')
        if payload.channel_id != welcomeChannel.id:
            return
        zoneRole = discord.utils.get(guild.roles, name='Zone Wars')
        wagerRole = discord.utils.get(guild.roles, name='Wagers')
        turtleRole = discord.utils.get(guild.roles, name='Turtle Wars')
    
        if str(payload.emoji) == '<:Wood:576383685042110475>':
            user = guild.get_member(payload.user_id)
            await user.add_roles(zoneRole)
        elif str(payload.emoji) == '<:Stone:576383787424808961>':
            user = guild.get_member(payload.user_id)
            await user.add_roles(wagerRole)
        elif str(payload.emoji) == '<:Metal:576383798292250651>':
            user = guild.get_member(payload.user_id)
            await user.add_roles(turtleRole)    


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):        
        guild = self.bot.get_guild(os.getenv("SERVER_ID"))
        welcomeChannel = discord.utils.get(guild.channels, name='welcome')
        if payload.channel_id != welcomeChannel.id:
            return
        zoneRole = discord.utils.get(guild.roles, name='Zone Wars')
        wagerRole = discord.utils.get(guild.roles, name='Wagers')
        turtleRole = discord.utils.get(guild.roles, name='Turtle Wars')
    
        if str(payload.emoji) == '<:Wood:576383685042110475>':
            user = guild.get_member(payload.user_id)
            await user.remove_roles(zoneRole)
        elif str(payload.emoji) == '<:Stone:576383787424808961>':
            user = guild.get_member(payload.user_id)
            await user.remove_roles(wagerRole)      
        elif str(payload.emoji) == '<:Metal:576383798292250651>':
            user = guild.get_member(payload.user_id)
            await user.remove_roles(turtleRole)        

    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def reaction(self, ctx):
        zoneRole = discord.utils.get(ctx.guild.roles, name='Zone Wars')
        wagerRole = discord.utils.get(ctx.guild.roles, name='Wagers')
        turtleRole = discord.utils.get(ctx.guild.roles, name='Turtle Wars')
        
        woodEmoji = self.bot.get_emoji(576383685042110475)
        stoneEmoji = self.bot.get_emoji(576383787424808961)
        metalEmoji = self.bot.get_emoji(576383798292250651)
        
        embed=discord.Embed(title="Notification Roles")
        embed.color = discord.Color.gold()
        embed.description = (f'Click the reaction(s) to toggle the role for notifications. This adds a role to your account so you may be alerted.\n\n {woodEmoji} {zoneRole.mention} - Receive alerts for **zone wars** related announcements\n\n {stoneEmoji} {wagerRole.mention} - Receive alerts for **wagers** related announcements\n\n {metalEmoji} {turtleRole.mention} - Receive alerts for **turtle wars** related announcements')
        embed.set_footer(text='React to join, unreact to leave • If stuck, double click')
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(':Wood:576383685042110475')
        await msg.add_reaction(':Stone:576383787424808961')
        await msg.add_reaction(':Metal:576383798292250651')

            
# Adding the cog to main script
def setup(bot):
    bot.add_cog(Roles(bot))            