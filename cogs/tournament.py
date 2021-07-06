import discord
import pymongo
import asyncio
import os

from discord.ext import commands
from cogs.utils.misc import level_up
from cogs.utils.checks import is_economy_channel, has_registered
from cogs.utils.embed import (passembed, errorembed)


class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
        self.client = pymongo.MongoClient(os.getenv("MONGO_DB"))
        self.db = self.client.get_database('Users')
        self.records = self.db.horizon_database
        self.bets = False
        self.betAmount = {}
    
    def genEmbed(self):
        embed = discord.Embed(title='Wager Listing', description='Bets are **open** right now! Hurry place your bets on the Competitor that you think will win the tournament!',color=discord.Color.gold())
        return embed

    @commands.command(aliases=['ctourney'])
    @commands.has_any_role('Server Moderator', 'Host')
    async def create_tournament(self, ctx, *users:discord.User):        
        for x in users:
            # Checks if Competitor is registered in database      
            try:
                userList = [x['userID'] for x in self.records.find({})]
                if str(x.id) not in userList:
                    eembed = errorembed(description=f'{ctx.author.mention} {x.mention} is currently not registered yet. Kindly type ``.register`` to be registered.')
                    return await ctx.send(embed=eembed)
            except:
                pass
                            
        try:
            self.db.create_collection('tournament')
            embed = discord.Embed(color=discord.Color.gold())
            embed.add_field(name='Description', value='• A **tournament** has just begun, do place your bets on whom you think will be the Winner\n • Competitors will be given **5 minutes** to prepare themselves\n • Failure to turn up will result in a penalty of **2,500**<:Wood:585780105696116736>')
            embed.add_field(name='Instructions', value='• Simply type ``.bet @User <Amount>`` to place your bet on the competitor\n • Default bet will be equivalent to **100**<:Wood:585780105696116736>')
            embed.set_footer(text=f'Tournament started by {ctx.author}', icon_url=f'{ctx.author.avatar_url}')
            for x in users:
                new_user = {
                    "userID":str(x.id),
                    "userName":str(x),
                    "betAmount":0
                    }
                self.db.tournament.insert_one(new_user)
                
                # Embed data
                userData = self.records.find({'userID':f'{str(x.id)}'})
                counter = 0
                for i in userData:
                    counter += 1 
                    repData = int(i['Profile']['Rep'])
                    levelData = int(i['Profile']['Level'])
                    gamesData = int(i['Profile']['gamesPlayed'])
                    winData = int(i['Profile']['Wins'])
                    winRate = round((winData/gamesData)*100, 2) if gamesData != 0 else 0
                    
                    embed.add_field(name=f'Competitor #{counter} Profile', value=f'Name: {x.mention}\n Level: **{levelData}**\n Reputation: **+{repData}**\n Win Rate: **{winRate}**%')
                    gamesData += 1
                    dataUpdate = {
                        'Profile.gamesPlayed':gamesData
                    }
                    update = self.records.update_one({'userID':str(x.id)}, {'$set':dataUpdate})
            
            wagerRole = discord.utils.get(ctx.guild.roles, name='Wagers')
            await ctx.send(wagerRole.mention)
            return await ctx.send(embed=embed)
        except Exception:
            eembed = errorembed(description=f'{ctx.author.mention} A tournament is currently **ongoing**. Kindly wait for it to end.')
            return await ctx.send(embed=eembed)    
            
    @create_tournament.error
    async def create_tournament_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.BadArgument):
            eembed = errorembed(description=f"{ctx.author.mention} Error: `{error}`. Kindly input a space between the Users")
            return await ctx.send(embed=eembed)        

    @commands.command()
    @has_registered()
    @is_economy_channel()
    async def bet(self, ctx, user:discord.User, amount:int=None):
        try:
            if self.bets is False:
                eembed = errorembed(description=f'{ctx.author.mention} Bets are not opened yet. Kindly try again later.')
                return await ctx.send(embed=eembed)
            if 'tournament' not in self.db.list_collection_names():
                    eembed = errorembed(description=f'{ctx.author.mention} There are **no tournaments** currently ongoing. Kindly try again later.')
                    return await ctx.send(embed=eembed) 
            competitorList = [x['userID'] for x in self.db.tournament.find({})]
            if str(ctx.author.id) in competitorList:
                eembed = errorembed(description=f"{ctx.author.mention} You're one of the participants. No betting is allowed")
                return await ctx.send(embed=eembed)
            elif str(user.id) not in competitorList:
                eembed = errorembed(description=f'{ctx.author.mention} {user.mention} is not one of the competitiors.')
                return await ctx.send(embed=eembed)
        except:
            pass 
        
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            woodData = float(x['Currencies']['Wood'])

        # Standardised amount of bet
        if amount is None:
            amount = 100

        # Checks if User has enough currency
        if woodData < amount:
            eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
            return await ctx.send(embed=eembed)
        else: 
            try:
                # Updates individual data in horizon_database collection
                userData = self.records.find({'userID':str(ctx.author.id)})
                for x in userData:
                    woodData = float(x['Currencies']['Wood'])
                woodData -= float(amount)
                dataUpdate = {
                    'Currencies.Wood':woodData
                }
                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                # Updates individual bets in tournament collection
                userData = self.db.tournament.distinct(str(ctx.author.id))
                woodData = int(" ".join(map(str, userData)))
                woodData += amount
                dataUpdate = {
                        str(ctx.author.id):woodData
                    }
                update = self.db.tournament.update_one({'userID':str(user.id)}, {'$set':dataUpdate}) 

                # Updates total betting pool
                competitorData = self.db.tournament.find({'userID':str(user.id)})
                for x in competitorData:
                    betData = float(x['betAmount'])
                betData += amount
                dataUpdate = {
                            'betAmount':betData
                        }
                update = self.db.tournament.update_one({'userID':str(user.id)}, {'$set':dataUpdate}) 
                
                dictionaryUpdate = self.betAmount.update({str(ctx.author.id):str(woodData)})
                pembed = passembed(description=f'{ctx.author.mention} You have successfully placed your bets on {user.mention}. All the best!')
                return await ctx.send(embed=pembed)
            except Exception:
                # Updates individual data in horizon_database collection
                userData = self.records.find({'userID':str(ctx.author.id)})
                for x in userData:
                    woodData = float(x['Currencies']['Wood'])
                woodData -= amount
                dataUpdate = {
                    'Currencies.Wood':woodData
                }
                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                # Updates individual bets in tournament collection
                dataUpdate = {
                            str(ctx.author.id):amount
                        }
                update = self.db.tournament.update_one({'userID':str(user.id)}, {'$set':dataUpdate}) 

                # Updates total betting pool
                competitorData = self.db.tournament.find({'userID':str(user.id)})
                for x in competitorData:
                    betData = float(x['betAmount'])
                betData += amount
                dataUpdate = {
                            'betAmount':betData
                        }
                update = self.db.tournament.update_one({'userID':str(user.id)}, {'$set':dataUpdate}) 

                dictionaryUpdate = self.betAmount.update({str(ctx.author.id):str(amount)})
                pembed = passembed(description=f'{ctx.author.mention} You have successfully placed your bets on {user.mention}. All the best!')
                return await ctx.send(embed=pembed)
    
    @bet.error
    async def bet_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Command Usage: ``.bet @User <Amount>``')   
            return await ctx.send(embed=eembed)
    
    @commands.command(aliases=['wtourney'])
    @commands.has_any_role('Server Moderator', 'Host')
    async def wintourney(self, ctx, user:discord.User):
        competitorList = [x['userID'] for x in self.db.tournament.find({})]
        if str(ctx.author.id) in competitorList:
            eembed = errorembed(description=f"{ctx.author.mention} You're one of the participants. No betting is allowed")
            return await ctx.send(embed=eembed)
        elif str(user.id) not in competitorList:
            eembed = errorembed(description=f'{ctx.author.mention} {user.mention} is not one of the competitiors.')
            return await ctx.send(embed=eembed)

        competitorData = self.db.tournament.find({'userID':f'{str(user.id)}'})
        for x in competitorData:
            totalBet = float(x['betAmount'])

        # 20% of pool goes to Competitor 
        competitorWinnings = totalBet*0.2 
        
        winnerDict = self.db.tournament.find({'userID':f'{str(user.id)}'})[0]
        winnersList = [x for x in winnerDict if x != '_id' and x != 'userID' and x != 'userName' and x != 'betAmount']
        # Creates a list for the Embed message 
        embedWinners = []
        embedEarnings = []

        for x in winnersList:
            winningMultiplier = 1.75
            embedWinners.append(f'<@!{x}>')
            winnerData = self.db.tournament.distinct(str(x))
            betAmount = int(" ".join(map(str, winnerData)))
            userData = self.records.find({'userID':f'{str(x)}'})
            for x in userData:
                expData = float(x['Profile']['Experience'])
                woodData = float(x['Currencies']['Wood'])
            woodData += float(betAmount*winningMultiplier)
            embedEarnings.append(f'**{round(betAmount*winningMultiplier)}**<:Wood:585780105696116736>')
            expData += float(betAmount*winningMultiplier)
            dataUpdate = {
                'Currencies.Wood':woodData,
                'Profile.Experience':expData
            }
            update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
            
        # Updates winnings for Competitor
        userData = self.records.find({'userID':f'{str(user.id)}'})
        for x in userData:
            expData = float(x['Profile']['Experience'])
            woodData = float(x['Currencies']['Wood'])
            winData = int(x['Profile']['Wins'])

        woodData += float(competitorWinnings)
        expData += float(competitorWinnings)
        winData += 1

        dataUpdate = {
                'Currencies.Wood':woodData,
                'Profile.Experience':expData,
                'Profile.Wins':winData
            }
        update = self.records.update_one({'userID':str(user.id)}, {'$set':dataUpdate}) 

        embedWinners.append(f'<@!{user.id}>')
        embedEarnings.append(f'**{round(float(competitorWinnings))}**<:Wood:585780105696116736>')

        # Embed message
        embed = discord.Embed(description=f'The tournament has ended. Congrulations to {user.mention} for winning! Do show him some support by ``.vote @User`` for his efforts.', color=0xf84848)
        embed.set_author(name='Results of Tournament')
        embed.add_field(name='Winners', value=f' \n'.join(embedWinners))
        embed.add_field(name='Earnings', value=f' \n'.join(embedEarnings))
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text='Type `.profile` to view your balance')
        # Deletes Tournament database
        removeDatabase = self.db.drop_collection('tournament')
        return await ctx.send(embed=embed)
    
    @wintourney.error
    async def wintourney_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return 

    @commands.command()            
    @commands.has_any_role('Server Moderator', 'Host')
    async def bets(self, ctx, status):
        if str(status) == 'open':
            await ctx.message.delete()
            self.bets = True
            pembed = passembed(description=f'**Wagers are officially opened.**')
            await ctx.send(embed=pembed)
            embed = self.genEmbed()
            msg = await ctx.send(embed=embed)
            while self.bets is True:
                try:
                    embed = self.genEmbed()
                    userList = []
                    amountList = []
                    for user, amount in self.betAmount.items():
                        userList.append(f'<@!{user}>')
                        amountList.append(f'**{amount}<:Wood:585780105696116736>**')
                    embed.add_field(name='User', value='\n'.join(userList))
                    embed.add_field(name='Bettings Amount', value='\n'.join(amountList))
                    await msg.edit(embed=embed)
                    await asyncio.sleep(10)
                except:
                    pass    
        elif str(status) == 'close':
            await ctx.message.delete()
            self.bets = False
            pembed = passembed(description=f'**Wagers are officially closed.**')
            return await ctx.send(embed=pembed)

    @bets.error
    async def bets_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return 

# Adding the cog to main script
def setup(bot):
    bot.add_cog(Tournament(bot))    