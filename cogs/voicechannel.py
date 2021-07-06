import asyncio
import pymongo
import os

from discord.ext import commands

class VoiceChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = pymongo.MongoClient(os.getenv("MONGO_DB"))
        self.db = self.client.get_database('Users')
        self.records = self.db.horizon_database
        self.bg_task = bot.loop.create_task(self.voicechat_task())
        self.wood = 25
        self.exp = 10
   
    async def voicechat_task(self):
        await self.bot.wait_until_ready()
        try:
            while not self.bot.is_closed():
                await self.vc_interval()
                await asyncio.sleep(300)
        except Exception as e:
            print(e)

    async def vc_interval(self):
        guild = self.bot.get_guild(os.getenv("SERVER_ID"))
        for vc in guild.voice_channels:
            for member in vc.members:
                try:
                    userData = self.records.find({'userID':str(member.id)})
                    for x in userData:
                        woodData = float(x['Currencies']['Wood'])
                        expData = float(x['Profile']['Experience'])
                    woodData += self.wood
                    expData += self.exp
                    dataUpdate = {
                            'Currencies.Wood':woodData,
                            'Profile.Experience':expData
                        }
                    self.records.update_one({'userID':str(member.id)}, {'$set':dataUpdate}) 
                    await asyncio.sleep(2)
                except:
                    continue   
    
    
       
    
# Adding the cog to main script
def setup(bot):
    bot.add_cog(VoiceChannel(bot))    