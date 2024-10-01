import random
from helpers import coin, heshe
from gennpc import Npc
from namelists import CatNames
from savedobjects import CatList


# Cat data taken from link below, doesn't account for chances or actual breeds of cat. That way lies madness.
# https://www.reddit.com/media?url=https%3A%2F%2Fi.redd.it%2Fjk1hor2f5hf11.jpg


class Cat:
    mutationlist = ["dichoic", "albino"]
    eyecolorlist = ["blue", "hazel", "gold", "yellow", "amber", "orange", "copper", "pink"]
    colorlist = ["black", "blue grey", "caramel", "brown", "lilac", "cinnamon", "fawn", "orange", "cream", "apricot", "white", "bald"]
    tortlist = ["distinct", "brindled"]
    tabbylist = ["mackerel", "classic", "spotted", "ticked"]
    colorpointlist = ["point", "mink", "sepia"]
    whitespotlist = ["mitted", "tuxedo", "mask and mantle", "cap and saddle", "harlequin", "van", "magpie", "seychellois"]
    tippedlist = ["silver chincilla", "silver shade", "silver smoke", "golden chinchilla", "golden shade", "golden smoke"]

    def __init__(self, mutation, color1, color2, eye1, eye2, tort, tabby, colorpoint, whitespot, tipped, whitespotpatt, sex, name, id):
        self.mutation = mutation
        self.color1 = color1
        self.color2 = color2
        self.eye1 = eye1
        self.eye2 = eye2
        self.tort = tort
        self.tabby = tabby
        self.colorpoint = colorpoint
        self.whitespot = whitespot
        self.tipped = tipped
        self.whitespotpatt = whitespotpatt
        self.sex = sex
        self.name = name
        self.id = id

    @staticmethod
    def genrandcat(mutation="", color1="", color2="", eye1="", eye2="", tort="", tabby="", colorpoint="", whitespot="", tipped="", whitespotpatt="", sex="", name=""):
        if mutation == "":
            mutation = Cat.genmutation()
        if eye1 == "":
            eye1 = Cat.geneyes()
            eye1 = Cat.buildalbinoeyes(mutation, eye1)
        if eye2 == "":
            eye2 = Cat.gendichroic(mutation, eye1)
        if color1 == "":  
            color1 = Cat.gencatcolor()
            color1 = Cat.buildalbinocolor(mutation, color1)
        if color2 == "":
            color2 = False
        if color1 not in ("white", "bald"):
            if tort == "":
                tort = Cat.gentort()
            if tort and color2 == False:
                while color2 == False or color2 == "bald":
                    color2 = Cat.gencatcolor()
            if tabby == "":
                tabby = Cat.gentabby()
            if colorpoint == "":
                colorpoint = Cat.gencolorpoint()
            if whitespot == "":
                whitespot = Cat.genwhitespotting()
                if whitespot is False:
                    whitespotpatt = False
                else:
                    whitespotpatt = Cat.genwhitespotpatt()
            if tipped == "":
                tipped = Cat.gentipped()
        else:
            if tort == "":
                tort = False
            if tabby == "":
                tabby = False
            if colorpoint == "":
                colorpoint = False
            if whitespot == "":
                whitespot = False
                whitespotpatt = False
            if tipped == "":
                tipped = False
        if sex == "":
            if color1 != "orange":
                sex = Npc.gensexrand()
            else:
                r = random.randint(1, 10)
                if r < 9:
                    sex = "M"
                else:
                    sex = "F"
        if name == "":
            name = Cat.genname(sex)
        id = 0
        return Cat(mutation, color1, color2, eye1, eye2, tort, tabby, colorpoint, whitespot, tipped, whitespotpatt, sex, name, id)

    @staticmethod
    def unpackcatsfromload(cats):
        CatList.catlist.clear()
        for cat in cats:
            CatList.catlist.append(Cat(cat["mutation"], cat["color1"], cat["color2"], cat["eye1"], cat["eye2"], cat["tort"], cat["tabby"], cat["colorpoint"], cat["whitespot"], cat["tipped"], cat["whitespotpatt"], cat["sex"], cat["name"], cat["id"]))
            if CatList.masterid <= cat["id"]:
                CatList.masterid = cat["id"] + 1

    # Converts cats from cat list in to a JSON ingestible dicitonary.
    @staticmethod
    def packcats():
        cats = []
        for cat in CatList.catlist:
            dict = {
                "mutation" : cat.mutation,
                "color1" : cat.color1,
                "color2" : cat.color2,
                "eye1" : cat.eye1,
                "eye2" : cat.eye2,
                "tort" : cat.tort,
                "tabby" : cat.tabby,
                "colorpoint" : cat.colorpoint,
                "whitespot" : cat.whitespot,
                "tipped" : cat.tipped,
                "whitespotpatt" : cat.whitespotpatt,
                "sex" : cat.sex,
                "name" : cat.name,
                "id" : cat.id
            }
            cats.append(dict)
        return cats
                
    def __str__(self):
            description = f"{self.name} is a very good kitty. {heshe(self.sex, 1)} is "
            if self.mutation == "albino":
                description += "an albino cat with "
            elif self.color1 == "bald":
                description += "a hairless cat with "
            else:
                if not self.color2:
                    description += f"a {self.color1} cat with "
                else:
                    description += f"a {self.color1} and {self.color2} cat with "
            if self.mutation == "dichronic":
                description += f"a {self.eye1} and {self.eye2} eye. "
            else:
                description += f"{self.eye1} eyes. "
            if self.tabby:
                description += f"{heshe(self.sex, 1)} is a {self.tabby} tabby with darker {self.color1} markings. "
            if self.tort:
                description += f"{heshe(self.sex, 1)} has a {self.tort} tortoiseshell pattern. "
            if self.whitespot:
                description += f"{heshe(self.sex, 1)} has patches of white in a {self.whitespotpatt} pattern. " 
            if self.sex == "M":
                description += f"{heshe(self.sex, 1)} is a male cat."
            else:
                description += f"{heshe(self.sex, 1)} is a female cat."

            return description
    
    @property
    def mutation(self):
        return self._mutation

    @mutation.setter
    def mutation(self, mutation):
        if mutation not in Cat.mutationlist:
            if mutation is not False:
                raise ValueError(f"Invalid cat mutation type {mutation}.")
        self._mutation = mutation

    @staticmethod
    def gendichroic(mutation, eye1):
        if mutation != "dichroic":
            return eye1
        eye2 = eye1
        while eye2 == eye1:
            eye2 = Cat.geneyes()
        return eye2

    @staticmethod
    def genmutation():
        r = random.randint(1,100)
        match r:
            case 98 | 99:
                mutation = "dichroic"
            case 100:
                mutation = "albino"
            case _:
                mutation = False
        return mutation
    
    @staticmethod
    def buildalbinoeyes(mutation, eye1):
        if mutation != "albino":
            return eye1
        flip = coin()
        if flip == 1:
            eye1 = "blue"
        else:
            eye1 = "pink"
        return eye1
    
    @staticmethod
    def buildalbinocolor(mutation, color1):
        if mutation == "albino":
            color1 = "white"
        return color1

    @property
    def eye1(self):
        return self._eye1

    @eye1.setter
    def eye1(self, eye1):
        if eye1 not in Cat.eyecolorlist:
            raise ValueError(f"Invalid cat eye color {eye1}.")
        self._eye1 = eye1

    @property
    def eye2(self):
        return self._eye2

    @eye2.setter
    def eye2(self, eye2):
        if eye2 not in Cat.eyecolorlist:
            raise ValueError(f"Invalid cat eye color {eye2}.")
        self._eye2 = eye2

    @staticmethod
    def geneyes():
        return random.choice(Cat.eyecolorlist)

    @property
    def color1(self):
        return self._color1

    @color1.setter
    def color1(self, color1):
        if color1 not in Cat.colorlist:
            raise ValueError(f"Invalid cat color {color1}.")
        self._color1 = color1

    @property
    def color2(self):
        return self._color2

    @color2.setter
    def color2(self, color2):
        if color2 not in Cat.colorlist:
            if color2 != False:
                raise ValueError(f"Invalid cat color {color2}.")
        self._color2 = color2

    @staticmethod
    def gencatcolor():
        return random.choice(Cat.colorlist)
    
    @property
    def tort(self):
        return self._tort

    @tort.setter
    def tort(self, tort):
        if tort not in Cat.tortlist:
            if tort != False:
                raise ValueError(f"Invalid cat tort type {tort}.")
        self._tort = tort

    @staticmethod
    def gentort():
        r = random.randint(1,9)
        if r < 5:
            tort = False
        else:
            tort = random.choice(Cat.tortlist)
        return tort
    
    @property
    def tabby(self):
        return self._tabby

    @tabby.setter
    def tabby(self, tabby):
        if tabby not in Cat.tabbylist:
            if tabby is not False:
                raise ValueError(f"Invalid cat tabby type {tabby}.")
        self._tabby = tabby

    @staticmethod
    def gentabby():
        r = random.randint(1,12)
        if r < 4:
            tabby = False
        else:
            tabby = random.choice(Cat.tabbylist)
        return tabby
    
    @property
    def colorpoint(self):
        return self._colorpoint
    
    @colorpoint.setter
    def colorpoint(self, colorpoint):
        if colorpoint not in Cat.colorpointlist:
            if colorpoint is not False:
                raise ValueError(f"Invalid cat colorpoint type {colorpoint}.")
        self._colorpoint = colorpoint

    @staticmethod
    def gencolorpoint():
        r = random.randint(1,6)
        if r < 4:
            colorpoint = False
        else:
            colorpoint = random.choice(Cat.colorpointlist)
        return colorpoint

    @property
    def whitespot(self):
        return self._whitespot
    
    @whitespot.setter
    def whitespot(self, whitespot):
        if whitespot is not False and whitespot is not True:
            raise ValueError(f"Invalid whitespot value {whitespot}, must be bool.")
        self._whitespot = whitespot

    @staticmethod
    def genwhitespotting():
        r = random.randint(1,6)
        if r < 5:
            whitespot = False
        else:
            whitespot = True
        return whitespot

    @property
    def whitespotpatt(self):
        return self._whitespotpatt
    
    @whitespotpatt.setter
    def whitespotpatt(self, whitespotpatt):
        if whitespotpatt not in Cat.whitespotlist:
            if whitespotpatt is not False:
                raise ValueError(f"Invalid cat whitespot type {whitespotpatt}.")
        self._whitespotpatt = whitespotpatt

    @staticmethod
    def genwhitespotpatt():
        return random.choice(Cat.whitespotlist)

    @property
    def tipped(self):
        return self._tipped
    
    @tipped.setter
    def tipped(self, tipped):
        if tipped not in Cat.tippedlist:
            if tipped is not False:
                raise ValueError(f"Invalid cat tip type {tipped}.")
        self._tipped = tipped

    @staticmethod
    def gentipped():
        r = random.randint(1,12)
        if r < 7:
            tipped = False
        else:
            tipped = random.choice(Cat.tippedlist)
        return tipped
    
    @property
    def sex(self):
        return self._sex
    
    @sex.setter
    def sex(self, sex):
        if sex not in Npc.sexlist:
            raise ValueError(f"Invalid cat sex {sex}.")
        self._sex = sex
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if name == "" or not isinstance(name, str):
            raise ValueError(f"Invalide cat name {name}.")
        self._name = name

    @staticmethod
    def genname(sex):
        r = random.randint(1,6)
        name = ""
        match r:
            case 1:
                x = Npc.gennametable()
                name = Npc.genname(x[0])
            case 2 | 3:
                x = Npc.gennametable()
                if sex == "F":
                    name = Npc.genname(x[1])
                else:
                    name = Npc.genname(x[2])
            case _:
                x = CatNames.catnametable()
                flip = coin()
                if flip == 1:
                    name = random.choice(x[0]) #Not going in to Npc for these calls as the lists are purely random names and the Npc.chance would skew results of a short list to the top.
                else:
                    if sex == "F":
                        name = random.choice(x[1])
                    else:
                        name = random.choice(x[2])
        r = random.randint(1,5)
        if r == 1:
            u = ["Honorable", "Senator", "President", "Councillor", "Alderman", "Mayor", "Governor", "Prefect", "Prelate", "Premier", "Ambassador", "Envoy", "Provost", "Chief", "Dr.", "Professor", "Admiral", "Captain", "Commander", "Colonel", "General", "Constable", "Sensei"]
            m = ["Mr.", "King", "Uncle", "Grandpa", "Prince", "Archduke", "Grand Duke", "Duke", "Marquis", "Count", "Earl", "Viscount", "Baron", "Lord", "Emperor", "Sir"]
            f = ["Ms.", "Mrs.", "Queen", "Aunt", "Grandma", "Princess", "Archdutchess", "Grand Duchess", "Duchess", "Marquise", "Countess", "Viscountess", "Baroness", "Lady", "Empress", "Dame"]
            flip = coin()
            if flip == 1:
                title = random.choice(u)
            else:
                if sex == "F":
                    title = random.choice(f)
                else:
                    title = random.choice(m)
            name = title + " " + name
        return name
    
