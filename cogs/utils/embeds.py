from discord.ext.commands import HelpFormatter
from discord import Embed
from datetime import datetime
from colors import BOT


class RichEmbed(Embed):
    def __init__(self, ctx, **kwargs):
        message = ctx.message
        bot = ctx.bot
        self.set_footer(text="Requested by: {}".format(message.author.name),
                        icon_url=message.author.avatar_url)
        self.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

        if kwargs['color'] is 'bot':
            kwargs['color'] = BOT
        elif kwargs['color'] is 'author':
            kwargs['color'] = message.author.colour

        super().__init__(**kwargs, timestamp=datetime.utcnow(), type='rich')

    # You can ignore this.
    def __len__(self):
        def clean(arr):
            return [v for v in arr if v]

        values = ([f.name for f in self.fields] + 
                  [f.value for f in self.fields] + 
                  [self.title, self.description, self.author.name, self.footer.text])
        
        return sum(clean([len(v) for v in values]))


class HelpEmbed(RichEmbed):
    """Basic embed for the help command, 
    returned when [p]help is called (without any arguments)
    """
    def __init__(self, ctx):
        bot = ctx.bot
        cogs = [c.__module__.split(".")[1] for c in bot.cogs.values() if c.__module__ != "cogs.owner"]
            
        super().__init__(ctx, title="Help",
                          description="""
                                    To get help with specific cogs, use `{0}help <cog>`
                                    To get help with specific commands, use `{0}help <command>`
                                    For more information about the bot, use `{0}info`

                                    You can also visit the [bot's wiki](https://github.com/quantomistro3178/PieBot) to get further 
                                    help with the TCG cog commands, or join the [support server](https://github.com/quantomistro3178/PieBot)
                                    if you have any questions!
                                    """.format(ctx.prefix),
                          color='bot')

        self.set_thumbnail(url=bot.user.avatar_url)
        self.add_field(name="Server Prefixes", value="lol i'll add this later. :v", inline=False)
        self.add_field(name="Cogs", value="```{}```".format("\n".join(cogs)), inline=False)


class CmdHelpEmbed(RichEmbed):
    """Help embed for bot commands"""
    def __init__(self, ctx, command):
        # Will do this soon :v
        formatter = HelpFormatter()

        name = command.name
        longdoc = command.help
        base = command.full_parent_name.split(' ')[0]
        cog = command.cog_name if command.cog_name is not None else '--/--'

        codeblocks = "\n".join(formatter.format_help_for(ctx, command))

        super().__init__(ctx, title="[{}]".format(name),
                              description=longdoc,
                              color='bot')

        self.add_field(name="Cog", value=cog)
        self.add_field(name="Base Command", value=base)
        self.add_field(name="Help", value=longdoc, inline=False)
        self.add_field(name="Subcommands", value=codeblocks)
        


class CogHelpEmbed(RichEmbed):
    """Help embed for cogs commands"""
    def __init__(self, ctx, cog):
        # This too :v
        pass

