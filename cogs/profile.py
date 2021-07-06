import pymongo
import discord
import random
import datetime
import time
import pytz
import os

from discord.ext import commands
from cogs.utils.misc import level_up
from cogs.utils.checks import is_economy_channel, has_registered
from cogs.utils.embed import (passembed, errorembed)


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = pymongo.MongoClient(os.getenv("MONGO_DB"))
        self.db = self.client.get_database('Users')
        self.records = self.db.horizon_database
        self.jobDict = {
        'Sash Sergeant':['https://cdn.discordapp.com/attachments/584361634051653642/584361793036615700/Sash_Sergeant.png', 30, 20, 8, 5],
        'Shock Trooper':['https://cdn.discordapp.com/attachments/584361634051653642/584361792952729601/Shocker_Trooper.png', 70], 
        'Commando':['https://cdn.discordapp.com/attachments/584361634051653642/584361792697008138/Commando.png', 100], 
        'Special Forces':['https://cdn.discordapp.com/attachments/584361634051653642/584362378997661707/Special_Forces.png', 120], 
        'Bullet Storm':['https://cdn.discordapp.com/attachments/584361634051653642/584361789106421771/Bullet_Storm.png', 121],
        'BASE':['https://cdn.discordapp.com/attachments/584361852419571712/584361960301395968/BASE.png', 30, 20, 4, 6],
        'Heavy BASE':['https://cdn.discordapp.com/attachments/584361852419571712/584361961198977059/Heavy_BASE.png', 70], 
        'MEGABASE':['https://cdn.discordapp.com/attachments/584361852419571712/584361963937857576/MEGABASE.png', 100], 
        'Riot Control':['https://cdn.discordapp.com/attachments/584361852419571712/584361965233766400/Riot_Control.png', 120], 
        'Warden':['https://cdn.discordapp.com/attachments/584361852419571712/584361969167892480/Warden.png', 121],
        'Assassin':['https://cdn.discordapp.com/attachments/584362039024025605/584362105214468119/Assassin.png', 30, 20, 7, 3], 
        'Deadly Blade':['https://cdn.discordapp.com/attachments/584362039024025605/584362105273057281/Deadly_Blade.png', 70], 
        'Energy Thief':['https://cdn.discordapp.com/attachments/584362039024025605/584362105960923136/Energy_Thief.png', 100], 
        'Harvester':['https://cdn.discordapp.com/attachments/584362039024025605/584362107919794188/Harvester.png', 120], 
        'Shuriken Master':['https://cdn.discordapp.com/attachments/584362039024025605/584362108347613194/Shuriken_Master.png', 121],
        'Pathfinder':['https://cdn.discordapp.com/attachments/584365545856696330/584365582158397472/Pathfinder.png', 30, 20, 3, 7], 
        'Reclaimer':['https://cdn.discordapp.com/attachments/584365545856696330/584365582850195456/Reclaimer.png', 70], 
        'Recon Scout':['https://cdn.discordapp.com/attachments/584365545856696330/584365584809197579/Recon_Scout.png', 100], 
        'T.E.D.D Shot':['https://cdn.discordapp.com/attachments/584365545856696330/584365587279642631/TEDD_Shot.png', 120], 
        'Trailblazer':['https://cdn.discordapp.com/attachments/584365545856696330/584365590731554816/Trailblazer.png', 121]
        }    
    
    @commands.command()
    @is_economy_channel()
    async def register(self, ctx): 	
        # Checks if User is registered in Database
        try:
            userList = [x['userID'] for x in self.records.find({})]
            if str(ctx.author.id) in userList:
                eembed = errorembed(description=f'{ctx.author.mention} You have already registered.')
                return await ctx.send(embed=eembed)
        except:
            pass      

        new_user = {
                "userID":str(ctx.author.id),
                "userName":str(ctx.author),
                "dateJoined":datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')),

                'Currencies':{
                    "Wood":1000,
                    "Stone":0,
                    "Metal":0
                },
                'Kits':{
                    "Daily":0,
                    "Weekly":0,
                    "Supporter":0,
                    "Votes":0
                },
                
                'Items':{
                    "pinataSlot":0,
                    "Crates":0,
                    "Keys":0,
                    "Gifts":0,
                    'hpPotion':0,
                    'shieldPotion':0
                },

                'Profile':{
                    "Level":1,
                    "Experience":0,
                    "Rep":0,
                    "Wins":0,
                    "gamesPlayed":0
                },

                'RPG':{
                    'Class':'None',
                    'Job':'None',
                    'Dungeon':'Battle Bus',
                    'dungeonTime':0,
                    'maxHP':0,
                    'HP':0,
                    'Weapon':{},
                    'Attack':0,
                    'Defence':0
                },

                'Weapons':{}
        }
        updateData = self.records.insert_one(new_user)
        pembed = passembed(description=f'{ctx.author.mention} has successfully registered.')
        return await ctx.send(embed=pembed)
    
    @commands.command(aliases=['p'])
    @has_registered()
    @is_economy_channel()
    async def profile(self, ctx, user:discord.User=None):
        if user is None:
            user = ctx.author     
        
        totalUsers = [list((x['userID'], x['Profile']['Experience'])) for x in self.records.find({})] 
        rank = sorted(totalUsers, key=lambda x:float(x[1]), reverse=True)
        positionCount = [i for i,x in enumerate(rank) if x[0] == str(ctx.author.id)]
        for i in positionCount:
            position = int(i) + 1

        userData = self.records.find({'userID':str(user.id)})
        for x in userData:
            levelData = int(x['Profile']['Level'])
            expData = float(x['Profile']['Experience'])
            repData = int(x['Profile']['Rep'])
            woodData = round(float(x['Currencies']['Wood']))
            stoneData = int(x['Currencies']['Stone'])
            metalData = int(x['Currencies']['Metal'])
            giftData = int(x['Items']['Gifts'])
            crateData = int(x['Items']['Crates'])
            keyData = int(x['Items']['Keys'])
            hpData = round(float(x['RPG']['HP']))
            maxHPData = round(float(x['RPG']['maxHP']))
            weaponEquippedData = list(x['RPG']['Weapon'].values())[0] if bool(x['RPG']['Weapon']) is True else ''
            attackData = round(float(x['RPG']['Attack']))
            defenceData = round(float(x['RPG']['Defence']))
            jobData = str(x['RPG']['Job'])
            dungeonData = str(x['RPG']['Dungeon'])
            hpPotionData = int(x['Items']['hpPotion'])
            shieldPotionData = int(x['Items']['shieldPotion'])
            gamesData = int(x['Profile']['gamesPlayed'])
            winData = int(x['Profile']['Wins'])
        
        winRate = round((winData/gamesData)*100, 2) if gamesData != 0 else 0
        endLevel = float(expData ** (1/4))
        expNeeded = round((endLevel - levelData), 4)
        
        weaponEquippedName = weaponEquippedData[0] if weaponEquippedData != '' else 'None'
        weaponEquppedEmoji = weaponEquippedData[3] if weaponEquippedData != '' else '⚔️'
        weaponEquippedRarity = weaponEquippedData[6] if weaponEquippedData != '' else ''
        totalAttackData = round(attackData + (weaponEquippedData[1] + weaponEquippedData[2])/2) if weaponEquippedData else attackData
        
        embed = discord.Embed(color=discord.Color.from_hsv(random.random(), 1, 1))

        if jobData == 'None':
            url = user.avatar_url
        else:
            url = self.jobDict[jobData][0]          
                
        embed.set_author(name=f'Profile of {user.name}', icon_url=user.avatar_url)
        embed.set_thumbnail(url=url)
        embed.add_field(name='Information', value=f'🏆 Level: **{levelData}** ({round(expNeeded*100, 2)})%\n ⭐ Reputation: **+{repData}**\n <:Win:584702095563685899> Wins: **{winData}** ({winRate}%) \n 🏞 Location: **{dungeonData}**')
        embed.add_field(name='Statistics', value=f'🥋 Job: **{jobData}**\n 💗 HP: **{hpData}/{maxHPData}**\n {weaponEquppedEmoji} Weapon: **{weaponEquippedName}** {weaponEquippedRarity}\n 🗡 Attack: **{totalAttackData}**\n 🛡 Defence: **{defenceData}**')
        embed.add_field(name='Currencies', value=f'<:Wood:585780105696116736> Wood: **{woodData}**\n <:Stone:585780065892171776> Stone: **{stoneData}**\n <:Metal:585780079955673108> Metal: **{metalData}**')
        embed.add_field(name='Cosmetics', value=f'🔑 Key(s): **{keyData}**\n 🎁 Gift(s): **{giftData}**\n 📦 Crate(s): **{crateData}**')
        embed.add_field(name='Consumables', value=f'<:HealthPotion:584669257002909726> HP Potion(s): **{hpPotionData}**\n <:ShieldPotion:584666738671616013> Shield Potion(s): **{shieldPotionData}**')
        embed.add_field(name='Gun Inventory', value='`Type .inventory to check`')     
        embed.set_footer(text=f'• Global Ranking: {position}/{len(totalUsers)}')   
        await ctx.send(embed=embed)   

    @commands.command(aliases=['t'])  
    @has_registered()
    @is_economy_channel()
    async def top(self, ctx):
        members = [list((x['userID'], x['Profile']['Rep'], x['Profile']['Level'], x['Profile']['Experience'], x['RPG']['Job'], float(x['Currencies']['Wood']), float(x['Currencies']['Stone']), float(x['Currencies']['Metal']))) for x in self.records.find({})]    
        if len(members) == 0:
            eembed = errorembed(description='{0} There are no data in the leaderboard.'.format(ctx.author.mention))
            return await ctx.send(embed=eembed)
        else:
            rank = sorted(members, key=lambda x:float(x[3]), reverse=True)
            embed = discord.Embed(color=discord.Color.gold())
            embed.set_author(name=f"Global Leaderboard", icon_url=ctx.guild.icon_url)
            positionCount = [i for i,x in enumerate(rank) if x[0] == str(ctx.author.id)]

            # For Debugging Purposes
            # for i, x in enumerate(rank):
            #     print(str(i)+':'+str(x))
            
            # Position in Server
            for i in positionCount:
                position = int(i) + 1
            embed.set_footer(text=f'Your Global Ranking: {position}/{len(members)}', icon_url=ctx.author.avatar_url)
            
            counter = 0
            for x in rank[:6]:    
                counter += 1
                try:
                    player=discord.utils.get(self.bot.get_all_members(),id=int(x[0]))
                    playerName = player.name
                except:
                    continue    
                embed.add_field(name=f'#{counter}. {playerName}', value=f'🏆 Level: **{x[2]}**\n 🥋 Job: **{x[4]}**\n ⭐ Reputation: **+{x[1]}**\n <:Wood:585780105696116736> Wood: **{round(x[5])}**\n <:Stone:585780065892171776> Stone: **{round(x[6])}**\n <:Metal:585780079955673108> Metal: **{round(x[7])}**', inline=True)
            await ctx.send(embed=embed)
    
    # @commands.command()
    # async def transfer(self, ctx, user: discord.User, amount: int):
    #     await economyChannel(ctx)

    #     # Checks if User is registered in Database
    #     try:
    #         userList = [x['userID'] for x in self.records.find({})]
    #         if str(ctx.author.id) not in userList:
    #             eembed = errorembed(description=f'{ctx.author.mention} You are currently not registered yet. Kindly type ``.register`` to be registered.')
    #             return await ctx.send(embed=eembed)
    #         elif str(user.id) not in userList:
    #             eembed = errorembed(description=f'{ctx.author.mention} {user.mention} has not registered yet.')
    #             return await ctx.send(embed=eembed)
    #     except:
    #         pass  
            
    #     userData = self.records.find({'userID':str(ctx.author.id)})
    #     for x in userData:
    #         woodData = float(x['Currencies']['Wood'])
    #         expData = float(x['Profile']['Experience'])

    #     # Checks if User have enough money to transfer
    #     if woodData < amount:
    #         eembed = errorembed(description=f'{ctx.author.mention} You do not have enough currency. Try again later.')
    #         return await ctx.send(embed=eembed)
            

    #     try:
    #         woodData -= amount
    #         dataUpdate = {
    #             'Currencies.Wood':woodData
    #         }
    #         update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

    #         userData = self.records.find({'userID':str(user.id)})
    #         for x in userData:
    #             woodData = float(x['Currencies']['Wood'])
    #         woodData += amount
    #         dataUpdate = {
    #             'Currencies.Wood':woodData
    #         }
    #         update = self.records.update_one({'userID':str(user.id)}, {'$set':dataUpdate}) 
    #         pembed = passembed(description=f'{ctx.author.mention} has successfully transferred **{amount}**<:Wood:585780105696116736> to {user.mention}.')
    #         return await ctx.send(embed=pembed)
    #     except:
    #         pass

    # @transfer.error
    # async def transfer_error(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         eembed = errorembed(description='Command Usage: ``.transfer @User <Amount>``') 
    #         return await ctx.send(embed=eembed)

    @commands.command()
    @has_registered()
    @is_economy_channel()
    async def inventory(self, ctx):
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            weaponEquippedData = list(x['RPG']['Weapon'].keys())[0] if bool(x['RPG']['Weapon']) is True else ''
            inventoryData = x['Weapons'] 

        # Checks if User has any weapons in inventory
        if bool(inventoryData) is False:
            eembed = errorembed(description=f'{ctx.author.mention} You do not have any weapons. Try again later.') 
            return await ctx.send(embed=eembed)

        embed = discord.Embed(color=discord.Color.from_hsv(random.random(), 1, 1))
        embed.set_author(name=f"{ctx.author.name}'s Inventory", icon_url=ctx.author.avatar_url)
        embed.set_footer(text='Type `.equip <weaponID>` to equip a weapon')
        counter = 0
        for weaponID, weaponData in inventoryData.items():
            counter += 1
            weaponName = weaponData[0]
            weaponRarity = weaponData[5]
            minDmg = weaponData[1]
            maxDmg = weaponData[2]
            weaponEmoji = weaponData[3]
            rarityEmoji = weaponData[6]
            equipped = '(✔️)' if weaponEquippedData in x['RPG']['Weapon'].keys() and weaponEquippedData == weaponID else ''
            embed.add_field(name=f'Weapon #{counter}', value=f'{weaponEmoji} Weapon Name: **{weaponName}** {equipped}\n 🆔 Weapon ID: **{weaponID}**\n {rarityEmoji} Weapon Rarity: **{weaponRarity}**\n 🎯 Damage Range: **{minDmg} - {maxDmg}**')
        await ctx.send(embed=embed)   

    @commands.command()
    @has_registered()
    @is_economy_channel()
    async def equip(self, ctx, weaponID):
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            weaponEquippedData = x['RPG']['Weapon']
            inventoryData = x['Weapons']

        # Checks if User has the weapon
        if str(weaponID) not in inventoryData.keys():
            eembed = errorembed(description=f'{ctx.author.mention} You do not have this weapon - ``{weaponID}``. Try again later.') 
            return await ctx.send(embed=eembed)

        # Checks if User has already equipped the weapon
        if str(weaponID) in weaponEquippedData.keys():
            weaponName = weaponEquippedData[str(weaponID)][0]
            eembed = errorembed(description=f'{ctx.author.mention} You have already equipped {weaponName}.') 
            return await ctx.send(embed=eembed)

        else:
            weaponEquipped = {
                weaponID:inventoryData[str(weaponID)]
            }

            dataUpdate = {
                'RPG.Weapon':weaponEquipped
            }

            update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})

            pembed = passembed(description=f'{ctx.author.mention} You have successfully equipped **{inventoryData[str(weaponID)][0]}**.')
            return await ctx.send(embed=pembed)

    @commands.command()
    @has_registered()
    @is_economy_channel()
    async def dump(self, ctx, weaponID):
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            weaponEquippedData = x['RPG']['Weapon']
            inventoryData = x['Weapons']            

        # Checks if User has the weapon
        if str(weaponID) not in inventoryData.keys():
            eembed = errorembed(description=f'{ctx.author.mention} You do not have this weapon - ``{weaponID}``. Try again later.') 
            return await ctx.send(embed=eembed)

        # Checks if User has already equipped the weapon
        if str(weaponID) in weaponEquippedData.keys():
            weaponName = weaponEquippedData[str(weaponID)][0]
            eembed = errorembed(description=f'{ctx.author.mention} You are currently equipped with {weaponName}. Try again later') 
            return await ctx.send(embed=eembed)

        else:
            weaponName = inventoryData[str(weaponID)][0]
            del inventoryData[weaponID]

            dataUpdate = {
                'Weapons':inventoryData
            }

            update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})

            pembed = passembed(description=f'{ctx.author.mention} You have successfully dumped **{weaponName}**.')
            return await ctx.send(embed=pembed)
            
# Adding the cog to main script
def setup(bot):
    bot.add_cog(Profile(bot))
