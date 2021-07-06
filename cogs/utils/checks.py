import discord
import pymongo
import os

from discord.ext import commands

class EconomyChannel(commands.CheckFailure):
    '''Exception raised when it's not the correct channel.'''
    pass

class NoDonator(commands.CheckFailure):
    '''Exception raised when User does not have @Donator role.'''
    pass

class NotRegistered(commands.CheckFailure):
    '''Exception raised when User has not register yet'''
    pass
    
def is_economy_channel():
    def predicate(ctx):
        if ctx.channel.name in ['pleasant-park', 'tilted-towers','loot-lake']:
            return True
        raise EconomyChannel  
    return commands.check(predicate)

def is_donator():
    def predicate(ctx):
        for x in ctx.author.roles:
            if x.name in ['Titan Donator', 'Mystic Donator', 'Immortal Donator']:
                return True
        raise NoDonator
    return commands.check(predicate)

def has_registered():
    def predicate(ctx):
        client = pymongo.MongoClient(os.getenv("MONGO_DB"))
        db = client.get_database('Users')
        records = db.horizon_database
        userList = [x['userID'] for x in records.find({})]
        if str(ctx.author.id) in userList:
            return True
        raise NotRegistered
    return commands.check(predicate)
