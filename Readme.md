# modmailCheckup bot v1.2

## To setup
1. in main.py add the token of your bot on line 35
2. in functions.py add your reddit script account and subreddit name on lines 5 and 6
3. in functions.py, set lim to the amount of modmails to search through. On line 8 (default is 1000)

## functions.py info so I don't forget how it works
lim: int, number of previous modmails to search through

threadsByMod: dict( username: [[ModMailConversation], index] )
    
    Set to `none` when the user is not a mod

mods: dict( lowercasename: actualusername )

    this stores the actual username of the mod
    and can be accessed with the lowercase version
    this is so capitalization from discord doesn't matter

def getConversations(username: String) -> boolean:

    This searches the last lim modmail threads, and adds all featuring mod username into threadsByMod

def generateMessage(username: String, index: int) -> discord.Embed:

    based on the username and index, we get all info from the modmail thread in threadsByMod[username][index]
    the username is stored in the `author` field in the embed. Which can be accessed with msg.embeds[0].author.name

def cycle(username: String, direction: int) -> discord.Embed:

    Gets the next thread. 
    We get the threadsByMod entry for that username and add 1 to the assosiated index.
    Then call GenerateMessage to get the embed

    DIRECTION: 1 to go up, -1 to go down

### V1.1 

    - cleaned up next/back functions into the cycle function
    - removed several if statements in favour of try/except in generateMessage()
    - removed return from getConversations() (was not needed)
    - other small code fixes

### V1.2

    - emojis don't appear on messages they shouldn't be on
    - capitalization of the username now does not matter

### V1.3 TBD

    - !!speed up getting the threads!!

