<div align="center">
  <img src="https://i.ibb.co/Yy8TNdm/ezgif-com-gif-maker-2.gif" />
  
  <br />

  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Made%20With-Python%203.7-blue.svg?style=for-the-badge&logo=Python" alt="Made with Python 3.6">
  </a>
</div>

## What is Horizon?
Horizon is a multipurpose discord bot that was first created in Feb 2019 to serve the needs of FortniteAsia discord server.

## Features
* In-built google translation for international players to converse in their native language
* Fully developed RPG game system
  * Classes (_developed based on Fortnite PvE characters_)
  * Dungeons (_mob hunting, sending character on a mission_)
  * Leaderboards
  * Game kits (_daily, weekly, supporter_)
  * Profiles
  * Games (_coin flip, lottery, slots, dice, rock paper scissors_)
  * Shop (_in-game items which are able to enhance users' stats_)
  * Events (_lottery events which users are able to purchase tickets_)
  * Passive income (_users are able to earn currency based on amount of time they spend in the server's voice channel_)
* Teams (_users are able to create solo/duo/squad teams for scrims_)
* Moderation utilities to manage the server (_purge, ban, mute, announcements etc._)
* Discord reaction listener (_tracks for user's reactions to add/remove roles_)
* FortniteAPI rank system (_award users server roles based on their Fortnite K/D_)
* Fortnite scrims system (_users are able to create/participate in scrims_)
* Tournament (_users are able to place bets to determine the winner in a Fortnite 1v1 showdown_)
* Chat logging functionality (_channels are created to log user actions/messages_)

## Commands
* **General**
  * `.time` - Displays local time of Horizon.
  * `.setnick` - Change your nickname displayed in server once.
  * `.userinfo <user>` -_Displays information of User.
  * `.serverinfo` - Displays information of server.
  * `.giveaway <role>` - Starts a giveaway for Discord role.
  * `.rollgiveaway <messageID> <#ofWinners>` - Manually rolls the winner of giveaway.

* **Moderation** (_Users must have @Server Moderator role to access these commands._)
  * `.ban <user> <reason>` - Permanently ban an user.
  * `.forceban <userID> <reason>` - Permanently ban an user outside of server.
  * `.unban <userID>` - Unban an user in server.
  * `.mute <user> <reason> <time>` - Mutes an user for specified period of time.
  * `.unmute <user> <reason>` - Unmutes an user.
  * `.userinfo <user>` - Displays information of an user.
  * `.grant <user>` - Grant access to an user to change nickname again.
  * `.announce <channel> <message>` - Announce a message in specified text channel.
  * `.emannounce <channel> <message>` - Announce an embedded message in specified text channel.
  * `.purge <amount>` - Purge messages in text channel. If amount is not specified, it will be defaulted as 100 messages.
  * `.lock <channel>` - Locks a specified text channel.
  * `.unlock <channel>` - Unlocks a specified text channel.
  
* **Team**
  * `.create solo` - Creates a solo team.
  * `.create duo <teamName> <teamMate>` - Creates a duo team.
  * `.create squad <teamName> <teamMate#1> <teamMate#2> <teamMate#3>` - Creates a squad team.
  * `.disband <mode>` - Disbands a team accordingly to the mode selected. **(Captains only)**
  * `.leave <mode>` - Leave a team accordingly to the mode selected. **(Members only)**

* **Leaderboard**
  * `.submit <mode> <kills> <placement> <gamecode>` - Submits the result of the match. Screenshot must be attached for verification purposes.
  * `.invite <mode> <teamMate>` - Invites a user to the team.
  * `.stats <mode>` - Display user's statistics accordingly to the mode selected.
  * `.leaderboard <mode>` - Display server's overall ranking according to the mode selected. @Points Manager is required to access this command.

  _Awarding of Point(s) - To accept/reject the submissions, moderators must have @Points Manager role in order to react :white_check_mark: or :x: on the submission accordingly._
  
* **Scrims** (_Users must have @Host to access these scrim commands._)
  * `.start solo` - Selects solo gamemode.
  * `.start duo` - Selects duo gamemode.
  * `.start squad` - Selects squad gamemode.

* **RPG Game**
  * **Kits**
    * `.daily` - Claims your daily currency kit
    * `.weekly` - Claims your weekly currency kit
    * `.supporter` - Claims your supporter currency kit
    * `.nitro` - Claims your nitro currency kit
  * **Information**
    * `.top` - Displays global leaderboard
    * `.profile` - Displays information of your profile
    * `.inventory` - Displays gun inventory
    * `.cooldown` - Checks the status of currency kits'
  * **Shop**
    * `.shop` - Displays item that are available for purchase
    * `.buy <ID> <amount>` - Purchase an item from the shop
  * **Events**
    * `.lottery <amount>` - Starts a lottery for the community that lasts for 3 minutes
    * `.participate <amount>` - Purchase a ticket in Llama Pinata event
    * `.chances` - Chance to win the Llama Pinata event
  * **Tournament**
    * `.bet <user>` - Bets 1,000 currency on the desired player in the tournament
  * **Classes/Dungeons**
    * `.tree` - Displays available classes
    * `.choose <jobName>` - Selects a class for RPG
    * `.evolve` - Advances to the next job in the class tree
    * `.dungeon <dungeonID>` - Starts an adventure in dungeon
    * `.dungeons` - Display available dungeons
    * `.status` - Checks the status of adventure
    * `.hunt` - Hunt monsters in the current dungeon
  * **Misc**
    * `.consume <potion>` - Increases HP by consuming health/shield potion
    * `.equip <weaponID>` - Equips a specific weapon
    * `.dump <weaponID>` - Dumps a specific weapon
    * `.vote <user>` - Upvotes an User
    * `.claim <type>` - Opens a crate/gift using a key
    * `.transfer <user> <amount>` - Transfers an amount to specified User

## Installation
Unfortunately, this discord bot is no longer maintained and developed. Any breaking changes/errors will not be fixed.
Nonetheless, you're able to host Horizon locally by setting up the necessary configs in .env file.

| Requirements             | Reference                                                        |
:------------------------- | :--------------------------------------------------------------: |
| Python                   | [Installation](https://www.python.org/)                          |
| Google Sheets API        | [Documentation](https://developers.google.com/sheets/api)        |
| MongoDB                  | [Documentation](https://docs.atlas.mongodb.com/)                 |
| Discord Bot Token        | [Documentation](https://discord.com/developers/docs/intro)       |
| Fortnite API Key         | [Documentation](https://fortnitetracker.com/site-api)            |
| FFmpeg                   | [Installation](https://www.ffmpeg.org/download.html)             |

Clone the repo:
```console
$ git clone https://github.com/jeraldlyh/Horizon
$ cd Horizon
```

Install dependencies:
```console
$ pip3 install -r requirements.txt
```
