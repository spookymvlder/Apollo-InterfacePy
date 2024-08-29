import random, math
from gencorp import Corp
import namelists
import string, copy, re
from helpers import coin

class HullTemplate:
    sizes = ["xsmall", "small", "smedium", "medium", "large", "xlarge"]
    types = ["lifeboat", "shuttle", "skiff", "fighter", "dropship", "heavy dropship", "assault transport", "frigate", "light frigate", 
            "escort frigate", "heavy frigate", "carrier frigate", "corvette", "light corvette", "heavy corvette", 
            "stealth corvette", "destroyer", "heavy destroyer", "cruiser", "surveillance cruiser", 
            "carrier", "assault carrier", "heavy carrier", "battleship", "mobile dockyard",
            "minehunter", "galleon", "monitor", "transport", "patrol", "research", "yacht", 
            "miner", "cargo freighter", "colony ship", "exploration"]
    shipcategories = ["courier", "cargo", "military", "science", "private", "government", "any", "emergency", "colony"]
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
        self.initmodules = HullTemplate.geninitmodules(self, self.modules, self.category, self.crew, self.carrier, self.size)
        self.thrusters = HullTemplate.genthrusters(self, self.size, self.armorcat, self.ordenance, self.category)
    
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
                while hardpoints[2] > 1:
                    hardpoints[0] +=1
                    hardpoints[2] -=1
            if ordenance == "support":
                while hardpoints[2] > 1:
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
        return self._armorval
    
    @armorval.setter
    def armorval(self, armorval):
        if not isinstance(armorval, int) or armorval < 1:
            raise ValueError(f"Invalid hull value {armorval}.")
        self._armorval = armorval

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
        self._modules = modules

    def genmodules(self, size, category):
        modules = [0, 0, 0, 0, 0]
        match size:
            case "xsmall":
                modules[0] = random.randint(3,4)
                modules[1] = random.randint(2,3)
            case "small":
                modules[0] = random.randint(4,8)
                modules[1] = random.randint(2,6)
                modules[2] = random.randint(2,3)
            case "smedium":
                modules[0] = random.randint(5,9)
                modules[1] = random.randint(3,7)
                modules[2] = random.randint(3,4)
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
        return choices
    
    
    @property
    def initmodules(self):
        return self._initmodules
    
    @initmodules.setter
    def initmodules(self, initmodules):
        for module in initmodules:
            if module == "" or not isinstance(module, str):
                raise ValueError(f"Invalid module {module}.")
        self._initmodules = initmodules

    #Need air scrubbers, AI, cryodeck, docking umbilical and galley. 
    #Cargo requires at least one cargo bay, may split off each type to own function.
    #Also changes value for modules
    def geninitmodules(self, modules, category, crew, carrier, size):
        initmodules = []
        self.pregenmodules = copy.copy(modules)
        if size == "xsmall":
            initmodules.append("None")
            return initmodules
        cargo = [.5, 10, 250, 5000, 100000]
        numlist = [1, 2, 3, 4, 5]
        people = [1, 10, 50, 500, 2500]
        evlist = [1, 4, 5, 20]
        #set AI in smallest slot
        unit, modules = HullTemplate.setmodulehelper(modules, "AI", 0, 4)
        if unit:
            initmodules.append(unit)

        #Can't use helper function for cryo/galley since we're trying to keep track of the total folks on the ship
        #Could be cleaner with more helper functions but also more complicated.
        passengers = crew[1]
        if carrier:
            count = 4
            for module in reversed(modules):
                if module >= 2:
                    modules[count] -= 1
                    initmodules.append(f"Cryo {people[count]}")
                    modules[count] -= 1
                    initmodules.append(f"Galley {people[count]}")
                    passengers = people[count]
                    break
                count -= 1
        else:
            #Try to assign the cryodeck as efficiently as possible.
            tcrew = passengers
            passengers = 0
            while tcrew > 0:
                if tcrew > 20:
                    if modules[2] > 2:
                        modules[2] -= 2
                        initmodules.append("Cryo 50")
                        initmodules.append("Galley 50")
                        tcrew -= 50
                        passengers += 50                      
                    else:
                        try:
                            modules[1] -= 2
                            initmodules.append("Cryo 10")
                            initmodules.append("Galley 10")
                        except:
                            initmodules.append("Cryo 10")
                            initmodules.append("Galley 10")
                        tcrew -= 10
                        passengers += 10
                else:
                    if modules[1] >= 2:
                        modules[1] -= 2
                        initmodules.append("Cryo 10")
                        initmodules.append("Galley 10")
                        tcrew -= 10
                        passengers += 10
                    else:
                        modules[2] -= 2
                        initmodules.append("Cryo 50")
                        initmodules.append("Galley 50")
                        tcrew -= 50
                        passengers += 50

        if category == "cargo":
            unit, modules = HullTemplate.setmodulehelper(modules, "Cargo Bay", 4, 0, 1, cargo)
            if unit:
                initmodules.append(unit)
    
        #air scrubbers
        if passengers <= 10:
            if modules[0] > 0:
                modules[0] -= 1
                initmodules.append("Air Scrubbers 10")
            elif modules[1] > 0:
                modules[1] -= 1
                initmodules.append("Air Scrubbers 50")
            else:
                modules[2] -= 1
                initmodules.append("Air Scrubbers 500")
        elif passengers <= 50:
            if modules[1] > 0:
                modules[1] -= 1
                initmodules.append("Air Scrubbers 50")
            else:
                modules[2] -= 1
                initmodules.append("Air Scrubbers 500")
        elif passengers <= 500:
            modules[2] -= 1
            initmodules.append("Air Scrubbers 500")
        else:
            modules[3] -= 1
            initmodules.append("Air Scrubbers 2500")
        
        if carrier:
            flip = coin()
            if flip:
                unit = "Hangar"
            else:
                unit = "Vehicle Bay"
            unit, modules = HullTemplate.setmodulehelper(modules, unit, 4, 0, 1, numlist)
            if unit:
                initmodules.append(unit)
            
        #EEVs
        max = crew[1]
        while max > 0:
            if max >= 15:
                if modules[3] > 1:
                    modules[3] -= 1
                    initmodules.append("EEV 20")
                    max -= 20
                else:
                    modules[2] -= 1
                    initmodules.append("EEV 5")
                    max -= 5
            elif max >= 9:
                    modules[2] -= 1
                    initmodules.append("EEV 5")
                    max -= 5
            elif max > 2:
                if modules[1] > 1:
                    modules[1] -= 1
                    initmodules.append("EEV 4")
                    max -= 4
                elif modules[2] > 2:
                    modules[2] -= 2
                    initmodules.append("EEV 4")
                    initmodules.append("EEV 4")
                    max -= 8
                else:
                    modules[0] -= 1
                    initmodules.append("EEV 1")
                    max -= 1
            else:
                if modules[0] > 0:
                    modules[0] -= 1
                    initmodules.append("EEV 1")
                    max -= 1
                elif modules[1] > 0:
                    modules[1] -= 1
                    initmodules.append("EEV 4")
                    max -= 4
                elif modules[2] > 0:
                    modules[2] -= 1
                    initmodules.append("EEV 5")
                    max -= 5
                else:
                    modules[0] -= 1
                    initmodules.append("EEV 1")
                    max -= 1
        #More EEVs. Essentially a non-Carrier ship may end up with more cryopods than escape pods due to crew sizes
        #not meshing with the cryopods available. If Carrier is true, ship is carrying extra passengers on purpose. 
        #It's a dark future so don't need to handle all those folks, but should handle some.
        extra = passengers - crew[1]
        if extra > 0 and carrier:
            if extra >= 20:
                unit, modules = HullTemplate.setmodulehelper(modules, "EEV 1 x 20", 4, 2, 1)
                if unit:
                    initmodules.append(unit)
            elif extra > 7:
                for i in range(1):
                    unit, modules = HullTemplate.setmodulehelper(modules, "EEV", 2, 1, 1, evlist)
                    if unit:
                        initmodules.append(unit)
            else:
                unit, modules = HullTemplate.setmodulehelper(modules, "EEV", 2, 1, 1, evlist)
                if unit:
                    initmodules.append(unit)


        unit, modules = HullTemplate.setmodulehelper(modules, "Docking Umbilical", 1, 3)
        if unit:
            initmodules.append(unit)


        #Module count is random anyways and this is an easier fix than keeping track of cryo and galley separately.
        for i, module in enumerate(modules):
            if module < 0:
                modules[i] = 0
        self.modules = modules
        return initmodules
    
    #Modules is the current list of available modules.
    #Unit is what we're appending
    #Start is the starting tier to check
    #End is the last value to check
    #Direction if left blank or set to zero counts forward, direction set to 1 counts backwards
    #Lists is optional for appending to the name to the module.
    @staticmethod
    def setmodulehelper(modules, unit, start, end, direction=0, list=""):
        if direction == 0:
            for i, module in enumerate(modules):
                if i >= start and module > 0 and i <= end:
                    if list != "":
                        unit = unit + " " + str(list[i])
                    modules[i] -= 1
                    return unit, modules
        else:
            i = 4
            for module in reversed(modules):
                if i <= start and module > 0 and i >= end:
                    if list != "":
                        unit = unit + " " + str(list[i])
                    modules[i] -= 1
                    return unit, modules
                i -= 1
        return False, modules
    
    @property
    def thrusters(self):
        return self._thrusters
    
    @thrusters.setter
    def thrusters(self, thrusters):
        if thrusters == "" or not isinstance(thrusters, int):
            raise ValueError(f"Invalid thruster level {thrusters}.")
        self._thrusters = thrusters

    #Thrusters based on size and how heavily armed/armored the ship is
    def genthrusters(self, size, armorcat, ordenance, category):
        thrusters = 0
        match size:
            case "xsmall":
                thrusters = 2
            case "small":
                thrusters = 1
            case "smedium":
                thrusters = 0
            case "medium":
                thrusters = -1
            case "large":
                thrusters = -2
            case "xlarge":
                thrusters = -3
        if armorcat == "heavy" or ordenance == "heavy":
            thrusters -= 1
        if category == "cargo" or "colony":
            thrusters -= 1
        if category == "courier":
            thrusters += 1
        if thrusters > 3:
            thrusters = 3
        elif thrusters < -3:
            thrusters = -3
        return thrusters
                    

    def __str__(self):
        description = f"This is a {self.manufacturer} {self.shipmodel}, a {self.category} {self.hulltype} ship. \n"
        description += f"Crew: {self.crew} \nLength: {self.hullen} \nSignature: {self.signature} \nHull: {self.hullval} \nArmor: {self.armorval} \n"
        description += "Hardpoints: "
        count = 1
        for hardpoint in self.hardpoints:
            description += f"{count}: {hardpoint} "
            count += 1
        description += "\nModules Total: "
        count = 1
        for module in self.modules:
            description += f"{count}: {module} "
            count += 1
        description += "\nModules Set: "
        for module in self.initmodules:
            description += f"{module}, "
        return description


#Templates are used as a basic frame, then variety added here.
class HullModel:
    hp1weapons = ["Light Railgun"]
    hp2weapons = ["Short Missiles (8)", "Medium Railgun", "Light Energy Beam", "Mines"]
    hp3weapons = ["Long Missiles (8)", "Heavy Railgun", "Heavy Energy Beam", "Nukes"]
    hp1def = ["Sensor Decoys"]
    hp2def = ["Sensor Drones"]
    hp3def = ["Flak Array"]
    xsmalllist = ["None"]
    #defensivelist = hp1weapons + hp1def + hp2def + hp3def
    allweaponslist = hp1weapons + hp2weapons + hp3weapons + hp1def + hp2def + hp3def + xsmalllist

    def __init__(self, template):
        self.size = template.size
        self.pregenmodules = template.pregenmodules
        self.hulltype = template.hulltype
        self.category = template.category
        self.ordenance = template.ordenance
        self.carrier = template.carrier
        self.armorcat = template.armorcat
        self.hardpoints = template.hardpoints
        self.signature = template.signature
        self.crew = template.crew
        self.hullen = template.hullen
        self.hullval = template.hullval
        self.armorval = template.armorval
        self.modules = template.modules
        self.manufacturer = template.manufacturer
        self.shipmodel = template.shipmodel + " " + HullModel.genshipmodelsuffix()
        self.eqmodules = template.initmodules
        eqmodules = HullModel.genmodules(self, self.eqmodules, self.modules, self.hulltype, self.category, self.size)
        if eqmodules:
            self.eqmodules = eqmodules
        self.thrusters = template.thrusters
        self.eqweapons = HullModel.genweapons(self, self.ordenance, self.hardpoints)
        self.rooms = HullModel.genrooms(self, self.eqmodules, self.crew, self.size, self.category)

    @property
    def eqmodules(self):
        return self._eqmodules
    
    @eqmodules.setter
    def eqmodules(self, eqmodules):
        for module in eqmodules:
            if module == "" or not isinstance(module, str):
                raise ValueError(f"Invalid module {module}.")
        self._eqmodules = eqmodules


#TODO - new function that takes in the module, ideal size for module, and then iterates from that point until it can slot it in. 
# If it can, returns level of slot, else returns false.
#TODO actual list for modules.
    def genmodules(self, eqmodules, modules, type, category, size):
        cargo = [.5, 10, 250, 5000, 100000]
        numlist = [1, 2, 3, 4, 5]
        if "None" in eqmodules:
            return False
        flip = coin()
        if category == ("science" or "military") or size == ("medium" or "large" or "xlarge") or type == ("exploration" or "research") or flip:
            unit, modules = HullTemplate.setmodulehelper(modules, "Medlab", 1, 3)
            if unit:
                eqmodules.append(unit)
            
        flip = coin()
        if category == "science" or size == ("large" or "xlarge") or flip or type == ("exploration" or "research"):
            unit, modules = HullTemplate.setmodulehelper(modules, "Science Lab", 2, 3)
            if unit:
                eqmodules.append(unit)

        r = random.randint(1,100)
        if type == "yacht" or r < 90:
            unit, modules = HullTemplate.setmodulehelper(modules, "Corp Suite", 1, 2)
            if unit:
                eqmodules.append(unit)

        r = random.randint(1, 100)
        if category == "cargo" or (category == "military" and (size == "small" or "smedium")) or (size != "xlarge" and r > 70):
            unit, modules = HullTemplate.setmodulehelper(modules, "Tractor Hitch", 2, 3)
            if unit:
                eqmodules.append(unit)

        flip = coin()
        if flip and category == "cargo":
            unit, modules = HullTemplate.setmodulehelper(modules, "Salvage Crane", 2, 3)
            if unit:
                eqmodules.append(unit)

        
        passes = 0
        while passes < 3:
            unit, modules = HullTemplate.setmodulehelper(modules, "Cargo Bay", 4, 0, 1, cargo)
            if unit:
                eqmodules.append(unit)
            passes += 1
        flip = coin()
        if flip:
            flip = coin()
            unit = False
            if flip:
                unit, modules = HullTemplate.setmodulehelper(modules, "Vehicle Bay", 4, 0, 1, numlist)
            else:
                unit, modules = HullTemplate.setmodulehelper(modules, "Hangar", 4, 0, 1, numlist)
            if unit:
                eqmodules.append(unit)
        self.modules = modules
        return eqmodules  
        
    @property
    def eqweapons(self):
        return self._eqweapons
    
    @eqweapons.setter
    def eqweapons(self, eqweapons):
        for weapon in eqweapons:
            if weapon not in HullModel.allweaponslist:
                raise ValueError(f"Invalid weapon {weapon}.")
        self._eqweapons = eqweapons

    def genweapons(self, ordenance, hardpoints):
        eqweapons = []
        ratio = 0
        match ordenance:
            case "none":
                eqweapons.append("None")
                return eqweapons
            case "light":
                ratio = 5
            case "defensive":
                ratio = 4
            case "medium":
                ratio = 6
            case "heavy":
                ratio = 7
            case "support":
                ratio = 6
        offense = ""
        for i, hardpoint in enumerate(hardpoints):
            for j in range(hardpoint):
                if hardpoint > 0:
                    r = random.randint(1, 9)
                    if r < ratio:
                        offense = True
                    else:
                        offense = False
                    eqweapons.append(HullModel.getweapons(self, offense, i))
        return eqweapons

#level starts at 0 due to computers
    def getweapons(cls, offensive, level):
        tlist = ""
        if level == 0:
            if offensive:
                tlist = HullModel.hp1weapons
            else:
                tlist = HullModel.hp1def
        elif level == 1:
            if offensive:
                tlist = HullModel.hp2weapons
            else:
                tlist = HullModel.hp2def
        else:
            if offensive:
                tlist = HullModel.hp3weapons
            else:
                tlist = HullModel.hp3def
        return random.choice(tlist)
    

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
    def rooms(self):
        return self._rooms
    
    @rooms.setter
    def rooms(self, rooms):
        self._rooms = rooms
    
    #Assumes every ship will have a bridge and AI core and that the Galley will match the cryodeck capacity.
    def genrooms(self, eqmodules, crew, size, category):
        roomlist = ["Bridge", "AI Access", "Air Scrubbers", "Engine Room", "Reactor Core"]
        bodies = 0
        qtype = ""
        #Find capacity of ship
        r = 1
        for module in eqmodules:
            match module:
                case "Cryo 1":
                    bodies += 1
                case "Cryo 10":
                    bodies += 10
                case "Cryo 50":
                    bodies += 50
                    r += 1
                case "Cryo 500":
                    bodies += 500
                    r += 3
                case "Cryo 2500":
                    bodies += 2500
                    r += 6
        if bodies > 0:
            roomlist.append(f"Cryo Deck x{str(r)}")
        if bodies / crew[1] > 2:
            qtype = "tight"
        else:
            qtype = "accom"
        roomlist = roomlist + HullModel.genroomlivquarters(self, qtype, bodies, crew[1], category)
        if size != ("xsmall" or "small"):
            roomlist.append("Quarantine Bunk")
            roomlist.append("Quarantine Rec")
            roomlist.append("Decontamination")
            roomlist.append("AI Core")
            roomlist.append("Workroom x2")
            roomlist.append("Reactor Core")
            roomlist.append("Coolant Tanks")
            roomlist.append("Air Scrubbers")
            roomlist.append("Captain's Quarters")
            roomlist.append("Admin")
            roomlist.append("Briefing Room")
            roomlist.append("Comm Array")
        elif size == ("small"):
            roomlist.append("Workroom")
            flip = coin()
            if flip:
                roomlist.append("Quarantine Bunk")
        rooms = HullModel.genroomscimed(self, eqmodules, size)
        if rooms:
            roomlist += rooms
        rooms = ""
        rooms = HullModel.genroomhangar(self, eqmodules)
        if rooms:
            roomlist += rooms
        rooms = ""
        rooms = HullModel.genroommilitary(self, category, size)
        if rooms:
            roomlist += rooms
        rooms = ""
        rooms = HullModel.genroomcargo(self, eqmodules)
        if rooms:
            roomlist += rooms
        rooms = ""
        roomlist = roomlist + HullModel.genroomairlocks(self, size)
        return roomlist
    
    def genroomcargo(self, eqmodules):
        rooms = []
        for module in eqmodules:
            if module == ("Cargo Bay .5" or "Cargo Bay 10" or "Cargo Bay 250" or "Cargo Bay 5000" or "Cargo Bay 100000"):
                rooms.append(module)
        if rooms:
            return rooms

    def genroommilitary(self, category, size):
        rooms = []
        if category == "military":
            if size != ("xsmall" or "small"):
                rooms.append("Brig")
                rooms.append("Munitions Storage")
            if size == ("large" or "xlarge"):
                rooms.append("Munitions Storage")
        if rooms:
            return rooms

    #Not all airlocks are going to have suit storage
    def genroomairlocks(self, size):
        r =  1
        rooms = []
        match size: 
            case "smedium":
                r += 1
            case "medium":
                r += 2
            case "large":
                r += 4
            case "xlarge":
                r += 8
        if size != "xsmall":
            flip = coin()
            if flip:
                    r += 1
        rooms.append(f"Airlock x{str(r)}")
        rooms.append(f"EEV Suit Storage x{str(r)}")
        return rooms

    
    def genroomhangar(self, eqmodules):
        rooms = []
        for module in eqmodules:
            span = re.search("Hangar", module)
            if span:
                rooms.append(module)
            span = re.search("Vehicle", module)
            if span:
                rooms.append(module)
        if rooms:
            rooms.append("Ready Room")
            rooms.append("Vehicle Workshop")
            rooms.append("Parts Storage")
            return rooms
        
        
    def genroomscimed(self, eqmodules, size):
        rooms = []
        s = 0
        if "Science Lab" in eqmodules:
            s += 1
            rooms.append("Science Stores")
            if size != ("small" or "xsmall"):
                s += 1
            if size == ("large" or "xlarge"):
                s += 1
            if s > 0:
                rooms.append(f"Science Lab x{str(s)}")
        if "Medlab" in eqmodules:
            if size == ("large" or "xlarge"):
                rooms.append("Infirmary x2")
            else:
                rooms.append("Infirmary")
        if rooms:
            return rooms

            
        


    #Creates bunks, bathrooms, and lockers
    def genroomlivquarters(self, qtype, bodies, crew, category):
        rooms = []
        if qtype == "tight" and (category != "colony" or bodies != 2500):
            split = math.ceil(bodies/6)
            rooms.append(f"Dorm Bunks x{str(split)}")
            rooms.append(f"Lockers x{str(math.ceil(split/4))}")
            rooms.append(f"Bathroom x{str(math.ceil(split/15))}")
        else:
            split = math.ceil(crew/4)
            rooms.append(f"Bunks x{str(split)}")
            rooms.append(f"Lockers x{str(math.ceil(split/4))}")
            rooms.append(f"Bathroom x{str(math.ceil(split/10))}")
        return rooms





    def __str__(self):
        description = f"This is a {self.manufacturer} {self.shipmodel}, a {self.category} {self.hulltype} ship. \n"
        description += f"Crew: {self.crew} \nLength: {self.hullen} \nSignature: {self.signature} \nHull: {self.hullval} \nArmor: {self.armorval} \n"
        description += "Hardpoints: "
        count = 1
        for hardpoint in self.hardpoints:
            description += f"{count}: {hardpoint} "
            count += 1
        description += "\nModules Total: "
        count = 1
        for module in self.modules:
            description += f"{count}: {module} "
            count += 1
        description += "\nOriginal Modules: "
        count = 1
        for module in self.pregenmodules:
            description += f"{count}: {module} "
            count += 1
        description += "\nModules Set: "
        for module in self.eqmodules:
            description += f"{module}, "
        description += f"\nWeapons: "
        count = 1
        for weapon in self.eqweapons:
            description += f"{weapon}, "
        description += f"\nRooms: "
        count = 1
        for room in self.rooms:
            description += f"{room}, "
        description += "\n"
        return description




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
    HullSpecs.hulls.append(HullTemplate("xlarge", "transport", "colony", "none", True, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "exploration", "science", "defensive", False, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "exploration", "private", "defensive", False, "light"))
    HullSpecs.hulls.append(HullTemplate("smedium", "exploration", "government", "defensive", False, "light"))
    HullSpecs.hulls.append(HullTemplate("large", "mobile dockyard", "any", "defensive", True, "light"))
    HullSpecs.hulls.append(HullTemplate("xlarge", "galleon", "cargo", "defensive", False, "medium"))



#hull = HullTemplate("small", "heavy dropship", "military", "light", True, "heavy")
#print(HullModel(hull))
initializehulls()
for hull in HullSpecs.hulls:
    print(HullModel(hull))