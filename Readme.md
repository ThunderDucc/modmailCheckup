# modmailCheckup bot

## To setup
1. in main.py add the token of your bot on line 35
2. in functions.py add your reddit script account and subreddit name on lines 5 and 6
3. in functions.py, set lim to the amount of modmails to search through. On line 8

## functions.py info so I don't forget how it works
lim: int, number of previous modmails to search through

threadsByMod: dict( username: [[ModMailConversation], index] )
    
    index is -1 when the user is not a mod

def getConversations(username: String) -> boolean:

    This searches the last lim modmail threads, and adds all featuring mod username into threadsByMod
    return is OPTIONAL: returns if the user exists, is modded, and has more than 1 thread.

def generateMessage(username: String, index: int) -> discord.Embed:

    based on the username and index, we get all info from the modmail thread in threadsByMod[username][index]

def next(username: String) -> discord.Embed:

    Gets the next thread. 
    We get the threadsByMod entry for that username and add 1 to the assosiated index.
    Then call GenerateMessage to get the embed

def back(username: String) -> discord.Embed:

    Same as next but subtract 1