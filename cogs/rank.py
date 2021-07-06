import discord
import requests
import datetime
import pytz
import os
from discord.ext import commands

from cogs.utils.embed import passembed
from cogs.utils.embed import errorembed

class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def check_me(ctx):
        return ctx.message.author.id == os.getenv("OWNER_ID")
    
    def get_role(self, server_roles, target_name):
            for each in server_roles:
                if each.name == target_name:
                    return each
            return None

    def print_nextLvl(self, begin, end, ratio):
        rang = end - begin
        if ratio >= rang * 0.00 + begin and ratio <= rang * 0.059999 + begin:
            return '[■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.06 + begin and ratio <= rang * 0.109999 + begin:
            return '[■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.11 + begin and ratio <= rang * 0.159999 + begin:
            return '[■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.16 + begin and ratio <= rang * 0.209999 + begin:
            return '[■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.21 + begin and ratio <= rang * 0.259999 + begin:
            return '[■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.26 + begin and ratio <= rang * 0.309999 + begin:
            return '[■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.31 + begin and ratio <= rang * 0.359999 + begin:
            return '[■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.36 + begin and ratio <= rang * 0.409999 + begin:
            return '[■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.41 + begin and ratio <= rang * 0.459999 + begin:
            return '[■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.46 + begin and ratio <= rang * 0.509999 + begin:
            return '[■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.51 + begin and ratio <= rang * 0.559999 + begin:
            return '[■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.56 + begin and ratio <= rang * 0.609999 + begin:
            return '[■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.61 + begin and ratio <= rang * 0.659999 + begin:
            return '[■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.66 + begin and ratio <= rang * 0.709999 + begin:
            return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□]'
        elif ratio >= rang * 0.71 + begin and ratio <= rang * 0.759999 + begin:
            return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□]'
        elif ratio >= rang * 0.76 + begin and ratio <= rang * 0.809999 + begin:
            return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□]'
        elif ratio >= rang * 0.81 + begin and ratio <= rang * 0.859999 + begin:
            return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□]'
        elif ratio >= rang * 0.86 + begin and ratio <= rang * 0.909999 + begin:
            return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□]'
        elif ratio >= rang * 0.91 + begin and ratio <= rang * 0.959999 + begin:
            return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□]'
        elif ratio >= rang * 0.96 + begin and ratio <= rang * 1.00 + begin:
            return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□]'
        elif ratio:
            return '[□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
    
    # Return the overall K/D of the fortnite player pass in parameter
    def get_ratio(self, platform, username):
        link = 'https://api.fortnitetracker.com/v1/profile/' + platform + '/' + username
        response = requests.get(link, headers={'TRN-Api-Key': os.getenv("TRN_API_KEY")})
        if response.status_code == 200:
            collection = response.json()
            if 'error' in collection:
                return "-1"
            else:
                for data_item in collection['lifeTimeStats']:
                    if data_item['key'] == 'K/d':
                        ratio = data_item['value']
                        return ratio       
        else:
            print("Error recovering fortnite data")
            return "-2"
        
    def get_matches(self, platform, username):
        link = 'https://api.fortnitetracker.com/v1/profile/' + platform + '/' + username
        response = requests.get(link, headers={'TRN-Api-Key': os.getenv("TRN_API_KEY")})
        if response.status_code == 200:
            collection = response.json()
            if 'error' in collection:
                return "-1"
            else:
                for data_item in collection['lifeTimeStats']:
                    if data_item['key'] == 'Matches Played':
                        matches = data_item['value']
                        return matches
        else:
            print("Error recovering fortnite data")
            return "-2"
    
    @commands.command()
    @commands.check(check_me)
    async def ranksetup(self, ctx):
        god_role = await ctx.guild.create_role(name='God', color=discord.Color(0xffd700))
        demigod_role = await ctx.guild.create_role(name='Demigod', color=discord.Color(0xff0000))
        grandmaster_role = await ctx.guild.create_role(name='Grandmaster', color=discord.Color(0x99cc79))
        legend_role = await ctx.guild.create_role(name='Legend', color=discord.Color(0xce9d5b))
        master_role = await ctx.guild.create_role(name='Master', color=discord.Color(0x3ca087))
        mercenary_role = await ctx.guild.create_role(name='Mercenary', color=discord.Color(0xa73b3b))
        epic_role = await ctx.guild.create_role(name='Epic', color=discord.Color(0x863ab8))
        apprentice_role = await ctx.guild.create_role(name='Apprentice', color=discord.Color(0xa2a860))
        elite_role = await ctx.guild.create_role(name='Elite', color=discord.Color(0x06b4f7))
        casual_role = await ctx.guild.create_role(name='Casual', color=discord.Color(0xb7a9f7))
        cousin_role = await ctx.guild.create_role(name='Cousin', color=discord.Color(0xbd7979))
        strike_role = await ctx.guild.create_role(name='Striked', color=discord.Color(0x2e2020))
        pembed = passembed(description='**Successfully setup the neccessary roles and channel. Please do not tamper/edit roles or channels.**')
        await ctx.send(embed=pembed)
    
    @commands.command()
    async def rank(self, ctx):        
        # List of roles
        LIST = ['Cousin', 'Casual', 'Elite', 'Apprentice', 'Epic', 'Mercenary', 'Master', 'Legend', 'Grandmaster', 'Demigod', 'God']
        WOOD_B = 0.00
        WOOD_E = 0.99
        CARTON_B = 1.00
        CARTON_E = 1.49
        BRONZE_B = 1.50
        BRONZE_E = 1.99
        SILVER_B = 2.00
        SILVER_E = 2.49
        GOLD_B = 2.50
        GOLD_E = 2.99
        PLATINUM_B = 3.00
        PLATINUM_E = 3.49
        DIAMOND_B = 3.50
        DIAMOND_E = 3.99
        RUBY_B = 4.00
        RUBY_E = 4.99
        ROYALITY_B = 5.00
        ROYALITY_E = 5.99
        ILLUMINATI_B = 6.00
        ILLUMINATI_E = 7.99
        HACKEUR_B = 8.00
        HACKEUR_E = 100        
                
        # The command .rank return attribute a rank according to the K/D of the user
        # Do not want the bot to reply to itself
        if ctx.message.author == self.bot.user:
            return
       
        # Ensure that command is used in correct channel
        if ctx.message.channel.name != 'bot-spam':
            rank = discord.utils.get(ctx.message.guild.channels, name='bot-spam')
            embed = discord.Embed(description='**{0} Command can only be used in {1}.**'.format(ctx.message.author.mention, rank.mention), color=discord.Colour.red())
            return await ctx.send(embed=embed)
            
        if discord.utils.get(ctx.message.guild.roles, name='Striked') in ctx.message.author.roles:
            return
        
        # Checks if user is exploiting the bot
        NAMES = 'Ninja' or 'DrLupo' or 'TSM_Hamlinz' or 'TSM_Daequan' or 'Liquid POACH' or 'Not Tfue'
        if ctx.message.author.display_name == NAMES:
            role = discord.utils.get(ctx.message.guild.roles, name='Striked')
            msg = "{0} Due to the violation of rules, you have been {1} and will not be able to use the command again!".format(ctx.message.author.mention, role.mention)
            embed=discord.Embed(description=msg, color=discord.Colour.red())
            await ctx.send(embed=embed)
            await ctx.message.author.add_roles(role)
                
        # Usage of command
        words = ctx.message.content.split(' ', 2)
        if len(words) < 2:
            eembed = errorembed(description="{0} Kindly indicate the platform you're playing on! Eg. .rank <platform>".format(ctx.message.author.mention))
            return await ctx.send(embed=eembed)
            
        # More acceptable platform names
        platform = words[1].lower()
        if platform == 'xbox':
            platform = 'xbl'
        elif platform == 'ps4':
            platform = 'psn'
        if platform not in ('pc','xb1','psn'):
            eembed = errorembed(description="{0} Ensure that you've selected the correct platform before using the command again! Eg. .rank <platform>".format(ctx.message.author.mention))
            return await ctx.send(embed=eembed)
            
        # Start of command    
        username = '{0}'.format(ctx.message.author.display_name)    
        matches = int(self.get_matches(platform, username))  
        dt_sg = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
        if matches <= 350 and matches != -1:
            eembed = errorembed(description="{0} In order to obtain a rank, your account must have at least **350 games** played! Continue the grind and see you at the ladder!".format(ctx.message.author.mention))
            return await ctx.send(embed=eembed)
        else:
            embed=discord.Embed(description='_Processing..._', color=discord.Colour.orange())
            await ctx.send(embed=embed)
            ratio = float(self.get_ratio(platform, username))
            if ratio >= WOOD_B and ratio <= WOOD_E:
                for list in LIST:
                    roles = discord.utils.get(ctx.message.guild.roles, name=list)
                    await ctx.message.author.remove_roles(roles)
                role = discord.utils.get(ctx.message.guild.roles, name=LIST[0])
                msg = ("{0}, You have been ranked {1}").format(ctx.message.author.mention, role.mention)
                msgRatio = "Next level: " + str(ratio) + "k/d  **→**  " + str(CARTON_B) + "k/d"
                embed=discord.Embed(description=msg, timestamp=(dt_sg), color=0xbd7979)
                embed.add_field(name=msgRatio, value=self.print_nextLvl(WOOD_B, WOOD_E, ratio), inline=False)
                embed.set_footer(text="{0}".format(ctx.message.guild.name), icon_url=ctx.message.guild.icon_url)
                await ctx.send(embed=embed)
                await ctx.message.author.add_roles(role) 
            elif ratio >= CARTON_B and ratio <= CARTON_E:
                for list in LIST:
                    roles = discord.utils.get(ctx.message.guild.roles, name=list)
                    await ctx.message.author.remove_roles(roles)
                role = discord.utils.get(ctx.message.guild.roles, name=LIST[1])
                msg = ("{0}, You have been ranked {1}").format(ctx.message.author.mention, role.mention)
                msgRatio = "Next level: " + str(ratio) + "k/d  **→**  " + str(BRONZE_B) + "k/d"
                embed=discord.Embed(description=msg, timestamp=(dt_sg), color=0xb7a9f7)
                embed.add_field(name=msgRatio, value=self.print_nextLvl(CARTON_B, CARTON_E, ratio), inline=False)
                embed.set_footer(text="{0}".format(ctx.message.guild.name), icon_url=ctx.message.guild.icon_url)
                await ctx.send(embed=embed)
                await ctx.message.author.add_roles(role)
            elif ratio >= BRONZE_B and ratio <= BRONZE_E:
                for list in LIST:
                    roles = discord.utils.get(ctx.message.guild.roles, name=list)
                    await ctx.message.author.remove_roles(roles)
                role = discord.utils.get(ctx.message.guild.roles, name=LIST[2])
                msg = ("{0}, You have been ranked {1}").format(ctx.message.author.mention, role.mention)
                msgRatio = "Next level: " + str(ratio) + "k/d  **→**  " + str(SILVER_B) + "k/d"
                embed=discord.Embed(description=msg, timestamp=(dt_sg), color=0x06b4f7)
                embed.add_field(name=msgRatio, value=self.print_nextLvl(BRONZE_B, BRONZE_E, ratio), inline=False)
                embed.set_footer(text="{0}".format(ctx.message.guild.name), icon_url=ctx.message.guild.icon_url)
                await ctx.send(embed=embed)
                await ctx.message.author.add_roles(role)
            elif ratio >= SILVER_B and ratio <= SILVER_E:
                for list in LIST:
                    roles = discord.utils.get(ctx.message.guild.roles, name=list)
                    await ctx.message.author.remove_roles(roles)
                role = discord.utils.get(ctx.message.guild.roles, name=LIST[3])
                msg = ("{0}, You have been ranked {1}").format(ctx.message.author.mention, role.mention)
                msgRatio = "Next level: " + str(ratio) + "k/d  **→**  " + str(GOLD_B) + "k/d"
                embed=discord.Embed(description=msg, timestamp=(dt_sg), color=0xa2a860)
                embed.add_field(name=msgRatio, value=self.print_nextLvl(SILVER_B, SILVER_E, ratio), inline=False)
                embed.set_footer(text="{0}".format(ctx.message.guild.name), icon_url=ctx.message.guild.icon_url)
                await ctx.send(embed=embed)
                await ctx.message.author.add_roles(role)
            elif ratio >= GOLD_B and ratio <= GOLD_E:
                for list in LIST:
                    roles = discord.utils.get(ctx.message.guild.roles, name=list)
                    await ctx.message.author.remove_roles(roles)
                role = discord.utils.get(ctx.message.guild.roles, name=LIST[4])
                msg = ("{0}, You have been ranked {1}").format(ctx.message.author.mention, role.mention)
                msgRatio = "Next level: " + str(ratio) + "k/d  **→**  " + str(PLATINUM_B) + "k/d"
                embed=discord.Embed(description=msg, timestamp=(dt_sg), color=0x863ab8)
                embed.add_field(name=msgRatio, value=self.print_nextLvl(GOLD_B, GOLD_E, ratio), inline=False)
                embed.set_footer(text="{0}".format(ctx.message.guild.name), icon_url=ctx.message.guild.icon_url)
                await ctx.send(embed=embed)
                await ctx.message.author.add_roles(role) 
            elif ratio >= PLATINUM_B and ratio <= PLATINUM_E:
                for list in LIST:
                    roles = discord.utils.get(ctx.message.guild.roles, name=list)
                    await ctx.message.author.remove_roles(roles)
                role = discord.utils.get(ctx.message.guild.roles, name=LIST[5])
                msg = ("{0}, You have been ranked {1}").format(ctx.message.author.mention, role.mention)
                msgRatio = "Next level: " + str(ratio) + "k/d  **→**  " + str(DIAMOND_B) + "k/d"
                embed=discord.Embed(description=msg, timestamp=(dt_sg), color=0xa73b3b)
                embed.add_field(name=msgRatio, value=self.print_nextLvl(PLATINUM_B, PLATINUM_E, ratio), inline=False)
                embed.set_footer(text="{0}".format(ctx.message.guild.name), icon_url=ctx.message.guild.icon_url)
                await ctx.send(embed=embed)
                await ctx.message.author.add_roles(role)  
            elif ratio >= DIAMOND_B and ratio <= DIAMOND_E:
                for list in LIST:
                    roles = discord.utils.get(ctx.message.guild.roles, name=list)
                    await ctx.message.author.remove_roles(roles)
                role = discord.utils.get(ctx.message.guild.roles, name=LIST[6])
                msg = ("{0}, You have been ranked {1}").format(ctx.message.author.mention, role.mention)
                msgRatio = "Next level: " + str(ratio) + "k/d  **→**  " + str(RUBY_B) + "k/d"
                embed=discord.Embed(description=msg, timestamp=(dt_sg), color=0x3ca087)
                embed.add_field(name=msgRatio, value=self.print_nextLvl(DIAMOND_B, DIAMOND_E, ratio), inline=False)
                embed.set_footer(text="{0}".format(ctx.message.guild.name), icon_url=ctx.message.guild.icon_url)
                await ctx.send(embed=embed)
                await ctx.message.author.add_roles(role)  
            elif ratio >= RUBY_B and ratio <= RUBY_E:
                for list in LIST:
                    roles = discord.utils.get(ctx.message.guild.roles, name=list)
                    await ctx.message.author.remove_roles(roles)
                role = discord.utils.get(ctx.message.guild.roles, name=LIST[7])
                msg = ("{0}, You have been ranked {1}").format(ctx.message.author.mention, role.mention)
                msgRatio = "Next level: " + str(ratio) + "k/d  **→**  " + str(ROYALITY_B) + "k/d"
                embed=discord.Embed(description=msg, timestamp=(dt_sg), color=0xce9d5b)
                embed.add_field(name=msgRatio, value=self.print_nextLvl(RUBY_B, RUBY_E, ratio), inline=False)
                embed.set_footer(text="{0}".format(ctx.message.guild.name), icon_url=ctx.message.guild.icon_url)
                await ctx.send(embed=embed)
                await ctx.message.author.add_roles(role) 
            elif ratio >= ROYALITY_B and ratio <= ROYALITY_E:
                for list in LIST:
                    roles = discord.utils.get(ctx.message.guild.roles, name=list)
                    await ctx.message.author.remove_roles(roles)
                role = discord.utils.get(ctx.message.guild.roles, name=LIST[8])
                msg = ("{0}, You have been ranked {1}").format(ctx.message.author.mention, role.mention)
                msgRatio = "Next level: " + str(ratio) + "k/d  **→**  " + str(ILLUMINATI_B) + "k/d"
                embed=discord.Embed(description=msg, timestamp=(dt_sg), color=0xce9d5b)
                embed.add_field(name=msgRatio, value=self.print_nextLvl(ROYALITY_B, ROYALITY_E, ratio), inline=False)
                embed.set_footer(text="{0}".format(ctx.message.guild.name), icon_url=ctx.message.guild.icon_url)
                await ctx.send(embed=embed)
                await ctx.message.author.add_roles(role) 
            elif ratio >= ILLUMINATI_B and ratio <= ILLUMINATI_E:
                for list in LIST:
                    roles = discord.utils.get(ctx.message.guild.roles, name=list)
                    await ctx.message.author.remove_roles(roles)
                role = discord.utils.get(ctx.message.guild.roles, name=LIST[9])
                msg = ("{0}, You have been ranked {1}").format(ctx.message.author.mention, role.mention)
                msgRatio = "Next level: " + str(ratio) + "k/d  **→**  " + str(HACKEUR_B) + "k/d"
                embed=discord.Embed(description=msg, timestamp=(dt_sg), color=0xff0000)
                embed.add_field(name=msgRatio, value=self.print_nextLvl(ILLUMINATI_B, ILLUMINATI_E, ratio), inline=False)
                embed.set_footer(text="{0}".format(ctx.message.guild.name), icon_url=ctx.message.guild.icon_url)
                await ctx.send(embed=embed)
                await ctx.message.author.add_roles(role)  
            elif ratio >= HACKEUR_B:
                for list in LIST:
                    roles = discord.utils.get(ctx.message.guild.roles, name=list)
                    await ctx.message.author.remove_roles(roles)
                role = discord.utils.get(ctx.message.guild.roles, name=LIST[10])
                msg = ("{0}, You have been ranked {1}").format(ctx.message.author.mention, role.mention)
                msgRatio = "You have achieved the highest role in the server with " + str(ratio) + "k/d!"
                embed=discord.Embed(description=msg, timestamp=(dt_sg), color=0xffd700)
                embed.add_field(name=msgRatio, value="'[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■]'", inline=False)
                embed.set_footer(text="{0}".format(ctx.message.guild.name), icon_url=ctx.message.guild.icon_url)
                await ctx.send(embed=embed)
                await ctx.message.author.add_roles(role) 
            elif ratio == -1:
                eembed = errorembed(description="{0} Your discord name may not be a fortnite username on that platform! Kindly type .setnick <ign> to change your username first before using the rank command again.".format(ctx.message.author.mention))
                return await ctx.send(embed=eembed)
            elif ratio == -2:
                eembed = errorembed(description='{0} The fortnite servers are offline right now. Try again later!'.format(ctx.message.author.mention))
                return await ctx.send(embed=eembed)
                

       
# Adding the cog to main script
def setup(bot):
    bot.add_cog(Rank(bot))
