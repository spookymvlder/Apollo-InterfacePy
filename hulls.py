import random, math
from gencorp import Corp
import namelists
import string
from helpers import coin

class HullTemplate:
    sizes = ["xsmall", "small", "smedium", "medium", "large", "xlarge"]
    types = ["lifeboat", "shuttle", "skiff", "fighter", "dropship", "heavy dropship", "assault transport", "frigate", "light frigate", 
            "escort frigate", "heavy frigate", "carrier frigate", "corvette", "light corvette", "heavy corvette", 
            "stealth corvette", "destroyer", "heavy destroyer", "cruiser", "surveillance cruiser", 
            "carrier", "assault carrier", "heavy carrier", "battleship", "mobile dockyard",
            "minehunter", "galleon", "monitor", "transport", "patrol", "research", "yacht", 
            "miner", "cargo freighter", "colony ship", "exploration"]
    shipcategories = ["courier", "cargo", "military", "science", "private", "government", "any", "emergency"]
    ordenancelevels = ["none", "light", "defensive", "medium", "heavy", "support"]
    armorlevels = ["light", "medium", "heavy"]
    #Eventually add function to combine this list with the existing list, so new categories can be added. Then can export just
    #these categories when creating saving format, probably JSON.
    newtypes = []
    newshipcategories = []
    newordenancelevels = []
    newarmorlevesl =[]
    

#TODO new variable for getsmodules. Can then skip for things like dropships and escape pods
#checks for carrier and armor
    def __init__(self, size, hulltype, category, ordenance, carrier, armorcat):
        self.size = size
        self.hulltype = hulltype
        self.category = category
        self.ordenance = ordenance
        self.carrier = carrier
        self.armorcat = armorcat
        self.hardpoints = HullTemplate.genhardpoints(self, self.size, self.ordenance)
        self.signature = HullTemplate.gensignature(self, self.size)
        self.crew = HullTemplate.gencrew(self, self.size)
        self.hullen = HullTemplate.genhullen(self, self.size)
        self.hullval = HullTemplate.genhullval(self, self.size, self.category)
        self.armorval = HullTemplate.genarmorval(self, self.armorcat, self.hullval)
        self.modules = HullTemplate.genmodules(self, self.size, self.category)
        #More robust manufacturer functionality, choose from Corps once gencorp is more built out. If new, save to list
        self.manufacturer = Corp.gencorpname()
        self.shipmodel = HullTemplate.genshipmodel(self, self.category, self.hulltype)
        self.initmodules = HullTemplate.geninitmodules(self, self.modules, self.category, self.crew, self.carrier)

    
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size):
        if size =="" or size not in HullTemplate.sizes:
            raise ValueError("Invalid ship size.")
        self._size = size

    @property
    def hulltype(self):
        return self._hulltype
    
    @hulltype.setter
    def hulltype(self, hulltype):
        if hulltype == "" or hulltype not in HullTemplate.types:
            raise ValueError(f"Invalid hull type {hulltype}.")
        self._hulltype = hulltype
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):
        if category =="" or category not in HullTemplate.shipcategories:
            raise ValueError(f"Invalid ship category type {category}.")
        self._category = category

    @property
    def ordenance(self):
        return self._ordenance
    
    @ordenance.setter
    def ordenance(self, ordenance):
        if ordenance =="" or ordenance not in HullTemplate.ordenancelevels:
            raise ValueError("Invalid ship ordenance.")
        self._ordenance = ordenance
    
    @property
    def carrier(self):
        return self._carrier
    
    @carrier.setter
    def carrier(self, carrier):
        if carrier == "" or not isinstance(carrier, bool):
            raise ValueError("Carrier must be bool.")
        self._carrier = carrier
    
    @property
    def armorcat(self):
        return self._armorcat
    
    @armorcat.setter
    def armorcat(self, armorcat):
        if armorcat == "" or armorcat not in HullTemplate.armorlevels:
            raise ValueError(f"Invalid armor level {armorcat}.")
        self._armorcat = armorcat

    @property
    def hardpoints(self):
        return self._hardpoints
    
    @hardpoints.setter
    def hardpoints(self, hardpoints):
        for hardpoint in hardpoints:
            if hardpoint < 0 or not isinstance(hardpoint, int):
                raise ValueError(f"Invalid hardpoint {hardpoint}.")
        self._hardpoints = hardpoints

    #Hardpoints ties to how many weapons can be added to ship, stored as a list for lvls 1, 2, and 3
    def genhardpoints(self, size, ordenance):
        hardpoints = [0,0,0]
        if ordenance != "none":
            match size:
                case "xsmall":
                    hardpoints[0] = 1
                case "small":
                    hardpoints[0] = 1
                    hardpoints[1] = 1
                case "smedium":
                    hardpoints[0] = 2
                    hardpoints[1] = 1
                case "medium":
                    hardpoints[1] = 2
                    hardpoints[2] = 1
                case "large":
                    hardpoints[1] = 2
                    hardpoints[2] = 2
                case "xlarge":
                    hardpoints[1] = 3
                    hardpoints[2] = 2
            #if category == "military": #seems maybe too many
                #hardpoints[0] += 1
            if ordenance == "defensive":
                while hardpoints[2] > 0:
                    hardpoints[0] +=1
                    hardpoints[2] -=1
            if ordenance == "support":
                while hardpoints[2] > 0:
                    hardpoints[1] +=1
                    hardpoints[2] -=1
            if ordenance == "medium":
                if hardpoints[1] > 0:
                    hardpoints[1] += 1
                else:
                    hardpoints[0] += 1
            if ordenance == "heavy":
                hardpoints[2] += 1
        return hardpoints

    @property
    def signature(self):
        return self._signature
    
    @signature.setter
    def signature(self, signature):
        if signature < -3 or signature > 3:
            raise ValueError(f"Invalid signature {signature}")
        self._signature = signature

    def gensignature(self, size):
        match size:
            case "xsmall":
                signature = -2
            case "small":
                signature = -1
            case "smedium":
                signature = -0
            case "medium":
                signature = 1
            case "large":
                signature = 2
            case "xlarge":
                signature = 3
        return signature
    
    '''@property
    def FTL(self):
        return self._FTL
    
    @FTL.setter
    def FTL(self, FTL):
        if FTL < 20 or not isinstance(FTL, int):
            raise ValueError(f"Invalid FTL value {FTL}.")
        self._FTL = FTL'''

    #Need to add variables later to input, not a priority for now. Likely needs some extra trait like speed or indication of how advanced the hardware should be.
    '''def genFTL(self, size):
        if size == "small":
            FTL = 0
        elif '''

    @property
    def crew(self):
        return self._crew
    
    @crew.setter
    def crew(self, crew):
        for sailor in crew:
            if not isinstance(sailor, int) or sailor < 0:
                raise ValueError(f"Invalid crew number {sailor}.")
        self._crew = crew

    #crew is a list with a min and max value
    def gencrew(self, size):
        crew = [0, 0]
        match size:
            case "xsmall":
                crew[0] = 1
                crew[1] = random.randint(1,4)
            case "small":
                crew[0] = 1
                crew[1] = random.randint(1,6)
            case "smedium":
                crew[0] = random.randint(2,4)
                crew[1] = random.randint(4,8)
            case "medium":
                crew[0] = random.randint(6,8)
                crew[1] = random.randint(9, 18)
            case "large":
                crew[0] = random.randint(6,10)
                crew[1] = random.randint(11,24)
            case "xlarge":
                crew[0] = random.randint(12, 15)
                crew[1] = random.randint(16, 36)
        return crew
    
    
    @property
    def hulllen(self):
        return self._hullen
    
    @hulllen.setter
    def hullen(self, hullen):
        if not isinstance(hullen, int):
            raise ValueError(f"Invalid hull length {hullen}.")
        self._hullen = hullen

    def genhullen(self, size):
        hullen = ""
        match size:
            case "xsmall":
                hullen = random.randint(10,18)
            case "small":
                hullen = random.randint(20,80)
            case "smedium":
                hullen = random.randint(80,225)
            case "medium":
                hullen = random.randint(225,400)
            case "large":
                hullen = random.randint(400,750)
            case "xlarge":
                hullen = random.randint(750, 1300)
        return hullen

    @property
    def hullval(self):
        return self._hullval
    
    @hullval.setter
    def hullval(self, hullval):
        if not isinstance(hullval, int) or hullval < 1:
            raise ValueError(f"Invalid hull value {hullval}.")
        self._hullval = hullval
        
    def genhullval(self, size, category):
        hullval = ""
        match size:
            case "xsmall":
                hullval = 2
            case "small":
                hullval = random.randint(2,6)
            case "smedium":
                hullval = random.randint(4,8)
            case "medium":
                hullval = random.randint(6,10)
            case "large":
                hullval = random.randint(7,12)
            case "xlarge":
                hullval = random.randint(9, 15)
        if category == "military":
            hullval += 2
        return hullval
    
    @property
    def armorval(self):
        return self.armorval
    
    @armorval.setter
    def armorval(self, armorval):
        if not isinstance(armorval, int) or armorval < 1:
            raise ValueError(f"Invalid hull value {armorval}.")
        self._armor = armorval

    def genarmorval(self, armorcat, hullval):
        if hullval == 0 or not isinstance(hullval, int):
            raise ValueError(f"Unable to calculate armor due to hullval {hullval}.")
        armor = math.ceil(hullval / 2)
        if armorcat == "light":
            if armor > 4:
                armor -= random.randint(1,2)
        elif armorcat == "heavy":
            armor += random.randint(2,3)
        else:
            armor += 1
        return armor

    @property
    def modules(self):
        return self._modules
    
    @modules.setter
    def modules(self, modules):
        for module in modules:
            if not isinstance(module, int) or module < 0:
                raise ValueError(f"Invalid module count {module}.")

    def genmodules(self, size, category):
        modules = [0, 0, 0, 0, 0]
        match size:
            case "xsmall":
                modules[0] = random.randint(3,4)
                modules[1] = random.randint(2,3)
            case "small":
                modules[0] = random.randint(4,8)
                modules[1] = random.randint(2,6)
                modules[2] = random.randint(1,3)
            case "smedium":
                modules[0] = random.randint(5,9)
                modules[1] = random.randint(3,7)
                modules[2] = random.randint(2,4)
            case "medium":
                modules[1] = random.randint(7,9)
                modules[2] = random.randint(4,7)
                modules[3] = random.randint(3,5)
            case "large":
                modules[2] = random.randint(7,9)
                modules[3] = random.randint(5,8)
                modules[4] = random.randint(3,6)
            case "xlarge":
                modules[2] = random.randint(10,17)
                modules[3] = random.randint(9,14)
                modules[4] = random.randint(4,9)
        #will consume at least one of the largest slots for a cargo module, should get around scenario where all rolls are low
        if category == "cargo":
            if modules[4] > 0:
                modules[4] += 1
            elif modules[3] > 0:
                modules[3] +=1
            else:
                modules[2] +=1
        return modules

    @property
    def shipmodel(self):
        return self._shipmodel
    
    @shipmodel.setter
    def shipmodel(self, shipmodel):
        if shipmodel == "" or not isinstance(shipmodel, str):
            raise ValueError(f"Invalid shipmodel {shipmodel}.")
        self._shipmodel = shipmodel
    

    def genshipmodel(self, category, type):
        choices = []
        if type == "yacht":
            choices.append(namelists.returnNamelist("yacht"))
        elif type == "exploration":
            choices.append(namelists.returnNamelist("explorer"))
        match category:
            case "courier":
                choices.append(namelists.returnNamelist("courier"))
            case "cargo":
                choices.append(namelists.returnNamelist("cargo"))
            case "military":
                choices.append(namelists.returnNamelist("mythical"))
                choices.append(namelists.returnNamelist("fantasy"))
                choices.append(namelists.returnNamelist("predator"))
                choices.append(namelists.returnNamelist("weather"))
        if choices == []:
            choices.append(namelists.returnNamelist("animal"))
        choices = random.choice(choices)
        #could end up with multiple lists stored to choices so guarantee we return a single value
        if isinstance(choices, list):
            choices = random.choice(choices)
        choices += " " + HullTemplate.genshipmodelsuffix()
        return choices
    
    #TODO move suffix to wherever modules are added to distinguish between variations in base design
    @classmethod
    def genshipmodelsuffix(cls):
        formats = ["H-H", "HA.H", "111A", "A.A.1", "HH", "A-A", "HHH", "A-11", "roman"]
        tchoice = random.choice(formats)
        letter = string.ascii_uppercase
        digit = string.digits
        hex = string.hexdigits
        roman = ["I", "II", "III", "IV", "V", "VI", "VII"]
        suffix = ""
        match tchoice:
            case "H-H":
                suffix = random.choice(hex).upper() + "-" + (random.choice(hex)).upper()
            case "HA.H":
                suffix = random.choice(hex).upper() + random.choice(letter) + "." + random.choice(hex).upper()
            case "111A":
                suffix = random.choice(digit) + random.choice(digit) + random.choice(digit) + random.choice(letter)
            case "A.A.1":
                suffix = random.choice(letter) + "." + random.choice(letter) + "." + random.choice(digit)
            case "HH":
                suffix = random.choice(hex).upper() + random.choice(hex).upper()
            case "A-A":
                suffix = random.choice(letter) + "-" + random.choice(letter)
            case "HHH":
                suffix = random.choice(hex).upper() + random.choice(hex).upper() + random.choice(hex).upper()
            case "A-11":
                suffix = random.choice(letter) + "-" + random.choice(digit) + random.choice(digit)
            case "roman":
                suffix = random.choice(roman)
        return suffix
    
    @property
    def initmodules(self):
        return self._initmodules
    
    @initmodules.setter
    def initmodules(self, initmodules):
        for module in initmodules:
            if module == "" or not isinstance(module, str):
                raise ValueError(f"Invalid module {module}.")
        self._initmodules = initmodules

    #Need air scrubbers, AI, cryodeck, and galley. Cargo requires at least one cargo bay, may split off each type to own function.
    def geninitmodules(self, modules, category, crew, carrier):
        initmodules = []
        #set AI in smallest slot
        for module in modules:
            if module > 0:
                module -= 1
                initmodules.append["AI"]
                break
        people = [1, 10, 50, 500, 2500]
        if carrier:
            count = 5
            success = False
            success2 = False
            for module in reversed(modules):
                if module > 2 and not success:
                    module -= 1
                    initmodules.append("Cryo {people[count]}")
                    module -= 1
                    initmodules.append("Galley {people[count]}")
                    success = True
                    crew += people[count]
                if module > 0 and not success2:
                    flip = coin()
                    module -= 1
                    if flip == 1:
                        initmodules.append("Hanger {people[count]}")
                    else:
                        initmodules.append("Vehicle Bay {people[count]}")
                count -= 1
                if success2:
                    break
        else:
            #Try to assign the cryodeck as efficiently as possible.
            tcrew = crew
            while tcrew > 0:
                if tcrew > 20:
                    if modules[2] > 2:
                        modules[2] -= 2
                        initmodules.append("Cryo 50")
                        initmodules.append("Galley 50")
                        tcrew - 50
                    else:
                        try:
                            modules[1] -= 2
                            initmodules.append("Cryo 10")
                            initmodules.append("Galley 10")
                        except:
                            initmodules.append("Cryo 10")
                            initmodules.append("Galley 10")
                        tcrew - 10
                else:
                    if modules[1] >= 2:
                        modules[1] -= 2
                        initmodules.append("Cryo 10")
                        initmodules.append("Galley 10")
                        tcrew - 10
                    else:
                        modules[2] -= 2
                        initmodules.append("Cryo 50")
                        initmodules.append("Galley 50")
                        tcrew - 50
        if category == "cargo":
            count = 5
            success = False
            for module in reversed(modules):
                if module > 2:
                    module -= 2
                    initmodules.append("Cargo Bay {count}")
                    success = True
                count -= 1
                if success:
                    break
        #air scrubbers
        tcrew = crew
        if tcrew < 10:
            if modules[0] > 0:
                modules[0] -= 1
                initmodules.append("Air Scrubbers 10")
            elif modules[1] > 0:
                modules[1] -= 1
                initmodules.append("Air Scrubbers 50")
            else:
                modules[2] -= 1
                initmodules.append("Air Scrubbers 500")
        elif tcrew < 50:
            if modules[1] > 0:
                modules[1] -= 1
                initmodules.append("Air Scrubbers 50")
            else:
                modules[2] -= 1
                initmodules.append("Air Scrubbers 500")
        elif tcrew <500:
            modules[2] -= 1
            initmodules.append("Air Scrubbers 500")
        else:
            modules[3] -= 1
            initmodules.append("Air Scrubbers 2500")
        return initmodules
                    



class HullSpecs:
    hulls = []


def initializehulls():
    HullSpecs.hulls.append(HullTemplate("xsmall", "lifeboat", "emergency", "none", False, "light"))
    HullSpecs.hulls.append(HullTemplate("xsmall", "shuttle", "any", "none", False, "light"))
    HullSpecs.hulls.append(HullTemplate("small", "skiff", "any", "none", False, "light"))
    HullSpecs.hulls.append(HullTemplate("xsmall", "fighter", "military", "medium", False, "light"))
    HullSpecs.hulls.append(HullTemplate("small", "dropship", "military", "none", True, "light"))
    HullSpecs.hulls.append(HullTemplate("small", "heavy dropship", "military", "light", True, "heavy"))
    HullSpecs.hulls.append(HullTemplate("small", "assault transport", "military", "light", True, "medium"))
    HullSpecs.hulls.append(HullTemplate("medium", "frigate", "military", "medium", True, "medium"))
    HullSpecs.hulls.append(HullTemplate("smedium", "light frigate", "military", "light", False, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "escort frigate", "military", "medium", False, "light"))
    HullSpecs.hulls.append(HullTemplate("medium", "carrier frigate", "military", "defensive", True, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "corvette", "military", "medium", False, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "light corvette", "military", "light", False, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "heavy corvette", "military", "heavy", False, "medium"))
    HullSpecs.hulls.append(HullTemplate("smedium", "stealth corvette", "military", "defensive", False, "light"))
    HullSpecs.hulls.append(HullTemplate("medium", "destroyer", "military", "heavy", False, "heavy"))
    HullSpecs.hulls.append(HullTemplate("medium", "heavy destroyer", "military", "heavy", False, "heavy"))
    HullSpecs.hulls.append(HullTemplate("medium", "cruiser", "military", "heavy", False, "heavy"))
    HullSpecs.hulls.append(HullTemplate("medium", "surveillance cruiser", "military", "support", False, "medium"))
    HullSpecs.hulls.append(HullTemplate("large", "carrier", "military", "support", True, "medium"))
    HullSpecs.hulls.append(HullTemplate("medium", "assault carrier", "military", "medium", True, "medium"))
    HullSpecs.hulls.append(HullTemplate("large", "heavy carrier", "military", "medium", True, "heavy"))
    HullSpecs.hulls.append(HullTemplate("large", "battleship", "military", "heavy", False, "heavy"))
    HullSpecs.hulls.append(HullTemplate("medium", "minehunter", "military", "support", False, "light")) 
    HullSpecs.hulls.append(HullTemplate("small", "monitor", "military", "heavy", False, "heavy"))
    HullSpecs.hulls.append(HullTemplate("smedium", "patrol", "military", "light", False, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "patrol", "government", "light", False, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "research", "science", "none", False, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "yacht", "private", "none", False, "light"))
    HullSpecs.hulls.append(HullTemplate("small", "miner", "cargo", "none", False, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "cargo freighter", "cargo", "none", False, "light"))
    HullSpecs.hulls.append(HullTemplate("medium", "cargo freighter", "cargo", "none", False, "light"))
    HullSpecs.hulls.append(HullTemplate("xlarge", "colony ship", "private", "none", True, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "exploration", "science", "defensive", False, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "exploration", "private", "defensive", False, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "exploration", "government", "defensive", False, "light"))
    HullSpecs.hulls.append(HullTemplate("large", "mobile dockyard", "any", "defensive", True, "light"))
    HullSpecs.hulls.append(HullTemplate("xlarge", "galleon", "cargo", "defensive", False, "medium"))

#initializehulls()
#print(HullSpecs.hulls)