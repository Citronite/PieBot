from discord import Embed
from datetime import datetime

class RichEmbed(Embed):
    def __init__(self, ctx, **kwargs):
        message = ctx.message
        bot = ctx.bot
        self.set_footer(text="Requested by: {}".format(message.author.name),
                        icon_url=message.author.avatar_url)
        self.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

        super().__init__(**kwargs, timestamp=datetime.utcnow(), type='rich')

    # You can ignore this.
    def __len__(self):
        return sum([f.name for f in self.fields] + 
                   [f.value for f in self.fields] + 
                   [self.title, self.description, self.author.name, self.footer.text])


class HelpEmbed(RichEmbed):
    """
    Basic embed for the help command, returned when [p]help is called, without any arguments.
    """
    def __init__(self, ctx):
        bot = ctx.bot
        cogs = [c.__module__.split(".")[1] for c in bot.cogs.values() if c.__module__ != "cogs.owner"]
            
        super().__init__(ctx, title="Help",
                          description="""
                                    To get help with specific cogs, use `{0}help <cog>`
                                    To get help with specific commands, use `{0}help <command>`

                                    You can also visit the [bot's wiki]() to get further 
                                    help with the TCG cog commands, or join the [support server]()
                                    if you have any questions!
                                    """.format(ctx.prefix),
                          color=0x3986c4)

        self.set_thumbnail(url=bot.user.avatar_url)
        self.add_field(name="Server Prefixes", value="OK")
        self.add_field(name="Cogs", value="```{}```".format("\n".join(cogs)))

class CommandHelpEmbed(RichEmbed):
    def __init__(self, ctx, command):
        # Will do this soon :v
        pass

class CogHelpEmbed(RichEmbed):
    def __init__(self, ctx, cog):
        # This too :v
        pass

