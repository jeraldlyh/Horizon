import pymongo
import discord
import os

from discord.ext import commands
from cogs.utils.checks import has_registered, is_economy_channel
from cogs.utils.embed import (passembed, errorembed)

class Classes(commands.Cog):
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
        self.perksDict = {
        'Soldier':['Advanced Tactics'],
        'Constructor':['Creative Engineering'],
        'Ninja':['Shinobi'],
        'Outlander':['Forced Acquisition']
        }
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
    @has_registered()
    @is_economy_channel()
    async def tree(self, ctx):
        await ctx.send('''```
Tree    | Soldier        | Constructor  | Ninja           | Outlander
--------|----------------|--------------|-----------------|-------------
Lvl 1   | Sash Sergeant  | BASE         | Assassin        | Pathfinder
Lvl 30  | Shock Trooper  | Heavy BASE   | Deadly Blade    | Reclaimer
Lvl 70  | Commando       | MEGABASE     | Energy Thief    | Recon Scout
Lvl 100 | Special Forces | Riot Control | Harvester       | T.E.D.D Shot 
Lvl 120 | Bullet Storm   | Warden       | Shuriken Master | Trailblazer
```''')
        embed = discord.Embed(title='Job Hidden Perks', description='Above shown are the classes available with hidden perks as following')
        embed.add_field(name='Soldier', value='**Advanced Tactics** - Gains extra 3 attack damage')
        embed.add_field(name='Constructor', value='**Creative Engineering** - Reduces building cost by 5%')
        embed.add_field(name='Ninja', value='**Shinobi** - Reduce 5% time taken for dungeons')
        embed.add_field(name='Outlander', value='**Forced Acquisition** - Increase dungeon loots by 15%')
        embed.set_footer(text='• Note that choosing of jobs is case-sensitive. Eg. `.choose Ninja` ')
        await ctx.send(embed=embed)
            
    
        
    @commands.command()
    @has_registered()
    @is_economy_channel()
    async def choose(self, ctx, JobName):

        if str(JobName) not in self.classDict:
            eembed = errorembed(description=f'{ctx.author.mention} There are currently **4** classes available. Refer to ``.tree``')
            return await ctx.send(embed=eembed)
        
        userData = self.records.find({'userID':str(ctx.author.id)})
        for x in userData:
            levelData = int(x['Profile']['Level'])
            classData = str(x['RPG']['Class'])
        
        # Checks if User already has a class
        if classData != 'None':
            eembed = errorembed(description=f'{ctx.author.mention} You have already selected a class - **{classData}**.')
            return await ctx.send(embed=eembed)

        jobName = str(self.classDict[JobName][0])
        hpStats = self.jobDict[jobName][2]*levelData
        attackStats = self.jobDict[jobName][3] + levelData*1
        defenceStats = self.jobDict[jobName][4] + levelData*0.75
        dataUpdate = {
            'RPG.Class':str(JobName).capitalize(),
            'RPG.Job':jobName,
            'RPG.maxHP':hpStats,
            'RPG.Attack':attackStats,
            'RPG.Defence':defenceStats,
            'RPG.HP':hpStats,      
        }
        self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 
        pembed = passembed(description=f"{ctx.author.mention} You have successfully selected **{JobName}** as your class. You're now officially a **{jobName}**!")
        return await ctx.send(embed=pembed)       

    @commands.command()
    @has_registered()
    @is_economy_channel()
    async def evolve(self, ctx):
        userData = self.records.find({'userID':f'{str(ctx.author.id)}'})
        for x in userData:
            levelData = int(x['Profile']['Level'])
            classData = str(x['RPG']['Class'])
            jobData = str(x['RPG']['Job'])

        if levelData < self.jobDict[jobData][1]:
            eembed = errorembed(description=f'{ctx.author.mention} You have not reached the required level to advance to the next job. Keep up the grind.')
            return await ctx.send(embed=eembed)
        elif levelData >= self.jobDict[jobData][1]:
            nextJobIndex = self.classDict[classData].index(jobData) + 1
            nextJob = self.classDict[classData][nextJobIndex]

            dataUpdate = {
                'RPG.Job':str(nextJob)
            }
            self.records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate}) 

            pembed = passembed(description=f'{ctx.author.mention} Congratulations, you have just advanced to **{nextJob}**!')
            return await ctx.send(embed=pembed)

# Adding the cog to main script
def setup(bot):
    bot.add_cog(Classes(bot))
