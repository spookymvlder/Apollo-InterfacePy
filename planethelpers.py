import random
from factions import FactionList
from helpers import coin

class PlanetBuilders:
    
    # Planets outside the gzone wouldn't have liquid water unless some weird chemical mixing was happening. 
    # Percentages found below have no basis in reality, but should keep things interesting.
    @staticmethod
    def genlwater(ptype, gzone):
        if gzone != "right":
            return False
        if ptype in ["hycean", "ocean"]:
            return True
        elif ptype in ["terrestrial", "silicate"]:
            if random.uniform(1, 100) > 60:
                return True
        elif ptype == "desert":
            if random.uniform(1, 100) > 95:
                return True
        return False

    # Any planet with liquid water would need an atmosphere
    # TODO replace with atmosphere composition and separate breathable air from atmosphere type
    @staticmethod
    def genatmo(lwater, ptype):
        if ptype in ["chthonian"]:
            return "none"
        if lwater == True:
            return random.choice(["breathable", "thin", "toxic", "dense", "corrosive", "infiltrating"])
        if ptype in ["gas dwarf", "gas giant"]:
            return "dense"
        else:
            return random.choice(["thin", "toxic", "dense", "corrosive", "infiltrating", "none"])

    # Anything with liquid water would probably have something even just a microbe. 
    # Anything in gzone could have something weird, outside of gzone something underground is possible, but currently out of scope.
    @staticmethod
    def genlife(lwater, gzone, atmo, ptype):
        life = False
        if lwater == True and atmo in ["breathable", "thin"]:
            life = True
        elif lwater:
            if random.randint(0, 100) > 60:
                life = True
        elif gzone == "right" and ptype in ["desert", "iron", "lava", "silicate", "terrestrial"] and atmo != "none":
            if random.randint(0, 100) > 95:
                life = True
        return life

    # Actual percent would be much lower, but that's less interesting. Will tweak later.
    # TODO actually tweak later
    @staticmethod
    def genpopulated(atmo):
        if atmo not in ["infiltrating", "dense", "corrosive"]:
            if random.randint(0, 100) > 90:
                return True
        return False

    @staticmethod
    def gensettlementfaction(populated):
        if not populated:
            return []
        limit = 1 + coin()
        factions = []
        count = 0
        while count < limit:
            faction = random.choice(FactionList.factionlist)
            if faction not in factions:
                factions.append(faction)
                count += 1
        return factions

    # Returns percent of planet that has been surveyed.
    @staticmethod
    def gensurveyed(factions):
        surveyed = 0
        if factions != []:
            for faction in factions:
                surveyed += random.uniform(20, 80)
            while surveyed > 100:
                surveyed -= random.uniform(10, 23)
        elif random.randint(0, 100) > 83:
            surveyed = random.randint(0, 100)
        return surveyed

    @staticmethod
    def genpressure(atmo, ptype):
        if ptype in ["gas giant", "gas dwarf", "ice giant", "puff", "super-puff", "helium"]:
            pressure = "high"
        else:
            pressure = "regular"
        return pressure