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

class Usage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = pymongo.MongoClient(os.getenv("MONGO_DB"))
        self.db = self.client.get_database('Users')
        self.records = self.db.horizon_database
        
    @commands.command()
    @has_registered()
    @is_economy_channel()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def claim(self, ctx, Item):
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            crateData = float(x['Items']['Crates'])
            keyData = float(x['Items']['Keys'])
            giftData = float(x['Items']['Gifts'])
            woodData = float(x['Currencies']['Wood'])
            expData = float(x['Profile']['Experience'])

        if str(Item) == 'crate':
            if crateData <1:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough crates. Try again later.')
                return await ctx.send(embed=eembed)    
            elif keyData < 1:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough keys. Try again later.')
                return await ctx.send(embed=eembed)    
            else:
                # Minus 1 crate and 1 key    
                keyData -= 1
                crateData -= 1
                dataUpdate = {
                    'Items.Keys':keyData,
                    'Items.Crates':crateData
                }
                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                prizeDict = {                   
                    '<:Wood:585780105696116736>':100,
                    '📤':600, 
                    '🎁':1,
                    '🔑':1,
                    '🛰️':1,
                    '<:Stone:585780065892171776>':1, 
                    '🎟️':3,
                    '<:Metal:585780079955673108>':1,
                    '⭐':1,
                    '📦':1
                }
                rarityDict ={
                    'Common':['<:Wood:585780105696116736>', '📤', '🎁', '🔑'],
                    'Rare':['🛰️','<:Stone:585780065892171776>', '🎟️'],
                    'Legendary':['<:Metal:585780079955673108>'],
                    'Mythic':['⭐', '📦']
                }
 
                rarity = list(rarityDict.keys())
                probability = ['0.73', '0.235', '0.03', '0.005']
                roll = random.randint(2,5)
                result = numpy.random.choice(rarity, roll, p=probability)
                
                # Creates a Counter that counts the rarity in result
                counter = collections.Counter(result)
                
                # Creates a prize dictionary for the different rarities
                commonPrize = {}
                rarePrize = {}
                legendaryPrize = {}
                mythicPrize = {}
                # Sorts the result according to rarity order

                for x, y in counter.items():
                    if str(x) == 'Common':
                        commonItems = rarityDict[str(x)]
                        commonResult = numpy.random.choice(commonItems, int(y), p=['0.30', '0.55', '0.1', '0.05'])
                        # Creates a Counter that counts Common items in result
                        commonCounter = collections.Counter(commonResult)
                        for x, y in commonCounter.items():
                            commonPrize[str(x)] = y
                    elif str(x) == 'Rare':
                        rareItems = rarityDict[str(x)]
                        rareResult = numpy.random.choice(rareItems, int(y), p=['0.18', '0.3', '0.52'])
                        # Creates a Counter that counts Rare items in result
                        rareCounter = collections.Counter(rareResult)
                        for x, y in rareCounter.items():
                            rarePrize[str(x)] = y
                    elif str(x) == 'Legendary':
                        mythicItems = rarityDict[str(x)]
                        mythicResult = numpy.random.choice(mythicItems, int(y))
                        # Creates a Counter that counts Mythic items in result
                        mythicCounter = collections.Counter(mythicResult)
                        for x, y in mythicCounter.items():
                            legendaryPrize[str(x)] = y
                    elif str(x) == 'Mythic':
                        marvelItems = rarityDict[str(x)]
                        marvelResult = numpy.random.choice(marvelItems, int(y), p=['0.95', '0.05'])
                        # Creates a Counter that counts Rare items in result
                        marvelCounter = collections.Counter(marvelResult)
                        for x, y in marvelCounter.items():
                            mythicPrize[str(x)] = y

                prizeStr = ''
                await ctx.send(ctx.author.mention)
                embed = discord.Embed(title='📦 Crate Opening', description=prizeStr, color=discord.Color.from_hsv(random.random(), 1, 1))
                crateMsg = await ctx.send(embed=embed)  
                
                # Refreshes User data
                userData = self.records.find({'userID':str(ctx.author.id)})
                for x in userData:
                    crateData = float(x['Items']['Crates'])
                    keyData = float(x['Items']['Keys'])
                    giftData = float(x['Items']['Gifts'])
                    woodData = float(x['Currencies']['Wood'])
                    stoneData = float(x['Currencies']['Stone'])
                    metalData = float(x['Currencies']['Metal'])
                    repData = int(x['Profile']['Rep'])
                    expData = float(x['Profile']['Experience'])
                    pinataData = float(x['Items']['pinataSlot'])

                for x, y in counter.items():
                    if str(x) == 'Common':
                        prizeStr += '\n\n**=== Common Resources ===**'
                        prizeName =''
                        for x, y in commonPrize.items():
                            if str(x) == '<:Wood:585780105696116736>':
                                prizeName = ' Wood'
                                woodData += float(prizeDict[str(x)]*int(y))
                                dataUpdate = {
                                    'Currencies.Wood':woodData
                                }
                                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                            if str(x) == '📤':
                                prizeName = ' Exp'
                                expData += int(prizeDict[str(x)]*int(y))
                                dataUpdate = {
                                    'Profile.Experience':expData
                                }
                                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                            if str(x) == '🎁':
                                prizeName = ' Gift(s)'
                                giftData += int(prizeDict[str(x)]*int(y))
                                dataUpdate = {
                                    'Items.Gifts':giftData
                                }
                                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                            if str(x) == '🔑':
                                prizeName = ' Key(s)'  
                                keyData += float(prizeDict[str(x)]*int(y))
                                dataUpdate = {
                                    'Items.Keys':keyData
                                }
                                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                            prizeStr += f'\n{str(x)}: **{prizeDict[str(x)]*int(y)}** {prizeName}'
                            embed = discord.Embed(title='📦 Crate Opening', description=prizeStr, color=discord.Color.from_hsv(random.random(), 1, 1))
                            await crateMsg.edit(embed=embed)
                            await asyncio.sleep(2)
                    if str(x) == 'Rare':
                        prizeStr += '\n\n**=== Rare Resources ===**'
                        prizeName =''
                        for x, y in rarePrize.items():
                            if str(x) == '🛰️':
                                prizeName = ' Paid Advertisement'
                                orderChannel = discord.utils.get(ctx.guild.channels, name='processing-orders')
                                embed = discord.Embed(title='🛰️ Paid Advertisement', description='You have won a paid advertisement from the crate opening. Kindly send this receipt to <@545977500275048448>.', color=discord.Color.gold())
                                embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(float(woodData))}**<:Wood:585780105696116736>, **{round(float(stoneData))}**<:Stone:585780065892171776>, **{round(float(metalData))}**<:Metal:585780079955673108>\n Items: **{giftData}**🎁, **{crateData}**📦, **{keyData}**🔑")
                                embed.set_thumbnail(url=ctx.author.avatar_url)
                                embed.set_footer(text=f"Date of Crate Opening: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
                                await orderChannel.send(embed=embed)
                            if str(x) == '<:Stone:585780065892171776>':
                                prizeName = ' Stone'
                                stoneData += int(prizeDict[str(x)]*int(y))
                                dataUpdate = {
                                    'Currencies.Stone':stoneData
                                }
                                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                            if str(x) == '🎟️':
                                prizeName = ' Pinata Ticket(s)'
                                pinataData += int(prizeDict[str(x)]*int(y))
                                dataUpdate = {
                                    'Items.pinataSlot':pinataData
                                }
                                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                            if str(x) == '🔑':
                                prizeName = ' Key(s)'  
                                keyData += float(prizeDict[str(x)]*int(y))
                                dataUpdate = {
                                    'Items.Keys':keyData
                                }
                                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                            prizeStr += f'\n{str(x)}: **{prizeDict[str(x)]*int(y)}** {prizeName}'
                            embed = discord.Embed(title='📦 Crate Opening', description=prizeStr, color=discord.Color.from_hsv(random.random(), 1, 1))
                            await crateMsg.edit(embed=embed)
                            await asyncio.sleep(2)
                    if str(x) == 'Legendary':
                        prizeStr += '\n\n**=== Legendary Resources ===**'
                        prizeName =''
                        for x, y in legendaryPrize.items(): 
                            if str(x) == '<:Metal:585780079955673108>':
                                prizeName = ' Metal'
                                metalData += int(prizeDict[str(x)]*int(y))
                                dataUpdate = {
                                    'Currencies.Metal':metalData
                                }
                                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})   
                            prizeStr += f'\n{str(x)}: **{prizeDict[str(x)]*int(y)}** {prizeName}'
                            embed = discord.Embed(title='📦 Crate Opening', description=prizeStr, color=discord.Color.from_hsv(random.random(), 1, 1))
                            await crateMsg.edit(embed=embed)
                            await asyncio.sleep(2)        
                    if str(x) == 'Mythic':
                        prizeStr += '\n\n**=== Mythic Resources ===**'
                        prizeName =''
                        for x, y in mythicPrize.items():
                            if str(x) == '⭐':
                                prizeName = ' Reputation'
                                repData += int(prizeDict[str(x)]*int(y))
                                dataUpdate = {
                                    'Profile.Rep':repData
                                }
                                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                            if str(x) == '📦':
                                prizeName = ' Crate'
                                crateData += int(prizeDict[str(x)]*int(y))
                                dataUpdate = {
                                    'Items.Crates':crateData
                                }    
                                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})       
                            prizeStr += f'\n{str(x)}: **{prizeDict[str(x)]*int(y)}** {prizeName}'
                            embed = discord.Embed(title='📦 Crate Opening', description=prizeStr, color=discord.Color.from_hsv(random.random(), 1, 1))
                            await crateMsg.edit(embed=embed)
                            await asyncio.sleep(2)
                return await level_up(ctx)

        elif str(Item) == 'gift':
            if giftData <1:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough gifts. Try again later.')
                return await ctx.send(embed=eembed)    
            elif keyData < 1:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough keys. Try again later.')
                return await ctx.send(embed=eembed)  
            else:
                # Minus 1 crate and 1 key    
                keyData -= 1
                giftData -= 1
                dataUpdate = {
                    'Items.Keys':keyData,
                    'Items.Gifts':giftData
                }
                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                # 20% to win more than 250 wood
                chanceToStrike = 35
                if random.randint(1,100) < chanceToStrike:
                    # Wins > 250 wood
                    prize = range(250, 400)
                    prize = numpy.random.choice(prize, 1)
                    
                    woodData += float(prize)
                    expData += float(prize)
                    dataUpdate = {
                        'Currencies.Wood':woodData,                        
                        'Profile.Experience':expData
                    }
                    self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                    await level_up(ctx)
                    await ctx.send(ctx.author.mention)
                    embed = discord.Embed(title='🎁 Gift Opening', description=f'You found **{int(prize)}**<:Wood:585780105696116736>', color=discord.Color.from_hsv(random.random(), 1, 1))
                    embed.add_field(name='💳 Balance', value=f'You now have **{round(woodData)}**<:Wood:585780105696116736>')
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text='Check your bank balance by typing `.profile`')
                    return await ctx.send(embed=embed)  
                    
                else:
                    prize = range(100, 250)
                    prize = numpy.random.choice(prize, 1)

                    woodData += float(prize)
                    expData += float(prize)
                    dataUpdate = {
                        'Currencies.Wood':woodData,                        
                        'Profile.Experience':expData
                    }
                    self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                    await level_up(ctx)
                    
                    await ctx.send(ctx.author.mention)
                    embed = discord.Embed(title='🎁 Gift Opening', description=f'You found **{int(prize)}**<:Wood:585780105696116736>', color=discord.Color.from_hsv(random.random(), 1, 1))
                    embed.add_field(name='💳 Balance', value=f'You now have **{round(woodData)}**<:Wood:585780105696116736>')
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text='Check your bank balance by typing `.profile`')
                    return await ctx.send(embed=embed)  
    @claim.error
    async def claim_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            eembed = errorembed(description=f"{ctx.author.mention} There's an User opening a **gift/crate** in this channel. Kindly head over to another economy channel or try again in **{error.retry_after:.2}s**.")
            return await ctx.send(embed=eembed)

    @commands.command()
    @has_registered()
    @is_economy_channel()
    async def consume(self, ctx, Potion, Amount:int=None):
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            hpData = float(x['RPG']['HP'])
            maxHPData = float(x['RPG']['maxHP'])
            hpPotionData = int(x['Items']['hpPotion'])
            shieldPotionData = int(x['Items']['shieldPotion'])
        
        if Amount is None:
            Amount = 1
        
        if str(Potion) in ['hp', 'health', 'Health', 'HP']:
            if hpPotionData < 1:
                eembed = errorembed(description=f"{ctx.author.mention} You currently do not have any health potions. Try again later.")
                return await ctx.send(embed=eembed)
            # Checks if HP is already full
            if hpData >= maxHPData:
                eembed = errorembed(description=f"{ctx.author.mention} Your HP is currently **100%**. There's no need for a health potion.")
                return await ctx.send(embed=eembed)
            else:
                hpPotionData -= 1
                hpData = maxHPData
                dataUpdate = {
                    'RPG.HP':hpData,
                    'Items.hpPotion':hpPotionData                     
                }
                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                pembed = passembed(description=f"{ctx.author.mention} You've successfully restored your life to **100%**!")
                return await ctx.send(embed=pembed)
        elif str(Potion) in ['shield', 'Shield']:
            if shieldPotionData < 1:
                eembed = errorembed(description=f"{ctx.author.mention} You currently do not have any shield potions. Try again later.")
                return await ctx.send(embed=eembed)
            else:
                shieldPotionData -= 1
                shieldGained = maxHPData*0.1
                hpData += shieldGained
                dataUpdate = {
                    'RPG.HP':hpData,
                    'Items.shieldPotion':shieldPotionData
                }
                self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                pembed = passembed(description=f"{ctx.author.mention} You've successfully gained **{round(shieldGained)}** extra health.")
                return await ctx.send(embed=pembed)

    
    
    
# Adding the cog to main script
def setup(bot):
    bot.add_cog(Usage(bot))    