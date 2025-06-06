import discord
import sqlite3
from vlrAPI import vlrAPI
from vlrAPI import valEsportsAPI

bot = discord.Bot()
testGuild = "1340995376055976030"
teamRegions = ["na", "eu", "br", "ap", "kr", "ch", "jp", "lan", "las", "oce", "mn", "gc", "all"]
primaryRegions = ['Asia-Pacific', 'Americas', 'China', 'EMEA']
eSportsAPP = valEsportsAPI()
con = sqlite3.connect("data/vlr.db")
cur = con.cursor()
cur.execute("CREATE TABLE movie(title, year, score)")

def initialiseDatabase():
    # Teams table
    # Player Table
    # Events Table
    # Matches Table
    # Results Table
    # Metadata Table
    pass

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

async def get_teams(ctx: discord.AutocompleteContext):
    """
    Here we will check if 'ctx.options['animal_type']' is a marine or land animal and return respective option choices
    """
    region = ctx.options['region']
    result = eSportsAPP.teams(page=1, limit="5", region=region)
    
    teamNames = [team["name"] for team in result["data"]]
    print(teamNames)
    
    return teamNames


@bot.slash_command(guild_ids=[testGuild])
async def subscribe(
    ctx: discord.ApplicationContext, 
    region: discord.Option(str, choices=teamRegions),
    team: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_teams))
    ):
    print(team)
    await ctx.respond("Hello!")
    

# @bot.slash_command(guild_ids=["1340995376055976030"])
# async def unsubscribe(ctx):
#     await ctx.respond("Hello!")

# @bot.slash_command(guild_ids=["1340995376055976030"])
# # pycord will figure out the types for you
# async def add(ctx, first: discord.Option(int), second: discord.Option(int)):
#   # you can use them as they were actual integers
#   sum = first + second
#   await ctx.respond(f"The sum of {first} and {second} is {sum}.")

if __name__ == "__main__":

    with open("token.txt", "r") as f:
        token = f.read()
    bot.run(token)