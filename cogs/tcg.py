
from discord.ext import commands

class Main:
    """Main TCG Module!"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pms=True)
    async def hello(self):
        await self.bot.say('Hello! :ZoomZoom:')

def setup(bot):
    bot.add_cog(Main(bot))