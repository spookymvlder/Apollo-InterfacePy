import random
from factions import FactionList
from helpers import coin
from planethelpers import PlanetBuilders

class Moon:
    typelist = ["ocean", "terrestrial", "silicate", "hyceanth", "desert", "carbon", "coreless", "gas dwarf", "helium", "ice", "iron", "lava", "protoplanet"]
    
    # TODO update pname when planet name changes
    def __init__(self, pname, gzone, id, name, mtype, lwater, atmo, life, populated, factions, systemobjects, surveyed, pressure):
        self.pname = pname
        self.gzone = gzone
        self.id = id
        self.name = name
        self.mtype = mtype
        self.lwater = lwater
        self.atmo = atmo
        self.life = life
        self.populated = populated
        self.factions = factions
        self.systemobjects = systemobjects
        self.surveyed = surveyed
        self.pressure = pressure
        
        
    def genrandommoon(pname, sundistance, gzone, id):
        pname = pname
        gzone = gzone
        id = id
        name = Moon.genmoonname(pname, id)
        mtype = Moon.genrandomtype(gzone)
        lwater = PlanetBuilders.genlwater(mtype, gzone)
        atmo = PlanetBuilders.genatmo(lwater, mtype)
        life = PlanetBuilders.genlife(lwater, gzone, atmo, mtype)
        populated = PlanetBuilders.genpopulated(atmo)
        factions = PlanetBuilders.gensettlementfaction(populated)
        systemobjects = []
        surveyed = PlanetBuilders.gensurveyed(factions)
        pressure = PlanetBuilders.genpressure(atmo, mtype)
        return Moon(pname, gzone, id, name, mtype, lwater, atmo, life, populated, factions, systemobjects, surveyed, pressure)

    def editmoon(self, name, lwater, life, mtype, atmo, factions, notes):
        self.name = name
        self.lwater = lwater
        self.life = life
        self.mtype = mtype
        self.atmosphere = atmo
        self.factions = factions
        self.notes = notes

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    # ID starts at 0, so to turn that in to a character need to bump the value up by 1.
    @staticmethod
    def genmoonname(pname, id):
        if id > 26:
            return ValueError("Too many moons.")
        suffix = chr(ord('`') + (id + 1))
        name = pname + suffix
        return name

    @property
    def mtype(self):
        return self._mtype

    @mtype.setter
    def mtype(self, mtype):
        self._mtype = mtype

    @staticmethod
    def genrandomtype(gzone):
        if gzone == "right":
            typelist = ["carbon", "desert", "hycean", "iron", "ocean", "protoplanet", "silicate", "terrestrial", "gas dwarf", "helium"]
        elif gzone == "hot":
            typelist = ["carbon", "desert", "iron", "lava", "protoplanet", "silicate", "terrestrial", "gas dwarf", "helium"]
        else:
            typelist = ["carbon", "coreless", "desert", "iron", "protoplanet", "silicate", "terrestrial", "gas dwarf", "helium", "ice"]
        return random.choice(typelist)

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
        


    def __str__(self):
        return f"Name: {self.name} \nType: {self.mtype} \nLife: {self.life} \nFactions: {self.factions} \nAtmosphere: {self.atmo}"
    