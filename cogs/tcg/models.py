from peewee import Model, CharField, TextField, IntegerField, ForeignKeyField, BooleanField
from playhouse.sqliteq import SqliteQueueDatabase

DB_PATH = "./global.db"

def get_global_db(path):
    return SqliteQueueDatabase(path,
                            use_gevent=False,
                            autostart=True,
                            queue_max_size=64,
                            results_timeout=5.0)



class Base(Model):
    class Meta:
        database = get_global_db(DB_PATH)

class Clan(Base):
    """Represents a user-created "clan". Clans are basically
    teams of players which can compete with other clans for points
    and prizes etc. At least 3 players are needed to create one.

    Fields
    ------
    name : [PK] The name of the clan.
    
    total_matches : Matches played by the clan.
    
    wins : Matches won by the clan.
    
    owner_id : id of the clan owner.
    
    about_text : Short description / information about the clan,
    to be shown in the ClanEmbed
    """

    name = CharField(primary_key = True)
    total_matches = IntegerField(default = 0)
    wins = IntegerField(default = 0)
    owner_id = CharField(unique = True)
    about_text = TextField(default = "This is a mysterious guild.")

class Player(Base):
    """Represents a "player".

    Fields
    ------
    id : [PK] Id of the discord.User.

    balance : Keeps track of money.

    total_matches : Total matches played.

    wins : Total wins.

    clan : [FK] The clan the player belongs to.
    """

    id = CharField(primary_key = True)
    balance = IntegerField(default = 0)
    total_matches = IntegerField(default = 0)
    wins = IntegerField(default = 0)
    clan = ForeignKeyField(Clan,
                           backref = 'members',
                           null = True)

class CardType(Base):
    """Represents a "type" of card in the TCG.

    Fields
    ------
    name : [PK] The name of the card.

    avatar_url : A url to the image which will be used
    as the avatar for the card in CardEmbed.

    appearance_rate : Kind of similar to the appearance
    rate for Pokemon. An int value between 1-100.

    base_hp : Base health points for all crds of this
    type.

    base_attack = Base attack stat. Determines damage dealt.

    base_defense = Base defense stat.Determines damage taken.

    **The final stats for the cards will be calculated from
    base stats, level and exp. The functions for that are
    defined in ./stat_funcs.py.
    """
    name = CharField(primary_key = True)
    avatar_url = TextField()
    appearance_rate = IntegerField()
    base_hp = IntegerField()
    base_attack = IntegerField()
    base_defense = IntegerField()

class Card(Base):
    """Represents an actual card, owned by a player.

    Fields
    ------
    owner : [FK] The owner of this card.

    card_type : [FK] The type this card belongs to.

    nickname : A nickname for the card, chosen by the player.
    Used to identify a players' cards. For this reason, all
    cards owned by a player must have unique nicknames.

    level : The level of this card. Level determines 
    the stats of the card, as well as the exp gained
    during fights. The functions for this are
    defined in ./stat_funcs.py.

    exp : The experience points for the card.
    """
    owner = ForeignKeyField(Player, backref='cards')
    card_type = ForeignKeyField(CardType)
    nickname = CharField()
    level = IntegerField(default = 1)
    exp = IntegerField(default = 0)


class ItemType(Base):
    """Similar to CardType, represents a type of 
    item in the TCG.

    Fields
    ------
    name : [PK] The name for this type of item.

    description : Info about this item.

    price : The price of this item.

    icon_url : A url to the image which will be
    used as the icon for the item in ItemEmbed.

    effect : An integer indicating what effect 
    this item has. Currently there are 4 effects
    an item can have. They can be found in 
    ./stat_funcs.py.

    effect_intensity : An integer indicating the s
    trength of the effect.
    """
    name = CharField(primary_key = True)
    description = TextField()
    price = IntegerField()
    icon_url = TextField()
    effect = IntegerField()
    effect_intensity = IntegerField()


class Item(Base):
    """Represents an actual card owned by a player.

    Fields
    ------
    owner : [FK] The owner of this item.

    item_type : [FK] The type this item belongs to.

    qty : The quantity of this item owned by the player.
    """
    owner = ForeignKeyField(Player, backref='items')
    item_type = ForeignKeyField(ItemType)
    qty = IntegerField()

