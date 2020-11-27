import discord
from discord.ext import commands
import functions as f

client = commands.Bot(command_prefix=">")

@client.command()
async def modmail(ctx, modName):
    # if we don't already have the threads by that mod in our dict
    # go get them
    if not modName in f.threadsByMod:
        f.getConversations(modName)
    # send the message based on the one generated in functions.generateMessage() with the index of 0
    # we use index 0 because we want the most recent
    msg = await ctx.send(embed=f.generateMessage(modName, 0))
    await msg.add_reaction("⬅")
    await msg.add_reaction("➡")

@client.event
async def on_reaction_add(ctx, user):
    msg = ctx.message
    # We ensure that the message was sent by the bot, but the reaction was not added by the bot
    if msg.author == client.user and user != client.user:
        description = msg.embeds[0].title
        user = description[19:]
        emb = None
        # if it's one of the arrows, remove the reaction and then use next() or back() to generate the new embed
        if ctx.emoji == "➡":
            await ctx.remove(user)
            await msg.edit(embed=f.next(user))
        elif ctx.emoji == "⬅":
            await ctx.remove(user)
            await msg.edit(embed=f.back(user))

client.run('')