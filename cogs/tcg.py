import os
import re
from discord.ext import commands
from cogs.utils.dataIO import dataIO

class Main:
    """Main TCG Module!"""
    def __init__(self, bot):
        self.bot = bot


    @commands.command(no_pms=True)
    async def hello(self):
        await self.bot.say('Hello! <a:ZoomZoom:525301223910277132> <a:ZoomZoom:525301223910277132> <a:ZoomZoom:525301223910277132>')


    @commands.command(pass_context=True)
    async def saveimg(self, ctx):
        path = "data/tcg/images.json"
        images = dataIO.load_json(path)

        await self.bot.say('Please send an image or a link to an img.')
        img_msg = await self.bot.wait_for_message(timeout=30, author=ctx.message.author)
        
        if not img_msg:
            return await self.bot.say("Command timed out.")
        elif img_msg.attachments:
            url = img_msg.attachments[0].get('url')
        elif img_msg.content:
            url = img_msg.content
        
        await self.bot.say('Please enter a name for this file.')
        name_msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
        
        if not name_msg:
            return await self.bot.say('Command timed out.')
        elif name_msg.content in images.keys():
            return await self.bot.say('An image under that name already exists.')
        else:
            images[name_msg.content] = url

        dataIO.save_json(path, images)

        return await self.bot.say('Your image has been saved. You can now view it by doing `[p]showimg <name>`')


    @commands.command(pass_context=True)
    async def showimg(self, ctx, name: str):
        path = "data/tcg/images.json"
        images = dataIO.load_json(path)

        if name in images.keys():
            return await self.bot.say(images[name])
        else:
            return await self.bot.say('Unable to find that image.')


        
def check_folders():
    if not os.path.exists(os.path.join("data", "tcg")):
        print('Making dir: data/tcg...')
        os.mkdir(os.path.join("data", "tcg"))


def check_files():
    f = os.path.join("data", "tcg", "images.json")
    if not dataIO.is_valid_json(f):
        print("Creating default data/tcg/images.json")
        dataIO.save_json(f, {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Main(bot))
