import random
from load_initial import factionlist
from helpers import coin

class Moon:
    def __init__(self, pname, sundistance, number):
        self.name = Moon.moonname(self, pname, number)
        self.factions = []
        self.systemobjects = []
        self.pname = pname
        Moon.habitable(self, sundistance)
    
    def moonname(self, pname, number):
        if number > 26:
            return ValueError("Too many moons.")
        suffix = chr(ord('`') + number)
        name = pname + suffix
        return name
    
    def habitable(self, sundistance):
        lwater = False
        type = ""
        life = False
        if sundistance == "medium":
            temperature = "medium"
            r = random.randint(1,100)
            if r > 80:
                lwater = True
            if lwater:
                tlist = ["Ocean", "Terrestrial", "Silicate", "Hyceanth", "Desert"]
                type = random.choice(tlist)
                tlist = ["thin", "breathable", "toxic", "dense", "none", "corrosive", "infiltrating"]
                atmosphere = random.choice(tlist)
                flip = coin()
                if flip == 1:
                    life = True
        if not bool(type):
            tlist = ["Carbon", "Coreless", "Gas dwarf", "Helium", "Ice", "Iron", "Lava", "Protoplanet", "Silicate", "Terrestrial"]
            type = random.choice(tlist)
            tlist = ["thin", "toxic", "dense", "none", "corrosive", "infiltrating"]
            atmosphere = random.choice(tlist)
        if sundistance == "close":
            temperature = "hot"
        elif sundistance == "far":
            temperature = "cold"
        self.temperature = temperature
        self.atmosphere = atmosphere
        self.lwater = lwater
        self.type = type
        self.life = life
        if self.atmosphere != "dense" or self.atmosphere != "infiltrating":
            r = random.randint(1,100)
            if r > 90:
                self.populated = True
            else:
                self.populated = False
        if self.populated:
            faction1 = random.choice(factionlist)
            flip = coin()
            if flip == 1:
                faction2 = faction1
                while faction2 == faction1:
                    faction2 = random.choice(factionlist)
                self.factions.append(faction1.name)
                self.factions.append(faction2.name)
            else:
                self.factions.append(faction1.name)

    @classmethod
    def __str__(self):
        return f"Name: {self.name}\nType: {self.type}\nTemp: {self.temperature}\nLife: {self.life}\nFactions: {self.factions}\nAtmosphere: {self.atmosphere}"
    