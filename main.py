import discord
from discord.ext import commands
import functions as f
import datetime

client = commands.Bot(command_prefix=">")
colour = 0xcdcd22
client.remove_command('help')

@client.command()
async def modmail(ctx, modName):
    # go get the threads for that mod
    f.getConversations(modName) 
    # send the message based on the one generated in functions.generateMessage() with the index of 0
    # we use index 0 because we want the most recent
    msg = await ctx.send(embed=f.generateMessage(modName, 0))
    if msg.embeds[0].author.name:
        await msg.add_reaction("⬅")
        await msg.add_reaction("➡")

@client.command()
async def help(ctx):
    emb = discord.Embed(title="Info for ModmailCheckup bot", color=colour)
    emb.description = "This is Hercs' minion for checking the status of our mods in modmail"
    emb.add_field(name="How does it work?", value="Simple! just use `>modmail [modname]` to get up to {} threads from the most recent {} threads for any mod on the sub. Simply use the arrows to move between threads. Be careful of your spelling, capitalization, and make sure not to include the u/! Be patient, the bot is a bit slow at gathering all the posts.".format(f.threadCap, f.lim), inline=False)
    emb.timestamp = datetime.datetime.utcnow()  
    emb.set_footer(text="Bot made by Canadapost Duck#3062")
    await ctx.send(embed=emb)

@client.event
async def on_reaction_add(ctx, user):
    msg = ctx.message
    # We ensure that the message was sent by the bot, but the reaction was not added by the bot
    if msg.author == client.user and user != client.user:
        if msg.embeds[0].author.name:
            description = msg.embeds[0].title
            mod = msg.embeds[0].author.name
            emb = None
            # if it's one of the arrows, remove the reaction and then use next() or back() to generate the new embed
            if ctx.emoji == "➡":
                await ctx.remove(user)
                await msg.edit(embed=f.cycle(mod, 1))
            elif ctx.emoji == "⬅":
                await ctx.remove(user)
                await msg.edit(embed=f.cycle(mod, -1))

client.run('')