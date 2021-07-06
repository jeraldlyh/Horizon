import pymongo
import discord
import random
import datetime
import time
import pytz
import os

from discord.ext import commands
from cogs.utils.misc import level_up
from cogs.utils.checks import is_donator, has_registered, is_economy_channel
from cogs.utils.embed import (passembed, errorembed)


class Kits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = pymongo.MongoClient(os.getenv("MONGO_DB"))
        self.db = self.client.get_database('Users')
        self.records = self.db.horizon_database
        self.classDict = {
        'Soldier':['Sash Sergeant', 'Shock Trooper', 'Commando', 'Special Forces', 'Bullet Storm'],
        'Constructor':['BASE', 'Heavy BASE', 'MEGABASE', 'Riot Control', 'Warden'],
        'Ninja':['Assassin', 'Deadly Blade', 'Dim Mak', 'Harvester', 'Shuriken Master'],
        'Outlander':['Pathfinder', 'Reclaimer', 'Recon Scout', 'T.E.D.D Shot', 'Trailblazer']
        } 

    def kitEmbed(self, ctx, amount, exp):
        embed = discord.Embed(color=discord.Color.from_hsv(random.random(), 1, 1))
        embed.set_author(name=f'{ctx.command.name.capitalize()} Kit', icon_url=ctx.author.avatar_url)
        embed.add_field(name='Rewards', value=f'Wood: **+{round(amount)}**<:Wood:585780105696116736>\n Experience: **+{round(exp)}**<:BattlePass:585742444092456960>')
        embed.set_footer(text='Type `.cd` to check your kit cooldowns')
        return embed

    @commands.command(aliases=['dl'])
    @has_registered()
    @is_economy_channel()
    async def daily(self, ctx):        
        amount = 150
        exp = 200
        
        try:
            userData = self.records.find({'userID':str(ctx.author.id)})
            for x in userData:
                timeData = str(x['Kits']['Daily'])
                woodData = float(x['Currencies']['Wood'])
                expData = float(x['Profile']['Experience'])
                jobData = str(x['RPG']['Job'])
                classData = str(x['RPG']['Class'])
                
            # Converts date from database to compare
            availableTime = datetime.datetime.strptime(timeData, '%Y-%m-%d %H:%M:%S.%f%z')

            # Current Time
            currentTime = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
            
            # Current Time in seconds
            if currentTime > availableTime:
                # Use this format to update database
                formatTime = (datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')) + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
                jobAdvancementBonus = self.classDict[classData].index(jobData) + 1 if jobData != 'None' else 1 if jobData != 'None' else 1
                kitAmount = amount*jobAdvancementBonus if classData else amount
                kitExp = exp*jobAdvancementBonus if classData else exp
                woodData += kitAmount
                expData += kitExp
                dataUpdate = {
                    'Kits.Daily':formatTime,
                    'Currencies.Wood':woodData,
                    'Profile.Experience':expData
                }

                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})              
                await level_up(ctx)

                await ctx.send(ctx.author.mention)
                embed = self.kitEmbed(ctx, kitAmount, kitExp)
                return await ctx.send(embed=embed)
            else:
                eembed = errorembed(description=f'{ctx.author.mention} You are currently on cooldown. Type ``.cd`` to check your cooldowns.')
                return await ctx.send(embed=eembed)
        except Exception as e:
            print(e)
            # Use this format to update database
            formatTime = (datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')) + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
            jobAdvancementBonus = self.classDict[classData].index(jobData) + 1 if jobData != 'None' else 1
            kitAmount = amount*jobAdvancementBonus if classData else amount
            kitExp = exp*jobAdvancementBonus if classData else exp
            woodData += kitAmount
            expData += kitExp
            dataUpdate = {
                    'Kits.Daily':formatTime,
                    'Currencies.Wood':woodData,
                    'Profile.Experience':expData
                }

            update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})            
            await level_up(ctx)

            await ctx.send(ctx.author.mention)
            embed = self.kitEmbed(ctx, kitAmount, kitExp)
            return await ctx.send(embed=embed)

    @commands.command(aliases=['wk'])
    @has_registered()
    @is_economy_channel()
    async def weekly(self, ctx):
        amount = 2000
        exp = 3500      
        
        try:
            userData = self.records.find({'userID':str(ctx.author.id)})
            for x in userData:
                timeData = str(x['Kits']['Weekly'])
                woodData = float(x['Currencies']['Wood'])
                expData = float(x['Profile']['Experience'])
                jobData = str(x['RPG']['Job'])
                classData = str(x['RPG']['Class'])
                
            # Converts date from database to compare
            availableTime = datetime.datetime.strptime(timeData, '%Y-%m-%d %H:%M:%S.%f%z')

            # Current Time
            currentTime = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
            
            # Current Time in seconds
            if currentTime > availableTime:
                # Use this format to update database
                formatTime = (datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')) + datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
                jobAdvancementBonus = self.classDict[classData].index(jobData) + 1 if jobData != 'None' else 1
                kitAmount = amount*jobAdvancementBonus if classData else amount
                kitExp = exp*jobAdvancementBonus if classData else exp
                woodData += kitAmount
                expData += kitExp
                dataUpdate = {
                    'Kits.Weekly':formatTime,
                    'Currencies.Wood':woodData,
                    'Profile.Experience':expData
                }

                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})              
                await level_up(ctx)

                await ctx.send(ctx.author.mention)
                embed = self.kitEmbed(ctx, kitAmount, kitExp)
                return await ctx.send(embed=embed)
            else:
                eembed = errorembed(description=f'{ctx.author.mention} You are currently on cooldown. Type ``.cd`` to check your cooldowns.')
                return await ctx.send(embed=eembed)
        except:
            # Use this format to update database
            formatTime = (datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')) + datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
            jobAdvancementBonus = self.classDict[classData].index(jobData) + 1 if jobData != 'None' else 1
            kitAmount = amount*jobAdvancementBonus if classData else amount
            kitExp = exp*jobAdvancementBonus if classData else exp
            woodData += kitAmount
            expData += kitExp
            dataUpdate = {
                'Kits.Weekly':formatTime,
                'Currencies.Wood':woodData,
                'Profile.Experience':expData
            }

            update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})            
            await level_up(ctx)

            await ctx.send(ctx.author.mention)
            embed = self.kitEmbed(ctx, kitAmount, kitExp)
            return await ctx.send(embed=embed)
               
    @commands.command(aliases=['sp'])
    @has_registered()
    @is_economy_channel()
    @commands.has_any_role('Titan Donator', 'Mystic Donator', 'Immortal Donator')
    async def supporter(self, ctx):
        amount = 350
        exp = 500     
        
        try:
            userData = self.records.find({'userID':str(ctx.author.id)})
            for x in userData:
                timeData = str(x['Kits']['Supporter'])
                woodData = float(x['Currencies']['Wood'])
                expData = float(x['Profile']['Experience'])
                jobData = str(x['RPG']['Job'])
                classData = str(x['RPG']['Class'])
                
            # Converts date from database to compare
            availableTime = datetime.datetime.strptime(timeData, '%Y-%m-%d %H:%M:%S.%f%z')

            # Current Time
            currentTime = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
            
            # Current Time in seconds
            if currentTime > availableTime:
                # Use this format to update database
                formatTime = (datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')) + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
                jobAdvancementBonus = self.classDict[classData].index(jobData) + 1 if jobData != 'None' else 1
                kitAmount = amount*jobAdvancementBonus if classData else amount
                kitExp = exp*jobAdvancementBonus if classData else exp
                woodData += kitAmount
                expData += kitExp
                dataUpdate = {
                    'Kits.Supporter':formatTime,
                    'Currencies.Wood':woodData,
                    'Profile.Experience':expData
                }

                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})              
                await level_up(ctx)

                await ctx.send(ctx.author.mention)
                embed = self.kitEmbed(ctx, kitAmount, kitExp)
                return await ctx.send(embed=embed)
            else:
                eembed = errorembed(description=f'{ctx.author.mention} You are currently on cooldown. Type ``.cd`` to check your cooldowns.')
                return await ctx.send(embed=eembed)
        except:
            # Use this format to update database
            formatTime = (datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')) + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
            jobAdvancementBonus = self.classDict[classData].index(jobData) + 1 if jobData != 'None' else 1
            kitAmount = amount*jobAdvancementBonus if classData else amount
            kitExp = exp*jobAdvancementBonus if classData else exp
            woodData += kitAmount
            expData += kitExp
            dataUpdate = {
                'Kits.Supporter':formatTime,
                'Currencies.Wood':woodData,
                'Profile.Experience':expData
            }
            update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})            
            await level_up(ctx)

            await ctx.send(ctx.author.mention)
            embed = self.kitEmbed(ctx, kitAmount, kitExp)
            return await ctx.send(embed=embed)
            
    @supporter.error
    async def supporter_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            supporterRole = discord.utils.get(ctx.message.guild.roles, name='Titan Donator').mention
            eembed = errorembed(description=f'{ctx.author.mention} Want to claim this **Supporter** kit? You have to minimally be a {supporterRole}')
            return await ctx.send(embed=eembed)

    @commands.command(aliases=['nt'])
    @has_registered()
    @is_economy_channel()
    @commands.has_any_role('Nitro Booster')
    async def nitro(self, ctx):
        amount = 250
        exp = 400     
        
        try:
            userData = self.records.find({'userID':str(ctx.author.id)})
            for x in userData:
                timeData = str(x['Kits']['Nitro'])
                woodData = float(x['Currencies']['Wood'])
                expData = float(x['Profile']['Experience'])
                jobData = str(x['RPG']['Job'])
                classData = str(x['RPG']['Class'])
                
            # Converts date from database to compare
            availableTime = datetime.datetime.strptime(timeData, '%Y-%m-%d %H:%M:%S.%f%z')

            # Current Time
            currentTime = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
            
            # Current Time in seconds
            if currentTime > availableTime:
                # Use this format to update database
                formatTime = (datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')) + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
                jobAdvancementBonus = self.classDict[classData].index(jobData) + 1 if jobData != 'None' else 1
                kitAmount = amount*jobAdvancementBonus if classData else amount
                kitExp = exp*jobAdvancementBonus if classData else exp
                woodData += kitAmount
                expData += kitExp
                dataUpdate = {
                    'Kits.Nitro':formatTime,
                    'Currencies.Wood':woodData,
                    'Profile.Experience':expData
                }

                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})              
                await level_up(ctx)

                await ctx.send(ctx.author.mention)
                embed = self.kitEmbed(ctx, kitAmount, kitExp)
                return await ctx.send(embed=embed)
            else:
                eembed = errorembed(description=f'{ctx.author.mention} You are currently on cooldown. Type ``.cd`` to check your cooldowns.')
                return await ctx.send(embed=eembed)
        except:
            # Use this format to update database
            formatTime = (datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')) + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
            jobAdvancementBonus = self.classDict[classData].index(jobData) + 1 if jobData != 'None' else 1
            kitAmount = amount*jobAdvancementBonus if classData else amount
            kitExp = exp*jobAdvancementBonus if classData else exp
            woodData += kitAmount
            expData += kitExp
            dataUpdate = {
                'Kits.Nitro':formatTime,
                'Currencies.Wood':woodData,
                'Profile.Experience':expData
            }
            update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})            
            await level_up(ctx)

            await ctx.send(ctx.author.mention)
            embed = self.kitEmbed(ctx, kitAmount, kitExp)
            return await ctx.send(embed=embed)
            
    @nitro.error
    async def nitro_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            nitroRole = discord.utils.get(ctx.message.guild.roles, name='Nitro Booster').mention
            eembed = errorembed(description=f'{ctx.author.mention} Want to claim this **Nitro** kit? You have to be a {nitroRole}')
            return await ctx.send(embed=eembed)            

    @commands.command(aliases=['v'])
    @has_registered()
    @is_economy_channel()
    async def vote(self, ctx, user:discord.User):
        if user == ctx.author:
            eembed = errorembed(description=f"{ctx.author.mention} You can't upvote yourself. Good try though! <:PepeHugs:541252355518365718>")
            return await ctx.send(embed=eembed)

        # Checks if User is inside Database
        try:
            userList = [x['userID'] for x in self.records.find({})]
            if str(ctx.author.id) not in userList:
                eembed = errorembed(description=f'{ctx.author.mention} You are currently not registered yet. Kindly type ``.register`` to be registered.')
                return await ctx.send(embed=eembed)
            elif str(user.id) not in userList:
                eembed = errorembed(description=f'{ctx.author.mention} {user.mention} has not registered yet.')
                return await ctx.send(embed=eembed)
        except:
            pass
        
        try:    
            userData = self.records.find({'userID':str(ctx.author.id)})
            for x in userData:
                voteData = str(x['Kits']['Votes'])
                
            # Converts date from database to compare
            availableTime = datetime.datetime.strptime(voteData, '%Y-%m-%d %H:%M:%S.%f%z')

            # Current Time
            currentTime = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))

            # Current Time in seconds
            if currentTime > availableTime:
                userData = self.records.find({'userID':str(user.id)})
                for x in userData:
                    repData = int(x['Profile']['Rep'])
                repData += 1 
                dataUpdate = {
                    'Profile.Rep':repData
                }
                update = self.records.update_one({'userID':str(user.id)}, {'$set':dataUpdate}) 

                # Use this format to update database
                formatTime = (datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')) + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
                dataUpdate = {
                    'Kits.Votes':formatTime
                }
                update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
                pembed = passembed(description=f'{ctx.author.mention} You have successfully added reputation for {user.mention}.')
                return await ctx.send(embed=pembed)
            else:
                eembed = errorembed(description=f'{ctx.author.mention} You are currently on cooldown. Type ``.cd`` to check your cooldowns.')
                return await ctx.send(embed=eembed)
        except Exception:
            userData = self.records.find({'userID':str(user.id)})
            for x in userData:
                repData = int(x['Profile']['Rep'])
            repData += 1 
            dataUpdate = {
                    'Profile.Rep':repData
                }
            update = self.records.update_one({'userID':str(user.id)}, {'$set':dataUpdate}) 

            # Use this format to update database
            formatTime = (datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')) + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S.%f%z')
            dataUpdate = {
                    'Kits.Votes':formatTime
                }
            update = self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
            pembed = passembed(description=f'{ctx.author.mention} You have successfully added reputation for {user.mention}.')
            return await ctx.send(embed=pembed)

    @vote.error
    async def vote_error(self, ctx, error):   
        if isinstance(error, commands.MissingRequiredArgument):
            eembed = errorembed(description='Kindly indicate the User that you wish to upvote.')
            return await ctx.send(embed=eembed)  

    @commands.command(aliases=['cd'])
    @has_registered()
    @is_economy_channel()
    async def cooldown(self, ctx):
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            dailyData = str(x['Kits']['Daily'])
            weeklyData = str(x['Kits']['Weekly'])
            supporterData = str(x['Kits']['Supporter'])
            nitroData = str(x['Kits']['Nitro'])
            voteData = str(x['Kits']['Votes'])
        
        # Daily Cooldown
        try:
            # Usable Time
            timeFormat = datetime.datetime.strptime(dailyData, '%Y-%m-%d %H:%M:%S.%f%z')
            timeInSeconds = time.mktime(timeFormat.timetuple())

            # Current Time
            timeNow = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
            timeNowInSeconds = time.mktime(timeNow.timetuple())
            
            # Before rounding off
            cooldownHours = ((timeInSeconds - timeNowInSeconds)/60)/60
            coolDownMins = float('.' + str(round(((timeInSeconds - timeNowInSeconds)/60)/60, 3)).split('.')[1])*60
            
            if int(cooldownHours) < 0:
                dailyCooldown = '• You have not claimed your **Daily** kit yet.'  
            
            else:
                # After rounding off
                coolDownMins = round(coolDownMins)
                coolDownHours = str(cooldownHours).split('.')[0]

                dailyCooldown = '• ' + str(coolDownHours) + 'H ' + str(coolDownMins) + 'M'
        except Exception:
            dailyCooldown = '• You have not claimed your **Daily** kit yet.'
        
        # Weekly Cooldown
        try:
            # Usable Time
            timeFormat = datetime.datetime.strptime(weeklyData, '%Y-%m-%d %H:%M:%S.%f%z')
            timeInSeconds = time.mktime(timeFormat.timetuple())

            # Current Time
            timeNow = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
            timeNowInSeconds = time.mktime(timeNow.timetuple())
            
            # Before rounding off
            coolDownHours = float('.' + str(round((((timeInSeconds - timeNowInSeconds)/60)/60)/24, 4)).split('.')[1])*24
            coolDownDays = (((timeInSeconds - timeNowInSeconds)/60)/60)/24
            
            if int(coolDownDays) < 0:
                weeklyCooldown = '• You have not claimed your **Weekly** kit yet.' 

            else:
                # After rounding off
                coolDownHours = round(coolDownHours)
                coolDownDays = str(coolDownDays).split('.')[0]     
                
                weeklyCooldown = '• ' + str(coolDownDays) + 'D ' + str(coolDownHours) + 'H'
        except Exception:
            weeklyCooldown = '• You have not claimed your **Weekly** kit yet.' 

        # Supporter Cooldown
        try:
            # Usable Time
            timeFormat = datetime.datetime.strptime(supporterData, '%Y-%m-%d %H:%M:%S.%f%z')
            timeInSeconds = time.mktime(timeFormat.timetuple())

            # Current Time
            timeNow = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
            timeNowInSeconds = time.mktime(timeNow.timetuple())
            
            # Before rounding off
            coolDownMins = float('.' + str(round(((timeInSeconds - timeNowInSeconds)/60)/60, 3)).split('.')[1])*60
            cooldownHours = ((timeInSeconds - timeNowInSeconds)/60)/60
            
            if int(cooldownHours) < 0:
                supporterCooldown = '• You have not claimed your **Supporter** kit yet.' 

            else:
                # After rounding off
                coolDownMins = round(coolDownMins)
                coolDownHours = str(cooldownHours).split('.')[0]

                supporterCooldown = '• ' + str(coolDownHours) + 'H ' + str(coolDownMins) + 'M'
        except Exception:
            supporterCooldown = '• You have not claimed your **Supporter** kit yet.'    

        # Nitro Cooldown
        try:
            # Usable Time
            timeFormat = datetime.datetime.strptime(nitroData, '%Y-%m-%d %H:%M:%S.%f%z')
            timeInSeconds = time.mktime(timeFormat.timetuple())

            # Current Time
            timeNow = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
            timeNowInSeconds = time.mktime(timeNow.timetuple())
            
            # Before rounding off
            coolDownMins = float('.' + str(round(((timeInSeconds - timeNowInSeconds)/60)/60, 3)).split('.')[1])*60
            cooldownHours = ((timeInSeconds - timeNowInSeconds)/60)/60
            
            if int(cooldownHours) < 0:
                nitroCooldown = '• You have not claimed your **Nitro** kit yet.' 

            else:
                # After rounding off
                coolDownMins = round(coolDownMins)
                coolDownHours = str(cooldownHours).split('.')[0]

                nitroCooldown = '• ' + str(coolDownHours) + 'H ' + str(coolDownMins) + 'M'
        except Exception:
            nitroCooldown = '• You have not claimed your **Nitro** kit yet.' 
        
        # Vote Cooldown
        try:
            # Usable Time
            timeFormat = datetime.datetime.strptime(voteData, '%Y-%m-%d %H:%M:%S.%f%z')
            timeInSeconds = time.mktime(timeFormat.timetuple())

            # Current Time
            timeNow = datetime.datetime.now(tz=pytz.timezone('Asia/Singapore'))
            timeNowInSeconds = time.mktime(timeNow.timetuple())
            
            # Before rounding off
            coolDownMins = float('.' + str(round(((timeInSeconds - timeNowInSeconds)/60)/60, 3)).split('.')[1])*60
            cooldownHours = ((timeInSeconds - timeNowInSeconds)/60)/60

            if int(cooldownHours) < 0:
                voteCooldown = '• You have not **voted** anyone today yet.'

            else:
                # After rounding off
                coolDownMins = round(coolDownMins)
                coolDownHours = str(cooldownHours).split('.')[0]

                voteCooldown = '• ' + str(coolDownHours) + 'H ' + str(coolDownMins) + 'M'
        except Exception:
            voteCooldown = '• You have not **voted** anyone today yet.'

        # Embed Cooldown Message
        embed = discord.Embed(title='Kit Cooldowns', color=discord.Color.from_hsv(random.random(), 1, 1), timestamp=datetime.datetime.now(tz=pytz.timezone('Asia/Singapore')))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name='⏰ Daily', value=dailyCooldown)
        embed.add_field(name='📅 Weekly', value=weeklyCooldown)
        embed.add_field(name='💎 Supporter', value=supporterCooldown)
        embed.add_field(name='⚡ Nitro', value=nitroCooldown)
        embed.add_field(name='🌟 Votes', value=voteCooldown)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)        

# Adding the cog to main script
def setup(bot):
    bot.add_cog(Kits(bot))