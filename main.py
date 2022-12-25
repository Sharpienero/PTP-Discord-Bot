import discord
import os
import ptpapi
from discord import option

bot = discord.Bot()
ptp_client = ptpapi.login(api_user=os.environ.get('PTPAPI_USERNAME'), api_key=os.environ.get('PTPAPI_PASSKEY'))


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.slash_command(guild_ids=[os.getenv("DISCORD_GUILD_ID")])
async def hello(ctx):
    await ctx.respond("Hello!")


@bot.slash_command(guild_ids=[os.getenv("DISCORD_GUILD_ID")])
@option("title", description="The title of the movie to search.", required=True)
async def search_movies(ctx: discord.ApplicationContext, title: str):

    results = ptp_client.search({
        "name": title
    })

    if len(results) == 0:
        await ctx.respond("No results found.", ephemeral=True)

    #await ctx.respond(f"Found {len(results)} torrents. Select a poster from below.", ephemeral=True)

    for result in results:
        desc_obj = {
            "year": result.data['Year'],
            "imdb": result.data['ImdbId'],
        }
        embed = discord.Embed(title=f"{result.data['Title']} - {result.data['Year']}", description=desc_obj)
        embed.set_thumbnail(url=result.data['Cover'])
        await ctx.respond(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
