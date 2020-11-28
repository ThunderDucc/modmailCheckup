import praw
import discord
import datetime

reddit = praw.Reddit('')
subreddit = reddit.subreddit("")
colour = 0xcdcd22
lim = 1000
threadCap = 30

# this will store all conversations for redditors that were called
# redditor.name: (ModmailConversation[], index)
threadsByMod = dict()

# this function gets all conversations with a certain mod
# and will put them into the master threadsByMod dictionary
def getConversations(username):
    if username not in subreddit.moderator():
        # we don't want to check threads for them
        threadsByMod[username] = [[], -1]
        return False
    
    # now actually check them out
    mod = reddit.redditor(username)
    # load the last few recent modmail threads (based on the variable lim), starting from most recent
    conversations = subreddit.modmail.conversations(limit=lim, sort="recent", state="archived")

    # this loop gives a list of all threads with the mod 
    # and puts it in an array
    withMod = []
    threadCount = 0
    for c in conversations:
        # check if the mod sent a message in that thread, cap it at 30
        if mod in c.authors:
            threadCount = 0
            if len(withMod) < threadCap: 
                withMod.append(c)
            else:
                break
        else:
            threadCount += 1

        if threadCount >= lim/10:
            break
    # We keep track of which index we're on by using an array
    # index 0 of the array is the array of threads
    # index 2 is the index which we should send the message from
    # start from 0, the most recent
    threadsByMod[mod.name] = [withMod, 0]
    if len(withMod) <= 1: # they have no threads, return false to not draw arrows
        return False
    return True

def generateMessage(username, index):
    try:
        # check threadsByMod if they are actually a mod
        if threadsByMod[username][1] != -1:
            mod = reddit.redditor(username)
            # check if there are actually threads
            if len(threadsByMod[mod.name][0]) > 0:
                # Gets the thread from the index provided
                msg = ""
                thread = threadsByMod[mod.name][0][index]
                participant = thread.authors[0]
                # stores the most recent message from the mod provided
                for m in thread.messages:
                    if m.author == mod:
                        msg = m

                # generates the embed
                emb = discord.Embed(title="Modmail info for u/{}".format(mod.name), color=colour)
                emb.set_thumbnail(url=mod.icon_img)
                emb.description = "Most recent interaction from thread **{}** of **{}** on {}".format(index + 1, len(threadsByMod[mod.name][0]), thread.last_mod_update[:10])
                emb.add_field(name="Link", value="[{}](https://mod.reddit.com/mail/all/{})".format(thread.id, thread.id), inline=True)
                emb.add_field(name="Participant", value=participant.name, inline=True)
                emb.add_field(name="Subject", value=thread.subject, inline=True)
                emb.add_field(name="Message", value=msg.body_markdown[:1024], inline=False)
                emb.timestamp = datetime.datetime.utcnow()  
                emb.set_footer(text="Bot made by Canadapost Duck#3062")
                # returns it to be sent by the bot
                return emb
            else: # there are no threads
                emb = discord.Embed(title="Modmail info for u/{}".format(mod.name), color=colour)
                emb.set_thumbnail(url=mod.icon_img)
                emb.description = "This user has no modmail threads"
                emb.timestamp = datetime.datetime.utcnow()  
                emb.set_footer(text="Bot made by Canadapost Duck#3062")
                return emb
        else: # They are not a mod
                emb = discord.Embed(title="Modmail info for u/{}".format(username), color=colour)
                emb.description = "This user is not a mod on the sub. Perhaps check the spelling and capitalization of their username"
                emb.timestamp = datetime.datetime.utcnow()  
                emb.set_footer(text="Bot made by Canadapost Duck#3062")
                return emb
    except:
        emb = discord.Embed(title="Modmail info for u/{}".format(username), color=colour)
        emb.description = "There was an error processing this user. Perhaps check the spelling and capitalization of their username"
        emb.timestamp = datetime.datetime.utcnow()  
        emb.set_footer(text="Bot made by Canadapost Duck#3062")
        return emb

def next(username):
    # if we already calculated the threads, just need to go back one
    index = 0
    if username in threadsByMod:
        if threadsByMod[username][1] != -1: # -1 means they are not a valid mod
            index = threadsByMod[username][1]
            index += 1
            if index >= len(threadsByMod[username][0]):
                index = 0
            threadsByMod[username][1] = index
    else:
        # mod hasn't been called yet, generate their threads and keep index at 0
        getConversations(username)
    return generateMessage(username, index)

def back(username):
    # if we already calculated the threads, just move on to the next one
    index = 0
    if username in threadsByMod:
        if threadsByMod[username][1] != -1: # -1 means they are not a valid mod
            index = threadsByMod[username][1]
            index -= 1
            if index < 0:
                index = len(threadsByMod[username][0]) - 1
            threadsByMod[username][1] = index
    else:
        # mod hasn't been called yet, generate their threads and keep index at 0
        getConversations(username)
    return generateMessage(username, index)