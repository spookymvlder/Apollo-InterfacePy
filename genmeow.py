import random
from helpers import coin
from gennpc import Npc
from load_initial import catnametable
#https://www.reddit.com/media?url=https%3A%2F%2Fi.redd.it%2Fjk1hor2f5hf11.jpg


class Cat:
    def __init__(self, mutation="", color1="", color2="", eye1="", eye2="", tort="", tabby="", colorpoint="", whitespot="", tipped="", whitespotpatt="", sex="", name=""):
        self.mutation = Cat.genmutation(self)
        self.eye1 = Cat.geneyes()
        self.color1 = Cat.gencatcolor()
        self.color2 = False
        if self.color1 != ("white" or "bald"):
            self.tort = Cat.gentort()
            if self.tort:
                while self.color2 == (False or "bald"):
                    self.color2 = Cat.gencatcolor()
            self.tabby = Cat.gentabby()
            self.colorpoint = Cat.gencolorpoint()
            self.whitespot = Cat.genwhitespotting()
            self.tipped = Cat.gentipped()
            if self.whitespot:
                self.whitespotpatt = Cat.genwhitespotpatt()
        else:
            self.tort = False
            self.tabby = False
            self.colorpoint = False
            self.whitespot = False
            self.tipped = False
            self.whitespotpatt = False
        if self.color1 != "orange":
            self.sex = Npc.gensexrand()
        else:
            r = random.randint(1, 10)
            if r < 9:
                self.sex = "M"
            else:
                self.sex = "F"
        self.name = Cat.genname(self)
            
    def __str__(self):
            description = f"{self.name} is a very good kitty. They are "
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
                description += f"It is a {self.tabby} tabby with darker {self.color1} markings. "
            if self.tort:
                description += f"It has a {self.tort} tortoiseshell pattern. "
            if self.whitespot:
                description += f"It has patches of white in a {self.whitespotpatt} pattern. " 
            if self.sex == "M":
                description += "It is a male cat."
            else:
                description += "It is a female cat."

            return description
    


    def genmutation(self):
        r = random.randint(1,100)
        match r:
            case 98 | 99:
                self.mutation = "dichroic"
                self.eye2 = Cat.geneyes()
            case 100:
                self.mutation = "albino"
                self.eye2 = False
                Cat.buildalbino()
            case _:
                self.mutation = False
                self.eye2 = False
    
    def buildalbino(self):
        self.color1 = "white"
        flip = coin()
        if flip == 1:
            self.eye1 = "blue"
        else:
            self.eye1 = "pink"

    def geneyes():
        r = random.randint(1, 7)
        match r:
            case 1:
                eyes = "blue"
            case 2:
                eyes = "hazel"
            case 3:
                eyes = "gold"
            case 4:
                eyes = "yellow"
            case 5:
                eyes = "amber"
            case 6:
                eyes = "orange"
            case 7:
                eyes = "copper"
        return eyes

    def gencatcolor():
        r = random.randint(1, 13)
        match r:
            case 1:
                color = "black"
            case 2:
                color = "blue grey"
            case 3:
                color = "caramel"
            case 4:
                color = "brown"
            case 5:
                color = "lilac"
            case 6:
                color = "cinnamon"
            case 7:
                color = "fawn"
            case 8:
                color = "orange"
            case 9:
                color = "cream"
            case 10:
                color = "apricot"
            case 11:
                color = "white"
            case 12:
                color = "apricot"
            case 13:
                color = "bald"
        return color
    
    def gentort():
        r = random.randint(1,9)
        if r < 5:
            tort = False
        elif r < 7:
            tort = "distinct"
        else:
            tort = "brindled"
        return tort
    
    def gentabby():
        r = random.randint(1,12)
        if r < 4:
            tabby = False
        elif r < 6:
            tabby = "mackerel"
        elif r < 8:
            tabby = "classic"
        elif r < 10:
            tabby = "spotted"
        else:
            tabby = "ticked"
        return tabby
    
    def gencolorpoint():
        r = random.randint(1,6)
        if r < 4:
            colorpoint = False
        elif r < 5:
            colorpoint = "point"
        elif r < 6:
            colorpoint = "mink"
        else:
            colorpoint = "sepia"
        return colorpoint

    def genwhitespotting():
        r = random.randint(1,6)
        if r < 5:
            whitespot = False
        else:
            whitespot = "yes"
        return whitespot

    def genwhitespotpatt():
        r = random.randint(1,8)
        match r:
            case 1:
                pattern = "mitted"
            case 2:
                pattern = "tuxedo"
            case 3:
                pattern = "mask and mantle"
            case 4:
                pattern = "cap and saddle"
            case 5:
                pattern = "harlequin"
            case 6:
                pattern = "van"
            case 7:
                pattern = "magpie"
            case 8:
                pattern = "seychellois"
        return pattern

    def gentipped():
        r = random.randint(1,12)
        if r < 7:
            tipped = False
        else:
            match r:
                case 7:
                    tipped = "silver chinchilla"
                case 8:
                    tipped = "silver shade"
                case 9:
                    tipped = "silver smoke"
                case 10:
                    tipped = "golden chinchilla"
                case 11:
                    tipped = "golden shade"
                case 12:
                    tipped = "golden smoke"
        return tipped
    
    def genname(self):
        r = random.randint(1,5)
        name = ""
        match r:
            case 1:
                x = Npc.gennametable()
                name = Npc.genname(x[0])
            case 2 | 3:
                x = Npc.gennametable()
                if self.sex == "F":
                    name = Npc.genname(x[1])
                else:
                    name = Npc.genname(x[2])
            case _:
                x = catnametable()
                flip = coin()
                if flip == 1:
                    name = random.choice(x[0]) #Not going in to Npc for these calls as the lists are purely random names and the Npc.chance would skew results of a short list to the top.
                else:
                    if self.sex == "F":
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
                if self.sex == "F":
                    title = random.choice(f)
                else:
                    title = random.choice(m)
            name = title + " " + name
        return name

cat = Cat()
print(cat)