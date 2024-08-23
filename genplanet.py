import random, string
from helpers import coin
from load_initial import factionlist
from genmoon import Moon

class Planet:
    def __init__(self, name="", gzone="", ptype=""):
        climate = ''
        temp = [] #min, mean, max
        atmosphere = ''
        life = ''
        biosphere = ''
        self.factions = []
        lwater = ''
        populated = ''
        self.pname = name
        size = ''
        rotation = ''
        period = ''
        self.moons = []
        rings = ''
        self.systemobjects = []
        self.ptype = ptype #Dwarf, gas, ect.
        gravity = ''
        self.gzone = gzone
        Planet.setplanet(self, self.ptype)
        Planet.setlife(self)
        Planet.setmoons(self)

    @property
    def pname(self):
        return self._pname

    @pname.setter
    def pname(self, pname):
        if not pname:
            pname = Planet.genpname(self)
        self._pname = pname

    def genpname(self, populated=''):
        #LV, LV-KG, MT, RF
        if not populated:
            r = 426 
            while r == 426:
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
            
    #Goldilocks zone - life possible        https://www.planetarybiology.com/calculating_habitable_zone.html
    @property
    def gzone(self):
        return self._gzone
    
    @gzone.setter
    def gzone(self, gzone):
        if not isinstance(gzone, bool):
            flip = coin()
            if flip == 1:
                gzone = True
            else:
                gzone = False
        self._gzone = gzone

    @property
    def ptype(self):
        return self._ptype
    @ptype.setter
    def ptype(self, ptype): #https://en.wikipedia.org/wiki/List_of_planet_types
        tlist = ["Chthonian", "Carbon", "Coreless", "Desert", "Gas dwarf", "Gas giant", "Helium", "Hycean", "Ice giant", "Ice", "Iron", "Lava", "Ocean", "Protoplanet", "Puffy", "Super-puff", "Silicate", "Terrestrial"]
        if ptype not in tlist and ptype != '':
            raise ValueError("Invalid planet type.")
        if not ptype:
            ptype = random.choice(tlist)
        self._ptype = ptype

    #Define most of the planets characteristics based on the type of planet it is.
    #period
    #size
    #atmosphere
    #lwater - False if not possible, but break out in to other function to base it off of AU
    def buildplanet(self, ptype):
        if not ptype:
            raise ValueError("Planet type missing.")
        match ptype:
            case "Chthonian":
                period = random.random(.765, 3.5)
                mass = random.random(6.06, 39.09)
                density = '' #use equation r=cube root of 3m/4PIdensity mass to kg, radius to m, density to kg/m^3 https://worldbuilding.stackexchange.com/questions/125543/given-the-mass-and-composition-of-a-planet-can-one-determine-what-the-radius-sh
                lwater = False
            case "Carbon":
                period = random.randome(25, 98)
                mass = random.random(3.9)
                radius = random.random(1.5)

    #Temporary build for planets until time to come back to build planet.
    #lwater, sundistance, atmosphere, pressure, mooncandidate, rings, temperature, size
    def setplanet(self, ptype):
        if not ptype:
            raise ValueError("Planet type missing.")
        lwater = ""
        sundistance = ""
        atmosphere = ""
        pressure = "regular"
        mooncandidate = True
        rings = ""
        temperature = ""
        size = "any"
        match ptype:
            case "Chthonian":
                lwater = False
                sundistance = "close"
                atmosphere = "none"
                size = "giant"
            case "Carbon":
                sundistance = "any"
            case "Coreless":
                sundistance = "far"
                atmosphere = "none"
            case "Desert":
                sundistance = "any"
                atmosphere = "thin"
            case "Gas dwarf":
                sundistance = "any"
                atmosphere = "poison"
                size = "small"
            case "Gas giant":
                flip = coin()
                if flip == 1: #too close and it would be chthonian
                    sundistance = "medium"
                else:
                    sundistance = "far"
                atmosphere = "poison"
                lwater = False
                pressure = "high"
                size = "giant"
            case "Helium":
                lwater = False
                sundistance = "any"
                atmosphere = "poison"
            case "Hycean":
                lwater = True
                sundistance = "medium"
                atmosphere = "any"
            case "Ice giant":
                lwater = False
                sundistance = "far"
                atmosphere = "thin"
                pressure = "high"
                size = "giant"
            case "Ice":
                lwater = False
                sundistance = "far"
                atmosphere = "any"
            case "Iron":
                lwater = False
                sundistance = "any"
                atmosphere = "none"
            case "Lava":
                lwater = False
                sundistance = "close"
                atmosphere = "toxic"
            case "Ocean":
                lwater = True
                sundistance = "medium"
                atmosphere = "any"
            case "Protoplanet":
                lwater = False
                sundistance = "any"
                atmosphere = "none"
                mooncandidate = False
                rings = False
                size = "small"
            case "Puffy":
                lwater = False
                atmosphere = "toxic"
                sundistance = "any"
                mooncandidate = False
            case "Super-puff":
                lwater = False
                atmosphere = "toxic"
                sundistance = "any"
                pressure = "high"
                mooncandidate = False
            case "Silicate":
                atmosphere = "any"
                sundistance = "any"
            case "Terrestrial":
                atmosphere = "any"
                sundistance = "any"
        if sundistance == "any":
            flip = coin()
            if flip == 1:
                sundistance = "far"
            else:
                flip = coin()
                if flip == 1:
                    sundistance = "medium"
                else:
                    sundistance = "close"
        if sundistance == "medium":
            self.gzone = True
        else:
            self.gzone = False
        if lwater == "":
            if sundistance == "medium":
                lwater = True
            else:
                lwater = False
        if atmosphere == "any": #Alien core p332
            if sundistance != "medium":
                tlist = ["thin", "toxic", "dense", "corrosive", "infiltrating", "none"]
                atmosphere = random.choice(tlist)
            else:
                tlist = ["breathable", "thin", "toxic", "dense", "corrosive", "infiltrating", "none"]
                atmosphere = random.choice(tlist)
        if rings == "":
            r = random.randint(1, 100)
            if r > 90:
                rings = True
        if sundistance == "close":
            temperature = "hot"
        elif sundistance == "medium":
            if atmosphere != ("none" or "thin"):
                temperature = "medium"
            else:
                temperature = "cold"
        else:
            temperature = "cold"
        if size == ("" or "any"):
            tlist = ["small", "medium", "large", "giant"]
            size = random.choice(tlist)
        self.size = size
        self.temperature = temperature
        self.sundistance = sundistance
        self.lwater = lwater
        self.atmosphere = atmosphere
        self.mooncandidate = mooncandidate
        self.pressure = pressure

    def setlife(self):
        self.life = False
        if self.lwater == True and self.atmosphere == "breathable":
            flip = coin()
            if flip == 1:
                self.life = True
        if self.pressure != "high" or self.atmosphere != "dense" or self.atmosphere != "infiltrating":
            r = random.randint(1,100)
            if r > 60:
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
        
    def setmoons(self):
        if not self.mooncandidate:
            self.mooncount = 0
            return
        if self.size == ("small" or "medium"):
            mooncount = random.randint(0,4)
        elif self.size == ("large"):
            mooncount = random.randint(0,12)
        else:
            mooncount = random.randint(0,20)
        self.mooncount = mooncount
        for x in range(mooncount):
            self.moons.append(Moon(self.pname, self.sundistance, x + 1))

    
    def __str__(self):
        #smoon = ''
        #if self.mooncount > 0:
            #for moon in self.moons:
                #smoon += f"{moon.name}\n"
        return (f"{self.pname} is a {self.ptype} planet.\nSize: {self.size}\n Temp: {self.temperature}\nDist: {self.sundistance}\nWater: {self.lwater}\nLife: {self.life}\nMoons: {self.mooncount}\nFactions: {self.factions}")

#planet = Planet()
#print(planet)
