import re
import AdvancedHTMLParser

import urllib.request
import requests
import json

from enum import Enum

from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select
from sqlalchemy import schema
from sqlalchemy.sql.sqltypes import Float

from numpy import *
import os

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent':user_agent,}

#...................................................................................................
#.DDDDDDDDD.......AAAAA...AATTTTTTTTTT.AAAAA.....AAABBBBBBB......AAAAA.......ASSSSSS...SSSEEEEEEEE..
#.DDDDDDDDDD......AAAAA...AATTTTTTTTTT.AAAAA.....AAABBBBBBBB.....AAAAA.....AAASSSSSSS..SSSEEEEEEEE..
#.DDDDDDDDDDD....AAAAAA...AATTTTTTTTTT.AAAAAA....AAABBBBBBBBB....AAAAAA....AAASSSSSSS..SSSEEEEEEEE..
#.DDDD...DDDD....AAAAAAA......TTTT....TAAAAAA....AAAB....BBBB...BAAAAAA....AAAS..SSSSS.SSSE.........
#.DDDD....DDDD..AAAAAAAA......TTTT....TAAAAAA....AAAB....BBBB...BAAAAAA....AAAS........SSSE.........
#.DDDD....DDDD..AAAAAAAA......TTTT...TTAA.AAAA...AAABBBBBBBB...BBAA.AAAA...AAASSSSS....SSSEEEEEEE...
#.DDDD....DDDD..AAAA.AAAA.....TTTT...TTAA.AAAA...AAABBBBBBBB...BBAA.AAAA....AASSSSSSS..SSSEEEEEEE...
#.DDDD....DDDD.AAAAAAAAAA.....TTTT...TTAAAAAAAA..AAABBBBBBBBB..BBAAAAAAAA.....SSSSSSSS.SSSEEEEEEE...
#.DDDD....DDDD.AAAAAAAAAAA....TTTT..TTTAAAAAAAA..AAAB....BBBB.BBBAAAAAAAA.........SSSS.SSSE.........
#.DDDD...DDDDD.AAAAAAAAAAA....TTTT..TTTAAAAAAAA..AAAB....BBBB.BBBAAAAAAAA.AAAAS...SSSS.SSSE.........
#.DDDDDDDDDDD.DAAA....AAAA....TTTT..TTTA....AAAA.AAABBBBBBBBB.BBBA....AAAA.AAASSSSSSSS.SSSEEEEEEEE..
#.DDDDDDDDDD..DAAA.....AAAA...TTTT.TTTT.....AAAA.AAABBBBBBBBBBBBB.....AAAA.AAASSSSSSS..SSSEEEEEEEE..
#.DDDDDDDDD..DDAAA.....AAAA...TTTT.TTTT.....AAAAAAAABBBBBBB..BBBB.....AAAAA..ASSSSSS...SSSEEEEEEEE..
#...................................................................................................

database_url = os.environ.get('DATABASE_URL')
engine = create_engine(database_url)
Base = declarative_base(bind=engine)

#...................................................
#.DDDDDDDDD....BBBBBBBBBB..............RRRRRRRRRR...
#.DDDDDDDDDD...BBBBBBBBBBB.............RRRRRRRRRRR..
#.DDDDDDDDDDD..BBBBBBBBBBB.............RRRRRRRRRRR..
#.DDDD...DDDD..BBBB...BBBB..::::.......RRRR...RRRR..
#.DDDD....DDDD.BBBB...BBBB..::::.......RRRR...RRRR..
#.DDDD....DDDD.BBBBBBBBBBB..::::.......RRRRRRRRRRR..
#.DDDD....DDDD.BBBBBBBBBB..............RRRRRRRRRRR..
#.DDDD....DDDD.BBBBBBBBBBB.............RRRRRRRR.....
#.DDDD....DDDD.BBBB....BBBB............RRRR.RRRR....
#.DDDD...DDDDD.BBBB....BBBB............RRRR..RRRR...
#.DDDDDDDDDDD..BBBBBBBBBBBB.::::.......RRRR..RRRRR..
#.DDDDDDDDDD...BBBBBBBBBBB..::::.......RRRR...RRRR..
#.DDDDDDDDD....BBBBBBBBBB...::::.......RRRR....RRR..
#...................................................

Ingc_Ite = Table('ingc_ite', Base.metadata,
    Column('item_id', ForeignKey('items.id'                ), primary_key="True"),
    Column('ingc_id', ForeignKey('ingredient_categories.id'), primary_key=True  )
)

class Ingredients_Table(Base):
    __tablename__ = 'ingredients_table'

    cooking_id = Column(ForeignKey('cooking.id'), primary_key=True)
    ing_number = Column(Integer, primary_key=True)
    item_id    = Column(ForeignKey('items.id'))
    ingc_id    = Column(ForeignKey('ingredient_categories.id'))
    qty        = Column(Integer)

    ingt_coo  = relationship("Cooking", back_populates="coo_ingt")
    ingt_ite  = relationship("Items", back_populates="ite_ingt")
    ingt_ingc = relationship("Ingredient_Categories", back_populates="ingc_ingt")

    def __init__(self, cooking_id, ing_number, item_id, ingc_id, qty):
        self.cooking_id = cooking_id
        self.ing_number = ing_number
        self.item_id    = item_id
        self.ingc_id    = ingc_id
        self.qty        = qty

Itec_Ite = Table('itec_ite', Base.metadata,
    Column('item_id', ForeignKey('items.id'), primary_key=True),
    Column('itec_id', ForeignKey('item_class.id'), primary_key=True)
)

class Gatherables_Table(Base):
    __tablename__ = 'gatherables_table'

    gat_id     = Column(ForeignKey('gatherables.id'), primary_key=True)
    item_id    = Column(ForeignKey('items.id'), primary_key=True)
    dropQtyMin = Column(Integer)
    dropQtyMax = Column(Integer)

    gatt_ite = relationship("Items", back_populates="ite_gatt")
    gatt_gat = relationship("Gatherables", back_populates="gat_gatt")

    def __init__(self, gat_id, item_id, dropQtyMin, dropQtyMax):
        self.gat_id     = gat_id
        self.item_id    = item_id
        self.dropQtyMin = dropQtyMin
        self.dropQtyMax = dropQtyMax

class Loot_Restrict(Base):
    __tablename__ = 'loot_restrict'

    item_id        = Column(ForeignKey('items.id'), primary_key=True)
    gatherable_id  = Column(ForeignKey('gatherables.id'), primary_key=True)
    condition_id   = Column(Integer, primary_key=True)
    region_id      = Column(ForeignKey('regions.id'))
    playerLevelMin = Column(Integer)
    poiLevelMin    = Column(Integer)
    poiLevelMax    = Column(Integer)
    zoneLevelMin   = Column(Integer)
    zoneLevelMax   = Column(Integer)

    ltr_reg = relationship("Regions", back_populates="reg_ltr")
    ltr_ite = relationship("Items", back_populates="ite_ltr")


    def __init__(self, item_id, gatherable_id, condition_id):
        self.item_id       = item_id
        self.gatherable_id = gatherable_id
        self.condition_id  = condition_id


#.................................................
#.DDDDDDDDD....BBBBBBBBBB..............TTTTTTTTT..
#.DDDDDDDDDD...BBBBBBBBBBB.............TTTTTTTTT..
#.DDDDDDDDDDD..BBBBBBBBBBB.............TTTTTTTTT..
#.DDDD...DDDD..BBBB...BBBB..::::..........TTTT....
#.DDDD....DDDD.BBBB...BBBB..::::..........TTTT....
#.DDDD....DDDD.BBBBBBBBBBB..::::..........TTTT....
#.DDDD....DDDD.BBBBBBBBBB.................TTTT....
#.DDDD....DDDD.BBBBBBBBBBB................TTTT....
#.DDDD....DDDD.BBBB....BBBB...............TTTT....
#.DDDD...DDDDD.BBBB....BBBB...............TTTT....
#.DDDDDDDDDDD..BBBBBBBBBBBB.::::..........TTTT....
#.DDDDDDDDDD...BBBBBBBBBBB..::::..........TTTT....
#.DDDDDDDDD....BBBBBBBBBB...::::..........TTTT....
#.................................................

class TradeSkills(Base):
    __tablename__ = 'tradeskills'
    id = Column(String(30), primary_key=True)

    def __init__(self, id):
        self.id = id

class Regions(Base):
    __tablename__ = 'regions'
    
    id   = Column(Integer, primary_key=True)
    name = Column(String(50))
    code = Column(String(10))
    
    reg_ltr = relationship("Loot_Restrict", back_populates="ltr_reg")

    def __init__(self, id, name, code):
        self.id   = id
        self.name = name
        self.code = code

class Gatherables(Base):
    __tablename__ = 'gatherables'

    id            = Column(String(50), primary_key=True)
    type          = Column(String(50))
    name          = Column(String(250))
    rarity        = Column(Integer)
    requiredTSLvl = Column(Integer)
    tradeskill_id = Column(String(30), ForeignKey('tradeskills.id'))
    region_id     = Column(Integer, ForeignKey('regions.id'))
    
    gat_ts   = relationship("TradeSkills")
    gat_reg  = relationship("Regions")
    gat_gatt = relationship("Gatherables_Table", back_populates="gatt_gat")

    def __init__(self, id, type, name, rarity, requiredTSLvl):
        self.id            = id
        self.type          = type
        self.name          = name
        self.rarity        = rarity
        self.requiredTSLvl = requiredTSLvl

class Item_Class(Base):
    __tablename__ = 'item_class'

    id = Column(String(20), primary_key=True)

    def __init__(self, id):
        self.id = id

class Items(Base):
    __tablename__ = 'items'

    id       = Column(String(50), primary_key=True)
    type     = Column(String(50))
    typeName = Column(String(50))
    name     = Column(String(150))
    tier     = Column(Integer)
    rarity   = Column(Integer)
    weight   = Column(Integer)
    maxStack = Column(Integer)
    itemType = Column(String(50))
    level    = Column(Integer)

    item_itec = relationship("Item_Class", secondary=Itec_Ite)
    ite_ingc  = relationship("Ingredient_Categories", secondary=Ingc_Ite, back_populates="ingc_ite")
    ite_gatt  = relationship("Gatherables_Table", back_populates="gatt_ite")
    ite_ingt  = relationship("Ingredients_Table", back_populates="ingt_ite")
    ite_ltr   = relationship("Loot_Restrict" , back_populates="ltr_ite" )
    ite_coo   = relationship("Cooking", back_populates="coo_ite", uselist=False)

    def __init__(self, id, type, typeName, name, tier, rarity, weight, maxStack, itemType, level):
        self.id       = id
        self.type     = type
        self.typeName = typeName
        self.name     = name
        self.tier     = tier
        self.rarity   = rarity
        self.weight   = weight
        self.maxStack = maxStack
        self.itemType = itemType
        self.level    = level

class Cooking(Base):
    __tablename__ = 'cooking'

    id             = Column(String(50), primary_key=True)
    type           = Column(String(50))
    name           = Column(String(250))
    tradeskill_id  = Column(String(30), ForeignKey('tradeskills.id'))
    rarity         = Column(Integer)
    itemType       = Column(String(50))
    stations       = Column(String(50))
    recipeLevel    = Column(Integer)
    recipeExp      = Column(Integer)
    recipeStanding = Column(Integer)
    craftingFee    = Column(Integer)
    output         = Column(String(50), ForeignKey('items.id'))
    qtyBonus       = Column(Float)

    coo_ts   = relationship("TradeSkills")
    coo_ingt = relationship("Ingredients_Table", back_populates="ingt_coo")
    coo_ite  = relationship("Items", back_populates="ite_coo")

    def __init__(self, id, type, name, tradeskill, rarity, itemType, stations, recipeLevel, recipeExp, recipeStanding, craftingFee, output, qtyBonus):
        self.id             = id
        self.type           = type
        self.name           = name
        self.tradeskill     = tradeskill
        self.rarity         = rarity
        self.itemType       = itemType
        self.stations       = stations
        self.recipeLevel    = recipeLevel
        self.recipeExp      = recipeExp
        self.recipeStanding = recipeStanding
        self.craftingFee    = craftingFee
        self.output         = output
        self.qtyBonus       = qtyBonus

class Ingredient_Categories(Base):
    __tablename__ = 'ingredient_categories'

    id = Column(String(50), primary_key=True)

    ingc_ite  = relationship("Items", secondary=Ingc_Ite, back_populates="ite_ingc")
    ingc_ingt = relationship("Ingredients_Table", back_populates="ingt_ingc")

    def __init__(self, id):
        self.id = id

Base.metadata.create_all()

Session = sessionmaker(bind=engine)
s = Session()

#..........................................................................................................
#.FFFFFFFFFF.UUUU...UUUU..NNNN...NNNN....CCCCCCC....TTTTTTTTTTTIIII...OOOOOOO.....NNNN...NNNN...SSSSSSS....
#.FFFFFFFFFF.UUUU...UUUU..NNNNN..NNNN...CCCCCCCCC...TTTTTTTTTTTIIII..OOOOOOOOOO...NNNNN..NNNN..SSSSSSSSS...
#.FFFFFFFFFF.UUUU...UUUU..NNNNN..NNNN..CCCCCCCCCCC..TTTTTTTTTTTIIII.OOOOOOOOOOOO..NNNNN..NNNN..SSSSSSSSSS..
#.FFFF.......UUUU...UUUU..NNNNNN.NNNN..CCCC...CCCCC....TTTT...TIIII.OOOOO..OOOOO..NNNNNN.NNNN.NSSSS..SSSS..
#.FFFF.......UUUU...UUUU..NNNNNN.NNNN.NCCC.....CCC.....TTTT...TIIIIIOOOO....OOOOO.NNNNNN.NNNN.NSSSS........
#.FFFFFFFFF..UUUU...UUUU..NNNNNNNNNNN.NCCC.............TTTT...TIIIIIOOO......OOOO.NNNNNNNNNNN..SSSSSSS.....
#.FFFFFFFFF..UUUU...UUUU..NNNNNNNNNNN.NCCC.............TTTT...TIIIIIOOO......OOOO.NNNNNNNNNNN...SSSSSSSSS..
#.FFFFFFFFF..UUUU...UUUU..NNNNNNNNNNN.NCCC.............TTTT...TIIIIIOOO......OOOO.NNNNNNNNNNN.....SSSSSSS..
#.FFFF.......UUUU...UUUU..NNNNNNNNNNN.NCCC.....CCC.....TTTT...TIIIIIOOOO....OOOOO.NNNNNNNNNNN........SSSS..
#.FFFF.......UUUU...UUUU..NNNN.NNNNNN..CCCC...CCCCC....TTTT...TIIII.OOOOO..OOOOO..NNNN.NNNNNN.NSSS....SSS..
#.FFFF.......UUUUUUUUUUU..NNNN..NNNNN..CCCCCCCCCCC.....TTTT...TIIII.OOOOOOOOOOOO..NNNN..NNNNN.NSSSSSSSSSS..
#.FFFF........UUUUUUUUU...NNNN..NNNNN...CCCCCCCCCC.....TTTT...TIIII..OOOOOOOOOO...NNNN..NNNNN..SSSSSSSSSS..
#.FFFF.........UUUUUUU....NNNN...NNNN....CCCCCCC.......TTTT...TIIII....OOOOOO.....NNNN...NNNN...SSSSSSSS...
#..........................................................................................................

class RestrictionType(Enum):
    rtPlayerLevel   = 0
    rtPOILevel      = 1
    rtZoneLevel     = 2
    rtZoneRegion    = 3
    rtEnemyLevel    = 4

def extractRestriction(text):
    restrictions = ['Player Level (.+)', 'POI Level (.+)', 'Zone Level (.+)', '{!zone}(.+)', 'Enemy Level (.+)']

    for i in range(0, len(restrictions)):
        m = re.search(restrictions[i], text)
        if m:
            return (RestrictionType)(i), m.group(1)

def extractLink(text):
    m = re.search('db/(.+?)\"', text)
    if m:
        return m.group(1)

def insertRegions():
    r_list = []
    r_list.append(Regions(1, "Brightwood", "BW"))           # Brightwood
    r_list.append(Regions(2, "Cutlass Keys", "CK"))         # Cutlass Keys
    r_list.append(Regions(3, "Everfall", "EF"))             # Everfall
    r_list.append(Regions(4, "Edengrove", "EG"))            # Edengrove
    r_list.append(Regions(5, "Ebonscale Reach", "ER"))      # Ebonscale Reach
    r_list.append(Regions(6, "First Light", "FL"))          # First Light
    r_list.append(Regions(7, "Great Cleave", "GC"))         # Great Cleave
    r_list.append(Regions(8, "Monarch\'s Bluffs", "MB"))    # Monarch’s Bluffs
    r_list.append(Regions(9, "Mourningdale", "MD"))         # Mourningdale
    r_list.append(Regions(10, "Restless Shore", "RS"))      # Restless Shore
    r_list.append(Regions(11, "Reekwater", "RW"))           # Reekwater
    r_list.append(Regions(12, "Shattered Mountain", "SM"))  # Shattered Mountain
    r_list.append(Regions(13, "Weaver\'s Fen", "WF"))       # Weaver’s Fen
    r_list.append(Regions(14, "Windsward", "WW"))           # Windsward
    r_list.append(Regions(15, "Brimstone Sands", "BS"))     # Brimstone Sands

    for r in r_list:
        s.add(r)
        
    s.commit()

def insertTradeskills():
    ts_list = []
    ts_list.append(TradeSkills("Cooking"))
    ts_list.append(TradeSkills("Harvesting"))
    ts_list.append(TradeSkills("Fishing"))
    ts_list.append(TradeSkills("Skinning"))

    for ts in ts_list:
        s.add(ts)

    s.commit()

def insertGatherables(headers):
    gat_list = []

    # Get list of gatherables
    for page in range(0, 14):

        requestList = urllib.request.Request("https://nwdb.info/db/gatherables/page/"+str(page+1), None, headers)
        contents = urllib.request.urlopen(requestList)
        data = contents.read()

        parser = AdvancedHTMLParser.AdvancedHTMLParser()
        parser.parseStr(data)
        tavola = parser.getElementsByClassName("table table-striped table-borderless")

        nodi = tavola[0].children[1]
            
        for i in range(0, nodi.childElementCount):
            child = nodi.children[i]
            id = extractLink(child.children[0].innerHTML)
            gat_list.append(id)

    # For each gatherable, visit page
    for c in gat_list:
        url = requests.get("https://nwdb.info/db/" + c + ".json", headers=headers)
        gat_json = url.json()
        gatherable = Gatherables(gat_json["data"]["id"], gat_json["data"]["type"], gat_json["data"]["name"], 
            gat_json["data"]["rarity"], gat_json["data"]["requiredTSLvl"])

        # Check if tradeskill is needed to gather
        ts = gat_json["data"]["Tradeskill"]
        if ts != "None":
            q = s.query(TradeSkills).filter(TradeSkills.id == ts).first()
            if not q:
                newts = TradeSkills(ts)
                s.add(newts)
                s.commit()
            gatherable.tradeskill_id = ts
            if ts == "Fishing":
                q = s.query(Regions).filter(Regions.name == gat_json["data"]["region"]).first()
                gatherable.region_id = q.id
        s.add(gatherable)
        s.commit()

def insertItem(item_id):
    url = requests.get("https://nwdb.info/db/item/" + item_id + ".json", headers=headers)
    x_json = url.json()
    
    item = Items(item_id, x_json["data"]["type"], x_json["data"]["typeName"], x_json["data"]["name"], x_json["data"]["tier"], x_json["data"]["rarity"],
        x_json["data"]["weight"], x_json["data"]["maxStack"], x_json["data"]["itemType"], x_json["data"]["level"])

    s.add(item)
    s.commit()

    # Check: can the item be gathered?
    if "gatherablesWithItem" in x_json["data"]:
        canBeGathered = x_json["data"]["gatherablesWithItem"]
        if len(canBeGathered) > 0:
            for i in range(0, len(canBeGathered)):
                gat = canBeGathered[i]
                gatherablesWithItem(gat, item_id)
    
    # Check: can the item be used as ingredient?
    if "IngredientCategories" in x_json["data"]:
        isIngredient = x_json["data"]["IngredientCategories"]
        if len(isIngredient) > 0:
            for i in range(0, len(isIngredient)):
                # query to check if the category is already in DB
                q = s.query(Ingredient_Categories).filter(Ingredient_Categories.id == isIngredient[i]).first()
                if not q:
                    ingcat = Ingredient_Categories(isIngredient[i])
                    s.add(ingcat)
                    s.commit()
                    q = s.query(Ingredient_Categories).filter(Ingredient_Categories.id == isIngredient[i]).first()
                item.ite_ingc.append(q)
                s.commit()

def gatherablesWithItem(gat, item_id):
    gat_id = gat["id"]

    # Transforms string into array of ints
    drops_str_list = str(gat["dropQty"]).split("-")
    integer_map = map(int, drops_str_list)
    drops = list(integer_map)

    # Checks if drop is fixed or within a range
    if len(drops) == 1:
        gt = Gatherables_Table(gat_id, item_id, drops[0], drops[0])
    if len(drops) == 2:
        gt = Gatherables_Table(gat_id, item_id, drops[0], drops[1])
    
    s.add(gt)

    if "lootTagRestrictions" in gat:
        lootTagRestrictions(gat, item_id)
        
    s.commit()

def lootTagRestrictions(gat, item_id):
    restrict_list = str(gat["lootTagRestrictions"]).split(",")
    for j in range(0, len(restrict_list)):
        num, restriction = extractRestriction(restrict_list[j])
        if num == RestrictionType.rtZoneRegion:
            q = s.query(Regions).filter(Regions.code == restriction).first()
            if q:
                r = Loot_Restrict(item_id, gat["id"], j)
                r.region_id = q.id
                s.add(r)
                s.commit()

def insertCraftRec(c_json):
    output = c_json["data"]["output"]["id"]
    q = s.query(Items).filter(Items.id == output).first()
    if not q:
        insertItem(output)

    c = Cooking(c_json["data"]["id"], c_json["data"]["type"], c_json["data"]["name"], c_json["data"]["tradeskill"], c_json["data"]["rarity"], 
        c_json["data"]["itemType"], c_json["data"]["stations"][0], c_json["data"]["recipeLevel"], c_json["data"]["recipeExp"], c_json["data"]["recipeStanding"], 
        c_json["data"]["CraftingFee"], c_json["data"]["output"]["id"], c_json["data"]["qtyBonus"])

    s.add(c)
    s.commit()

    ingredients = c_json["data"]["ingredients"]
    for i in range(0, len(ingredients)):
        if ingredients[i]["type"] == "item":
            q = s.query(Items).filter(Items.id == ingredients[i]["id"]).first()
            if not q:
                insertItem(ingredients[i]["id"])
            newingr = Ingredients_Table(c_json["data"]["id"], i, ingredients[i]["id"], None, ingredients[i]["quantity"])
            s.add(newingr)
            s.commit()
        elif ingredients[i]["type"] == "category":
            q = s.query(Ingredient_Categories).filter(Ingredient_Categories.id == ingredients[i]["name"]).first()
            if not q:
                ingcat = Ingredient_Categories(ingredients[i]["name"])
                s.add(ingcat)
                s.commit()
            newingr = Ingredients_Table(c_json["data"]["id"], i, None, ingredients[i]["name"], ingredients[i]["quantity"])
            s.add(newingr)
            s.commit()

#..............................................................
#.MMMMMMM....MMMMMMM......AAAAAAA......AIIII..NNNNNN....NNNNN..
#.MMMMMMM....MMMMMMM......AAAAAAA......AIIII..NNNNNN....NNNNN..
#.MMMMMMM....MMMMMMM.....AAAAAAAA......AIIII..NNNNNNN...NNNNN..
#.MMMMMMMM...MMMMMMM.....AAAAAAAAA.....AIIII..NNNNNNNN..NNNNN..
#.MMMMMMMM..MMMMMMMM.....AAAAAAAAA.....AIIII..NNNNNNNN..NNNNN..
#.MMMMMMMM..MMMMMMMM....AAAAAAAAAAA....AIIII..NNNNNNNNN.NNNNN..
#.MMMMMMMM..MMMMMMMM....AAAAA.AAAAA....AIIII..NNNNNNNNN.NNNNN..
#.MMMMMMMMMMMMMMMMMM...AAAAAA.AAAAA....AIIII..NNNNNNNNNNNNNNN..
#.MMMMMMMMMMMMMMMMMM...AAAAA..AAAAAA...AIIII..NNNNNNNNNNNNNNN..
#.MMMMMMMMMMMMMMMMMM...AAAAA...AAAAA...AIIII..NNNNNNNNNNNNNNN..
#.MMMMMMMMMMMMMMMMMM..AAAAAAAAAAAAAA...AIIII..NNNNN.NNNNNNNNN..
#.MMMMMMMMMMMMMMMMMM..AAAAAAAAAAAAAAA..AIIII..NNNNN.NNNNNNNNN..
#.MMMMM.MMMMMMMMMMMM..AAAAAAAAAAAAAAA..AIIII..NNNNN..NNNNNNNN..
#.MMMMM.MMMMMM.MMMMM.MAAAAA.....AAAAAA.AIIII..NNNNN...NNNNNNN..
#.MMMMM.MMMMMM.MMMMM.MAAAA......AAAAAA.AIIII..NNNNN...NNNNNNN..
#.MMMMM.MMMMMM.MMMMM.MAAAA.......AAAAA.AIIII..NNNNN....NNNNNN..
#.MMMMM..MMMMM..MMMMMMAAAA.......AAAAAAAIIII..NNNNN....NNNNNN..
#..............................................................

def main():
    insertRegions()
    insertTradeskills()
    insertGatherables(headers)

    ci_list = []

    # Aquires list of craftables at a kitchen

    for page in range(1,7):
        requestList = urllib.request.Request("https://nwdb.info/db/recipes/crafting/cooking/page/"+str(page), None, headers)
        contents = urllib.request.urlopen(requestList)
        data = contents.read()

        parser = AdvancedHTMLParser.AdvancedHTMLParser()
        parser.parseStr(data)
        tavola = parser.getElementsByClassName("table table-striped table-borderless")

        nodi = tavola[0].children[1]
        
        for i in range(0, nodi.childElementCount):
            child = nodi.children[i]
            cookingid = extractLink(child.children[0].innerHTML)
            ci_list.append(cookingid)

    # Visits each element of the list and adds all the relevant information into the database

    for x in ci_list:
        url = requests.get("https://nwdb.info/db/"+str(x)+".json", headers=headers)
        j = url.json()
        insertCraftRec(j)

if __name__ == "__main__":
    main()