import asyncio
import discord
import random
import numpy
import collections
import pymongo 
import os

from discord.ext import commands
from cogs.utils.misc import level_up
from cogs.utils.checks import is_economy_channel, has_registered
from cogs.utils.embed import (passembed, errorembed)


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = pymongo.MongoClient(os.getenv("MONGO_DB"))
        self.db = self.client.get_database('Users')
        self.records = self.db.horizon_database
    
    async def member_win(self, ctx, member, amount):
        # Member Data
        userData = self.records.find({'userID':str(member.id)})
        for x in userData:
            woodData = float(x['Currencies']['Wood'])
            expData = float(x['Profile']['Experience'])

        woodData += float(amount)*0.98
        expData += float(amount)*2
        dataUpdate = {
                'Currencies.Wood':woodData,
                'Profile.Experience':expData
            }
        self.records.update_one({'userID':str(member.id)}, {'$set':dataUpdate}) 
        await level_up(ctx)
        
        # Author data
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            woodData = float(x['Currencies']['Wood'])
            expData = float(x['Profile']['Experience'])

        woodData -= float(amount)
        expData += float(amount)
        dataUpdate = {
                'Currencies.Wood':woodData,
                'Profile.Experience':expData
            }
        self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
        await level_up(ctx)

        
    async def author_win(self, ctx, member, amount):
        # Author data
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            woodData = float(x['Currencies']['Wood'])
            expData = float(x['Profile']['Experience'])

        woodData += float(amount)*0.98
        expData += float(amount)*2
        dataUpdate = {
                'Currencies.Wood':woodData,
                'Profile.Experience':expData
            }
        self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
        await level_up(ctx)
        
        # Member data
        userData = self.records.find({'userID':str(member.id)})
        for x in userData:
            woodData = float(x['Currencies']['Wood'])
            expData = float(x['Profile']['Experience'])

        woodData -= float(amount)
        expData += float(amount)
        dataUpdate = {
                'Currencies.Wood':woodData,
                'Profile.Experience':expData
            }
        self.records.update_one({'userID':str(member.id)}, {'$set':dataUpdate}) 
        await level_up(ctx)
        
    
    @commands.command(aliases=['cf'])
    @has_registered()
    @is_economy_channel()
    @commands.cooldown(1, 2.5, commands.BucketType.channel)
    async def coinflip(self, ctx, Side, Amount: int):      
        if str(Side) not in ('heads', 'tails'):
            eembed = errorembed(description=f'{ctx.author.mention} You can only choose ``heads`` or ``tails``.')
            return await ctx.send(embed=eembed)
            
        # Ensures that Bet is limited to 10,000 wood
        elif Amount > 10000:
            eembed = errorembed(description=f'{ctx.author.mention} Maximum bet is **10000**<:Wood:585780105696116736>')
            return await ctx.send(embed=eembed)
        
        # Ensures that minimum Bet is 10 wood
        elif Amount < 10:
            eembed = errorembed(description=f'{ctx.author.mention} Minimum amount is **10**<:Wood:585780105696116736>')
            return await ctx.send(embed=eembed)
                        
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            woodData = float(x['Currencies']['Wood'])
            expData = float(x['Profile']['Experience'])
        
        if Amount > float(woodData):
            eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
            return await ctx.send(embed=eembed)
        else:          
            result = random.randint(0,1)
            if result == 0:
                # Lose Message
                if Side == 'heads':
                    Side = 'tails'
                elif Side == 'tails':
                    Side = 'heads'
                woodData -= float(Amount)
                expData += float(Amount)
                dataUpdate = {
                'Currencies.Wood':woodData,
                'Profile.Experience':expData
            }
                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                await level_up(ctx)

                embed = discord.Embed(color=discord.Colour.red())
                embed.add_field(name='<:Coin:584686716955131924> Results', value=f"It's **{Side}**")
                embed.add_field(name='💸 Losses', value=f'You lost **{Amount}**<:Wood:585780105696116736>', inline=False)
                embed.add_field(name='💳 Balance', value=f'You now have **{round(woodData)}**<:Wood:585780105696116736>', inline=False)
                embed.set_author(name='Coin Flip', icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text='Check your bank balance by typing `.profile`')
                return await ctx.send(embed=embed)  
            else:
                # Win Message
                woodData += float(Amount)*0.9
                expData += float(Amount)
                dataUpdate = {
                'Currencies.Wood':woodData,
                'Profile.Experience':expData
            }
                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                await level_up(ctx)

                embed = discord.Embed(color=discord.Colour.green())
                embed.add_field(name='<:Coin:584686716955131924> Results', value=f"It's **{Side}**")
                embed.add_field(name='💰 Winnings', value=f'You won **{round(Amount*0.9)}**<:Wood:585780105696116736>', inline=False)
                embed.add_field(name='💳 Balance', value=f'You now have **{round(woodData)}**<:Wood:585780105696116736>', inline=False)
                embed.set_author(name='Coin Flip', icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text='Check your bank balance by typing `.profile`')
                return await ctx.send(embed=embed)     

    @coinflip.error
    async def coinflip_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            eembed = errorembed(description=f'{ctx.author.mention} Kindly try again in **{error.retry_after:.2}s**.')
            return await ctx.send(embed=eembed)     

    @commands.command()
    @has_registered()
    @is_economy_channel()
    @commands.cooldown(1, 60, commands.BucketType.channel)
    async def lottery(self, ctx, Amount:int):
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            woodData = float(x['Currencies']['Wood'])
            expData = float(x['Profile']['Experience'])
        
        if Amount > woodData:
            eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
            return await ctx.send(embed=eembed)
        elif Amount < 300:
            eembed = errorembed(description=f'{ctx.author.mention} Minimum amount is **300**<:Wood:585780105696116736>')
            return await ctx.send(embed=eembed)    
        else:
            # Giveaway Message
            await ctx.send('<@&579296665828327499>')
            embed = discord.Embed(title='🎰 Ongoing Lottery', description=f'Amount: **{Amount}**<:Wood:585780105696116736>\n\n Sponsored by {ctx.author.mention}', color=discord.Color.orange())
            embed.set_footer(text=f'React 🎫 to participate • Ends in 3 minutes')
            giveAwayMsg = await ctx.send(embed=embed)
            await giveAwayMsg.add_reaction('🎫')
            
            # Host Data
            woodData -= float(Amount)
            expData += float(Amount)
            dataUpdate = {
                'Currencies.Wood':woodData,
                'Profile.Experience':expData
            }
            self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
            await level_up(ctx)
            
            # Duration of Lottery aka 3 Minutes
            await asyncio.sleep(3*60)
            
            giveAwayMsg = await ctx.message.channel.fetch_message(giveAwayMsg.id)
            # List of Winners
            msgReactions = giveAwayMsg.reactions[0]
            msgReactionList = await msgReactions.users().flatten()
            msgReactionList.remove(ctx.me) # Remove Bot's reaction
            msgReactionList.remove(ctx.author) # Removes Author's reaction
            winner = random.choice(msgReactionList)

            # Winner Data
            userData = self.records.find({'userID':str(ctx.author.id)})
            for x in userData:
                woodData = float(x['Currencies']['Wood'])
                expData = float(x['Currencies']['Experience'])
            woodData += float(Amount)
            expData += float(Amount)
            dataUpdate = {
                'Currencies.Wood':woodData,
                'Profile.Experience':expData
            }
            self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

            embed = discord.Embed(title='🔚 Ongoing Lottery', description=f'Amount: **{Amount}** <:Wood:585780105696116736>\n\n Winner: {winner.mention}', color=discord.Color(0x222121))
            embed.set_footer(text=f'Sponsored by {ctx.author.name}', icon_url=ctx.author.avatar_url)
            await giveAwayMsg.edit(embed=embed)
            

    @lottery.error
    async def lottery_error(self, ctx, error):   
        if isinstance(error, commands.CommandOnCooldown):
            eembed = errorembed(description=f'{ctx.author.mention} Kindly try again in **{error.retry_after:.3}s**.')
            return await ctx.send(embed=eembed)

    @commands.command(aliases=['sl'])
    @has_registered()
    @is_economy_channel()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def slots(self, ctx):        
        # Creates a Dictionary that matches the Emoji and Exp
        symbolTable = {
                '<:Metal:585780079955673108>':100,
                '<:Stone:585780065892171776>':50,
                '<:Wood:585780105696116736>':10,
                }

        emojis = ['<:Metal:585780079955673108>', '<:Stone:585780065892171776>', '<:Wood:585780105696116736>']
        probability = ['0.25', '0.35', '0.4']
        roll = numpy.random.choice(emojis, 3, p=probability)
        
        # Creates a Counter that counts the Emoji in a Dictionary
        counter = collections.Counter(roll)
        key = counter.keys()
        value = counter.values()
        
        expList = []
        # Matching Emoji to Dictionary
        for x, y in zip(key, value):
            exp = symbolTable[x]
            expList.append(exp*y)
        totalXp = sum(expList)
        
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            expData = float(x['Profile']['Experience'])
        expData += float(totalXp)*2
        dataUpdate = {
                'Profile.Experience':expData
            }
        self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
        await level_up(ctx)

        # Updates Level if applicable
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            levelData = int(x['Profile']['Level'])

        embed = discord.Embed(description=f'**---------------------\n | {roll[0]} | {roll[1]} | {roll[2]} |\n ---------------------**\n', color=discord.Color.from_hsv(random.random(), 1, 1))
        embed.set_author(name='Slot XP Machine', icon_url=ctx.author.avatar_url)
        embed.add_field(name='🏆 Current Level', value=f'**{levelData}**')
        embed.add_field(name='📤 Experience Gained', value=f'**{totalXp}**')
        embed.set_footer(text='Check your profile by typing `.profile`')
        return await ctx.send(embed=embed)
        
    @slots.error
    async def slots_error(self, ctx, error):  
        if isinstance(error, commands.CommandOnCooldown):
            eembed = errorembed(description=f'{ctx.author.mention} Kindly try again in **{error.retry_after:.2}s**.')
            return await ctx.send(embed=eembed)       
    
    @commands.command()
    @has_registered()
    @is_economy_channel()
    @commands.cooldown(1, 2.5, commands.BucketType.channel)
    async def dice(self, ctx, number:int, amount:int):
        # Ensures that Bet is limited to $5
        if amount > 10000:
            eembed = errorembed(description=f'{ctx.author.mention} Maximum bet is **10000**<:Wood:585780105696116736>')
            return await ctx.send(embed=eembed)
        
        # Ensures that minimum Bet is $1
        elif amount < 10:
            eembed = errorembed(description=f'{ctx.author.mention} Minimum amount is **10**<:Wood:585780105696116736>')
            return await ctx.send(embed=eembed)

        if 1 <= number <= 6:
            userData = self.records.find({'userID':str(ctx.author.id)})
            for x in userData:
                expData = float(x['Profile']['Experience'])
                woodData = float(x['Currencies']['Wood'])

            if amount > float(woodData):
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
                return await ctx.send(embed=eembed)
            else:
                result = random.randint(1,6)
                if number == result:
                    # Win Message
                    multiplier = 3
                    woodData += float(amount)*multiplier
                    expData += float(amount)*(multiplier+0.5)
                    dataUpdate = {
                        'Currencies.Wood':woodData,
                        'Profile.Experience':expData
                    }
                    self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                    await level_up(ctx)

                    embed = discord.Embed(color=discord.Colour.green())
                    embed.add_field(name='🎲 Results', value=f"The dice rolled **{result}**")
                    embed.add_field(name='💰 Winnings', value=f'You won **{round(amount*multiplier)}**<:Wood:585780105696116736>', inline=False)
                    embed.add_field(name='💳 Balance', value=f'You now have **{round(woodData)}**<:Wood:585780105696116736>', inline=False)
                    embed.set_author(name='Dice Roll', icon_url=ctx.author.avatar_url)
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text='Check your bank balance by typing `.profile`')
                    return await ctx.send(embed=embed)     
                else:
                    # Lose Message
                    woodData -= float(amount)
                    expData += float(amount)
                    dataUpdate = {
                        'Currencies.Wood':woodData,
                        'Profile.Experience':expData
                    }
                    self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                    await level_up(ctx)

                    embed = discord.Embed(color=discord.Colour.red())
                    embed.add_field(name='🎲 Results', value=f"The dice rolled **{result}**")
                    embed.add_field(name='💸 Losses', value=f'You lost **{amount}**<:Wood:585780105696116736>', inline=False)
                    embed.add_field(name='💳 Balance', value=f'You now have **{round(woodData)}**<:Wood:585780105696116736>', inline=False)
                    embed.set_author(name='Dice Roll', icon_url=ctx.author.avatar_url)
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text='Check your bank balance by typing `.profile`')
                    return await ctx.send(embed=embed)
        else:
            eembed = errorembed(description=f'{ctx.author.mention} You can only choose between ``1`` to ``6``.')
            return await ctx.send(embed=eembed)
    
    @dice.error
    async def dice_error(self, ctx, error): 
        if isinstance(error, commands.CommandOnCooldown):
            eembed = errorembed(description=f'{ctx.author.mention} Kindly try again in **{error.retry_after:.2}s**.')
            return await ctx.send(embed=eembed) 
        elif isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Command Usage: ``.dice <Number> <Amount>``')
            return await ctx.send(embed=eembed)    
    
    @commands.command()
    @has_registered()
    @is_economy_channel()
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def rps(self, ctx, member:discord.Member, amount:int):
        # Checks if User is registered in Database
        try:
            userList = [x['userID'] for x in self.records.find({})]
            if str(ctx.author.id) not in userList:
                eembed = errorembed(description=f'{ctx.author.mention} You are currently not registered yet. Kindly type ``.register`` to be registered.')
                return await ctx.send(embed=eembed)
            elif str(member.id) not in userList:
                eembed = errorembed(description=f'{ctx.author.mention} {member.mention} has not registered yet.')
                return await ctx.send(embed=eembed)
        except:
            pass  

        # Ensures that Bet is limited to $5
        if amount > 10000:
            eembed = errorembed(description=f'{ctx.author.mention} Maximum bet is **10000**<:Wood:585780105696116736>')
            return await ctx.send(embed=eembed)
        
        # Ensures that minimum Bet is $1
        elif amount < 10:
            eembed = errorembed(description=f'{ctx.author.mention} Minimum amount is **10**<:Wood:585780105696116736>')
            return await ctx.send(embed=eembed)
        
        # User's data
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            userRepData = int(x['Profile']['Rep'])
            userLevelData = int(x['Profile']['Level'])
            userWoodData = float(x['Currencies']['Wood'])

        # Checks if both User and Member has enough currencies
        try:
            if amount > userWoodData:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
                return await ctx.send(embed=eembed)
            
            userData = self.records.find({'userID':str(member.id)})
            for x in userData:
                memberRepData = int(x['Profile']['Rep'])
                memberWoodData = float(x['Currencies']['Wood'])
                memberlevelData = int(x['Profile']['Level'])

            if amount > memberWoodData:
                eembed = errorembed(description=f'{ctx.author.mention} {member.mention} does not have enough currency. Try again later.')
                return await ctx.send(embed=eembed)
        except:
            pass

        # Sends message in public chat
        embed = discord.Embed(color=discord.Color.from_hsv(random.random(), 1, 1))
        embed.add_field(name='Description', value=f'**RPS Challenge** has just begun between {member.mention} and {ctx.author.mention}')
        embed.add_field(name='Amount', value=f'**{amount}**<:Wood:585780105696116736>')
        embed.add_field(name='Winner', value='❓')
        embed.set_author(name=f'Contentor - {member}', icon_url=member.avatar_url)
        embed.set_footer(text=f'Initiator - {ctx.author}', icon_url=ctx.author.avatar_url)
        publicMsg = await ctx.send(embed=embed)
        
        # Creates a challenge embed message
        embed = discord.Embed(title='Make the first move!', color=discord.Color.from_hsv(random.random(), 1, 1))
        embed.add_field(name='🏆 User Level', value=f'**{userLevelData}**')
        embed.add_field(name='⭐ Reputation', value=f'+ **{userRepData}**')
        embed.add_field(name='💵 Amount', value=f'**{amount}**<:Wood:585780105696116736>', inline=False)
        embed.set_author(name=f'You have been challenged to a RPS by {ctx.author}', icon_url=ctx.author.avatar_url)
        embed.set_footer(text='React on the emojis below to make a move!')
        challengeMsg = await member.send(embed=embed)
        
        await challengeMsg.add_reaction('\U0001f44a')
        await challengeMsg.add_reaction('\U0001f590')
        await challengeMsg.add_reaction('\U0000270c')
        # Creates a string for User and Author reaction
        memberReaction = ''
        authorReaction = ''

        try:
            def check(reaction, user):
                return reaction.message.id == challengeMsg.id and user.id == member.id
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
            # Adds reaction back to global string
            memberReaction += str(reaction)              
        except asyncio.TimeoutError:
            embed = discord.Embed(title='Challenge Expired', description=f'**{member}** did not make his move. Kindly initiate another challenge if you wish to battle.', color=discord.Color.red())
            await member.send(embed=embed)
            await ctx.author.send(embed=embed)
            return await publicMsg.edit(embed=embed)
        
        userData = self.records.find({'userID':str(member.id)})
        for x in userData:
            memberRepData = int(x['Profile']['Rep'])
            memberLevelData = int(x['Profile']['Level'])

        embed = discord.Embed(title=f"{member} has made his move, it's your turn now!", color=discord.Color.from_hsv(random.random(), 1, 1))
        embed.add_field(name='🏆 User Level', value=f'**{memberLevelData}**')
        embed.add_field(name='⭐ Reputation', value=f'+ **{memberRepData}**')
        embed.add_field(name='💵 Amount', value=f'**{amount}**<:Wood:585780105696116736>', inline=False)
        embed.set_author(name=f'You have been challenged to a RPS by {member}', icon_url=ctx.author.avatar_url)
        embed.set_footer(text='React on the emojis below to make a move!')
        replyMsg = await ctx.author.send(embed=embed)
        await replyMsg.add_reaction('\U0001f44a') # Rock
        await replyMsg.add_reaction('\U0001f590') # Paper 
        await replyMsg.add_reaction('\U0000270c') # Scissors

        try:
            def check(reaction, user):
                return reaction.message.id == replyMsg.id and user.id == ctx.author.id
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
            # Adds reaction back to global string
            authorReaction += str(reaction)            
        except asyncio.TimeoutError:
            embed = discord.Embed(title='Challenge Expired', description=f'**{ctx.author}** did not make his move. Kindly initiate another challenge if you wish to battle.', color=discord.Color.red())
            await member.send(embed=embed)
            await ctx.author.send(embed=embed)
            return await publicMsg.edit(embed=embed)

        # Determines the Winner

        if memberReaction == authorReaction:
            embed = discord.Embed(color=discord.Color.from_hsv(random.random(), 1, 1))
            embed.add_field(name='🏁 Results', value=f'{member.mention} chose {memberReaction}\n {ctx.author.mention} chose {authorReaction}', inline=False)
            embed.add_field(name='💵 Amount', value=f'**{amount}**<:Wood:585780105696116736>')
            embed.add_field(name='🏅 Winner', value="It's a **draw**")
            embed.set_author(name=f'🤝 RPS Challenge')
            return await publicMsg.edit(embed=embed)

        elif memberReaction == '\U0001f44a': # Rock
            if authorReaction == '\U0001f590': # Paper
                await self.author_win(ctx, member, amount)
                embed = discord.Embed(color=discord.Color.from_hsv(random.random(), 1, 1))
                embed.add_field(name='🏁 Results', value=f'{member.mention} chose {memberReaction}\n {ctx.author.mention} chose {authorReaction}', inline=False)
                embed.add_field(name='💵 Amount', value=f'**{round(amount*0.98)}**<:Wood:585780105696116736>')
                embed.add_field(name='🏅 Winner', value=ctx.author.mention)
                embed.set_author(name=f'🤝 RPS Challenge')
                return await publicMsg.edit(embed=embed)
            else:
                await self.member_win(ctx, member, amount)    
                embed = discord.Embed(color=discord.Color.from_hsv(random.random(), 1, 1))
                embed.add_field(name='🏁 Results', value=f'{member.mention} chose {memberReaction}\n {ctx.author.mention} chose {authorReaction}', inline=False)
                embed.add_field(name='💵 Winnings', value=f'**{round(amount*0.98)}**<:Wood:585780105696116736>')
                embed.add_field(name='🏅 Winner', value=member.mention)
                embed.set_author(name=f'🤝 RPS Challenge')
                return await publicMsg.edit(embed=embed)
        elif memberReaction == '\U0001f590': # Paper
            if authorReaction == '\U0000270c': # Scissors
                await self.author_win(ctx, member, amount)
                embed = discord.Embed(color=discord.Color.from_hsv(random.random(), 1, 1))
                embed.add_field(name='🏁 Results', value=f'{member.mention} chose {memberReaction}\n {ctx.author.mention} chose {authorReaction}', inline=False)
                embed.add_field(name='💵 Amount', value=f'**{round(amount*0.98)}**<:Wood:585780105696116736>')
                embed.add_field(name='🏅 Winner', value=ctx.author.mention)
                embed.set_author(name=f'🤝 RPS Challenge')
                return await publicMsg.edit(embed=embed)
            else:
                await self.member_win(ctx, member, amount)    
                embed = discord.Embed(color=discord.Color.from_hsv(random.random(), 1, 1))
                embed.add_field(name='🏁 Results', value=f'{member.mention} chose {memberReaction}\n {ctx.author.mention} chose {authorReaction}', inline=False)
                embed.add_field(name='💵 Winnings', value=f'**{round(amount*0.98)}**<:Wood:585780105696116736>')
                embed.add_field(name='🏅 Winner', value=member.mention)
                embed.set_author(name=f'🤝 RPS Challenge')
                return await publicMsg.edit(embed=embed)
        elif memberReaction == '\U0000270c': # Scissors
            if authorReaction == '\U0001f44a': # Rock
                await self.author_win(ctx, member, amount)
                embed = discord.Embed(color=discord.Color.from_hsv(random.random(), 1, 1))
                embed.add_field(name='🏁 Results', value=f'{member.mention} chose {memberReaction}\n {ctx.author.mention} chose {authorReaction}', inline=False)
                embed.add_field(name='💵 Amount', value=f'**{round(amount*0.98)}**<:Wood:585780105696116736>')
                embed.add_field(name='🏅 Winner', value=ctx.author.mention)
                embed.set_author(name=f'🤝 RPS Challenge')
                return await publicMsg.edit(embed=embed)
            else:
                await self.member_win(ctx, member, amount)    
                embed = discord.Embed(color=discord.Color.from_hsv(random.random(), 1, 1))
                embed.add_field(name='🏁 Results', value=f'{member.mention} chose {memberReaction}\n {ctx.author.mention} chose {authorReaction}', inline=False)
                embed.add_field(name='💵 Winnings', value=f'**{round(amount*0.98)}**<:Wood:585780105696116736>')
                embed.add_field(name='🏅 Winner', value=member.mention)
                embed.set_author(name=f'🤝 RPS Challenge')
                return await publicMsg.edit(embed=embed)
    
    @rps.error
    async def rps_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            eembed = errorembed(description=f"{ctx.author.mention} There's a **RPS Challenge** going on in this channel. Kindly head over to another economy channel or try again in **{error.retry_after:.3}s**.")
            return await ctx.send(embed=eembed)
        elif isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Command Usage: ``.rps <User> <Amount>``')
            return await ctx.send(embed=eembed)
           
    
# Adding the cog to main script
def setup(bot):
    bot.add_cog(Games(bot))            