import discord
import pymongo
import datetime
import pytz
import random
import time
import math
import os

from discord.ext import commands
from cogs.utils.misc import level_up, generateWeapon
from cogs.utils.checks import has_registered, is_economy_channel
from cogs.utils.embed import (passembed, errorembed)

class Dungeon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = pymongo.MongoClient(os.getenv("MONGO_DB"))
        self.db = self.client.get_database('Users')
        self.records = self.db.horizon_database
        self.dungeonName = ['Stonewood', 'Junk Junction', 'Haunted Hills', 'Plankerton', 'Pleasant Park', 'Leaky Lake', 'Neo Tilted', 'Canny Valley', 'Happy Hamlet', 'Polar Peak', 'Frosty Flights', 'Twine Peaks']
        self.dungeonTime = {
            'Stonewood':15, 
            'Junk Junction':30, 
            'Haunted Hills':45, 
            'Plankerton':60, 
            'Pleasant Park':80, 
            'Leaky Lake':95, 
            'Neo Tilted':120, 
            'Canny Valley':155, 
            'Happy Hamlet':180, 
            'Polar Peak':210, 
            'Frosty Flights':250, 
            'Twine Peaks':300
            }
        self.monsters = ['Husks', 'Zapper', 'Beehive', 'Hubby Husks', 'Lobber', 'Midget', 'Pitcher', 'Sploder', 'Riot Husky', 'Blaster', 'Flinger', 'Mimic', 'Smasher', 'Taker', 'Storm King']

    @commands.command()
    @has_registered()
    @is_economy_channel()
    async def dungeons(self, ctx):
        embed = discord.Embed(title='List of Available Dungeons', description='Difficulty increases as you advance each stage in the dungeon', color=0xb8e6e6)
        embed.add_field(name='Dungeon Name (ID)', value=f'#1. **{self.dungeonName[0]}**\n #2. **{self.dungeonName[1]}**\n #3. **{self.dungeonName[2]}**\n #4. **{self.dungeonName[3]}**\n #5. **{self.dungeonName[4]}**\n #6. **{self.dungeonName[5]}**\n #7. **{self.dungeonName[6]}**\n #8. **{self.dungeonName[7]}**\n #9. **{self.dungeonName[8]}**\n #10. **{self.dungeonName[9]}**\n #11. **{self.dungeonName[10]}**\n #12. **{self.dungeonName[11]}**')
        embed.add_field(name='Time Required (Mins)', value='\n'.join(x for x in map(str,list(self.dungeonTime.values()))))
        embed.set_footer(text='Type .dungeon <ID> to start your adventure')
        await ctx.send(embed=embed)

    @commands.command()
    @has_registered()
    @is_economy_channel()
    async def dungeon(self, ctx, dungeonID:int):
        if dungeonID < 1 or dungeonID > 12:
            eembed = errorembed(description=f"{ctx.author.mention} There's only 12 dungeons available. Try again later.")
            return await ctx.send(embed=eembed)

        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            dungeonTimeData = str(x['RPG']['dungeonTime'])
            dungeonData = str(x['RPG']['Dungeon'])
            classData = str(x['RPG']['Class'])
            hpData = float(x['RPG']['HP'])
            maxHPData  = float(x['RPG']['maxHP'])

        # Checks if User has a class
        if classData == 'None':
            eembed = errorembed(description=f'{ctx.author.mention} You have not chose a class yet. Kindly type ``.choose <Class>`` to select a class.')
            return await ctx.send(embed=eembed)

        # Checks if User is inside a dungeon
        if dungeonData != 'Battle Bus':
            eembed = errorembed(description=f'{ctx.author.mention} You are currently inside **{dungeonData}**. Kindly type ``.status`` to check on the progress.')
            return await ctx.send(embed=eembed)

        # Checks if User has enough HP
        if hpData < maxHPData/4:
            eembed = errorembed(description=f'{ctx.author.mention} You do not have enough HP to enter the dungeon. Try again later.')
            return await ctx.send(embed=eembed)

        try:
            # Converts date from database to compare
            availableTime = datetime.datetime.strptime(dungeonTimeData, '%Y-%m-%d %H:%M:%S.%f%z')

            # Current Time
            currentTime = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))

            # Current Time in seconds
            if currentTime < availableTime:
                eembed = errorembed(description=f"{ctx.author.mention} You are currently in **{dungeonData}**. Try again later.")
                return await ctx.send(embed=eembed)
            
            else:
                dungeonName = self.dungeonName[dungeonID-1]
                timeRequired = self.dungeonTime[dungeonName]*0.95 if classData == 'Ninja' else self.dungeonTime[dungeonName]
                # Use this format to update database
                formatTime = (datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')) + datetime.timedelta(minutes=timeRequired)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
                dataUpdate = {
                    'RPG.dungeonTime':formatTime,
                    'RPG.Dungeon':dungeonName
                }

                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})

                pembed = passembed(description=f"{ctx.author.mention} You've just entered into **{dungeonName}**. Type ``.status`` to check the progress of the mission.")
                return await ctx.send(embed=pembed)
        except:
            dungeonName = self.dungeonName[dungeonID-1]
            timeRequired = self.dungeonTime[dungeonName]*0.95 if classData == 'Ninja' else self.dungeonTime[dungeonName]
            # Use this format to update database
            formatTime = (datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')) + datetime.timedelta(minutes=timeRequired)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
            dataUpdate = {
                'RPG.dungeonTime':formatTime,
                'RPG.Dungeon':dungeonName
            }

            update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})

            pembed = passembed(description=f"{ctx.author.mention} You've just entered into **{dungeonName}**. Type ``.status`` to check the progress of the mission.")
            return await ctx.send(embed=pembed)


    @commands.command()
    @has_registered()
    @is_economy_channel()
    async def status(self, ctx):
        try:
            userData = self.records.find({'userID':str(ctx.author.id)})
            for x in userData:
                levelData = int(x['Profile']['Level'])
                expData = float(x['Profile']['Experience'])
                woodData = float(x['Currencies']['Wood'])
                hpData = round(float(x['RPG']['HP']))
                attackData = round(float(x['RPG']['Attack']))
                defenceData = round(float(x['RPG']['Defence']))
                classData = str(x['RPG']['Class'])
                dungeonData = str(x['RPG']['Dungeon'])
                dungeonTimeData = str(x['RPG']['dungeonTime'])
            
            # Checks if User is inside a dungeon
            if dungeonData == 'Battle Bus':
                eembed = errorembed(description=f'{ctx.author.mention} You are currently not inside any dungeon. Kindly type ``.dungeon <ID>`` to enter a dungeon.')
                return await ctx.send(embed=eembed)

            # Checks if User has remaining health after hunting
            if hpData <= 0:
                eembed = errorembed(description=f'{ctx.author.mention} You are currently at the final stage of the dungeon but do not have sufficient health to continue.')
                return await ctx.send(embed=eembed)

            # Converts date from database to compare
            availableTime = datetime.datetime.strptime(dungeonTimeData, '%Y-%m-%d %H:%M:%S.%f%z')
            timeInSeconds = time.mktime(availableTime.timetuple())

            # Current Time
            currentTime = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
            timeNowInSeconds = time.mktime(currentTime.timetuple())

            # Checks if Dungeon has been completed
            if currentTime > availableTime:
                dungeonDifficulty = self.dungeonName.index(dungeonData) + 1
                chanceToPass = random.randint(0, 100)
                successRate = (
                    attackData + defenceData + 75
                    - (dungeonDifficulty * random.randint(2, 10) + dungeonDifficulty * dungeonDifficulty )
                    + random.choice([levelData, -levelData])
                )
                if successRate > chanceToPass:
                    expMultiplier = dungeonDifficulty*dungeonDifficulty*1000
                    expExact = math.log10(50**(dungeonDifficulty*dungeonDifficulty))*expMultiplier
                    expGain = random.randint(int(expExact/2), int(expExact))
                    woodGain = random.randint(100 * (dungeonDifficulty - 1) or 100, 300 * (dungeonDifficulty - 1) or 200)
                    hpLostPercent = random.randint(1, 100)
                    hpLost = hpData*(hpLostPercent/100)
                    hpData -= hpLost
                    if hpData < 0:
                        hpData = 0
                    
                    classBonusWood = woodGain*1.15 if classData == 'Outlander' else woodGain
                    woodData += classBonusWood
                    classBonusExp = expGain*1.15 if classData == 'Outlander' else expGain
                    expData += classBonusExp

                    dataUpdate = {
                        'Currencies.Wood':woodData,
                        'Profile.Experience':expData,
                        'RPG.HP':hpData,
                        'RPG.dungeonTime':0,
                        'RPG.Dungeon':'Battle Bus'
                    }

                    update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})
                    await level_up(ctx)

                    chanceToGetWep = random.randint(0, 10)
                    weaponLoot = 3
                    if chanceToGetWep < weaponLoot:
                        weapon = generateWeapon(ctx)
                        weaponName = weapon[1]
                        rarityName = weapon[3]
                        rarityEmoji = weapon[4]
                        weaponID = weapon[0]
                        weaponEmoji = weapon[2]
                    embedWeapon = f'{weaponEmoji} Weapon: **{weaponName}** (ID: {weaponID})\n {rarityEmoji} Weapon Rarity: **{rarityName}**\n' if chanceToGetWep < weaponLoot else ''

                    embed = discord.Embed(title=f"{ctx.author.name}'s Dungeon", description='You have successfully **completed** the dungeon', color=discord.Color.green())
                    embed.add_field(name='Description', value=f'🏝 Dungeon: **{dungeonData}**\n 💗 HP: **-{round(hpLost)}**\n{embedWeapon}<:Wood:585780105696116736> Wood: **+{round(classBonusWood)}**\n <:BattlePass:585742444092456960> Experience: **+{round(classBonusExp)}**')
                    return await ctx.send(embed=embed)
                else:
                    # expMultiplier = dungeonDifficulty*dungeonDifficulty*1000
                    # expExact = math.log10(50**(dungeonDifficulty*dungeonDifficulty))*expMultiplier
                    # expGain = random.randint(int(expExact/2), int(expExact))/10
                    hpLost = hpData
                    hpData -= hpLost
                    
                    # classBonusExp = expGain*1.15 if classData == 'Outlander' else expGain
                    # expData += classBonusExp

                    dataUpdate = {
                        # 'Profile.Experience':expData,
                        'RPG.HP':hpData,
                        'RPG.dungeonTime':0,
                        'RPG.Dungeon':'Battle Bus'
                    }

                    update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})
                    # await level_up(ctx)

                    embed = discord.Embed(title=f"{ctx.author.name}'s Dungeon", description='You have **failed** the dungeon and unexpectedly died', color=discord.Color.red())
                    embed.add_field(name='Description', value=f'🏝 Dungeon: **{dungeonData}**\n 💗 HP: **-{round(hpLost)}**\n <:BattlePass:585742444092456960> Experience: **+{round(classBonusExp)}**')
                    return await ctx.send(embed=embed)
            else:
                cooldownMinutes = str((timeInSeconds - timeNowInSeconds)/60).split('.')[0]
                cooldownSeconds = round(float('.' + str((timeInSeconds - timeNowInSeconds)/60).split('.')[1])*60)
                dungeonDifficulty = self.dungeonName.index(dungeonData) + 1
                embed = discord.Embed(description=f"🏝 Dungeon Name: **{dungeonData}**\n 📶 Dungeon Difficulty: **{dungeonDifficulty}**\n <a:Loading:586942963905724439> Time to Completion: **{cooldownMinutes}** mins and **{cooldownSeconds}** secs", color=discord.Color.from_hsv(random.random(), 1, 1))
                embed.set_author(name=f"{ctx.author.name}'s Dungeon Progress", icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
        except:
            raise Exception


    @commands.command()
    @has_registered()
    @is_economy_channel()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def hunt(self, ctx):
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            levelData = int(x['Profile']['Level'])
            expData = float(x['Profile']['Experience'])
            woodData = float(x['Currencies']['Wood'])
            hpData = round(float(x['RPG']['HP']))
            maxHPData = round(float(x['RPG']['maxHP']))
            attackData = round(float(x['RPG']['Attack']))
            defenceData = round(float(x['RPG']['Defence']))
            jobData = str(x['RPG']['Job'])
            classData = str(x['RPG']['Class'])
            dungeonData = str(x['RPG']['Dungeon'])
            weaponEquippedData = list(x['RPG']['Weapon'].values())[0] if bool(x['RPG']['Weapon']) is True else ''

        # Checks if User is inside a dungeon
        if dungeonData == 'Battle Bus':
            eembed = errorembed(description=f'{ctx.author.mention} You are currently not inside any dungeon. Kindly type ``.dungeon <ID>`` to enter a dungeon to hunt for monsters.')
            return await ctx.send(embed=eembed)
        
        # Checks if User has enough HP
        if hpData < maxHPData/4:
            eembed = errorembed(description=f'{ctx.author.mention} You do not have enough HP to hunt monsters. Try again later.')
            return await ctx.send(embed=eembed)

        monsterName = random.choice(self.monsters)
        monsterMinLevel = self.dungeonName.index(str(dungeonData)) + 1
        monsterMinLevel = int(str(monsterMinLevel) + '0')
        monsterMaxLevel = monsterMinLevel + 10
        monsterActualLevel = random.choice(list(range(monsterMinLevel, monsterMaxLevel)))
        monsterHP = monsterActualLevel*10
        monsterMinDmg = monsterActualLevel 
        monsterMaxDmg = monsterMinDmg + random.randint(1 + monsterActualLevel, 5 + monsterActualLevel)
        weaponMinDmg = weaponEquippedData[1] if weaponEquippedData != '' else 0
        weaponMaxDmg = weaponEquippedData[2] if weaponEquippedData != '' else 0
        totalAttackData = round(attackData + (weaponEquippedData[1] + weaponEquippedData[2])/2) if weaponEquippedData else attackData
                
        embed = discord.Embed(color=0x35363B)
        embed.add_field(name='User Stats', value=f'📜 Name: {ctx.author.mention}\n 🥋 Job: **{jobData}**\n 🏆 Level: **{levelData}**\n 💗 Health: **{hpData}/{maxHPData}**\n 🗡 Attack: **{totalAttackData}**\n 🛡 Defence: **{defenceData}**')
        embed.add_field(name='Monster Stats', value=f'📜 Name: **{monsterName}**\n 🏞 Location: **{dungeonData}**\n 🏆 Level: **{monsterActualLevel}**\n 💗 Health: **{monsterHP}**\n 🗡 Attack: **{round((monsterMinDmg + monsterMaxDmg)/2)}**')
        embed.set_footer(text='Ensure that you have sufficient health to finish the dungeon')
        battleDescription = ''
        while True:
            # Damage to User
            hpLost = random.randint(monsterMinDmg, monsterMaxDmg)
            chanceToDefend = random.randint(0, 1)
            if chanceToDefend == 1:
                # Ensure that hpLost does not become negative which in turn heals the User
                if (hpLost - defenceData) < 0:
                    battleDescription += f'{ctx.author.mention} has successfully **blocked** the damage `🛡️`\n'
                else:
                    hpData -= hpLost
                    battleDescription += f'=> Dealt **{round(hpLost)}**`💗` to {ctx.author.mention} ({round(hpData)}`💗`)\n'
            else:
                hpData -= hpLost
                battleDescription += f'=> Dealt **{round(hpLost)}**`💗` to {ctx.author.mention} ({round(hpData)}`💗`)\n'

            if hpData <= 0:
                # expExact = math.log10(50**(monsterActualLevel*monsterActualLevel))*monsterActualLevel/3
                # expGain = random.randint(int(expExact/2), int(expExact))/50

                # classBonusExp = expGain*1.15 if classData == 'Outlander' else expGain
                # expData += classBonusExp
                hpData = 0

                dataUpdate = {
                    # 'Profile.Experience':expData,
                    'RPG.HP':hpData
                }

                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})
                # await level_up(ctx)
                
                listBattleDescription = battleDescription.splitlines()                
                newBattleDescription = str('\n'.join(listBattleDescription[:10]))

                embed.add_field(name='Battle Info', value=(newBattleDescription + '\n + more information...\n' + f'\n You have died to **{monsterName}**!' if len(listBattleDescription) > 10 else battleDescription + f'\n You have died to **{monsterName}**!'))
                # embed.add_field(name='Rewards', value=f'<:BattlePass:585742444092456960> Experience: **+{round(classBonusExp)}**', inline=False)
                embed.add_field(name='Rewards', value="There are no rewards. Try hunting again when you're stronger")
                return await ctx.send(embed=embed)
            # Damage to Monster
            hpLost = random.randint(attackData + weaponMinDmg, attackData + weaponMaxDmg)
            monsterHP -= hpLost
            battleDescription += f'=> Dealt **{round(hpLost)}**`💗` to {monsterName} ({(monsterHP)}`💗`)\n'
            
            if monsterHP <= 0:
                expExact = math.log10(50**(monsterActualLevel*monsterActualLevel))*monsterActualLevel/3
                expGain = random.randint(int(expExact/2), int(expExact))
                woodGain = random.randint(5 * monsterActualLevel, 20 * monsterActualLevel)

                classBonusWood = woodGain*1.15 if classData == 'Outlander' else woodGain
                woodData += classBonusWood
                classBonusExp = expGain*1.15 if classData == 'Outlander' else expGain
                expData += classBonusExp

                dataUpdate = {
                    'Currencies.Wood':woodData,
                    'Profile.Experience':expData,
                    'RPG.HP':hpData
                }

                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})
                await level_up(ctx)

                listBattleDescription = battleDescription.splitlines()                
                newBattleDescription = str('\n'.join(listBattleDescription[:10]))

                embed.add_field(name='Battle Info', value=(newBattleDescription + '\n + more information...\n' + f'\n You have defeated **{monsterName}**!' if len(listBattleDescription) > 10 else battleDescription + f'\n You have defeated **{monsterName}**!'))
                embed.add_field(name='Rewards', value=f'<:Wood:585780105696116736> Wood: **+{round(classBonusWood)}**\n <:BattlePass:585742444092456960> Experience: **+{round(classBonusExp)}**', inline=False)       
                return await ctx.send(embed=embed)
    @hunt.error
    async def hunt_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            eembed = errorembed(description=f'{ctx.author.mention} Kindly try again in **{error.retry_after:.3}s**.')
            return await ctx.send(embed=eembed) 

# Adding the cog to main script
def setup(bot):
    bot.add_cog(Dungeon(bot))
