import discord

from discord.ext import commands
from googletrans import Translator

class Translation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dictionary = {
                'ar': 'Arabic (Iraq)',
                'bn': 'Bengali (Bangladesh)',
                'zh-CN': 'Chinese (Simplified)',
                'zh-TW': 'Chinese (Traditional)',
                'en': 'English',
                'tl': 'Filipino (Philippines)',
                'hi': 'Hindi (India)',
                'id': 'Indonesian (Indonesia)',
                'jw': 'Javanese (Indonesia)',
                'ja': 'Japanese (Japan)',
                'km': 'Khmer (Cambodia)',
                'ko': 'Korean (Korea)',
                'lo': 'Lao (Laos)',
                'ms': 'Malay (Malaysia)',
                'my': 'Burmese (Myanmar)',
                'ne': 'Nepali (Nepal)',
                'ps': 'Pashto (Afghanistan)',
                'fa': 'Persian (Iran)',
                'ru': 'Russian (Russia)',
                'ta': 'Tamil (India)',
                'th': 'Thai (Thailand)',
                'ur': 'Urdu (Pakistan)',
                'vi': 'Vietnamese (Vietnam)'                
        }


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.channel.name == 'international-chat':
            translator = Translator()
            # await message.delete()
            # detected_language = translator.detect(msg).lang
            # embed = discord.Embed(color=0xff9b72)
            # embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            # embed.add_field(name=f'Language - {self.dictionary[detected_language]}', value=msg, inline=False)
            # embed.add_field(name='Translation - English', value=translator.translate(msg, dest='en').text)
            # embed.add_field(name='Translation - Korean', value=translator.translate(msg, dest='ko').text)
            # embed.add_field(name='Translation - Japanese', value=translator.translate(msg, dest='ja').text)
            # embed.add_field(name='Translation - Chinese', value=translator.translate(msg, dest='zh-cn').text)
            # embed.add_field(name='Translation - Thai', value=translator.translate(msg, dest='th').text)
            # embed.add_field(name='Translation - Filipino', value=translator.translate(msg, dest='fil').text)
            # embed.set_footer(text='Translated by Google', icon_url='https://cdn.discordapp.com/attachments/495521657566527489/581707996518940672/Google.png')
            # await message.channel.send(embed=embed)

            for i in self.dictionary.keys():
                if message.content.startswith(f"!{i}"):
                    try:
                        msg = message.content.replace("!" + i, "")
                        detected_language = translator.detect(msg).lang
                        embed = discord.Embed(color=0xff9b72)
                        embed.add_field(name=f'Language - {self.dictionary[detected_language]}', value=msg, inline=False)
                        embed.add_field(name=f'Translation - {self.dictionary[i]}', value=translator.translate(msg, dest=i).text, inline=True)
                        embed.set_footer(text='Translated by Google', icon_url='https://cdn.discordapp.com/attachments/495521657566527489/581707996518940672/Google.png')
                        await message.channel.send(embed=embed)
                    except:
                        pass
                
        if message.content.startswith("!language"):
            embed = discord.Embed(color=0xff9b72)
            embed.add_field(name='Prefix', value='\n'.join(self.dictionary.keys()))
            embed.add_field(name='Language', value='\n'.join(self.dictionary.values()))
            await message.channel.send(embed=embed)
            
def setup(bot):
    bot.add_cog(Translation(bot))                       