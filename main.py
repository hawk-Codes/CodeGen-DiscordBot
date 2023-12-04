import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot_token = "******************************"
github_access_token = "****************************"

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command()
async def codegen(ctx, *, query):
    try:
        headers = {
            "Authorization": f"token {github_access_token}"
        }

        url = f"https://api.github.com/search/code?q={query}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            if items:
                code_url = items[0].get("html_url", "")
                await ctx.send(f"Here's a code example for '{query}':\n{code_url}")
            else:
                await ctx.send(f"No code examples found for '{query}'.")
        else:
            await ctx.send(f"An error occurred: {response.status_code}")

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

bot.run(bot_token)
