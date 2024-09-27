import random, string
from helpers import coin, isbool
from factions import FactionList
from genmoon import Moon
from planethelpers import PlanetBuilders


# Trying something different in formatting for refactor of genplanet.
class Planet:
    distancelist = ["close", "medium", "far"]
    ptypelist = ["chthonian", "carbon", "coreless", "desert", "gas dwarf", "gas giant", "helium", "hycean", 
    "ice giant", "ice", "iron", "lava", "ocean", "protoplanet", "puffy", "super-puff", "silicate", "terrestrial"]
    atmolist = ["breathable", "thin", "toxic", "dense", "corrosive", "infiltrating", "none"]
    sizelist = ["small", "medium", "large", "giant"]
    templist = ["hot", "medium", "cold"]
    pressurelist = ["regular", "high"]
    gzonelist = ["right", "hot", "cold"]

    def __init__(self, distance, gzone, basetemp, terrestrial, ptype, lwater, atmo, mass, radius, rings, mooncandidate, mooncount, gravity, relativeg, notes, life, populated, pname, factions, surveyed, pressure, settlements, moons, id):
        self.distance = distance
        self.gzone = gzone
        self.basetemp = basetemp
        self.terrestrial = terrestrial
        self.ptype = ptype
        self.lwater = lwater
        self.atmo = atmo
        self.mass = mass
        self.radius = radius
        self.rings = rings
        self.mooncandidate = mooncandidate
        self.mooncount = mooncount
        self.gravity = gravity
        self.relativeg = relativeg
        self.notes = notes
        self.life = life
        self.populated = populated
        self.pname = pname
        self.factions = factions
        self.surveyed = surveyed
        self.settlements = settlements
        self.pressure = pressure
        self.moons = moons
        self.id = id
        self.symbols = Planet.assemblesymbols(self.ptype, self.gzone, self.rings, self.lwater, self.life, self.mooncount)
        self.tooltip = Planet.buildtooltip(self.ptype, self.gzone, self.rings, self.lwater, self.life, self.mooncount)

    @staticmethod
    def genplanetfromstar(inzone, outzone, min, startemp, starmass, lum, spacing, id):
        id = id
        distance = Planet.calcdistance(min, spacing)
        gzone = Planet.calcgzone(distance, inzone, outzone)
        basetemp = Planet.calcbasetemp(distance, lum)
        terrestrial = Planet.genplanetcategory()
        ptype = Planet.genplanettype(terrestrial, gzone)
        lwater = PlanetBuilders.genlwater(ptype, gzone)
        atmo = PlanetBuilders.genatmo(lwater, ptype)
        mass = Planet.genmass(ptype) # Returns Earth Mass
        radius = Planet.genradius(mass) # Returns Earth Radius
        rings = Planet.genrings()
        mooncandidate = Planet.genmooncandidate(ptype)
        mooncount = Planet.genmooncount(radius, mooncandidate)
        gravity = Planet.gengravity(radius, mass)
        relativeg = Planet.genrelativeg(radius, mass)
        notes = ""
        life = PlanetBuilders.genlife(lwater, gzone, atmo, ptype)
        populated = PlanetBuilders.genpopulated(atmo)
        pname = Planet.genpname() # TODO update with populated when we have name lists for that.
        factions = PlanetBuilders.gensettlementfaction(populated)
        surveyed = PlanetBuilders.gensurveyed(factions)
        pressure = PlanetBuilders.genpressure(atmo, ptype)
        settlements = [] # Empty list for now, may generate later to pass in
        moons = Planet.genmoons(pname, mooncount, distance, gzone)
        return Planet(distance, gzone, basetemp, terrestrial, ptype, lwater, atmo, mass, radius, rings, mooncandidate, mooncount, gravity, relativeg, notes, life, populated, pname, factions, surveyed, pressure, settlements, moons, id)

    # For use with /editplanet in app.py. Should be converting HTML inputs to non-string data types first.
    def editplanet(self, pname, distance, ptype, atmo, mass, radius, basetemp, pressure, mooncount, factionlist, lwater, rings, life, notes, surveyed, star):
        if self.distance != distance:
            self.distance = distance
            self.gzone = Planet.calcgzone(distance, star.inzone, star.outzone)
        self.basetemp = basetemp
        if ptype != self.ptype:
            self.ptype = ptype
            self.terrestrial = Planet.calcplanetcategory(self.ptype)
        self.lwater = lwater
        self.atmo = atmo
        if self.mass != mass or self.radius != radius:
            self.mass = mass
            self.radius = radius
            self.gravity = Planet.gengravity(self.radius, self.mass)
            self.relativeg = Planet.genrelativeg(self.radius, self.mass)
        self.rings = rings
        self.factions = factionlist
        self.notes = notes
        self.life = life
        self.pname = pname
        self.factions = factionlist
        self.surveyed = surveyed
        self.pressure = pressure
        if self.mooncount != mooncount:
            diff = mooncount - self.mooncount
            self.mooncount = mooncount
            if diff > 0:
                for i in range(self.mooncount, self.mooncount + diff):
                    self.moons.append(Planet.gennewmoon(pname, distance, self.gzone, i))
            else:
                for i in reversed(range(self.mooncount, self.mooncount + diff, -1)):
                    del self.moons[i]
        self.symbols = Planet.assemblesymbols(self.ptype, self.gzone, self.rings, self.lwater, self.life, self.mooncount)
        self.tooltip = Planet.buildtooltip(self.ptype, self.gzone, self.rings, self.lwater, self.life, self.mooncount)

    # For editing planet's temperature and gzone data if the host star's values have changed.
    def sunedit(self, star):
        self.gzone = Planet.calcgzone(self.distance, star.inzone, star.outzone)
        self.basetemp = Planet.calcbasetemp(self.distance, star.lum)
        self.symbols = Planet.assemblesymbols(self.ptype, self.gzone, self.rings, self.lwater, self.life, self.mooncount)
        self.tooltip = Planet.buildtooltip(self.ptype, self.gzone, self.rings, self.lwater, self.life, self.mooncount)
        
    def delmoon(self, moonnum):
        del self.moons[moonnum]
        self.mooncount -= 1
        for moon in self.moons:
            if moon.id > moonnum:
                moon.id -= 1

    def replacemoon(self, moonnum):
        self.moons[moonnum] = Planet.gennewmoon(self.pname, self.distance, self.gzone, moonnum)

    # Distance from star in AU
    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, distance):
        if distance < 0 or not isinstance(distance, (float, int)):
            raise ValueError(f"Invalid Planetary distance {distance}.")
        self._distance = distance

    @staticmethod
    def calcdistance(min, spacing):
        return round(random.uniform(min, min + spacing), 2)

    # Min is set in a loop while generating initial star size. 
    # This ensures that the new planet is the same relative distance from the sun in order to not make the planet jump around on the screen.
    @staticmethod
    def randomdistance(star, id):
        min = 0.0013
        target = id - 1
        if target > 0:
            min = star.solarobjects[target].distance
        return min

    # Finds the next highest distance to ensure that we don't place planets out of order
    # First checks to see if it's the last star on the list.
    @staticmethod
    def randomdistancelimit(star, id):
        if id == len(star.solarobjects) - 1:
            spacing = star.spacing
        else:
            spacing = star.solarobjects[id + 1].distance
            spacing -= spacing * .1
        return spacing
    
    # Goldilocks zone, the zone that "could" host life. Just takes in temperature, doesn't account for light spectrum or safe infrared distance, ect. 
    @property
    def gzone(self):
        return self._gzone

    @gzone.setter
    def gzone(self, gzone):
        if gzone not in Planet.gzonelist:
            raise ValueError(f"Invalid planet gzone {gzone}.")
        self._gzone = gzone
    
    @staticmethod
    def calcgzone(distance, inzone, outzone):
        if distance > inzone and distance < outzone:
            gzone = "right"
        elif distance < inzone:
            gzone = "hot"
        else:
            gzone = "cold"
        return gzone   

    # Planetary basetemp is not entirely accurate as it doesn't account for planet's albido, which is determined by atmosphere composition and surface. Nice to have in the future
    # TODO Incorporate albedo 
    @property
    def basetemp(self):
        return self._basetemp

    #Should be in K so no negatives
    @basetemp.setter
    def basetemp(self, basetemp):
        if not isinstance(basetemp, (int, float)) or basetemp < -273.15:
            raise ValueError(f"Invalid planet temp of {basetemp}.")
        self._basetemp = basetemp

    # Base temperature before any atmosphere math gets invovled.
    @staticmethod
    def calcbasetemp(distance, lum):
        return round((255 / ((distance / (lum)**0.5)**0.5)) - 273.15, 2)
    
    # Allows us to bucket planet types to make random a little easier. Useful for improved random in the future.
    @property
    def terrestrial(self):
        return self._terrestrial

    @terrestrial.setter
    def terrestrial(self, terrestrial):
        if not isbool(terrestrial):
            raise ValueError(f"Invalid terrestrial value {terrestrial}, must be bool.")
        self._terrestrial = terrestrial

    # Terrestrial accounts for solid planets, while False, counts for gas planets
    @staticmethod
    def genplanetcategory():
        if coin() == 1: 
            return True
        return False

    @staticmethod
    def calcplanetcategory(ptype):
        if ptype in ["chthonian", "gas dwarf", "gas giant", "helium", "puffy", "super-puff", "ice", "ice giant"]:
            return False
        return True
    
    # https://en.wikipedia.org/wiki/List_of_planet_types
    @property
    def ptype(self):
        return self._ptype

    @ptype.setter
    def ptype(self, ptype): 
        if ptype not in Planet.ptypelist:
            raise ValueError(f"Invalid planet type {ptype}.")
        self._ptype = ptype

    # Based on distance from sun, determines which planet types are possible for terrestrial or gas. Ice may not technically be a gas planet, but treating it like one due to size.
    @staticmethod
    def genplanettype(terrestrial, gzone):
        if terrestrial:
            if gzone == "right":
                typelist = ["carbon", "desert", "hycean", "iron", "ocean", "protoplanet", "silicate", "terrestrial"]
            if gzone == "hot":
                typelist = ["carbon", "desert", "iron", "lava", "protoplanet", "silicate", "terrestrial"]
            else:
                typelist = ["carbon", "coreless", "desert", "iron", "protoplanet", "silicate", "terrestrial"]
        else:
            if gzone == "hot":
                typelist = ["chthonian", "gas dwarf", "gas giant", "helium", "puffy", "super-puff"]
            elif gzone == "right":
                typelist = ["gas dwarf", "gas giant", "helium", "puffy", "super-puff"]
            else:
                typelist = ["gas dwarf", "gas giant", "helium", "ice", "ice giant"]
        return random.choice(typelist)

    # Liquid water, doesn't account for liquid water locked under ice or water with a high methane count keeping it liquid at subzero temperatures.
    @property
    def lwater(self):
        return self._lwater

    @lwater.setter
    def lwater(self, lwater):
        if not isbool(lwater):
            raise ValueError(f"Invalid liquid water value {lwater}, must be bool.")
        self._lwater = lwater


    # Atmosphere composition largely a placeholder at the moment until gas compositions can be incorporated. 
    # https://worldbuildingpasta.blogspot.com/2019/10/an-apple-pie-from-scratch-part-ivb.html#atmospheres
    @property
    def atmo(self):
        return self._atmo

    @atmo.setter
    def atmo(self, atmo):
        if atmo not in Planet.atmolist:
            raise ValueError(f"Invalid planet atmostphere {atmo}.")
        self._atmo = atmo

    # Mass relative to Earth Mass.
    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass):
        if mass < .03 or mass > 4132.78:
            raise ValueError(f"Invalid planet mass value {mass}.")
        self._mass = mass

    # Skimmed this article for quick math: https://worldbuildingpasta.blogspot.com/2019/10/an-apple-pie-from-scratch-part-ivb.html
    # TODO return to this when there's time to calculate atmosphere composition and materials
    # Returns Earth Mass
    @staticmethod
    def genmass(ptype):
        if ptype in ["carbon", "coreless", "desert", "ice", "iron", "lava", "protoplanet", "silicate", "terrestrial", "ocean"]:
            min = .03
            max = 2.04 # earth mass
        elif ptype in ["hycean", "ice giant", "gas dwarf", "helium", "puffy"]:
            min = 2.04
            max = 131.99
        else:
            min = 132
            max = 4132.78 # 13x size of Jupiter
        return round(random.uniform(min, max), 2)

    # Radius relative to Earth Radius.
    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        if not isinstance(radius, (int, float)):
            raise ValueError(f"Invalid planet radius value {radius}.")
        self._radius = radius

    # Returns Earth Radius
    @staticmethod
    def genradius(mass):
        if mass < 2.04:
            r = 1.008 * (mass**0.279)
        elif mass < 132:
            r = 0.808 * (mass**0.589)
        else:
            r = 17.745 * (mass**-0.044)
        return round(r, 2)

    # Planetary rings are currently just a fun thing and don't drive anything else.
    @property
    def rings(self):
        return self._rings

    @rings.setter
    def rings(self, rings):
        if not isbool(rings):
            raise ValueError(f"Invalid planetary rings value {rings}, must be bool.")
        self._rings = rings
    
    @staticmethod
    def genrings():
        r = random.randint(1, 100)
        if r > 90:
            return True
        return False
    
    # Currently don't remember why puff and super-puff are ineligible for moons, likely because they are not dense? Protoplanet can be anything, but for now assuming it's just a lifeless rock.
    @property
    def mooncandidate(self):
        return self._mooncandidate

    @mooncandidate.setter
    def mooncandidate(self, mooncandidate):
        if not isbool(mooncandidate):
            raise ValueError(f"Invalid planet moon candidate value {mooncandidate}, must be bool.")
        self._mooncandidate = mooncandidate

    @staticmethod
    def genmooncandidate(ptype):
        if ptype in ["puffy", "super-puff", "protoplanet"]:
            return False
        return True
    
    # While more than 20 moons is possible, too messy to display.
    @property
    def mooncount(self):
        return self._mooncount

    @mooncount.setter
    def mooncount(self, mooncount):
        if mooncount < 0 or mooncount > 20:
            raise ValueError(f"Invalid mooncount {mooncount}.")
        self._mooncount = mooncount
        
    # Smaller planets will have less moons. Radius numbers are based on max terrestrial size.
    @staticmethod
    def genmooncount(radius, mooncandidate):
        if not mooncandidate:
            return 0
        if radius < 2.04:
            if coin() == 1:
                mooncount = random.randint(0,4)
            else:
                mooncount = 0
        elif radius < 132:
            mooncount = random.randint(0,12)
        else:
            mooncount = random.randint(0,20)
        return mooncount
    
    @property
    def gravity(self):
        return self._gravity

    @gravity.setter
    def gravity(self, gravity):
        if not isinstance(gravity, (int, float)):
            raise ValueError(f"Invalid planet gravity value {gravity}.")
        self._gravity = gravity

    # Leaving here in case it is necessary later, but going to list relative gravity instead as that is more useful as a gaming reference.
    @staticmethod
    def gengravity(radius, mass):
        mass = mass * (5.9722 * 10**24) # Convert Earth Mass unit to KG
        radius = radius * (6.378 * 10**6) # Convert Earth Radius unit to M
        g = 6.67 * 10**-11
        grav = g * mass/(radius**2)
        return round(grav, 2)
    
    # Gravity as a % of Earth's gravity. 
    @property
    def relativeg(self):
        return self._relativeg

    @relativeg.setter
    def relativeg(self, relativeg):
        if not isinstance(relativeg, (int, float)):
            raise ValueError(f"Invalid planet relative gravity value {relativeg}.")
        self._relativeg = relativeg

    @staticmethod
    def genrelativeg(radius, mass):
        return round(mass/(radius**2), 2)
    
    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        if len(notes) > 999:
            raise ValueError(f"Faction notes are too long.")
        self._notes = notes

    # Currently no functionality related to life being present other than an increased chance it's populated. 
    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, life):
        if not isbool(life):
            raise ValueError(f"Invalid planet life value {life}, must be bool.")
        self._life = life

    # Determines if factions are present during generation.
    @property
    def populated(self):
        return self._populated

    @populated.setter
    def populated(self, populated):
        if not isbool(populated):
            raise ValueError(f"Invalid planet populated value {populated}, must be bool.")
        self._populated = populated

    # Planet Name
    @property
    def pname(self):
        return self._pname

    @pname.setter
    def pname(self, pname):
        if pname == "":
            raise ValueError("Missing planet name.")
        self._pname = pname

    # TODO Handle populated name from name lists.
    @staticmethod
    def genpname(populated=''):
        # LV, LV-KG, MT, RF
        if not populated:
            r = 426 
            while r == 426: # Prevents us from using Alien's most popular planet by mistake
                r = random.randint(1,999)
            flip = coin()
            prefix = ''
            if flip == 1:
                tlist = ["LV", "LV-KG", "MT", "RF"]
                prefix = random.choice(tlist)
            else:
                tlist = string.ascii_uppercase
                prefix = random.choice(tlist) + random.choice(tlist)
            return prefix + "-" + str(r)
        else:
            r = random.randint(1,999)
            return "Planet " + str(r) + " (Placeholder)"

    # Which factions are present on the planet. Up to 2.
    @property
    def factions(self):
        return self._factions

    @factions.setter
    def factions(self, factions):
        if factions != []:
            for faction in factions:
                if faction not in FactionList.factionlist:
                    raise ValueError(f"Invalid planetary faction {faction}.")
        self._factions = factions


    # How much has been explored. Never 100.
    @property
    def surveyed(self):
        return self._surveyed

    @surveyed.setter
    def surveyed(self, surveyed):
        if surveyed < 0 or surveyed > 100:
            raise ValueError(f"Invalid planet surveyed value {surveyed}.")
        self._surveyed = surveyed

    @staticmethod
    def genmoons(pname, mooncount, distance, gzone):
        moons = []
        for i in range(mooncount):
            moons.append(Planet.gennewmoon(pname, distance, gzone, i))
        return moons

    # Extra step to break this out so it can be shared by edit planet.
    @staticmethod
    def gennewmoon(pname, distance, gzone, number):
        return Moon.genrandommoon(pname, distance, gzone, number)

    # Pressure is currently mostly useless. Can determine accurately after atmospheres are fleshed out.
    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, pressure):
        if pressure not in Planet.pressurelist:
            raise ValueError(f"Invalid planet pressure {pressure}.")
        self._pressure = pressure
    

    # What to show for the planet row of HTML to save space.
    @staticmethod
    def assemblesymbols(ptype, gzone, rings, lwater, life, mooncount):
        symbols = Planet.typesymbol(ptype) + " " + Planet.gzonesymbol(gzone) + " "
        if rings:
            symbols += Planet.ringsymbol(rings) + " "
        if lwater:
            symbols += Planet.lwatersymbol(lwater) + " "
        if life:
            symbols += Planet.lifesymbol(life) + " "
        symbols += Planet.moonsymbol(mooncount)
        return symbols

    @staticmethod
    def lwatersymbol(lwater):
        symbol = ""
        if lwater == True:
            symbol = "🌢"
        return symbol

    @staticmethod
    def gzonesymbol(gzone):
        if gzone == "right":
            symbol = "⚖"
        elif gzone == "hot":
            symbol = "♨"
        else:
            symbol = "❄"
        return symbol

    @staticmethod
    def ringsymbol(rings):
        symbol = ""
        if rings == True:
            symbol = "⍉"
        return symbol

    @staticmethod
    def lifesymbol(life):
        symbol = ""
        if life == True:
            symbol = "🧬"
        return symbol

    @staticmethod
    def typesymbol(ptype):
        symbol = ""
        match ptype:
            case "chthonian":
                symbol = 'Ⓒ'
            case "carbon":
                symbol = 'ⓒ'
            case "coreless":
                symbol = "⊚"
            case "desert":
                symbol = "ⓓ"
            case "gas dwarf":
                symbol = "ⓖ"
            case "gas giant":
                symbol = "Ⓖ"
            case "helium":
                symbol = "ⓗ"
            case "hycean":
                symbol = "☵"
            case "ice giant":
                symbol = "Ⓘ"
            case "ice":
                symbol = "ⓘ"
            case "iron":
                symbol = "ⓕ"
            case "lava":
                symbol = "ⓛ"
            case "ocean":
                symbol = "䷜"
            case "protoplanet":
                symbol = "⨷"
            case "puffy":
                symbol = "ⓟ"
            case "super-puff":
                symbol = "Ⓟ"
            case "silicate":
                symbol = "ⓢ"
            case "terrestrial":
                symbol = "ⓣ"
        return symbol

    @staticmethod
    def moonsymbol(mooncount):
        symbol = ""
        match mooncount:
            case 0:
                symbol = "⓪"
            case 1:
                symbol = "①"
            case 2:
                symbol = "②"
            case 3:
                symbol = "③"
            case 4:
                symbol = "④"
            case 5:
                symbol = "⑤"
            case 6:
                symbol = "⑥"
            case 7:
                symbol = "⑦"
            case 8:
                symbol = "⑧"
            case 9:
                symbol = "⑨"
            case 10:
                symbol = "⑩"
            case 11:
                symbol = "⑪"
            case 12:
                symbol = "⑫"
            case 13:
                symbol = "⑬"
            case 14:
                symbol = "⑭"
            case 15:
                symbol = "⑮"
            case 16:
                symbol = "⑯"
            case 17:
                symbol = "⑰"
            case 18:
                symbol = "⑱"
            case 19:
                symbol = "⑲"
            case 20:
                symbol = "⑳"
        return symbol

    # HTML tooltip for the planet.
    @staticmethod
    def buildtooltip(ptype, gzone, rings, lwater, life, mooncount):
        tooltip = ptype + " Planet, "
        if gzone == "right":
            tooltip += "Goldilocks Zone, "
        elif gzone == "hot":
            tooltip += "before Goldilocks Zone, "
        else:
            tooltip += "beyond Goldilocks Zone, "
        if rings == True:
            tooltip += "Rings, "
        if lwater == True:
            tooltip += "Liquid Water, "
        if life == True:
            tooltip += "Life, "
        tooltip += str(mooncount) + " Moons"
        return tooltip

    def __str__(self):
        description = f"{self.pname} is a {self.ptype.title()} planet. \n"
        description += f"Mass: {self.mass}Me Radius: {self.radius}Re Distance: {self.distance}AU Relative Gravity: {self.relativeg} Pressure: {self.pressure.title()} Atmosphere: {self.atmo.title()} \n"
        description += f"Rings: {self.rings} Liquid Water: {self.lwater} Life: {self.life} Populated: {self.populated} Surevey Percentage: {self.surveyed}% \n"
        description += f"Your notes: {self.notes} \n"
        if len(self.factions) > 0:
            description += f"Factions: \n"
            for faction in self.factions:
                description += f"{faction.name} \n"
        description += f"Moon Count: {self.mooncount} \n"
        if self.mooncount > 0:
            for moon in self.moons:
                description += f"{moon} \n"
        return description


#initializeall()
#factions = Planet.gensettlementfaction(True)
#for faction in factions:
#    print(faction.name)