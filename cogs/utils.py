import discord
from discord.ext import commands
import os
import sys
import urllib
import json

class utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    # Returns the latency of the selfbot
    @commands.command(name='ping', aliases=['latency'])
    async def ping(self, ctx):
        """Pong! Returns your ping"""
        # Get the latency
        latency = self.bot.latency
        # Create the embed
        embed = discord.Embed(title="Pong!", description=f"Latency: {latency * 1000:.0f}ms", color=0x00ff00)
        # Send the embed
        await ctx.send(embed=embed)
        




    @commands.command()
    # Reloads all of the cogs
    async def reload(self, ctx, *, cog=None):
        """Reloads one or all of the cogs in

        Paramaters:
            • cog - The name of the cog you want to reload e.g crypto
            If not name is specified it'll reload all cogs"""
        if not cog:
            # If no cog is specified then reload all cogs
            async with ctx.typing():
                embed = discord.Embed(
                    title=f'Reloading all cogs',
                    color=discord.Color.green(),
                    timestamp=ctx.message.created_at
                )
                # For ext in ./cogs/ which ends with .py and does not start with "_" 
                # Try to unload then reload each cog then add a field to then embed which says it reloaded the cog
                for ext in [f for f in ctx.bot.extensions if f.endswith('.py') and not f.startswith('_')]:
                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        print(green + "Loaded cog " + reset + ext)
                        embed.add_field(name=f"Reloaded {ext}", value="\uFEFF", inline=False)
                    except Exception as e:
                        embed.add_field(name=f"Failed to reload {ext}", value=f"```{e}```", inline=False)
                await ctx.send(embed=embed)
        else:
            # reload the specific cog
            async with ctx.typing():
                embed = discord .Embed(
                    title=f'Reloading {cog}',
                    color=discord.Color.green(),
                    timestamp=ctx.message.created_at
                )

                ext = f"{cog.lower()}.py"

                if not os.path.exists((f"cogs/{ext}")):
                    embed.add_field(
                        name=f"Failed to reload " + ext,
                        value = "because it does not exist",
                        inline=False
                    )
                
                if ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`", value="\uFEFF", inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                            inline=False,
                        )
                        await ctx.send(embed=embed)

    @commands.command()
    #Restarts the Bot
    async def restart(self, ctx):
        """Restarts the bot"""
        await ctx.send(f"Restarting...")
        os.execv(sys.executable, ['python'] + sys.argv)

    # Checks the bot for updates using autoupdater in selfbot.py
    @commands.command()
    async def update(self, ctx):
        """Checks the selfbot for updates"""
        print(cyan + "Checking for updates..." + reset)
        # Github repo is https://github.com/GoByeBye/Ares
        # Check the raw file on github https://github.com/GoByeBye/Ares/data/version.json against __version__ of selfbot.py
        # if version differs run update.py and close selfbot.py
        try:
            import urllib.request
            version = urllib.request.urlopen("https://raw.githubusercontent.com/GoByeBye/Ares/master/data/version.json").read()
            
            version = version.decode("utf-8")
            version = json.loads(version)
            version = version["version"]
            if version != __version__:
                print(green + "A new update is available!" + reset)
                print(green + "Updating..." + reset)
                os.system("python update.py")
                sys.exit()
            else:
                print(green + "You are running the latest version!" + reset)
        except:
            print(red + "Error: Could not check for updates." + reset)
            print(red + "Please check your internet connection." + reset)
            sys.exit()

def setup(bot):
    bot.add_cog(utils(bot))