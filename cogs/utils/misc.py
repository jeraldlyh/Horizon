import pymongo
import random
import numpy
import os

from cogs.utils.embed import (passembed, errorembed)

client = pymongo.MongoClient(os.getenv("MONGO_DB"))
db = client.get_database('Users')
records = db.horizon_database

rarityDict = {
    'Common':'<:Common:587174581052375050>',
    'Uncommon':'<:Uncommon:587174580498464794>',
    'Rare':'<:Rare:587174580385349632>',
    'Epic':'<:Epic:587174580498726942>',
    'Legendary':'<:Legendary:587174580452327454>'
}

weaponDict = {
    'Assault_Rifle':{
        'Common':['Assault Rifle (AR)','Semi-Auto Rifle (AR)'],
        'Uncommon':['Specter (AR)'],
        'Rare':['Slug (AR)'],
        'Epic':['Dragon (AR)', 'Raygun (AR)','Vindertech (AR)'],
        'Legendary':['Gravedigger (AR)','Bundlebuss (AR)','Mercury (AR)','Razorblade (AR)','Tiger (AR)']
    },
    'Shotgun':{
        'Common':['Semi-Auto (SG)', 'Pump (SG)'],
        'Uncommon':['Templar (SG)'],
        'Rare':['Double Barrel (SG)'],
        'Epic':['Helium (SG)', 'Enforcer (SG)', 'Dragoon (SG)'],
        'Legendary':['Roomsweeper (SG)','Tigerjaw (SG)','Thunderbolt (SG)','Nightclaw (SG)']
    },
    'Sniper':{
        'Common':['Hunting Rifle (S)', 'Automatic Sniper (S)'],
        'Uncommon':['One Shot (S)'],
        'Rare':['Laser Rifle (S)'],
        'Epic':['Tsunami (S)', 'Crankshot (S)', 'Dragon (S)'],
        'Legendary':['Dragonfly (S)','Neon (S)']
    }    
    
}

weaponEmojiDict = {
    'Assault Rifle (AR)':['<:Assault_Rifle:586922233428180993>', 'https://cdn.discordapp.com/attachments/586921758347624544/586921809778049035/Assault_Rifle.png'],
    'Semi-Auto Rifle (AR)':['<:Semi_Auto:586922234866696195>', 'https://cdn.discordapp.com/attachments/586921758347624544/586921818041090050/Semi_Auto.png'],
    'Specter (AR)':['<:Specter:586922233331712021>', 'https://cdn.discordapp.com/attachments/586921758347624544/586921819274215436/Specter.png'],
    'Slug (AR)':['<:Slug:586942333354770437>', 'https://cdn.discordapp.com/attachments/586921758347624544/586942275687284773/Slug.png'],
    'Dragon (AR)':['<:Dragon:586922234766032917>', 'https://cdn.discordapp.com/attachments/586921758347624544/586921813016313886/Dragon.png'],
    'Raygun (AR)':['<:Raygun:586922233692422154>', 'https://cdn.discordapp.com/attachments/586921758347624544/586921816581472272/Raygun.png'],
    'Vindertech (AR)':['<:Vindertech:586922234942324786>', 'https://cdn.discordapp.com/attachments/586921758347624544/586921866166403091/Vindertech.png'],
    'Gravedigger (AR)':['<:Gravedigger:586922234677821440>', 'https://cdn.discordapp.com/attachments/586921758347624544/586921813213446165/Gravedigger.png'], 
    'Bundlebuss (AR)':['<:Bundlebuss:586922234711375903>', 'https://cdn.discordapp.com/attachments/586921758347624544/586921809732042841/Bundlebuss.png'],
    'Mercury (AR)':['<:Mercury:586922234803650591>', 'https://cdn.discordapp.com/attachments/586921758347624544/586921815394353163/Mercury.png'],
    'Razorblade (AR)':['<:Razorblade:586922235093319692>', 'https://cdn.discordapp.com/attachments/586921758347624544/586921817856409619/Razorblade.png'],
    'Tiger (AR)':['<:Tiger:586922235130937364>', 'https://cdn.discordapp.com/attachments/586921758347624544/586921822189256715/Tiger.png'],
    'Semi-Auto (SG)':['<:Semi_Auto:586923976991965184>', 'https://cdn.discordapp.com/attachments/586923891469844496/586923931596881924/Semi_Auto.png'],
    'Pump (SG)':['<:Pump_Shotgun:586923976400306176>', 'https://cdn.discordapp.com/attachments/586923891469844496/586923929017384973/Pump_Shotgun.png'],
    'Templar (SG)':['<:Templar:586923975276363786>', 'https://cdn.discordapp.com/attachments/586923891469844496/586923934142824454/Templar.png'],
    'Double Barrel (SG)':['<:Double_Barrel:586943621849415681>', 'https://cdn.discordapp.com/attachments/586923891469844496/586943604430209043/Double_Barrel.png'],
    'Helium (SG)':['<:Helium:586923975951515649>', 'https://cdn.discordapp.com/attachments/586923891469844496/586923927847174148/Helium.png'],
    'Enforcer (SG)':['<:Enforcer:586923976467546122>', 'https://cdn.discordapp.com/attachments/586923891469844496/586923926534357042/Enforcer.png'],
    'Dragoon (SG)':['<:Dragoon:586923975687274507>','https://cdn.discordapp.com/attachments/586923891469844496/586923924894384130/Dragoon.png'],
    'Roomsweeper (SG)':['<:Roomsweeper:586923974441697300>', 'https://cdn.discordapp.com/attachments/586923891469844496/586923931554807814/Roomsweeper.png'],
    'Tigerjaw (SG)':['<:Tigerjaw:586923976643837962>', 'https://cdn.discordapp.com/attachments/586923891469844496/586923937850589247/Tigerjaw.png'],
    'Thunderbolt (SG)':['<:Thunderbolt:586923975343472651>', 'https://cdn.discordapp.com/attachments/586923891469844496/586923934759518232/Thunderbolt.png'],
    'Nightclaw (SG)':['<:Nightclaw:586923976182464512>', 'https://cdn.discordapp.com/attachments/586923891469844496/586923929113853952/Nightclaw.png'],
    'Hunting Rifle (S)':['<:Hunting_Rifle:586925174117629984>', 'https://cdn.discordapp.com/attachments/586925107537248274/586925139313164289/Hunting_Rifle.png'],
    'Automatic Sniper (S)':['<:Automatic_Sniper:586925175144972308>', 'https://cdn.discordapp.com/attachments/586925107537248274/586925134791573536/Automatic_Sniper.png'],
    'One Shot (S)':['<:One_Shot:586925174633398355>', 'https://cdn.discordapp.com/attachments/586925107537248274/586925143092101150/One_Shot.png'],
    'Laser Rifle (S)':['<:Laser_Rifle:586925175350755378>', 'https://cdn.discordapp.com/attachments/586925107537248274/586925140047036426/Laser_Rifle.png'],
    'Tsunami (S)':['<:Tsunami:586925174847438870>', 'https://cdn.discordapp.com/attachments/586925107537248274/586925144455380994/Tsunami.png'],
    'Crankshot (S)':['<:Crankshot:586925176533418004>', 'https://cdn.discordapp.com/attachments/586925107537248274/586925136830005268/Crankshot.png'],
    'Dragon (S)':['<:Dragon:586925174855827457>', 'https://cdn.discordapp.com/attachments/586925107537248274/586925136721215488/Dragon.png'],
    'Dragonfly (S)':['<:Dragonfly:586925174406774794>', 'https://cdn.discordapp.com/attachments/586925107537248274/586925137396498455/Dragonfly.png'],
    'Neon (S)':['<:Neon:586925175191371776>', 'https://cdn.discordapp.com/attachments/586925107537248274/586925142375137320/Neon.png']
}

async def level_up(ctx):
    userData = records.find({'userID':str(ctx.author.id)})
    for x in userData:
        levelData = int(x['Profile']['Level'])
        expData = float(x['Profile']['Experience'])
        hpData = int(x['RPG']['HP'])
        maxHPData = int(x['RPG']['maxHP'])
        attackData = round(float(x['RPG']['Attack']))
        defenceData = round(float(x['RPG']['Defence']))

    startLevel = levelData
    endLevel = int(expData ** (1/4))

    if startLevel < endLevel:
        amount = endLevel - startLevel
        hpData += 5*amount
        maxHPData += 5*amount
        attackData += 0.75*amount
        defenceData += 0.25*amount
        dataUpdate = {
            'Profile.Level':endLevel,
            'RPG.HP':hpData,
            'RPG.maxHP':maxHPData,
            'RPG.Attack':attackData,
            'RPG.Defence':defenceData
        }
        records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})   
        await ctx.send(f'{ctx.author.mention} has leveled up to **{endLevel}**.')

def calculateDmg(weapon, rarity):
    if str(rarity) == 'Common':
        rarityDmg = 1
    if str(rarity) == 'Uncommon':
        rarityDmg = 2
    if str(rarity) == 'Rare':
        rarityDmg = 3
    if str(rarity) == 'Epic':
        rarityDmg = 4
    if str(rarity) == 'Legendary':
        rarityDmg = 5

    # Consistent Spread
    if '(AR)' in str(weapon):
        minDmg = 1 + rarityDmg
        maxDmg = 1 + rarityDmg

    # High Spread
    if '(SG)' in str(weapon):
        minDmg = 2
        maxDmg = random.randint(1 + rarityDmg , 5 + rarityDmg)

    # Low Spread but High Damage
    if '(S)' in str(weapon):
        minDmg = 1 + rarityDmg
        maxDmg = random.randint(1 + rarityDmg , 3 + rarityDmg)

    return minDmg, maxDmg

def generateWeaponID():
    with open('cogs/utils/weaponID.txt', 'r+') as f:
        uniqueIDList = [x.rstrip('\n') for x in f.readlines()]
        uniqueID = random.choice(uniqueIDList)
        uniqueIDList.remove(str(uniqueID))
        f.seek(0)
        f.truncate()
        for x in uniqueIDList:
            f.write(x+'\n')
        f.close()
        return uniqueID

def generateWeapon(ctx):
    weaponTypeList = list(weaponDict.keys())
    weaponType = random.choice(weaponTypeList)
    weaponRarityList = list(weaponDict[weaponType])
    probability = ['0.35', '0.3', '0.2', '0.1', '0.05']
    rarityResult = numpy.random.choice(weaponRarityList, 1, p=probability)
    rarityName = list(rarityResult)[0]
    rarityEmoji = rarityDict[str(rarityName)]
    weaponList = weaponDict[weaponType][list(rarityResult)[0]]
    weaponName = random.choice(weaponList)
    
    userData = records.find({'userID':str(ctx.author.id)})
    for x in userData:
        weaponData = x['Weapons']
    weaponEmoji = weaponEmojiDict[str(weaponName)][0]
    weaponPicture = weaponEmojiDict[str(weaponName)][1]
    weaponDamage = calculateDmg(weaponName, rarityName)

    uniqueID = generateWeaponID()
    weaponData.update({
                uniqueID:[str(weaponName), weaponDamage[0], weaponDamage[1], weaponEmoji, weaponPicture, rarityName, rarityEmoji]
            })
    dataUpdate = {
        f'Weapons':weaponData
    }

    update = records.update_one({'userID':str(ctx.author.id)}, {'$set':dataUpdate})
    
    return uniqueID, weaponName, weaponEmoji, rarityName, rarityEmoji


def retrieveUserData(ctx, author):
    userData = records.find({'userID':str(author)})
    for x in userData:
        # Currency Data
        woodData = float(x['Currencies']['Wood'])
        stoneData = int(x['Currencies']['Stone'])
        metalData = int(x['Currencies']['Metal'])
        # Kits Data
        dailyData = str(x['Kits']['Daily'])
        weeklyData = str(x['Kits']['Weekly'])
        supporterData = str(x['Kits']['Supporter'])
        voteData = str(x['Kits']['Votes'])
        # Profile Data
        repData = int(x['Profile']['Rep'])
        dataJoinedData = str(x['dateJoined'])
        levelData = int(x['Profile']['Level'])
        expData = float(x['Profile']['Experience'])
        winData = int(x['Profile']['Wins'])
        gamesPlayedData = int(x['Profile']['gamesPlayed'])
        # Shop Data
        pinataData = float(x['Items']['pinataSlot'])
        giftData = int(x['Items']['Gifts'])
        crateData = int(x['Items']['Crates'])
        keyData = int(x['Items']['Keys'])
        # Battle Data
        classData = str(x['RPG']['Class'])
        jobData = str(x['RPG']['Job'])
        hpData = float(x['RPG']['HP'])
        maxHPData = float(x['RPG']['maxHP'])
        attackData = float(x['RPG']['Attack'])
        defenceData = float(x['RPG']['Defence'])
        dungeonData = str(x['RPG']['Dungeon'])
        hpPotionData = int(x['Items']['hpPotion'])
        shieldPotionData = int(x['Items']['shieldPotion'])
        dungeonTimeData = str(x['RPG']['dungeonTime'])
        return woodData, stoneData, metalData, dailyData, weeklyData, supporterData, voteData, repData, dataJoinedData, levelData, expData, winData, gamesPlayedData, pinataData, giftData, crateData, keyData, classData, jobData, hpData, maxHPData, attackData, defenceData, dungeonData, hpPotionData, shieldPotionData, dungeonTimeData

# Exp bar for .profile command
def print_nextLvl(expNeeded):
    if 0.00 <= expNeeded <= 0.05:
        return '[■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
    elif 0.06 <= expNeeded <= 0.10:
        return '[■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
    elif 0.11 <= expNeeded <= 0.15:
        return '[■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
    elif 0.16 <= expNeeded <= 0.20:
        return '[■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
    elif 0.21 <= expNeeded <= 0.25:
        return '[■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
    elif 0.26 <= expNeeded <= 0.30:
        return '[■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
    elif 0.31 <= expNeeded <= 0.35:
        return '[■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'
    elif 0.36 <= expNeeded <= 0.40:
        return '[■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□]'
    elif 0.41 <= expNeeded <= 0.45:
        return '[■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□]'
    elif 0.46 <= expNeeded <= 0.50:
        return '[■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□]'
    elif 0.51 <= expNeeded <= 0.55:
        return '[■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□]'
    elif 0.56 <= expNeeded <= 0.60:
        return '[■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□]'
    elif 0.61 <= expNeeded <= 0.65:
        return '[■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□]'
    elif 0.66 <= expNeeded <= 0.70:
        return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□]'
    elif 0.71 <= expNeeded <= 0.75:
        return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□]'
    elif 0.76 <= expNeeded <= 0.80:
        return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□]'
    elif 0.81 <= expNeeded <= 0.85:
        return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□]'
    elif 0.86 <= expNeeded <= 0.90:
        return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□]'
    elif 0.91 <= expNeeded <= 0.95:
        return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□]'
    elif 0.96 <= expNeeded <= 1.00:
        return '[■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□]'
    else:
        return '[□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]'        