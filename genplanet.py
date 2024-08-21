import random, string
from helpers import coin

class Planet:
    def __init__(self, name, gzone, ptype):
        climate = ''
        temp = [] #min, mean, max
        atmosphere = ''
        life = ''
        biosphere = ''
        factions = []
        lwater = ''
        populated = ''
        self.pname = name
        size = ''
        rotation = ''
        period = ''
        moons = []
        rings = ''
        systemobjects = []
        self.ptype = ptype #Dwarf, gas, ect.
        gravity = ''
        self.gzone = gzone

    @property
    def pname(self):
        return self._pname

    @pname.setter
    def pname(self, pname):
        if not pname:
            pname = Planet.genpname()
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
            
    #Goldilocks zone - life possible        
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
    def ptype(self, ptype):
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


                