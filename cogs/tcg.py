import os
import re
from discord.ext import commands
from cogs.utils.dataIO import dataIO

class TCG:
    """TCG Module!"""
    def __init__(self, bot):
        self.bot = bot


    @commands.command(no_pms=True)
    async def hello(self):
        await self.bot.say('Hello!')



def init_db(bot):
    bot.db = "OK"
    pass 
        
def check_folders():
    f = os.path.join("data", "tcg")
    if not os.path.exists(f):
        print('Making dir: {}'.format(f))
        os.mkdir(f)


def check_files():
    f = os.path.join("data", "tcg", "images.json")
    if not dataIO.is_valid_json(f):
        print("Creating default {}".format(f))
        dataIO.save_json(f, {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(TCG(bot))
