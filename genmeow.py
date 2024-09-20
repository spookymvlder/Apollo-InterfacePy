import random
from helpers import coin, hisher, heshe
from gennpc import Npc
from namelists import CatNames
from savedobjects import CatList
#https://www.reddit.com/media?url=https%3A%2F%2Fi.redd.it%2Fjk1hor2f5hf11.jpg


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
            if tipped == "":
                tipped = Cat.gentipped()
            if whitespot and whitespotpatt == "":
                whitespotpatt = Cat.genwhitespotpatt()
        else:
            if tort == "":
                tort = False
            if tabby == "":
                tabby = False
            if colorpoint == "":
                colorpoint = False
            if whitespot == "":
                whitespot = False
            if tipped == "":
                tipped = False
            if whitespotpatt == "":
                whitespotpatt = False
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

    @staticmethod
    def geneyes():
        return random.choice(Cat.eyecolorlist)

    @staticmethod
    def gencatcolor():
        return random.choice(Cat.colorlist)
    
    @staticmethod
    def gentort():
        r = random.randint(1,9)
        if r < 5:
            tort = False
        else:
            tort = random.choice(Cat.tortlist)
        return tort
    
    @staticmethod
    def gentabby():
        r = random.randint(1,12)
        if r < 4:
            tabby = False
        else:
            tabby = random.choice(Cat.tabbylist)
        return tabby
    
    @staticmethod
    def gencolorpoint():
        r = random.randint(1,6)
        if r < 4:
            colorpoint = False
        else:
            colorpoint = random.choice(Cat.colorpointlist)
        return colorpoint

    @staticmethod
    def genwhitespotting():
        r = random.randint(1,6)
        if r < 5:
            whitespot = False
        else:
            whitespot = True
        return whitespot

    @staticmethod
    def genwhitespotpatt():
        return random.choice(Cat.whitespotlist)

    @staticmethod
    def gentipped():
        r = random.randint(1,12)
        if r < 7:
            tipped = False
        else:
            tipped = random.choice(Cat.tippedlist)
        return tipped
    
    @staticmethod
    def genname(sex):
        r = random.randint(1,5)
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
        if name:
            return name
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
    
#cat = Cat()
#print(cat)