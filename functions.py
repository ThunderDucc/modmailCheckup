import praw
import discord
import datetime

reddit = praw.Reddit('')
subreddit = reddit.subreddit("")
colour = 0xcdcd22
lim = 10

# this will store all conversations for redditors that were called
# redditor.name: (ModmailConversation[], index)
threadsByMod = dict()

# this function gets all conversations with a certain mod
# and will put them into the master threadsByMod dictionary
def getConversations(username):
    mod = reddit.redditor(username)

    # load the last few recent modmail threads (based on the variable lim), starting from most recent
    conversations = subreddit.modmail.conversations(limit=lim, sort="recent")

    # this loop gives a list of all threads with the mod 
    # and puts it in an array
    withMod = []
    for c in conversations:
        if mod in c.authors: 
            withMod.append(c)
    
    # We keep track of which index we're on by using an array
    # index 0 of the array is the array of threads
    # index 2 is the index which we should send the message from
    # start from 0, the most recent
    threadsByMod[mod.name] = [withMod, 0]

def generateMessage(username, index):
    mod = reddit.redditor(username)

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
    emb.description = "Most recent interaction from thread **{}** of **{}**".format(index + 1, len(threadsByMod[mod.name][0]))
    emb.add_field(name="Link", value="https://mod.reddit.com/mail/all/{}".format(thread.id), inline=True)
    emb.add_field(name="Participant", value=participant.name, inline=True)
    emb.add_field(name="Subject", value=thread.subject, inline=True)
    emb.add_field(name="Message", value=msg.body_markdown, inline=False)
    emb.timestamp = datetime.datetime.utcnow()  
    emb.set_footer(text="Bot made by Canadapost Duck#3062")
    # returns it to be sent by the bot
    return emb

def next(username):
    # if we already calculated the threads, just need to go back one
    index = 0
    if username in threadsByMod:
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
        index = threadsByMod[username][1]
        index -= 1
        if index < 0:
            index = len(threadsByMod[username][0]) - 1
        threadsByMod[username][1] = index
    else:
        # mod hasn't been called yet, generate their threads and keep index at 0
        getConversations(username)
    return generateMessage(username, index)
