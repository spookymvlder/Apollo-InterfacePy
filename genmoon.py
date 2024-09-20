import random
from factions import FactionList
from helpers import coin

class Moon:
    typelist = ["ocean", "terrestrial", "silicate", "hyceanth", "desert", "carbon", "coreless", "gas dwarf", "helium", "ice", "iron", "lava", "protoplanet"]
    
    def __init__(self, pname, sundistance, gzone, id):
        self.name = Moon.moonname(self, pname, id)
        self.factions = []
        self.systemobjects = []
        self.pname = pname
        self.id = id
        Moon.habitable(self, sundistance, gzone)

    def editmoon(self, name, lwater, life, mtype, atmo, factions, notes):
        self.name = name
        self.lwater = lwater
        self.life = life
        self.type = mtype
        self.atmosphere = atmo
        self.factions = factions
        self.notes = notes

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type
    
    @property
    def lwater(self):
        return self._lwater

    @lwater.setter
    def lwater(self, lwater):
        self._lwater = lwater
    
    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, life):
        self._life = life
    
    @property
    def atmosphere(self):
        return self._atmosphere

    @atmosphere.setter
    def atmosphere(self, atmosphere):
        self._atmosphere = atmosphere

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes = notes

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, temperature):
        self._temperature = temperature

    @property
    def factions(self):
        return self._factions

    @factions.setter
    def factions(self, factions):
        self._factions = factions
        
    # ID starts at 0, so to turn that in to a character need to bump the value up by 1.
    def moonname(self, pname, id):
        if id > 26:
            return ValueError("Too many moons.")
        suffix = chr(ord('`') + (id + 1))
        name = pname + suffix
        return name
    
    def habitable(self, sundistance, gzone):
        lwater = False
        type = ""
        life = False
        if gzone == "right":
            temperature = "medium"
            r = random.randint(1,100)
            if r > 80:
                lwater = True
            if lwater:
                tlist = ["ocean", "terrestrial", "silicate", "hyceanth", "desert"]
                type = random.choice(tlist)
                tlist = ["thin", "breathable", "toxic", "dense", "none", "corrosive", "infiltrating"]
                atmosphere = random.choice(tlist)
                flip = coin()
                if flip == 1:
                    life = True
        if not bool(type):
            tlist = ["carbon", "coreless", "gas dwarf", "helium", "ice", "iron", "lava", "protoplanet", "silicate", "terrestrial"]
            type = random.choice(tlist)
            tlist = ["thin", "toxic", "dense", "none", "corrosive", "infiltrating"]
            atmosphere = random.choice(tlist)
        if gzone == "hot":
            temperature = "hot"
        elif gzone == "cold":
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
            faction1 = random.choice(FactionList.factionlist)
            flip = coin()
            if flip == 1:
                faction2 = faction1
                while faction2 == faction1:
                    faction2 = random.choice(FactionList.factionlist)
                self.factions.append(faction1.name)
                self.factions.append(faction2.name)
            else:
                self.factions.append(faction1.name)

    def __str__(self):
        return f"Name: {self.name} \nType: {self.type} \nTemp: {self.temperature} \nLife: {self.life} \nFactions: {self.factions} \nAtmosphere: {self.atmosphere}"
    