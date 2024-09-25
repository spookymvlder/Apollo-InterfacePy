import random
from genplanet import Planet
from genmoon import Moon
from helpers import skewvalue
from math import sqrt
from factions import FactionList
from savedobjects import StarList



# https://terraforming.fandom.com/wiki/Main_Sequence_A_Type_Stars_-_Habitable_Simulation
# Generates a star as well as its planets.
class Star:
    colorlist = ["white", "blue white", "blue", "yellow white", "yellow", "orange", "orange red", "red"]
    classlist = ["O", "B", "A", "F", "G", "K", "M"]
    sizelist = ["hypergiant", "supergiant", "bright giant", "giant", "subgiant", "dwarf", "subdwarf", "white dwarf"]

    def __init__(self, name, starclass, spectype, color, mass, radius, lum, startemp, notes, pcount, inzone, outzone, id, spacing, solarobjects):
        self.name = name
        self.starclass = starclass
        self.spectype = spectype
        self.color = color
        self.mass = mass
        self.radius = radius
        self.lum = lum
        self.startemp = startemp
        self.notes = notes
        self.pcount = pcount
        self.inzone = inzone
        self.outzone = outzone
        self.solarobjects = solarobjects
        self.id = id
        self.spacing = spacing
        
        
    @staticmethod
    def genrandomstar(name="", starclass="", spectype="", mass="", radius="", lum="", startemp="", notes="", pcount="", id=0, solarobjects=""):
        if name =="":
            name = Star.genname()
        if starclass == "":
            starclass = Star.genstarclass()
        if spectype == "":
            spectype = Star.genspectraltype(starclass)
        color = Star.genstarcolor(starclass, spectype)
        if mass == "":
            mass = Star.genstarmass(starclass, spectype)
        if radius == "":
            radius = Star.genstarradius(starclass, spectype)
        if lum == "":
            lum = Star.genstarlum(starclass, spectype)
        if startemp == "":
            startemp = Star.genstartemp(starclass, spectype)
        if pcount == "":
            pcount = Star.genplanetcount()
        inzone = Star.geninzone(lum)
        outzone = Star.genoutzone(lum)
        id = id
        spacing = Star.genspacing(pcount)
        if solarobjects == "": # Defaulting in an empty list was not properly clearing it, so need to default in "" and then overwrite that. 
            solarobjects = []
        solarobjects = Star.genplanet(pcount, spacing, inzone, outzone, startemp, mass, lum, solarobjects)
        return Star(name, starclass, spectype, color, mass, radius, lum, startemp, notes, pcount, inzone, outzone, id, spacing, solarobjects)
     
    def editstar(self, name, pcount, starclass, spectype, notes):
        self.name = name
        if not Star.validatestaredit(starclass, spectype):
            spectype = 3 # OK to force change here because user warned as tooltip. TODO Ideally this could be handled client side.
        if self.starclass != starclass or self.spectype != spectype:
            self.starclass = starclass
            self.spectype = spectype
            self.color = Star.genstarcolor(self.starclass, self.spectype)
            self.mass = Star.genstarmass(self.starclass, self.spectype)
            self.radius = Star.genstarradius(self.starclass, self.spectype)
            self.lum = Star.genstarlum(self.starclass, self.spectype)
            self.startemp = Star.genstartemp(self.starclass, self.spectype)
            self.inzone = Star.geninzone(self.lum)
            self.outzone = Star.genoutzone(self.lum)
            for planet in self.solarobjects:
                Planet.sunedit(planet, self)
        self.notes = notes
        if self.pcount != pcount:
            diff = pcount - self.pcount
            self.pcount = pcount
            self.spacing = Star.genspacing(self.pcount)
            if diff > 0:
                for i in range(self.pcount, self.pcount + diff):
                    self.solarobjects.append(Planet.genplanetfromstar(self.inzone, self.outzone, Planet.randomdistance(self, i), self.startemp, self.mass, self.lum, Planet.randomdistancelimit(self, i), i))
            else:
                for i in reversed(range(self.pcount, self.pcount + diff, -1)):
                    del self.solarobjects[i]

    @staticmethod
    def unpackstarfromload(stars):
        StarList.starlist.clear()
        for star in stars:
            planets = []
            for planet in star["solarobjects"]:
                moons = []
                for moon in planet["moons"]:
                    factions = []
                    for faction in moon["factions"]:
                        factions.append(FactionList.getclassfromid(faction))
                    moons.append(Moon(moon["pname"], moon["gzone"], moon["id"], moon["name"], moon["mtype"], moon["lwater"], moon["atmo"], moon["life"], moon["populated"], 
                    factions, moon["systemobjects"], moon["surveyed"], moon["pressure"]))
                factions = []
                for faction in planet["factions"]:
                    factions.append(FactionList.getclassfromid(faction))
                planets.append(Planet(planet["distance"], planet["gzone"], planet["basetemp"], planet["terrestrial"], planet["ptype"], planet["lwater"], planet["atmo"], planet["mass"], 
                planet["radius"], planet["rings"], planet["mooncandidate"], planet["mooncount"], planet["gravity"], planet["relativeg"], planet["notes"], planet["life"], planet["populated"],
                planet["pname"], factions, planet["surveyed"], planet["pressure"], planet["settlements"], moons, planet["id"]))
            StarList.starlist.append(Star(star["name"], star["starclass"], star["spectype"], star["color"], star["mass"], star["radius"], star["lum"], star["startemp"], star["notes"], 
            star["pcount"], star["inzone"], star["outzone"], star["id"], star["spacing"], planets))
            if StarList.masterid <= star["id"]:
                StarList.masterid = star["id"] + 1
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name == "" or not isinstance(name, str):
            raise ValueError("Star name required.")
        self._name = name

    @staticmethod
    def genname():
        classifications = ["LAL", "BD", "HD", "BS", "SAO", "USNO", "GSC", "PPM", "HIP", "GI", "GCTP", "HAT", "WASP", "XO"]
        convention = random.choice(classifications)
        match convention:
            case "LAL":
                r = random.randint(1,47390)
                name = convention + " " + str(r)
            case "BD":
                classifications = ["BD", "SD", "CD", "CP"]
                convention = random.choice(classifications)
                match convention:
                    case "BD":
                        r = random.randint(0, 90)
                        s = random.randint(1, 32000)
                    case "SD":
                        r = random.randint(1, 23)
                        s = random.randint(1, 12000)
                    case "CD":
                        r = random.randint(22, 90)
                        s = random.randint(1,58000)
                    case "CP":
                        r = random.randint(18, 90)
                        s = random.randint(1, 45000)
                if convention == "BD":
                    name = convention + "+" + str(r) + "°" + str(s)
                else:
                    name = convention + "-" + str(r) + "°" + str(s)
            case "HD":
                r = random.randint(1, 359083)
                if r < 225301:
                    name = "HD " + str(r)
                elif r < 272151:
                    name = "HDE " + str(r)
                else:
                    name = "HDEC " + str(r)
            case "BS":
                r = random.randint(1, 9110)
                name = "BS " + str(r)
            case "SAO":
                r = random.randint(1, 258997)
                name = "SAO " + str(r)
            case "USNO":
                classifications = ["USNO-B1.0", "USNO UACAC3", "USNO UCAC2", "USNO-A2.0", "USNO-SA2.0", "USNO-A1.0", "USNO-SA1.0"]
                convention = random.choice(classifications)
                r = random.randint(1000, 9999)
                s = random.randint(1, 99999999)
                s = str(s)
                l = len(s)
                while l < 9:
                    s = "0" + s
                    l += 1
                name = convention + " " + str(r) + "." + s
            case "GSC":
                r = random.randint(1, 99999)
                s = random.randint(1, 99999)
                r = str(r)
                l = len(r)
                while l < 5:
                    r = "0" + r
                    l += 1
                s = str(s)
                l = len(s)
                while l < 5:
                    s = "0" + s
                    l += 1
                name = convention + r + "-" + s
            case "PPM":
                r = random.randint(1, 99999)
                name = "PPM " + str(r)
            case "HIP":
                r = random.randint(1, 118218)
                name = "HIP " + str(r)
            case "GI":
                r = random.randint(1,9850)
                if r > 9000 and r < 9851:
                    convention = "Wo "
                elif (r > 999 and r < 1295) or (r > 2000 and r < 2160):
                    convention = "GJ "
                else:
                    convention = "GI "
                name = convention + str(r)
            case "GCTP":
                r = random.randint(1,9000)
                name = convention + " " + str(r)
            case "HAT":
                classifications = ["HAT-P", "HATS"]
                convention = random.choice(classifications)
                r = random.randint(1,999)
                name = convention + "-" + str(r)
            case "WASP":
                r = random.randint(1,500)
                name = convention + "-" + str(r)
            case "XO":
                r = random.randint(1,40)
                name = convention + "-" + str(r)
        return name

    @property
    def starclass(self):
        return self._starclass

    @starclass.setter
    def starclass(self, starclass):
        if starclass not in Star.classlist:
            raise ValueError(f"Invalid star class {starclass}.")
        self._starclass = starclass

    #The distribution here turned out to be not terribly interesting.
    @staticmethod
    def genstarclass():
        '''r = random.uniform(0, 100)
        if r <= .03:
            starclass = "O"
        elif r <= .15:
            starclass = "B"
        elif r <= .76:
            starclass = "A"
        elif r <= 3.76:
            starclass = "F"
        elif r <= 11.36:
            starclass = "G"
        elif r <= 23.36:
            starclass = "K"
        elif r <= 99.36:
            starclass = "M"'''
        return random.choice(Star.classlist)


    # Class and Color are related, so providing a way to get the remaining star details based on each depending on user.
    @staticmethod
    def genstarclassfromcolor(color):
        match color:
            case "blue":
                starclass = "O"
            case "blue white":
                starclass = "B"
            case "white":
                starclass = "A"
            case "yellow white":
                starclass = "F"
            case "yellow":
                starclass = "G"
            case "orange":
                starclass = "K"
            case "orange red" | "red":
                starclass = "M"
        return starclass

    @property
    def spectype(self):
        return self._spectype

    @spectype.setter
    def spectype(self, spectype):
        if spectype < 0 or spectype > 9:
            raise ValueError(f"Invalid star spectral type {spectype}.")
        self._spectype = spectype

    @staticmethod
    def genspectraltype(starclass):
        if starclass == "O":
            spectype = random.randint(3,9)
        else:
            spectype = random.randint(0,9)
        return spectype
    
    # Changing spectral type and class will always have one changed before the other, allows for both to be changed simultaneously without worrying about race conditions.
    @staticmethod
    def validatestaredit(starclass, spectype):
        if starclass == "O":
            if spectype < 3:
                return False
        return True

    @property
    def starcolor(self):
        return self._starcolor

    @starcolor.setter
    def starcolor(self, starcolor):
        if starcolor not in Star.colorlist:
            raise ValueError(f"Invalid star color {starcolor}.")
        self._starcolor = starcolor

    @staticmethod
    def genstarcolor(starclass, spectype):
        match starclass:
            case "O":
                color = "blue"
            case "B":
                color = "blue white"
            case "A":
                color = "white"
            case "F":
                color = "yellow white"
            case "G":
                color = "yellow"
            case "K":
                color = "orange"
            case "M":
                if spectype < 5:
                    color = "orange red"
                else:
                    color = "red"
        return color

    @property
    def starmass(self):
        return self._starmass

    @starmass.setter
    def starmass(self, starmass):
        if not isinstance(starmass, (int, float)):
            raise ValueError(f"Invalid star mass {starmass}.")
        self._starmass = starmass

    # Returns solar mass M, 1M = 1.988416 x 10^30 kg
    # Details from links in classifciation page. Some guesstimating being done to avoid big brain math. https://en.wikipedia.org/wiki/Main_sequence#Sample_parameters
    @staticmethod
    def genstarmass(starclass, spectype):
        mass = ""
        match starclass:
            case "O": # https://en.wikipedia.org/wiki/O-type_main-sequence_star
                match spectype:
                    case 3:
                        mass = 120.00
                    case 4:
                        mass = 85.31
                    case 5:
                        mass = 60.00
                    case 6:
                        mass = 43.71
                    case 7:
                        mass = 30.85
                    case 8:
                        mass = 23.00
                    case 9:
                        mass = 19.63
            case "B": # https://en.wikipedia.org/wiki/B-type_main-sequence_star
                match spectype:
                    case 0:
                        mass = 17.70
                    case 1:
                        mass = 11.00
                    case 2:
                        mass = 7.30
                    case 3:
                        mass = 5.4
                    case 4:
                        mass = 5.1
                    case 5:
                        mass = 4.7
                    case 6:
                        mass = 4.3
                    case 7:
                        mass = 3.92
                    case 8:
                        mass = 3.38
                    case 9:
                        mass = 2.75
            case "A": # https://en.wikipedia.org/wiki/A-type_main-sequence_star
                match spectype:
                    case 0:
                        mass = 2.18
                    case 1:
                        mass = 2.05
                    case 2:
                        mass = 1.98
                    case 3:
                        mass = 1.93
                    case 4:
                        mass = 1.88
                    case 5:
                        mass = 1.86
                    case 6:
                        mass = 1.83
                    case 7:
                        mass = 1.81
                    case 8:
                        mass = 1.77
                    case 9:
                        mass = 1.75
            case "F": # https://en.wikipedia.org/wiki/F-type_main-sequence_star
                match spectype:
                    case 0:
                        mass = 1.61
                    case 1:
                        mass = 1.50
                    case 2:
                        mass = 1.46
                    case 3:
                        mass = 1.44
                    case 4:
                        mass = 1.38
                    case 5:
                        mass = 1.33
                    case 6:
                        mass = 1.25
                    case 7:
                        mass = 1.21
                    case 8:
                        mass = 1.18
                    case 9:
                        mass = 1.13
            case "G": # https://en.wikipedia.org/wiki/G-type_main-sequence_star
                match spectype:
                    case 0:
                        mass = 1.06
                    case 1:
                        mass = 1.03
                    case 2:
                        mass = 1.0
                    case 3:
                        mass = 0.99
                    case 4:
                        mass = 0.985
                    case 5:
                        mass = 0.98
                    case 6:
                        mass = 0.97
                    case 7:
                        mass = 0.95
                    case 8:
                        mass = 0.94
                    case 9:
                        mass = 0.9
            case "K": # https://en.wikipedia.org/wiki/K-type_main-sequence_star
                match spectype:
                    case 0:
                        mass = 0.88
                    case 1:
                        mass = 0.86
                    case 2:
                        mass = 0.82
                    case 3:
                        mass = 0.78
                    case 4:
                        mass = 0.73
                    case 5:
                        mass = 0.70
                    case 6:
                        mass = 0.69
                    case 7:
                        mass = 0.64
                    case 8:
                        mass = 0.62
                    case 9:
                        mass = 0.59
            case "M": # https://en.wikipedia.org/wiki/Red_dwarf
                match spectype:
                    case 0:
                        mass = 0.57
                    case 1:
                        mass = 0.50
                    case 2:
                        mass = 0.44
                    case 3:
                        mass = 0.37
                    case 4:
                        mass = 0.23
                    case 5:
                        mass = 0.162
                    case 6:
                        mass = 0.102
                    case 7:
                        mass = 0.09
                    case 8:
                        mass = 0.085
                    case 9:
                        mass = 0.079
        return round(skewvalue(mass), 5)

    @property
    def starradius(self):
        return self._starradius

    @starradius.setter
    def starradius(self, starradius):
        if not isinstance(starradius, (int, float)):
            raise ValueError(f"Invalid star radius {starradius}.")
        self._starradius = starradius

    # Returns solar radius R, 1R = 6.957 x 10^8 m
    @staticmethod
    def genstarradius(starclass, spectype):
        radius = ""
        match starclass:
            case "O": # https://en.wikipedia.org/wiki/O-type_main-sequence_star
                match spectype:
                    case 3:
                        radius = 15.00
                    case 4:
                        radius = 13.43
                    case 5:
                        radius = 12.00
                    case 6:
                        radius = 10.71
                    case 7:
                        radius = 9.52
                    case 8:
                        radius = 8.5
                    case 9:
                        radius = 7.51
            case "B": # https://en.wikipedia.org/wiki/B-type_main-sequence_star
                match spectype:
                    case 0:
                        radius = 7.16
                    case 1:
                        radius = 5.71
                    case 2:
                        radius = 4.06
                    case 3:
                        radius = 3.61
                    case 4:
                        radius = 3.46
                    case 5:
                        radius = 3.36
                    case 6:
                        radius = 3.27
                    case 7:
                        radius = 2.94
                    case 8:
                        radius = 2.86
                    case 9:
                        radius = 2.49
            case "A": # https://en.wikipedia.org/wiki/A-type_main-sequence_star
                match spectype:
                    case 0:
                        radius = 2.193
                    case 1:
                        radius = 2.136
                    case 2:
                        radius = 2.117
                    case 3:
                        radius = 1.861
                    case 4:
                        radius = 1.794
                    case 5:
                        radius = 1.785
                    case 6:
                        radius = 1.775
                    case 7:
                        radius = 1.750
                    case 8:
                        radius = 1.748
                    case 9:
                        radius = 1.747
            case "F": # https://en.wikipedia.org/wiki/F-type_main-sequence_star
                match spectype:
                    case 0:
                        radius = 1.728
                    case 1:
                        radius = 1.679
                    case 2:
                        radius = 1.622
                    case 3:
                        radius = 1.578
                    case 4:
                        radius = 1.533
                    case 5:
                        radius = 1.473
                    case 6:
                        radius = 1.359
                    case 7:
                        radius = 1.324
                    case 8:
                        radius = 1.221
                    case 9:
                        radius = 1.167
            case "G": # https://en.wikipedia.org/wiki/G-type_main-sequence_star
                match spectype:
                    case 0:
                        radius = 1.1
                    case 1:
                        radius = 1.060
                    case 2:
                        radius = 1.012
                    case 3:
                        radius = 1.002
                    case 4:
                        radius = 0.991
                    case 5:
                        radius = 0.977
                    case 6:
                        radius = 0.949
                    case 7:
                        radius = 0.927
                    case 8:
                        radius = 0.914
                    case 9:
                        radius = 0.853
            case "K": # https://en.wikipedia.org/wiki/K-type_main-sequence_star
                match spectype:
                    case 0:
                        radius = 0.813
                    case 1:
                        radius = 0.797
                    case 2:
                        radius = 0.783
                    case 3:
                        radius = 0.755
                    case 4:
                        radius = 0.713
                    case 5:
                        radius = 0.701
                    case 6:
                        radius = 0.669
                    case 7:
                        radius = 0.630
                    case 8:
                        radius = 0.615
                    case 9:
                        radius = 0.608
            case "M": # https://en.wikipedia.org/wiki/Red_dwarf
                match spectype:
                    case 0:
                        radius = 0.588
                    case 1:
                        radius = 0.501
                    case 2:
                        radius = 0.446
                    case 3:
                        radius = 0.361
                    case 4:
                        radius = 0.274
                    case 5:
                        radius = 0.196
                    case 6:
                        radius = 0.137
                    case 7:
                        radius = 0.12
                    case 8:
                        radius = 0.114
                    case 9:
                        radius = 0.102
        return round(skewvalue(radius), 5)

    @property
    def starlum(self):
        return self._starlum

    @starlum.setter
    def starlum(self, starlum):
        if not isinstance(starlum, (int, float)):
            raise ValueError(f"Invalid star luminosity {starlum}.")
        self._starlum = starlum

    # Returns absolute luminosity L
    @staticmethod
    def genstarlum(starclass, spectype):
        lum = ""
        match starclass:
            case "O": # https://en.wikipedia.org/wiki/O-type_main-sequence_star
                match spectype:
                    case 3:
                        lum = 1400000
                    case 4:
                        lum = 1073019
                    case 5:
                        lum = 790000
                    case 6:
                        lum = 540422
                    case 7:
                        lum = 317322
                    case 8:
                        lum = 170000
                    case 9:
                        lum = 92762
            case "B": # https://en.wikipedia.org/wiki/B-type_main-sequence_star
                match spectype:
                    case 0:
                        lum = 44668
                    case 1:
                        lum = 13490
                    case 2:
                        lum = 2692
                    case 3:
                        lum = 977
                    case 4:
                        lum = 776
                    case 5:
                        lum = 589
                    case 6:
                        lum = 372
                    case 7:
                        lum = 302
                    case 8:
                        lum = 155
                    case 9:
                        lum = 72
            case "A": # https://en.wikipedia.org/wiki/A-type_main-sequence_star
                match spectype:
                    case 0:
                        lum = 38.02
                    case 1:
                        lum = 30.90
                    case 2:
                        lum = 23.99
                    case 3:
                        lum = 16.98
                    case 4:
                        lum = 13.49
                    case 5:
                        lum = 12.30
                    case 6:
                        lum = 11.22
                    case 7:
                        lum = 10.00
                    case 8:
                        lum = 9.12
                    case 9:
                        lum = 8.32
            case "F": # https://en.wikipedia.org/wiki/F-type_main-sequence_star
                match spectype:
                    case 0:
                        lum = 7.24
                    case 1:
                        lum = 7.24
                    case 2:
                        lum = 5.13
                    case 3:
                        lum = 4.68
                    case 4:
                        lum = 4.17
                    case 5:
                        lum = 3.63
                    case 6:
                        lum = 2.69
                    case 7:
                        lum = 2.45
                    case 8:
                        lum = 1.95
                    case 9:
                        lum = 1.66
            case "G": # https://en.wikipedia.org/wiki/G-type_main-sequence_star
                match spectype:
                    case 0:
                        lum = 1.35
                    case 1:
                        lum = 1.2
                    case 2:
                        lum = 1.02
                    case 3:
                        lum = 0.98
                    case 4:
                        lum = 0.91
                    case 5:
                        lum = 0.89
                    case 6:
                        lum = 0.79
                    case 7:
                        lum = 0.74
                    case 8:
                        lum = 0.68
                    case 9:
                        lum = 0.55
            case "K": # https://en.wikipedia.org/wiki/K-type_main-sequence_star
                match spectype:
                    case 0:
                        lum = 0.46
                    case 1:
                        lum = 0.41
                    case 2:
                        lum = 0.37
                    case 3:
                        lum = 0.28
                    case 4:
                        lum = 0.20
                    case 5:
                        lum = 0.17
                    case 6:
                        lum = 0.14
                    case 7:
                        lum = 0.10
                    case 8:
                        lum = 0.087
                    case 9:
                        lum = 0.079
            case "M": # https://en.wikipedia.org/wiki/Red_dwarf
                match spectype:
                    case 0:
                        lum = 0.069
                    case 1:
                        lum = 0.041
                    case 2:
                        lum = 0.029
                    case 3:
                        lum = 0.016
                    case 4:
                        lum = 0.0072
                    case 5:
                        lum = 0.003
                    case 6:
                        lum = 0.001
                    case 7:
                        lum = 0.00065
                    case 8:
                        lum = 0.00052
                    case 9:
                        lum = 0.0003
        return round(skewvalue(lum), 5)

    @property
    def startemp(self):
        return self._startemp

    @startemp.setter
    def startemp(self, startemp):
        if not isinstance(startemp, (int, float)):
            raise ValueError(f"Invalid star temperature {startemp}.")
        self._startemp = startemp

    # Returns temperature K
    @staticmethod
    def genstartemp(starclass, spectype):
        startemp = ""
        match starclass:
            case "O": # https://en.wikipedia.org/wiki/O-type_main-sequence_star
                match spectype:
                    case 3:
                        startemp = 44900
                    case 4:
                        startemp = 42900
                    case 5:
                        startemp = 41400
                    case 6:
                        startemp = 39500
                    case 7:
                        startemp = 37100
                    case 8:
                        startemp = 35100
                    case 9:
                        startemp = 33300
            case "B": # https://en.wikipedia.org/wiki/B-type_main-sequence_star
                match spectype:
                    case 0:
                        startemp = 31400
                    case 1:
                        startemp = 26000
                    case 2:
                        startemp = 20600
                    case 3:
                        startemp = 17000
                    case 4:
                        startemp = 16400
                    case 5:
                        startemp = 15700
                    case 6:
                        startemp = 14500
                    case 7:
                        startemp = 14000
                    case 8:
                        startemp = 12300
                    case 9:
                        startemp = 10700
            case "A": # https://en.wikipedia.org/wiki/A-type_main-sequence_star
                match spectype:
                    case 0:
                        startemp = 9700
                    case 1:
                        startemp = 9300
                    case 2:
                        startemp = 8800
                    case 3:
                        startemp = 8600
                    case 4:
                        startemp = 8250
                    case 5:
                        startemp = 8100
                    case 6:
                        startemp = 7910
                    case 7:
                        startemp = 7760
                    case 8:
                        startemp = 7590
                    case 9:
                        startemp = 7400
            case "F": # https://en.wikipedia.org/wiki/F-type_main-sequence_star
                match spectype:
                    case 0:
                        startemp = 7220
                    case 1:
                        startemp = 7220
                    case 2:
                        startemp = 6820
                    case 3:
                        startemp = 6750
                    case 4:
                        startemp = 6670
                    case 5:
                        startemp = 6550
                    case 6:
                        startemp = 6350
                    case 7:
                        startemp = 6280
                    case 8:
                        startemp = 6180
                    case 9:
                        startemp = 6050
            case "G": # https://en.wikipedia.org/wiki/G-type_main-sequence_star
                match spectype:
                    case 0:
                        startemp = 5930
                    case 1:
                        startemp = 5860
                    case 2:
                        startemp = 5770
                    case 3:
                        startemp = 5720
                    case 4:
                        startemp = 5680
                    case 5:
                        startemp = 5660
                    case 6:
                        startemp = 5600
                    case 7:
                        startemp = 5550
                    case 8:
                        startemp = 5480
                    case 9:
                        startemp = 5380
            case "K": # https://en.wikipedia.org/wiki/K-type_main-sequence_star
                match spectype:
                    case 0:
                        startemp = 5270
                    case 1:
                        startemp = 5170
                    case 2:
                        startemp = 5100
                    case 3:
                        startemp = 4830
                    case 4:
                        startemp = 4600
                    case 5:
                        startemp = 4440
                    case 6:
                        startemp = 4300
                    case 7:
                        startemp = 4100
                    case 8:
                        startemp = 3990
                    case 9:
                        startemp = 3930
            case "M": # https://en.wikipedia.org/wiki/Red_dwarf
                match spectype:
                    case 0:
                        startemp = 3850
                    case 1:
                        startemp = 3660
                    case 2:
                        startemp = 3560
                    case 3:
                        startemp = 3430
                    case 4:
                        startemp = 3210
                    case 5:
                        startemp = 3060
                    case 6:
                        startemp = 2810
                    case 7:
                        startemp = 2680
                    case 8:
                        startemp = 2570
                    case 9:
                        startemp = 2380
        return round(skewvalue(startemp), 5)

    @property
    def pcount(self):
        return self._pcount

    @pcount.setter
    def pcount(self, pcount):
        if pcount < 0 or pcount > 13:
            raise ValueError(f"Invalid planet count {pcount}.")
        self._pcount = pcount

    # Any more than 13 would be unweildy. Percentages based on one of the observed catalogues returned by this study: https://academic.oup.com/mnras/article/490/4/4575/5613397?login=false 
    # Admittedly the percents here don't take in to account star size or class.
    @staticmethod
    def genplanetcount():
        r = random.randint(1, 86760)
        if r < 7103:
            pcount = 0
        elif r < 22142:
            pcount = 1
        elif r < 41100:
            pcount = 2
        elif r < 57765:
            pcount = 3
        elif r < 69929:
            pcount = 4
        elif r < 77732:
            pcount = 5
        elif r < 82417:
            pcount = 6
        elif r < 84856:
            pcount = 7
        elif r < 85950:
            pcount = 8
        elif r < 86480:
            pcount = 9
        elif r < 86645:
            pcount = 10
        elif r < 86728:
            pcount = 11
        elif r < 86752:
            pcount = 12
        else:
            pcount = 13
        return pcount

    
    @property
    def inzone(self):
        return self._inzone

    @inzone.setter
    def inzone(self, inzone):
        if not isinstance(inzone, (int, float)):
            raise ValueError(f"Invalid star hab zone inner radius {inzone}.")
        self._inzone = inzone

    # Returns AU
    # https://www.planetarybiology.com/calculating_habitable_zone.html
    @staticmethod
    def geninzone(lum):
        return round(sqrt(lum / 1.1), 4)
    
    @property
    def outzone(self):
        return self._outzone
    @outzone.setter
    def outzone(self, outzone):
        if not isinstance(outzone, (int, float)):
            raise ValueError(f"Invalid star hab zone outer radius {outzone}.")
        self._outzone = outzone

    # Returns AU
    # https://www.planetarybiology.com/calculating_habitable_zone.html
    @staticmethod
    def genoutzone(lum):
        return round(sqrt(lum / 0.53), 4)

    @property
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, spacing):
        if spacing < 0:
            raise ValueError(f"Invalid planet spacing {spacing}.")
        self._spacing = spacing
    
    # TODO figure out a way to make spacing interesting, right now seems to cluster as cold planets.
    # Pluto is 40 AU at its furthest, anything beyone that is in the darkness of space and while it may be interesting, hard to account for.
    @staticmethod
    def genspacing(pcount):
        if pcount != 0:
            spacing = 40 / pcount
        else:
            spacing = 40
        return round(spacing, 4)
    
    # Generates a new planet based on characteristics of the sun.
    @staticmethod
    def genplanet(pcount, spacing, inzone, outzone, startemp, starmass, lum, solarobjects=[]):
        min = 0.0013
        for i in range(pcount):
            planet = Planet.genplanetfromstar(inzone, outzone, min, startemp, starmass, lum, spacing, i)
            min = planet.distance
            solarobjects.append(planet)
        return solarobjects

    # Removes planet from solar objects list. 
    # TODO make update to planet ids more efficient.
    def delplanet(self, planetid):
        del self.solarobjects[planetid]
        for planet in self.solarobjects:
            if planet.id > planetid:
                planet.id -= 1
        
    def __str__(self):
        description = f"Star system {self.name} is a {self.color} class {self.starclass}{self.spectype} star. \n"
        description += f"Mass: {self.mass} Radius: {self.radius} Luminosity: {self.lum} Temperature: {self.startemp} \n"
        description += f"Planets: {self.pcount} \n"
        description += f"Your notes: {self.notes} \n"
        if self.pcount > 0:
            description += f"Planets: \n"
            for planet in self.solarobjects:
                description += f"{planet} \n"
        return description