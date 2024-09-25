import random, string
from gennpc import Npc


# Creates corporations, can also be called via gencorpname to get a random one that isn't saved.
# Currently only gencorpname is in use, needs updates if being used for anything else.
# TODO: Add tags and associate them with names like the tag transport with Shipping so the name ABC Shipping, Inc. would be possible
# TODO: Add things like board members, subsidiaries, locations
class Corp:
    suffixes = [", Inc.", " Corporation", " Co.", " Company", " Services, Inc.", " Group, Inc.", " Materials, Inc.", 
                " Products", " Incorporated", " and Company", " Brands Inc."]
    patterns = ["AAA", "L.L. Name", "NaN", "N-N", "3H"]
    
    def __init__(self, corpname=""):
        self.corpname = corpname

    @property
    def corpname(self):
        return self._corpname
    
    @corpname.setter
    def corpname(self, corpname):
        if corpname == "":
            corpname = Corp.gencorpname()
        elif not isinstance(corpname, str):
            raise ValueError(f"Invalid corporation name {corpname}.")
        self._corpname = corpname

    @staticmethod
    def gencorpname():
        pattern = random.choice(Corp.patterns)
        name = ""
        letters = string.ascii_uppercase
        match pattern:
            case "AAA":   
                for i in range(2):
                    name += random.choice(letters)
            case "L.L. Name":
                name = random.choice(letters) + "." + random.choice(letters) + "."
                table = Npc.gennametable()
                name += Npc.genname(table[0])
            case "NaN":
                table1, table2 = Npc.gennametable(), Npc.gennametable()
                i = random.randint(0,2)
                name = Npc.genname(table1[i]) + " and " + Npc.genname(table2[i])
            case "N-N":
                table1, table2 = Npc.gennametable(), Npc.gennametable()
                name = Npc.genname(table1[0]) + "-" + Npc.genname(table2[0])
            case "3H":
                digits = string.hexdigits
                r = random.randint(2, 4)
                tlist = [digits, letters]
                for i in range(r):
                    source = random.choice(tlist)
                    name += random.choice(source)
        name += random.choice(Corp.suffixes)
        return name
    

# Functionality to store a list of corps
# TODO - improve functionality with use of tags, add prefered nations, faction allegiance
class Corps:
    corps = []

    @staticmethod
    def addCorps(corpname=""):
        corp = Corp(corpname)
        Corps.corps.append(corp)