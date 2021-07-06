import discord


def passembed(description=''):
    pembed = discord.Embed(title='✅ Command Processed')
    pembed.description = description
    pembed.color = discord.Colour.green()
    return pembed
    
def errorembed(description=''):
    eembed = discord.Embed(title='❌ Command Error')
    eembed.description = description
    eembed.color = discord.Colour.red()
    return eembed
    
def pointspro(description=''):
    poembed = discord.Embed(title='✅ Points Processed')
    poembed.description = description
    poembed.color = discord.Colour.green()
    return poembed    
    
def pointsrej(description=''):
    rejembed = discord.Embed(title='❌ Points Rejected')
    rejembed.description = description
    rejembed.color = discord.Colour.red()
    return rejembed        
