import asyncio
import discord
import random
import datetime
import numpy
import pytz
import collections
import pymongo
import os

from discord.ext import commands
from cogs.utils.misc import level_up
from cogs.utils.checks import is_economy_channel, has_registered
from cogs.utils.embed import (passembed, errorembed)

class Rewards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = pymongo.MongoClient(os.getenv("MONGO_DB"))
        self.db = self.client.get_database('Users')
        self.records = self.db.horizon_database
    
    @commands.command()
    @commands.is_owner()
    async def llama(self, ctx):      
        await ctx.send('<@&579296665828327499>')
        embed = discord.Embed(title='<:llama:489132205881294848> Llama Lootcrate', description='has just spawned, hurry react <:llama:489132205881294848> to stand a chance to grab it.', color=discord.Color.purple())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/495521657566527489/576421068512821269/Fortnite_llama_pinata.png')
        llama = await ctx.send(embed=embed)
        await llama.add_reaction(':llama:489132205881294848')

        # Duration of Llama aka 1 Minute
        await asyncio.sleep(45)
        
        try:
            winner = await ctx.message.channel.fetch_message(llama.id)
            # List of Winners
            msgReactions = winner.reactions[0]
            msgReactionList = await msgReactions.users().flatten()
            msgReactionList.remove(ctx.me) # Remove Bot's reaction
            winner = random.choice(msgReactionList)

            # Prize Prizepool
            prize = ['100', '300', '500']
            prize = random.choice(prize)

            # Winner Data
            userData = self.records.find({'userID':f'{str(winner.id)}'})
            for x in userData:
                woodData = float(x['Currencies']['Wood'])
                expData = float(x['Profile']['Experience'])

            woodData += float(prize)
            expData += float(prize)
            dataUpdate = {
                'Currencies.Wood':woodData,
                'Profile.Experience':expData
            }
            self.records.update_one({'userID':str(winner.id)}, {'$set':dataUpdate}) 
            await level_up(ctx)

            embed = discord.Embed(title='<:llama:489132205881294848> Llama Lootcrate', description=f'has been looted by {winner.mention} and won **{prize}**<:Wood:585780105696116736>', color=discord.Color.purple())
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/495521657566527489/576421068512821269/Fortnite_llama_pinata.png')
            return await llama.edit(embed=embed)

        except:
            embed = discord.Embed(title='<:llama:489132205881294848> Llama Lootcrate', description='has not been looted and has despawned...', color=discord.Color.purple())
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/495521657566527489/576421068512821269/Fortnite_llama_pinata.png')
            await llama.clear_reactions()
            return await llama.edit(embed=embed)

    @llama.error
    async def llama_error(self, ctx, error):
       if isinstance(error, commands.CheckFailure):
           return 
    
    @commands.command(aliases=['pin'])
    @commands.has_any_role('Server Moderator')
    async def pinata(self, ctx):
        await ctx.send('<@&579296665828327499>')
        embed = discord.Embed(title='<:llama:489132205881294848> Llama Pinata Event', color=0xdb52ec)
        embed.add_field(name='Description of Event', value='• Long-awaited monthly **Llama Pinata** event has finally arrived.\n • Stand a chance to win either ``300``, ``500``, ``1,000``, ``2,000`` or ``3,000`` <:Wood:585780105696116736>')
        embed.add_field(name='Instructions', value='• Simply type ``.participate <Amount>`` to join the **Llama Pinata** event!')
        embed.add_field(name='Number of Winners', value=f'• **5** lucky winners will be randomly picked from the participants.')
        currentTime = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d')
        endTime = (datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')) + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        embed.add_field(name='Duration of Event', value=f"• From **{currentTime}** to **{endTime}**")
        embed.add_field(name='Additional Tips', value='• Note that the amount is directly proportionate to the chances of winning. This means that the higher amount you invest increases your chances of winning the event.')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/495521657566527489/576721251842916352/epic-rainbow-smash-pickaxe-naaitoh.png')
        embed.set_footer(text='Check your chance to win by typing `.chances`')
        await ctx.send(embed=embed)
    
    @pinata.error
    async def pinata_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return

    @commands.command(aliases=['cs'])
    @has_registered()
    @is_economy_channel()
    async def chances(self, ctx):
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            pinataSlot = float(x['Items']['pinataSlot'])
        
        # Converts all number to floats
        try:
            pinataList = [x['Items']['pinataSlot'] for x in self.records.find({})]
            # totalChances = sum(float(x) for x in pinataList if x.isdigit())
            floatChances = 0
            for x in pinataList:
                try:
                    floatChances += float(x)
                except:
                    pass

            chanceToWin = (pinataSlot/floatChances)*100
            await ctx.send(f'{ctx.author.mention} You stand a **{round(chanceToWin, 2)}%** to win the **Llama Pinata** event!')
        except:
            await ctx.send(f'{ctx.author.mention} There are currently no ongoing **Llama Pinata** event!')  

    @commands.command(aliases=['pt'])
    @has_registered()
    @is_economy_channel()
    async def participate(self, ctx, amount:float):
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            woodData = float(x['Currencies']['Wood'])
            slotData = float(x['Items']['pinataSlot'])

        # Checks if User has enough currency
        if woodData < amount:
            eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
            return await ctx.send(embed=eembed)
        
        # Ensures that minimum Bet is 100 currency
        elif amount < 100:
            eembed = errorembed(description=f'{ctx.author.mention} Minimum amount is **100**<:Wood:585780105696116736>')
            return await ctx.send(embed=eembed)
        else:
            woodData -= float(amount)
            slots = amount/100
            slotData += slots
            dataUpdate = {
                'Currencies.Wood':woodData,
                'Items.pinataSlot':slotData
            }
            self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

            pembed = passembed(description=f'{ctx.author.mention} You have successfully purchased **{slots}** ticket(s) in the **Llama Pinata** event. Type ``.chances`` to check your chances to win the event!')
            await ctx.send(embed=pembed)
    
    @participate.error
    async def participate_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Command Usage: ``.participate <Amount>``')
            return await ctx.send(embed=eembed)   
    
    @commands.command()
    @commands.has_any_role('Server Moderator')
    async def pinatawin(self, ctx, messageID:int):
        slotsList = [x['Items']['pinataSlot'] for x in self.records.find({})]
        prize = ['3000', '2000', '1000', '500', '300']
        pinataMsg = await ctx.channel.fetch_message(messageID)
        
        totalChances = 0
        for x in slotsList:
            try:
                totalChances += float(x)
            except:
                continue

        # Creates a Weighted Probability list
        weightedList = []
        for x in slotsList:
            weightedList.append(float(x)/totalChances)
        
        # Picks winner without duplicates
        probabilityWinners = numpy.random.choice(slotsList, 5, p=weightedList, replace=False)
        embed = discord.Embed(title='Results of <:llama:489132205881294848> Llama Pinata Event', description="Long-awaited results are here. We're glad to announce that these are the lucky winners of the event!", color=discord.Color.green())
        embedWinners = []
        embedPrize = []
        for x, y in zip(probabilityWinners, prize):
            userData = self.records.find({'userID':f'{str(x)}'})
            for x in userData:
                woodData = float(x['Currencies']['Wood'])
                userID = float(x['userID'])
                expData = float(x['Profile']['Experience'])

            # Adds Winner + Prize into List
            embedWinners.append(f'<@!{userID}>')
            embedPrize.append(f'{y}<:Wood:585780105696116736>')

            # Updates Prize for User in database
            woodData += float(y)
            expData += float(y)
            dataUpdate = {
                'Currencies.Wood':woodData,
                'Profile.Experience':expData,
                'Items.pinataSlot':0
            }
            self.records.update_one({'userID':str(x)}, {'$set':dataUpdate})

        embed.add_field(name='Winners', value='\n'.join(embedWinners))
        embed.add_field(name='Prize', value=' \n'.join(embedPrize))
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/495521657566527489/576721251842916352/epic-rainbow-smash-pickaxe-naaitoh.png')
        embed.set_footer(text='Thanks for the participation!')
        await pinataMsg.edit(embed=embed)    
    
    @pinatawin.error
    async def pinatawin_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            return  
    
    
# Adding the cog to main script
def setup(bot):
    bot.add_cog(Rewards(bot))    