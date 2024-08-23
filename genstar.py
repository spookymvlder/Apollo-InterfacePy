import random
from genplanet import Planet
#Define star type and number

#Define planet type https://en.wikipedia.org/wiki/List_of_planet_types https://astronomy.stackexchange.com/questions/13165/what-is-the-frequency-distribution-for-luminosity-classes-in-the-milky-way-galax 
# https://academic.oup.com/mnras/article/490/4/4575/5613397?login=false
'''Ia0     16     0.03%
Ia     241     0.43%
Iab    191     0.34%
Ib     694     1.23%
I       17     0.03%
II    1627     2.89%
III  22026    39.13%
IV    6418    11.40%
V    24873    44.19%
VI      92     0.16%
VII     89     0.16%'''


#Define celestial objects
#Flesh out planet

#Main sequence stars may be all we care about

class Star:
    def __init__(self, name=False, type=False, color=False):
        self.name = Star.genname(self, name)
        self.color = Star.gencolor(self, color)
        self.type = Star.gentype(self, type)
        self.solarobjects = []
        self.size = Star.gensize(self, self.type, self.color)
        self.pcount = Star.planetcount(self)
        Star.genplanet(self, self.pcount)

    def gensize(self, type, color):
        size = ""
        match type:
            case "0":
                size = "hypergiant"
            case "Ia" | "Iab" | "Ib":
                size = "supergiant"
            case "II":
                size = "bright giant"
            case "III":
                size = "giant"
            case "IV":
                size = "subgiant"
            case "V":
                size = "dwarf"
            case "VI":
                size = "subdwarf"
            case "VII":
                size = "white dwarf"
                if color != "white":
                    self.color = "white"
        return size

    def genplanet(self, pcount):
        if pcount != 0:
            for i in range(pcount):
                self.solarobjects.append(Planet())


    def gencolor(self, color):
        colors = ["white", "blueish white", "blue", "yellow white", "yellow", "light orange", "orange", "orangish red", "red"]
        if color in colors:
            return color
        return random.choice(colors)

    def genname(self, name):
        if name:
            return name
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

    def gentype(self, type):
        types = ["0", "Ia", "Iab", "Ib", "I", "II", "III", "IV", "V", "VI", "VII"]
        if type not in types:
            r = random.uniform(0, 100)
            if r <= .03:
                type = "0"
            elif r <= .46:
                type = "Ia"
            elif r <= .8:
                type = "Iab"
            elif type <= 2.03:
                type = "Ib"
            elif type <= 2.06:
                type = "I"
            elif type <= 4.95:
                type = "II"
            elif type <= 44.08:
                type = "III"
            elif type <= 55.48:
                type = "IV"
            elif type <= 99.67:
                type = "V"
            elif type <= 99.83:
                type = "VI"
            else:
                type = "VII"
        return type

    def planetcount(self):
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
    

    #https://en.wikipedia.org/wiki/O-type_main-sequence_star
    #https://en.wikipedia.org/wiki/Main_sequence#Sample_parameters
    #Maybe use for something, easy radius could be used for habitable zones
    def spectraltypeo(self):
        r = random.randint(1,7)
        match r:
            case 1:
                mass = 120
                radius = 15
                lum = 1400000
                temp = 44900
                colorindex = -0.330
            case 2:
                mass = 85.31
                radius = 13.43
                lum = 1073019
                temp = 42900
                colorindex = -0.326
            case 3:
                mass = 60.00
                radius = 12.00
                lum = 790000
                temp = 41400
                colorindex = -0.323
            case 4:
                mass = 43.71
                radius = 10.71
                lum = 540422
                temp = 39500
                colorindex = -0.321
            case 5:
                mass = 30.85
                radius = 9.52
                lum = 317322
                temp = 37100
                colorindex = -0.318
            case 6:
                mass = 23.00
                radius = 8.5
                lum = 170000
                temp = 35100
                colorindex = -0.315
            case 7:
                mass = 19.63
                radius = 7.51
                lum = 92762
                temp = 33300
                colorindex = -0.312


    def __str__(self):
        planetd = ""
        if self.pcount != 0:
            for planet in self.solarobjects:
                planetd += f"{planet.pname}, "
        return f"A {self.color} star named {self.name}. It has {self.pcount} planet(s) named:\n{planetd}"
    
#star = Star()
#print(star)