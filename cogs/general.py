import asyncio
import discord
import datetime
import pytz
import ast
import json
import random
import os
from discord.ext import commands

from cogs.utils import logins
from cogs.utils.embed import passembed
from cogs.utils.embed import errorembed

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def check_me(ctx):
        return ctx.message.author.id == os.getenv("OWNER_ID")
    
    # Shows local server time
    @commands.command()
    async def time(self, ctx):
        # Singapore Timezone
        dt_sg = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
        # Using Canada as Fortnite Timezone
        dt_et = datetime.datetime.now(tz=pytz.timezone('Canada/Eastern'))
        embed=discord.Embed(title="Fortnite Patches", description="Patches are usually released around Coordinated Universal Time (UTC-5) 4/5AM  which is equivalent to Greenwich Mean Time (GMT+8) 5/6PM", color=discord.Colour.blue())
        embed.add_field(name="Local Server Time of Horizon", value=format(dt_sg, "**GMT+8 %I:%M %p**"), inline=True)
        embed.add_field(name="Fortnite Server Time", value=format(dt_et, "**UTC-5 %I:%M %p**"), inline=True)
        await ctx.send(embed=embed)
        
    # Nickname command
    @commands.command()
    async def setnick(self, ctx, *, nickname):
        guild_id = ctx.message.guild.id
        if ctx.message.channel.name != 'bot-spam':
            spam = discord.utils.get(ctx.message.guild.channels, name='bot-spam')
            eembed = errorembed(description='{0} Commands can only be used in {1}'.format(ctx.message.author.mention, spam.mention))
            return await ctx.send(embed=eembed)
        else:
            guild_id = ctx.message.guild.id
            if ctx.message.channel.name != 'bot-spam':
                return await ctx.send('no')
            else:
                wks = logins.gSheets().worksheet('Nicknames')
                if str(guild_id) in [x for x in wks.col_values(1) if x != 'Servers']:
                    guildCell = wks.find(str(guild_id))
                    guildCellRow = guildCell.row
                    guildCellCol = guildCell.col
                    nickNames = wks.cell(guildCellRow, guildCellCol+1).value
                    nameList = ast.literal_eval(nickNames)            
                    if str(ctx.message.author.id) in nameList:
                        eembed = errorembed(description='{0} Please refer to [this](https://discordapp.com/channels/376595440734306306/386784154571898880/557467607020732425) and contact <@!545977500275048448> to change your nickname again.'.format(ctx.message.author.mention))
                        await ctx.send(embed=eembed)
                    else:
                        nameList.append(str(ctx.message.author.id))
                        wks.update_cell(guildCellRow, guildCellCol+1, str(nameList))
                        await ctx.message.author.edit(nick=nickname)
                        pembed = passembed(description='Successfully updated your nickname to {0}.'.format(nickname))
                        await ctx.send(embed=pembed)
                else:
                    wks.append_row([str(guild_id), "['{0}']".format(ctx.message.author.id)])
                    await ctx.message.author.edit(nick=nickname)
                    pembed = passembed(description='Successfully updated your nickname to {0}.'.format(nickname))
                    await ctx.send(embed=pembed)

    @setnick.error
    async def setnick_error(self, error, ctx):
        if isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Please input your desired nickname you wish to change.')
            await ctx.send(embed=eembed)

    # Grant access to change nickname 
    @commands.command()
    @commands.has_any_role('Server Support')
    async def grant(self, ctx, user: discord.Member):
        guild_id = ctx.message.guild.id
        wks = logins.gSheets().worksheet('Nicknames')
        if str(guild_id) in [x for x in wks.col_values(1) if x != 'Servers']:
            guildCell = wks.find(str(guild_id))
            guildCellRow = guildCell.row
            guildCellCol = guildCell.col
            nickNames = wks.cell(guildCellRow, guildCellCol+1).value
            nameList = ast.literal_eval(nickNames)
            nameList.remove(str(user.id))
            wks.update_cell(guildCellRow, guildCellCol+1, str(nameList))
            pembed = passembed(description='{0} has been granted access to change nickname.'.format(user.name))
            await ctx.send(embed=pembed)
    
    @grant.error
    async def grant_error(self, error, ctx):
        if isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Please indicate which user you wish grant access to.')
            await ctx.send(embed=eembed)
        elif isinstance(error, commands.CheckFailure):
            return
    
    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def giveaway(self, ctx, channel: discord.TextChannel, role: discord.Role):
        embed = discord.Embed(description='Kindly enter the title for the giveaway.', color=discord.Color.green())
        giveAway = await ctx.send(embed=embed)
        # Title of Giveaway
        try:
            def check(message):
                return message.author == ctx.author
            giveAwayTitle = await self.bot.wait_for('message', check=check, timeout=30)
        except:
            errorEmbed = discord.Embed(description='Giveaway has timed out. Kindly retry again.', color=discord.Color.red())
            return await giveAway.edit(embed=errorEmbed)
         
        # # Prize of Giveaway
        # embed = discord.Embed(description='What is the prize for the giveaway?', color=discord.Color.green())
        # await giveAway.edit(embed=embed)
        # try:            
        #     prize = await self.bot.wait_for('message', timeout=30)
        # except:
        #     errorEmbed = discord.Embed(description='Timeout', color=discord.Color.red())
        #     return await giveAway.edit(embed=errorEmbed)
        
        # Duration of Giveaway
        embed = discord.Embed(description='When does the giveaway ends?', color=discord.Color.green())
        await giveAway.edit(embed=embed)
        try:
            def check(message):
                return message.author == ctx.author
            giveAwayEnd = await self.bot.wait_for('message', check=check, timeout=30)
        except:
            errorEmbed = discord.Embed(description='Giveaway has timed out. Kindly retry again.', color=discord.Color.red())
            return await giveAway.edit(embed=errorEmbed)
        
        # Giveaway Message    
        embed = discord.Embed(title=giveAwayTitle.content, description=f'Prize - {role.mention}', color=discord.Color(0xae2323))
        embed.set_author(name='Ongoing Giveaway')
        embed.set_footer(text=f'React 🍩 to participate ● Ends at {giveAwayEnd.content}')
        giveAwayMsg = await channel.send(embed=embed)
        await giveAwayMsg.add_reaction('🍩')

  
        
    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def rollgiveaway(self, ctx, messageID, count):        
        giveAwayMsg = await ctx.message.channel.fetch_message(messageID)
        
        #List of users of first emoji in the list
        msgReactions = giveAwayMsg.reactions[0]
        msgReactionList = await msgReactions.users().flatten()
        msgReactionList.remove(ctx.me) # Remove Bot's reaction
        
        title = giveAwayMsg.embeds[0].title
        prize = giveAwayMsg.embeds[0].description
        roleID = (''.join(i for i in prize if i.isdigit()))
        role = ctx.message.guild.get_role(int(roleID))
        winner = random.sample(msgReactionList, int(count))
        userNames = []
        for user in list(winner):
            try:
                await user.add_roles(role)
                userNames.append(user.mention)
            except AttributeError:
                continue
        embed = discord.Embed(title=title , description=('Winners: ' + ','.join(userNames[:25]) + ' + more...' if len(userNames) > 25 else (','.join(userNames))), color=discord.Color(0x222121))   
        embed.set_author(name='Giveaway Expired')
        embed.set_footer(text='Thanks for participating!')
        await giveAwayMsg.edit(embed=embed)
        
    @commands.command()
    async def rules(self, ctx):
        '''Warn Template for FortniteAsia'''
        embed = discord.Embed(color=discord.Color.purple())
        embed.add_field(name='Abuse of Rank Bot', value="Exploiting of bot is strictly not tolerated. Mimicking another user's IGN or creation of smurf/alternate accounts to obtain a higher rank than your current skill level is not allowed. Note that you have receieved a strike and will not be able to use the rank command again.")
        embed.add_field(name='Foreign Languages', value='Violation of rules - Being a server dedicated to the Asia region, use ONLY english as a mean of communication. Refrain from using foreign languages unless other parties consent to do so. Note that subsequent warnings on your profile may cause you to get banned.')
        embed.add_field(name='Advertising', value='Violation of rules - Advertisement is strictly not allowed unless permitted to do so. Note that subsequent warnings on your profile may result in you getting banned.')
        embed.add_field(name='Hate Speech', value='Violation of rules - Trash-talking/Hate speech against any particular person or a group of people is not tolerated. Note that subsequent warnings on your profile may cause you to get banned.')
        embed.add_field(name='Hacking/Cheating', value="Violation of rules - Hacking/Cheating are against the Terms of Services (TOS) of Fortnite. Note that you're being banned from FortniteAsia till investigation has been completed.")
        embed.add_field(name='NSFW', value='Violation of rules - Such contents are not allowed in this friend gaming community.  Note that subsequent warnings on your profile may cause you to get banned.')
        embed.add_field(name='Spamming', value='Violation of rules - Spamming hinders the community from finding people to play with in the text channels and is not tolerated. Note that subsequent warnings on your profile may result in you getting banned.')
        embed.add_field(name='Troll', value='Violation of rules - Any form of trolling such as earraping in voice channels will not be condemned.  Note that subsequent warnings on your profile may cause you to get banned.')
        embed.add_field(name='Buy/Sell Accounts', value='Violation of rules - Actions such as account selling, buying, sharing, and/or trading are against the Terms of Services (TOS) of Fortnite, and your account may be banned for this offense. Note that such behaviour is not tolerated in our server and has resulted in you getting banned.')
        embed.add_field(name='Misusing of Channels', value='Violation of rules - Ensure you use appropriate channels to communicate and misusing of channels may result in you getting timed out or banned.')
        embed.add_field(name='Profanities', value="Violation of rules - Usage of profanities against people of other culture/countries is not accepted in this server where it's based in Asia. Note that subsequent warnings on your profile may result in you getting banned.")
        embed.set_author(name='Warn Template', icon_url='https://cdn.discordapp.com/attachments/507933635341451270/509296817259675658/FA_main_server_27.10.18.png')
        embed.set_footer(text='• Kindly issue out warnings accordingly')
        await ctx.send(embed=embed)
    
    @commands.command()
    async def serverinfo(self, ctx):
        '''Displays Server information'''
        if ctx.message.channel.name != 'bot-spam':
            spamChannel = discord.utils.get(ctx.message.guild.channels, name='bot-spam')
            embed = discord.Embed(description='{0} Command can only be used in {1}.'.format(ctx.message.author.mention, spamChannel.mention), color=discord.Colour.red())
            return await ctx.send(embed=embed)
        else:    
            guild = ctx.message.guild
            online = len([member.status for member in guild.members 
                            if member.status == discord.Status.online or member.status == discord.Status.idle])
            total_users = len(guild.members)
            text_channels = len([x for x in guild.channels if isinstance(x, discord.TextChannel)])
            voice_channels = len([x for x in guild.channels if isinstance(x, discord.VoiceChannel)])
            created_at = guild.created_at.strftime('%d %b %Y')
            embed=discord.Embed(color=0xa59c9c, timestamp=guild.created_at)
            embed.set_author(name=guild.name, icon_url=guild.icon_url)
            embed.set_thumbnail(url=guild.icon_url)
            embed.add_field(name='Owner', value=str(guild.owner.mention))
            embed.add_field(name="Server Region", value=str(guild.region))
            embed.add_field(name='Text Channels', value=text_channels)
            embed.add_field(name='Voice Channels', value=voice_channels)
            embed.add_field(name='Members', value=total_users)
            embed.add_field(name='Online', value=online)
            embed.add_field(name='Roles', value=len(guild.roles))
            embed.add_field(name='Verification Level', value=str(guild.verification_level))
            embed.set_footer(text='Server Created at ')
            await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member=None):
        '''Displays User information'''
        if ctx.message.channel.name != 'bot-spam':
            spamChannel = discord.utils.get(ctx.message.guild.channels, name='bot-spam')
            embed = discord.Embed(description='{0} Command can only be used in {1}.'.format(ctx.message.author.mention, spamChannel.mention), color=discord.Colour.red())
            return await ctx.send(embed=embed)
        else:    
            if member is None:
                member = ctx.message.author
            roles = [x.name for x in member.roles if x.name != "@everyone"]
            if roles: 
                roles = sorted(member.roles, key=lambda c: c.position)
                rolenames = ' '.join([r.mention for r in roles if r.name != "@everyone"])
            else:
                rolenames = 'None'
            guild = ctx.message.guild
            timestamp=(datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')))
            user_created = member.created_at.strftime('%d %b %Y %H:%M %p')        
            user_joined = member.joined_at.strftime('%d %b %Y %H:%M %p')
            join_position = sorted(guild.members, key=lambda m: m.joined_at).index(member) + 1
            embed=discord.Embed(color=0xa59c9c, timestamp=timestamp)
            embed.set_author(name=member, icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)        
            embed.add_field(name='Nickname', value=member.nick)
            embed.add_field(name='Registered', value=user_created)
            embed.add_field(name='Join Position', value=join_position)   
            embed.add_field(name='Joined', value=user_joined)
             # Minus @everyone role
            roles_number = [x for x in rolenames.split() if x != 'None'] 
            #roles_number = rolenames.split()
            embed.add_field(name='Roles [{0}]'.format(len(roles_number)), value=rolenames)
            embed.add_field(name='Status', value=member.status)
            embed.set_footer(text='ID: {0} '.format(member.id))
            await ctx.send(embed=embed) 
    
    @commands.command()
    async def help(self, ctx):
        if ctx.message.channel.name not in ['bot-spam', 'loot-lake', 'pleasant-park', 'tilted-towers']:
            spamChannel = discord.utils.get(ctx.message.guild.channels, name='bot-spam').mention
            lootLake = discord.utils.get(ctx.message.guild.channels, name='loot-lake').mention
            pleasantPark = discord.utils.get(ctx.message.guild.channels, name='pleasant-park').mention
            tiltedTowers = discord.utils.get(ctx.message.guild.channels, name='tilted-towers').mention
            eembed = errorembed(description=f'{ctx.author.mention} Command can only be used in {spamChannel}, {lootLake}, {pleasantPark}, {tiltedTowers}') 
            return await ctx.send(embed=eembed)
        embed = discord.Embed(color=0x8ce498)
        embed.add_field(name='General', value='`.setnick` - Change your nickname displayed in the server **once**\n `.rank <platform>` - Obtain a role based on your Fortnite **lifetime** K/D.\n `.userinfo <User>` - Displays information of **Discord** profile')
        embed.add_field(name='Games', value='`.coinflip <Side> <Amount>` - Flips a coin, either **heads** or **tails**\n `.slots` - Earns **experience** by playing slots machine\n `.dice <Amount>` - Rolls a dice from **1 to 6** with a winning multiplier of **300%**\n `.rps <User> <Amount>` - Challenge an User to **rock-paper-scissors** game')
        embed.add_field(name='Kits', value='`.daily` - Claims your **daily** currency kit\n `.weekly` - Claims your **weekly** currency kit\n `.supporter` - Claims your **supporter** currency kit\n `.nitro` - Claims your **nitro** currency kit')
        embed.add_field(name='Information', value='`.top` - Displays **global** leaderboard\n `.profile` - Displays information of **your profile**\n `.inventory` - Displays **gun** inventory\n `.cooldown`  - Checks the **status** of currency kits')
        embed.add_field(name='Shop', value='`.shop` - Displays **item** that are available for purchase\n `.buy <ID> <Amount>` - **Purchase** an item from the shop')
        embed.add_field(name='Events', value='`.lottery <Amount>` - Starts a **lottery** for the community that lasts for 3 minutes\n `.participate <Amount>` - Purchase a ticket in **Llama Pinata** event\n `.chances` - Chance to win the **Llama Pinata** event')
        embed.add_field(name='Tournament', value='`.bet <User>` - Bets **1,000 Wood** on the desired player in the Tournament')
        embed.add_field(name='RPG Game', value='`.tree` - Displays **available classes**\n `.choose <JobName>` - **Selects** a class for RPG\n `.evolve` - **Advances** to the next job in the class tree\n `.dungeon <dungeonID>` - Starts an **adventure** in dungeon\n `.dungeons` - Display **available** dungeons\n `.status` - Checks the **status** of adventure\n `.consume <Potion>` - **Increases HP** by consuming health/shield potion\n `.equip <weaponID>` - **Equips** a specific weapon\n `.dump <weaponID>` - **Dumps** a specific weapon\n `.hunt` - **Hunt** monsters in the current dungeon')
        embed.add_field(name='Etc', value='`.vote <User>` - **Upvotes** an User\n `.claim <Type>` - Opens a **crate/gift** using a **key**\n `.transfer <User> <Amount>` - **Transfers** an amount to specified User')
        await ctx.author.send(embed=embed)
        await ctx.send(f'{ctx.author.mention} Message has been sent to your DMs')
        
# Adding the cog to main script
def setup(bot):
    bot.add_cog(General(bot))
    
