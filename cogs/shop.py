import pymongo
import discord
import datetime
import pytz
import os

from discord.ext import commands
from cogs.utils.checks import is_economy_channel, has_registered
from cogs.utils.embed import (passembed, errorembed)


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = pymongo.MongoClient(os.getenv("MONGO_DB"))
        self.db = self.client.get_database('Users')
        self.records = self.db.horizon_database

    @commands.command()
    @has_registered()
    @is_economy_channel()
    async def shop(self, ctx):
        embed = discord.Embed(description='Welcome! Type ``.buy <itemNumber> <Amount>`` to purchase something', color=discord.Color.purple()) 
        embed.set_author(name=f'{ctx.guild.name} Store', icon_url=ctx.guild.icon_url)
        embed.add_field(name='Cash Items', value='<a:Loading:586942963905724439> _Coming soon..._')
        #embed.add_field(name='Cash Items', value='**#1** <:vBucks:576671666789154816> **1,000** V-Bucks - **18** Stone<:Stone:585780065892171776>\n **#2** 🛰️ Paid Advertisement - **195** Wood<:Wood:585780105696116736>\n **#3** 💶 **$30** Paypal - **17** Metal<:Metal:585780079955673108>\n **#4** <:Steam:578949627467005953> Steam Games (**$1**) - **90** Wood<:Wood:585780105696116736>', inline=False)embed.add_field(name='Cash Items', value='**#1** <:vBucks:576671666789154816> **1,000** V-Bucks - **18** Stone<:Stone:585780065892171776>\n **#2** 🛰️ Paid Advertisement - **195** Wood<:Wood:585780105696116736>\n **#3** 💶 **$30** Paypal - **17** Metal<:Metal:585780079955673108>\n **#4** <:Steam:578949627467005953> Steam Games (**$1**) - **90** Wood<:Wood:585780105696116736>', inline=False)
        embed.add_field(name='Cosmetics', value='**#5** 🔑 **1** Key - **300** Wood<:Wood:585780105696116736>\n **#6** 🎁 **1** Gift - **350** Wood<:Wood:585780105696116736>\n **#7** 📦 **1** Crate - **5** <:Stone:585780065892171776>', inline=False)
        embed.add_field(name='Consumables', value='**#8** <:HealthPotion:584669257002909726> **1** Health Potion - **25** Wood<:Wood:585780105696116736>\n **#9** <:ShieldPotion:584666738671616013> **1** Shield Potion - **5** Stone<:Stone:585780065892171776>', inline=False)
        embed.add_field(name='Conversion of Currencies', value='**#10** <:Stone:585780065892171776> **1** Stone - **100** Wood<:Wood:585780105696116736>\n **#11** <:Metal:585780079955673108> **1** Metal - **300** Wood<:Wood:585780105696116736>\n **#12** <:Wood:585780105696116736> **100** Wood - **1** Stone<:Stone:585780065892171776>\n **#13** <:Wood:585780105696116736> **300** Wood - **1** Metal<:Metal:585780079955673108>', inline=False)
        await ctx.send(embed=embed)   

    @commands.command()
    @has_registered()
    @is_economy_channel()
    @commands.cooldown(1, 1.0, commands.BucketType.user)
    async def buy(self, ctx, itemNumber: int, Amount:int=None):
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            woodData = float(x['Currencies']['Wood'])
            stoneData = int(x['Currencies']['Stone'])
            metalData = int(x['Currencies']['Metal'])
            crateData = int(x['Items']['Crates'])
            keyData = int(x['Items']['Keys'])
            giftData = int(x['Items']['Gifts'])
            hpPotionData = int(x['Items']['hpPotion'])
            shieldPotionData = int(x['Items']['shieldPotion'])
        
        if Amount is None:
            Amount = 1
            
        if itemNumber < 5 or itemNumber > 13:
            eembed = errorembed(description=f"{ctx.author.mention} There's only 8 itemNumbers in the shop currently.")
            return await ctx.send(embed=eembed)
            
        # # vBucks
        # elif itemNumber == 1:
        #     price = 18
        #     # Checks if User has enough currency
        #     if stoneData < price*Amount:
        #         eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
        #         return await ctx.send(embed=eembed)
        #     else:    
        #         stoneData -= float(price*Amount)
        #         dataUpdate = {
        #             'Currencies.Stone':stoneData
        #         }
        #         update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

        #         pembed = passembed(description=f'{ctx.author.mention} You have successfully purchased **{Amount}** **1,000 V-Bucks**.')
        #         await ctx.send(embed=pembed)
        #     orderChannel = discord.utils.get(ctx.guild.channels, name='order-receipts')
        #     embed = discord.Embed(title='<:vBucks:576671666789154816> 1,000 V-Bucks Order', description=f'You have successfully purchased **{Amount}** **1,000 V-Bucks**. Kindly send this receipt to <@545977500275048448>.', color=discord.Color.green())
        #     embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(woodData)}**<:Wood:585780105696116736>, **{round(stoneData)}**<:Stone:585780065892171776>, **{round(metalData)}**<:Metal:585780079955673108>\n Items: **{round(giftData)}**🎁, **{round(crateData)}**📦, **{round(keyData)}**🔑\n Consumables: **{hpPotionData}**<:HealthPotion:584669257002909726>, **{shieldPotionData}**<:ShieldPotion:584666738671616013>")
        #     embed.set_thumbnail(url=ctx.author.avatar_url)
        #     embed.set_footer(text=f"• Date of Purchase: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
        #     return await orderChannel.send(embed=embed)

        # # Paid Advertisment
        # elif itemNumber == 2:            
        #     price = 150
        #     # Checks if User has enough currency
        #     if woodData < price*Amount:
        #         eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
        #         return await ctx.send(embed=eembed)
        #     else:    
        #         woodData -= float(price*Amount)
        #         dataUpdate = {
        #             'Currencies.Wood':woodData
        #         }
        #         update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                
        #         pembed = passembed(description=f'{ctx.author.mention} You have successfully purchased **{Amount}** **paid advertisement(s)**.')
        #         await ctx.send(embed=pembed)
        #         orderChannel = discord.utils.get(ctx.guild.channels, name='order-receipts')
        #         embed = discord.Embed(title='🛰️ Paid Advertisement Order', description=f'You have successfully purchased **{Amount}** paid advertisement(s). Kindly send this receipt to <@545977500275048448>.', color=discord.Color.green())
        #         embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(woodData)}**<:Wood:585780105696116736>, **{round(stoneData)}**<:Stone:585780065892171776>, **{round(metalData)}**<:Metal:585780079955673108>\n Items: **{round(giftData)}**🎁, **{round(crateData)}**📦, **{round(keyData)}**🔑\n Consumables: **{hpPotionData}**<:HealthPotion:584669257002909726>, **{shieldPotionData}**<:ShieldPotion:584666738671616013>")
        #         embed.set_thumbnail(url=ctx.author.avatar_url)
        #         embed.set_footer(text=f"• Date of Purchase: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
        #         return await orderChannel.send(embed=embed)
        
        # # $30 Cash Out
        # if itemNumber == 3:
        #     price = 17
        #     # Checks if User has enough currency
        #     if metalData < price*Amount:
        #         eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
        #         return await ctx.send(embed=eembed)
        #     else:
        #         metalData -= float(price*Amount)
        #         dataUpdate = {
        #             'Currencies.Metal':metalData
        #         }
        #         update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

        #         pembed = passembed(description=f'{ctx.author.mention} You have successfully purchased **{Amount}** **$30** cash payout.')
        #         await ctx.send(embed=pembed)
        #         orderChannel = discord.utils.get(ctx.guild.channels, name='order-receipts')
        #         embed = discord.Embed(title='💶 $30 Paypal', description=f'You have successfully purchased **{Amount}** **$30 cash payout(s)**. Kindly send this receipt to <@545977500275048448>.', color=discord.Color.green())
        #         embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(woodData)}**<:Wood:585780105696116736>, **{round(stoneData)}**<:Stone:585780065892171776>, **{round(metalData)}**<:Metal:585780079955673108>\n Items: **{round(giftData)}**🎁, **{round(crateData)}**📦, **{round(keyData)}**🔑\n Consumables: **{hpPotionData}**<:HealthPotion:584669257002909726>, **{shieldPotionData}**<:ShieldPotion:584666738671616013>")
        #         embed.set_thumbnail(url=ctx.author.avatar_url)
        #         embed.set_footer(text=f"• Date of Purchase: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
        #         return await orderChannel.send(embed=embed)
        
        # # Steam Game
        # if itemNumber == 4:
        #     price = 90
        #     # Checks if User has enough currency
        #     if woodData < price*Amount:
        #         eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
        #         return await ctx.send(embed=eembed)
        #     else:
        #         woodData -= float(price*Amount)
        #         dataUpdate = {
        #             'Currencies.Wood':woodData
        #         }
        #         update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

        #         pembed = passembed(description=f'{ctx.author.mention} You have successfully purchased **{Amount}** **{price*Amount}** Steam Game.')
        #         await ctx.send(embed=pembed)
        #         orderChannel = discord.utils.get(ctx.guild.channels, name='order-receipts')
        #         embed = discord.Embed(title='💶 $30 Paypal', description=f'You have successfully purchased **{Amount}** **{price*Amount}** Steam Game**. Kindly send this receipt to <@545977500275048448>.', color=discord.Color.green())
        #         embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(woodData)}**<:Wood:585780105696116736>, **{round(stoneData)}**<:Stone:585780065892171776>, **{round(metalData)}**<:Metal:585780079955673108>\n Items: **{round(giftData)}**🎁, **{round(crateData)}**📦, **{round(keyData)}**🔑\n Consumables: **{hpPotionData}**<:HealthPotion:584669257002909726>, **{shieldPotionData}**<:ShieldPotion:584666738671616013>")
        #         embed.set_thumbnail(url=ctx.author.avatar_url)
        #         embed.set_footer(text=f"• Date of Purchase: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
        #         return await orderChannel.send(embed=embed)
        
        # Convert 300 wood to 1 key
        if itemNumber == 5:
            price = 300
            # Checks if User has enough currency
            if woodData < price*Amount:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
                return await ctx.send(embed=eembed)
            else:
                woodData -= float(price*Amount)
                keyData += 1*Amount
                dataUpdate = {
                    'Currencies.Wood':woodData,
                    'Items.Keys':keyData
                }
                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                pembed = passembed(description=f'{ctx.author.mention} You have successfully purchased **{Amount}** key(s).')
                await ctx.send(embed=pembed)
                orderChannel = discord.utils.get(ctx.guild.channels, name='order-receipts')
                embed = discord.Embed(title='🔮 Cosmetics', description=f'Your order has been processed. You have successfully purchased **{Amount}** **key(s)**. Do contact a moderator if there are any issues.', color=discord.Color.green())
                embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(woodData)}**<:Wood:585780105696116736>, **{round(stoneData)}**<:Stone:585780065892171776>, **{round(metalData)}**<:Metal:585780079955673108>\n Items: **{round(giftData)}**🎁, **{round(crateData)}**📦, **{round(keyData)}**🔑\n Consumables: **{hpPotionData}**<:HealthPotion:584669257002909726>, **{shieldPotionData}**<:ShieldPotion:584666738671616013>")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=f"• Date of Purchase: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
                return await orderChannel.send(embed=embed)

        # Convert 350 wood to 1 gift
        if itemNumber == 6:
            price = 350
            # Checks if User has enough currency
            if woodData < price*Amount:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
                return await ctx.send(embed=eembed)
            else:
                woodData -= float(price*Amount)
                giftData += 1*Amount
                dataUpdate = {
                    'Currencies.Wood':woodData,
                    'Items.Gifts':giftData
                }
                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                pembed = passembed(description=f'{ctx.author.mention} You have successfully purchased **{Amount}** gift(s).')
                await ctx.send(embed=pembed)
                orderChannel = discord.utils.get(ctx.guild.channels, name='order-receipts')
                embed = discord.Embed(title='🔮 Cosmetics', description=f'Your order has been processed. You have successfully purchased **{Amount}** **gift(s)**. Do contact a moderator if there are any issues.', color=discord.Color.green())
                embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(woodData)}**<:Wood:585780105696116736>, **{round(stoneData)}**<:Stone:585780065892171776>, **{round(metalData)}**<:Metal:585780079955673108>\n Items: **{round(giftData)}**🎁, **{round(crateData)}**📦, **{round(keyData)}**🔑\n Consumables: **{hpPotionData}**<:HealthPotion:584669257002909726>, **{shieldPotionData}**<:ShieldPotion:584666738671616013>")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=f"• Date of Purchase: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
                return await orderChannel.send(embed=embed)

        # Convert 5 stone to 1 crate
        if itemNumber == 7:
            price = 3
            # Checks if User has enough currency
            if stoneData < price*Amount:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
                return await ctx.send(embed=eembed)
            else:
                stoneData -= float(price*Amount)
                crateData += 1*Amount 
                dataUpdate = {
                    'Currencies.Stone':stoneData,
                    'Items.Crates':crateData
                }
                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                pembed = passembed(description=f'{ctx.author.mention} You have successfully purchased **{Amount}** crate(s).')
                await ctx.send(embed=pembed)
                orderChannel = discord.utils.get(ctx.guild.channels, name='order-receipts')
                embed = discord.Embed(title='🔮 Cosmetics', description=f'Your order has been processed. You have successfully purchased **{Amount}** **crate(s)**. Do contact a moderator if there are any issues.', color=discord.Color.green())
                embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(woodData)}**<:Wood:585780105696116736>, **{round(stoneData)}**<:Stone:585780065892171776>, **{round(metalData)}**<:Metal:585780079955673108>\n Items: **{round(giftData)}**🎁, **{round(crateData)}**📦, **{round(keyData)}**🔑\n Consumables: **{hpPotionData}**<:HealthPotion:584669257002909726>, **{shieldPotionData}**<:ShieldPotion:584666738671616013>")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=f"• Date of Purchase: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
                return await orderChannel.send(embed=embed)

        # Convert 25 wood to 1 health potion
        if itemNumber == 8:
            price = 25
            # Checks if User has enough currency
            if woodData < price*Amount:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
                return await ctx.send(embed=eembed)
            else:
                woodData -= float(price*Amount)
                hpPotionData += 1*Amount 
                dataUpdate = {
                    'Currencies.Wood':woodData,
                    'Items.hpPotion':hpPotionData
                }
                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                pembed = passembed(description=f'{ctx.author.mention} You have successfully purchased **{Amount}** health potion(s).')
                await ctx.send(embed=pembed)
                orderChannel = discord.utils.get(ctx.guild.channels, name='order-receipts')
                embed = discord.Embed(title='⚔️ Consumables', description=f'Your order has been processed. You have successfully purchased **{Amount}** **health potion(s)**. Do contact a moderator if there are any issues.', color=discord.Color.green())
                embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(woodData)}**<:Wood:585780105696116736>, **{round(stoneData)}**<:Stone:585780065892171776>, **{round(metalData)}**<:Metal:585780079955673108>\n Items: **{round(giftData)}**🎁, **{round(crateData)}**📦, **{round(keyData)}**🔑\n Consumables: **{hpPotionData}**<:HealthPotion:584669257002909726>, **{shieldPotionData}**<:ShieldPotion:584666738671616013>")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=f"• Date of Purchase: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
                return await orderChannel.send(embed=embed)

        # Convert 5 stone to 1 shield potion
        if itemNumber == 9:
            price = 5
            # Checks if User has enough currency
            if stoneData < price*Amount:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
                return await ctx.send(embed=eembed)
            else:
                stoneData -= float(price*Amount)
                shieldPotionData += 1*Amount 
                dataUpdate = {
                    'Currencies.Stone':stoneData,
                    'Items.shieldPotion':shieldPotionData
                }
                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                pembed = passembed(description=f'{ctx.author.mention} You have successfully purchased **{Amount}** shield potion(s).')
                await ctx.send(embed=pembed)
                orderChannel = discord.utils.get(ctx.guild.channels, name='order-receipts')
                embed = discord.Embed(title='⚔️ Consumables', description=f'Your order has been processed. You have successfully purchased **{Amount}** **shield potion(s)**. Do contact a moderator if there are any issues.', color=discord.Color.green())
                embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(woodData)}**<:Wood:585780105696116736>, **{round(stoneData)}**<:Stone:585780065892171776>, **{round(metalData)}**<:Metal:585780079955673108>\n Items: **{round(giftData)}**🎁, **{round(crateData)}**📦, **{round(keyData)}**🔑\n Consumables: **{hpPotionData}**<:HealthPotion:584669257002909726>, **{shieldPotionData}**<:ShieldPotion:584666738671616013>")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=f"• Date of Purchase: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
                return await orderChannel.send(embed=embed)        

        # Convert 100 wood to 1 stone
        if itemNumber == 10:
            price = 100
            # Checks if User has enough currency
            if woodData < price*Amount:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
                return await ctx.send(embed=eembed)
            else:
                woodData -= float(price*Amount)
                stoneData += 1*Amount
                dataUpdate = {
                    'Currencies.Wood':woodData,
                    'Currencies.Stone':stoneData
                }
                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                pembed = passembed(description=f'{ctx.author.mention} You have successfully converted **{price*Amount}**<:Wood:585780105696116736> to **{1*Amount}**<:Stone:585780065892171776>')
                await ctx.send(embed=pembed)
                orderChannel = discord.utils.get(ctx.guild.channels, name='order-receipts')
                embed = discord.Embed(title='🌍 Conversion of Currency', description='Your order has been processed. Do contact a moderator if there are any issues.', color=discord.Color.green())
                embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(woodData)}**<:Wood:585780105696116736>, **{round(stoneData)}**<:Stone:585780065892171776>, **{round(metalData)}**<:Metal:585780079955673108>\n Items: **{round(giftData)}**🎁, **{round(crateData)}**📦, **{round(keyData)}**🔑\n Consumables: **{hpPotionData}**<:HealthPotion:584669257002909726>, **{shieldPotionData}**<:ShieldPotion:584666738671616013>")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=f"• Date of Purchase: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
                return await orderChannel.send(embed=embed)

        # Converts 300 wood to 1 metal        
        elif itemNumber == 11:
            price = 300
            if woodData < price*Amount:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
                return await ctx.send(embed=eembed)
            else:
                woodData -= float(price*Amount)
                metalData += 1*Amount
                dataUpdate = {
                    'Currencies.Wood':woodData,
                    'Currencies.Metal':metalData
                }
                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                pembed = passembed(description=f'{ctx.author.mention} You have successfully converted **{price*Amount}**<:Wood:585780105696116736> to **{1*Amount}**<:Metal:585780079955673108>')
                await ctx.send(embed=pembed)
                orderChannel = discord.utils.get(ctx.guild.channels, name='order-receipts')
                embed = discord.Embed(title='🌍 Conversion of Currency', description='Your order has been processed. Do contact a moderator if there are any issues.', color=discord.Color.green())
                embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(woodData)}**<:Wood:585780105696116736>, **{round(stoneData)}**<:Stone:585780065892171776>, **{round(metalData)}**<:Metal:585780079955673108>\n Items: **{round(giftData)}**🎁, **{round(crateData)}**📦, **{round(keyData)}**🔑\n Consumables: **{hpPotionData}**<:HealthPotion:584669257002909726>, **{shieldPotionData}**<:ShieldPotion:584666738671616013>")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=f"• Date of Purchase: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
                return await orderChannel.send(embed=embed)

        # Converts 1 stone to 100 wood
        elif itemNumber == 12:
            price = 1
            if stoneData < price*Amount:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
                return await ctx.send(embed=eembed)
            else:
                woodData += float(100*Amount)                
                stoneData -= price*Amount
                dataUpdate = {
                    'Currencies.Wood':woodData,
                    'Currencies.Stone':stoneData
                }
                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                pembed = passembed(description=f'{ctx.author.mention} You have successfully converted **{price*Amount}**<:Stone:585780065892171776> to **{100*Amount}**<:Wood:585780105696116736>')
                await ctx.send(embed=pembed)
                orderChannel = discord.utils.get(ctx.guild.channels, name='order-receipts')
                embed = discord.Embed(title='🌍 Conversion of Currency', description='Your order has been processed. Do contact a moderator if there are any issues.', color=discord.Color.green())
                embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(woodData)}**<:Wood:585780105696116736>, **{round(stoneData)}**<:Stone:585780065892171776>, **{round(metalData)}**<:Metal:585780079955673108>\n Items: **{round(giftData)}**🎁, **{round(crateData)}**📦, **{round(keyData)}**🔑\n Consumables: **{hpPotionData}**<:HealthPotion:584669257002909726>, **{shieldPotionData}**<:ShieldPotion:584666738671616013>")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=f"• Date of Purchase: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
                return await orderChannel.send(embed=embed)
        
        # Converts 1 metal to 300 wood
        elif itemNumber == 13:
            price = 1
            if metalData < price*Amount:
                eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
                return await ctx.send(embed=eembed)
            else:
                woodData += float(300*Amount)
                metalData -= price*Amount
                dataUpdate = {
                    'Currencies.Wood':woodData,
                    'Currencies.Metal':metalData
                }
                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

                pembed = passembed(description=f'{ctx.author.mention} You have successfully converted **{price*Amount}**<:Metal:585780079955673108> to **{300*Amount}**<:Wood:585780105696116736>')
                await ctx.send(embed=pembed)
                orderChannel = discord.utils.get(ctx.guild.channels, name='order-receipts')
                embed = discord.Embed(title='🌍 Conversion of Currency', description='Your order has been processed. Do contact a moderator if there are any issues.', color=discord.Color.green())
                embed.add_field(name='Particulars', value=f"Name: **{ctx.author.name}**\n ID: **{ctx.author.id}**\n Balance: **{round(woodData)}**<:Wood:585780105696116736>, **{round(stoneData)}**<:Stone:585780065892171776>, **{round(metalData)}**<:Metal:585780079955673108>\n Items: **{round(giftData)}**🎁, **{round(crateData)}**📦, **{round(keyData)}**🔑\n Consumables: **{hpPotionData}**<:HealthPotion:584669257002909726>, **{shieldPotionData}**<:ShieldPotion:584666738671616013>")
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=f"• Date of Purchase: {datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')).strftime('%Y-%m-%d %H:%M%p')}")
                return await orderChannel.send(embed=embed) 

    @buy.error
    async def buy_error(self, ctx, error):   
        if isinstance(error, commands.CommandOnCooldown):
            eembed = errorembed(description=f'{ctx.author.mention} Kindly try again in **{error.retry_after:.2}s**.')
            return await ctx.send(embed=eembed)    
        elif isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Command Usage: ``.buy <Number> <Amount>``')    
            return await ctx.send(embed=eembed)

# Adding the cog to main script
def setup(bot):
    bot.add_cog(Shop(bot))