import random, math
from gencorp import Corp
import namelists
import string, copy, re
from helpers import coin
from shipparts import Module, ShipRoomType

#Size of small not currently supported as it will not receive modules.
#Types do not drive any behavior, but can be used to assign other variables if they are not present upon building class.
#Categories have some 
class HullTemplate:
    sizes = ["small", "smedium", "medium", "large", "xlarge"]
    types = ["skiff", "dropship", "transport", "frigate", "corvette", "destroyer", "cruiser", 
            "carrier", "battleship", "mobile dockyard",
            "minehunter", "galleon", "monitor", "patrol", "research", "yacht", 
            "miner", "freighter", "colony", "exploration"]
    shipcategories = ["courier", "cargo", "warship", "passenger", "science", "luxury",  
                      "colony", "industrial", "support", "lander", "transport", "carrier", "exploration", "research"]
    ordenancelevels = ["none", "light", "defensive", "medium", "heavy", "support"]
    armorlevels = ["light", "medium", "heavy"]
    shiprange = ["short", "medium", "long"]
    priorities = ["cargo", "speed", "quality", "stealth", "signal", "carrier", "rail", "missile", "lander", "troops", "mines"]
    #Eventually add function to combine this list with the existing list, so new categories can be added. Then can export just
    #these categories when creating saving format, probably JSON.
    newtypes = []
    newshipcategories = []
    newordenancelevels = []
    newarmorlevesl =[]
    

#TODO new variable for getsmodules. Can then skip for things like dropships and escape pods
#checks for carrier and armor
#TODO defaults for variables should be a randomizing function
    def __init__(self, size, hulltype, category, ordenance, armorcat, troops, priority=""):
        self.size = size
        self.hulltype = hulltype
        self.category = category
        self.ordenance = ordenance
        self.armorcat = armorcat
        self.priority = priority
        self.hardpoints = HullTemplate.genhardpoints(self, self.size, self.ordenance)
        self.signature = HullTemplate.gensignature(self, self.size, self.priority)
        self.crew = HullTemplate.gencrew(self, self.size)
        self.hullen = HullTemplate.genhullen(self, self.size)
        self.hullval = HullTemplate.genhullval(self, self.size, self.category)
        self.armorval = HullTemplate.genarmorval(self, self.armorcat, self.hullval)
        self.modules = HullTemplate.genmodules(self, self.size, self.priority)
        self.squads = HullTemplate.gensquadcount(size, troops, self.priority, category)
        #More robust manufacturer functionality, choose from Corps once gencorp is more built out. If new, save to list
        self.manufacturer = Corp.gencorpname()
        self.shipmodel = HullTemplate.genshipmodel(self, self.category)
        self.eqmodules = HullTemplate.geninitmodules(self, self.modules, self.category, self.crew, self.size, self.squads)
        self.availmodules = HullTemplate.countavailmodules(self.modules, self.eqmodules, 1)
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
    def armorcat(self):
        return self._armorcat
    
    @armorcat.setter
    def armorcat(self, armorcat):
        if armorcat == "" or armorcat not in HullTemplate.armorlevels:
            raise ValueError(f"Invalid armor level {armorcat}.")
        self._armorcat = armorcat

    @property
    def priority(self):
        return self._priority
    
    @priority.setter
    def priority(self, priority):
        if priority != "" and priority not in HullTemplate.priorities:
            raise ValueError(f"Invalid priority {priority}.")
        self._priority = priority

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

    def gensignature(self, size, priority):
        match size:
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
        if priority == "stealth":
            signature -= 2
        if signature < -3:
            signature = -3
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
            case "small":
                hullen = random.randint(15,70)
            case "smedium":
                hullen = random.randint(70,225)
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
        if category == "warship":
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

    def genmodules(self, size, priority):
        modules = [0, 0, 0, 0, 0]
        match size:
            case "xsmall":
                modules[0] = random.randint(3,4)
                modules[1] = random.randint(2,3)
            case "small":
                modules[0] = random.randint(4,8)
                modules[1] = random.randint(2,6)
                modules[2] = random.randint(3,3)
            case "smedium":
                modules[0] = random.randint(5,9)
                modules[1] = random.randint(3,7)
                modules[2] = random.randint(3,4)
            case "medium":
                modules[1] = random.randint(7,9)
                modules[2] = random.randint(4,7)
                modules[3] = random.randint(4,5)
            case "large":
                modules[2] = random.randint(7,9)
                modules[3] = random.randint(5,8)
                modules[4] = random.randint(5,6)
            case "xlarge":
                modules[2] = random.randint(10,17)
                modules[3] = random.randint(9,14)
                modules[4] = random.randint(6,9)
        if priority == "quality":
            for i, module in enumerate(modules):
                modules[i] += 1
        return modules

    @property
    def shipmodel(self):
        return self._shipmodel
    
    @shipmodel.setter
    def shipmodel(self, shipmodel):
        if shipmodel == "" or not isinstance(shipmodel, str):
            raise ValueError(f"Invalid shipmodel {shipmodel}.")
        self._shipmodel = shipmodel
    

    def genshipmodel(self, category):
        choices = []
        match category:
            case "courier":
                choices.append(namelists.returnNamelist("courier"))
            case "cargo":
                choices.append(namelists.returnNamelist("cargo"))
            case "warship":
                choices.append(namelists.returnNamelist("mythical"))
                choices.append(namelists.returnNamelist("fantasy"))
                choices.append(namelists.returnNamelist("predator"))
                choices.append(namelists.returnNamelist("weather"))
            case "luxury":
                choices.append(namelists.returnNamelist("yacht"))
            case "exploration":
                choices.append(namelists.returnNamelist("explorer"))
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

    @property
    def squads(self):
        return self._squads
    
    @squads.setter
    def squads(self, squads):
        if squads < 0:
            raise ValueError(f"Invalid number of squads {squads}.")
        self._squads = squads
        
    #TODO review code and make failed returns consistent between none and False.
    #squad size is 26 for 20 marines, 2 crew/dropship, and 2 command staff
    #sets the max squad size based on what seems reasonable based on ship size, adds more if priority is transporting troops.
    #Picks a random number as how many troops are actually carried since cryodeck max isn't what is cannonically in use.
    @staticmethod
    def gensquadcount(size, troops, priority, category):
        squads = 0
        if not troops:
            return squads
        min = 1
        match size:
            case "small":
                squads = 1
            case "smedium":
                squads = 2
            case "medium":
                squads = 4
            case "large":
                squads = 8
            case "xlarge":
                squads = 16
        if priority != "troops" or (category != "transport") and size != "small":
            squads = math.ceil(squads / 2)
        if priority == "troops" or category == "transport":
            min = int(squads/2)
        squads = (random.randint(min, squads)) #doesn't take crew into account, will deal with elsewhere in case passengers too.
        return squads

    #Need air scrubbers, AI, cryodeck, docking umbilical and galley. 
    #Cargo requires at least one cargo bay, may split off each type to own function.
    #Also changes value for modules
    def geninitmodules(self, modules, category, crew,  priority, squads):
        initmodules = []
        # Retains original module count for troubleshooting
        cmodules = copy.copy(modules)
        
        #set AI in smallest slot
        lvl = HullTemplate.findopenmodule(cmodules, 0, 4, 1, direction=0)
        if lvl != "":
            initmodules.append(Module("AI", lvl, 1))
            cmodules[lvl] -= 1

        passengers = HullTemplate.genpassengers(modules, category, priority)
        if passengers > 0:
            passengers -= crew[1]
        capacity = passengers + (squads*26) + crew[1]
        capacitylvl = HullTemplate.findpopmodule(capacity)
        if category == "passenger" or "colony":
            quant = 1
        else:
            quant = 2
        lvl = HullTemplate.findopenmodule(cmodules, capacitylvl, 4, quant, 0)
        if lvl != "":
            initmodules.append(Module("Cryo", lvl, 1))
            cmodules[lvl] -= 1
            if capacitylvl != 0:
                airlvl = capacitylvl - 1
            else:
                airlvl = capacitylvl
            airlvl = HullTemplate.findopenmodule(cmodules, airlvl, 4, 1, 0)
            initmodules.append(Module("Air Scrubbers", airlvl, 1))
            cmodules[airlvl] -= 1
        else:
            raise ValueError("Unable to set appropriate cryo module level for hull template.")
        if quant != 2:
            capacitylvl = HullTemplate.findpopmodule(crew[1])
        lvl = HullTemplate.findopenmodule(cmodules, capacitylvl, 4, 1, 0) #confirm there is still galley room in case air scrubbers somehow stole slot.
        if lvl != "":
            initmodules.append(Module("Galley", lvl, 1))
            cmodules[lvl] -= 1
        else:
            raise ValueError("Unable to set appropriate galley level for hull template.")

        #No error message here, because dropships are a matter of us trying our best. 
        if squads > 0:
            dropships = HullTemplate.dropshipcalc(cmodules, priority, squads)
            for i, dropship in enumerate(dropships):
                if dropship > 0:
                    initmodules.append(Module("Hangar", i, dropship))
                    cmodules[i] -= 1
        
        elif category == "carrier" or priority == "carrier":
            lvl = HullTemplate.findopenmodule(cmodules, 4, 1, 1, 1)
            if lvl != "":
                initmodules.append(Module("Hangar", lvl, 1))
                cmodules[lvl] -= 1
        
        if category == "cargo" or priority == "cargo":
            lvl = HullTemplate.findopenmodule(cmodules, 4, 0, 2, 1)
            if lvl != "":
                initmodules.append(Module("Cargo Bay", lvl, 2))
                cmodules[lvl] -= 2
    
            #can maybe revamp the dropship function, but also the previous logic isn't awful. Would be good to have a function that could permutate through 
            #the options and see what's the most efficient. Like start at 4 and work down, then start at 0 and work up, then start at 2 and work down then at 2 and work up.
            #Then compare results and see what was the most efficient.
            ...#maybe warship function to set a x20 escape pods because those are cool.
        eevs = HullTemplate.eevcalc(cmodules, crew[1])
        for i, eev in enumerate(eevs):
            if eev > 0:
                initmodules.append(Module("EEV", i, eev))
                cmodules[i] -= eev

        lvl = HullTemplate.findopenmodule(cmodules, 1, 4, 1, direction=0)
        if lvl != "":
            initmodules.append(Module("Docking", lvl, 1))
            cmodules[lvl] -= 1

        if category == ("exploration" or "lander" or "colony"):
                lvl = HullTemplate.findopenmodule(cmodules, 3, 1, 1, 1)
                if lvl != "":
                    cmodules.append(Module("Vehicle Bay", lvl, 1))
                    modules[lvl] -= 1

        return initmodules

    @staticmethod
    def eevcalc(cmodules, bodies):
        evlist = [1, 4, 5, 20, 20]
        eevs = [0, 0, 0, 0, 0]
        while (bodies > 0):
            lvl = ""
            if bodies > 15:
                lvl = HullTemplate.findopenmodule(cmodules, 3, 3, 1, 1)
                if lvl == "":
                    lvl = HullTemplate.findopenmodule(cmodules, 4, 0, 1, 1) #attempt to save the larger slots
            elif bodies >= 9:
                lvl = HullTemplate.findopenmodule(cmodules, 2, 0, 1, 1)
            elif bodies >= 2:
                lvl = HullTemplate.findopenmodule(cmodules, 1, 0, 1, 1)
            else:
                lvl = HullTemplate.findopenmodule(cmodules, 0, 4, 1, 0)
            if lvl == "":
                lvl = HullTemplate.findopenmodule(cmodules, 0, 4, 1, 0)
            if lvl !="":
                eevs[lvl] += 1
                cmodules[lvl] -= 1
                bodies -= evlist[lvl]
            else:
                break
        return eevs




    #Takes in squads and remaining modules, pops out the amount of hangars needed to support 
    @staticmethod
    def dropshipcalc(cmodules, priority, squads):
        #Calculate how many dropships needed to support squad count
        if priority != "lander" and squads > 0:
            shipcnt = math.ceil(squads / 2)
            baysize = [1, 1, 2, 3, 5] #How many dropships fit in each hanger level
            stored = [0, 0, 0, 0, 0]
            saved = 0
            while saved < shipcnt:
                lvl = HullTemplate.findopenmodule(cmodules, 4, 0, 1, 1)
                if lvl:
                    saved += baysize[lvl]
                    cmodules[lvl] -= 1
                    stored[lvl] += 1
                else:
                    return False
        return stored



    #TODO Need to make it so that civilian transport and military transport are mutually exclusive.
    #Gets the highest amount of passengers the ship can support using all modules of the same level.
    def genpassengers(modules, category, priority):
        if category == ("passenger" or "colony"): #Cryo, Air
            quant = 2
        elif priority == "transport": #Cryo, air, galley
            quant = 3
        else:
            return 0
        passengerlvl =  HullTemplate.findopenmodule(modules, 4, 0, quant, 1)
        return Module.poplvls[passengerlvl]
    
    @classmethod
    def findpopmodule(cls, capacity):
        for i, lvl in enumerate(Module.poplvls):
            if lvl >= capacity:
                return i
        

    #Modules is a list of open modules
    #Start is the module level to start search, end is end search (up to and including)
    #Quant is quantity of modules you want found
    #Direction 0 loops upwards, direction=1 loops downwards
    @staticmethod
    def findopenmodule(modules, start, end, quant, direction=0):
        if direction == 0:
            for i, module in enumerate(modules):
                if i >= start and module >= quant and i <= end:
                    return i
        else:
            i = 4
            for module in reversed(modules):
                if i <= start and module >= quant and i >= end:
                    return i
                i -= 1
        return ""


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
    
    @property
    def availmodules(self):
        return self._availmodules
    
    @availmodules.setter
    def availmodules(self, availmodules):
        for module in availmodules:
            if module < 0:
                raise ValueError(f"Module count must be greater than or equal to 0, not {module}.")
        self._availmodules = availmodules

    #Initmodules is a list of module slots that the ship had before having modules equipped. 
    #Savedmodules is a list of module classes assigned to the ship.
    #Guard will set the number of available modueles to 0 rather than returning a negative number. Ensures it is possible to generate a ship
    #that meets all ship requirements despite having a random module count. Set to 1 to ignore.
    @staticmethod
    def countavailmodules(initmodules, savedmodules, guard=0):
        for module in savedmodules:
            initmodules[module.lvl] -= module.quantity
        if guard == 1:
            for i, module in enumerate(initmodules):
                if module < 0:
                    initmodules[i] = 0
        return initmodules

                    

    def __str__(self):
        description = f"This is a {self.manufacturer} {self.shipmodel}, a {self.category} {self.hulltype} ship. \n"
        description += f"Crew: {self.crew} \nLength: {self.hullen} \nSignature: {self.signature} \nHull: {self.hullval} \nArmor: {self.armorval} \nThrusters: {self.thrusters}\n"
        description += "Hardpoints: "
        count = 1
        for hardpoint in self.hardpoints:
            description += f"{count}: {hardpoint} "
            count += 1
        description += "\nModules Total: "
        count = 1
        for module in self.availmodules:
            description += f"{count}: {module} "
            count += 1
        description += "\nModules Set: "
        for module in self.eqmodules:
            description += f"{module.name} x{module.quantity}, "
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
        self.hulltype = template.hulltype
        self.category = template.category
        self.ordenance = template.ordenance
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
        self.eqmodules = template.eqmodules
        self.priority = template.priority
        self.availmodules = template.availmodules
        self.squads = template.squads
        eqmodules = HullModel.genmodules(self, self.eqmodules, self.modules, self.priority, self.category, self.size)
        if eqmodules:
            self.eqmodules = self.eqmodules + eqmodules
        self.thrusters = template.thrusters
        self.eqweapons = HullModel.genweapons(self, self.ordenance, self.hardpoints, self.priority)
        self.rooms = HullModel.genrooms(self, self.eqmodules, self.crew, self.size, self.category, self.squads)

    @property
    def eqmodules(self):
        return self._eqmodules
    
    @eqmodules.setter
    def eqmodules(self, eqmodules):
        for module in eqmodules:
            if module.type not in Module.all:
                raise ValueError(f"Invalid module {module.name}.")
        self._eqmodules = eqmodules


#TODO - new function that takes in the module, ideal size for module, and then iterates from that point until it can slot it in. 
# If it can, returns level of slot, else returns false.
#TODO actual list for modules.
    def genmodules(self, eqmodules, modules, priority, category, size):
        if "None" in eqmodules:
            return False
        flip = coin()
        if category == ("science" or "warship" or "exploration" or "research") or size == ("medium" or "large" or "xlarge") or flip:
            lvl = HullTemplate.findopenmodule(modules, 1, 3, 1, 0)
            if lvl != "":
                eqmodules.append(Module("Medlab", lvl, 1))
                modules[lvl] -= 1
            
        flip = coin()
        if category == ("exploration" or "research" or "science") or size == ("large" or "xlarge") or flip:
            lvl = HullTemplate.findopenmodule(modules, 2, 3, 1, 0)
            if lvl != "":
                eqmodules.append(Module("Science Lab", lvl, 1))
                modules[lvl] -= 1
                

        r = random.randint(1,100)
        if category == "luxury" or r < 90:
            lvl = HullTemplate.findopenmodule(modules, 1, 2, 1, 0)
            if lvl != "":
                eqmodules.append(Module("Corp Suite", lvl, 1))
                modules[lvl] -= 1

        r = random.randint(1, 100)
        if category == "cargo" or (category == "warship" and (size == "small" or "smedium")) or (size != "xlarge" and r > 70):
            lvl = HullTemplate.findopenmodule(modules, 2, 3, 1, 0)
            if lvl != "":
                eqmodules.append(Module("Tractor", lvl, 1))
                modules[lvl] -= 1

        flip = coin()
        crane = False
        if flip and category == "cargo":
            crane = True
        if crane == True or priority == "salvage":
            lvl = HullTemplate.findopenmodule(modules, 2, 3, 1, 0)
            if lvl != "":
                eqmodules.append(Module("Crane", lvl, 1))
                modules[lvl] -= 1
        
        for i in range(2):
            lvl = HullTemplate.findopenmodule(modules, 4, 0, 1, 0)
            if lvl != "":
                eqmodules.append(Module("Cargo Bay", lvl, 1))
                modules[lvl] -= 1
        
        for i in range(1):
            flip = coin()
            if flip == 1:
                flip = coin()
                if flip == 1:
                    type = "Vehicle Bay"
                else:
                    type = "Hangar"
                lvl = HullTemplate.findopenmodule(modules, 3, 0, 1, 0)
                if lvl != "":
                    eqmodules.append(Module(type, lvl, 1))
                    modules[lvl] -= 1
    
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

    def genweapons(self, ordenance, hardpoints, priority):
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
                    eqweapons.append(HullModel.getweapons(self, offense, i, priority))
        return eqweapons

#level starts at 0 due to computers
    def getweapons(cls, offensive, level, priority):
        tlist = ""
        if level == 0:
            if offensive:
                tlist = HullModel.hp1weapons
            else:
                tlist = HullModel.hp1def
        elif level == 1:
            if offensive:
                if priority == "rail":
                    return "Medium Railgun"
                elif priority == "missiles":
                    return "Short Missiles (8)"
                elif priority == "mines":
                    return "Mines"
                tlist = HullModel.hp2weapons
            else:
                tlist = HullModel.hp2def
        else:
            if offensive:
                if priority == "rail":
                    return "Heavy Railgun"
                elif priority == "missiles":
                    return "Long Missiles (8)"
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
    def genrooms(self, eqmodules, crew, shipsize, category, squads):
        roomdefault = ["Bridge", "Engine Room", "Reactor Core"]
        roomlist = []
        qtype = ""
        #Find capacity of ship
        r = 1

        for room in roomdefault:
            roomlist.append(ShipRoomType(room, 0, 1, shipsize))
        for module in eqmodules:
            for room in module.rooms:
                roomlist.append(ShipRoomType(room, module.lvl, module.quantity, shipsize))
        bodies = crew[1] + (squads * 26)
        
        if bodies / crew[1] > 2:
            qtype = "tight"
        else:
            qtype = "accom"
        roomlist = roomlist + HullModel.genroomlivquarters(self, qtype, bodies, shipsize)
        if shipsize != ("xsmall" or "small"):
            roomlist.append(ShipRoomType("Quarantine Bunk", 0, 1, shipsize))
            roomlist.append(ShipRoomType("Quarantine Rec", 0, 1, shipsize))
            roomlist.append(ShipRoomType("Decontamination", 0, 1, shipsize))
            roomlist.append(ShipRoomType("AI Core", 0, 1, shipsize))
            roomlist.append(ShipRoomType("Workroom", 0, 2, shipsize))
            roomlist.append(ShipRoomType("Coolant Tanks", 0, 1, shipsize))
            roomlist.append(ShipRoomType("Briefing Room", 0, 1, shipsize))
            roomlist.append(ShipRoomType("Comm Array", 0, 1, shipsize))
        elif shipsize == ("small"):
            roomlist.append(ShipRoomType("Workroom", 0, 1, shipsize))
            flip = coin()
            if flip or (category == "science" or "research" or "exploration"):
                roomlist.append(ShipRoomType("Decontamination", 0, 1, shipsize))
            flip = coin()
            if flip:
                roomlist.append(ShipRoomType("Comm Array", 0, 1, shipsize))
        if shipsize == ("large" or "xlarge"):
            r = random.randint(1,4)
            roomlist.append(ShipRoomType("Private Quarters", 0, r, shipsize))
            roomlist.append(ShipRoomType("Admin Office", 0, 1, shipsize))
        
        rooms = HullModel.genroommilitary(self, category, shipsize)
        if rooms:
            roomlist += rooms
        rooms = ""
        r = HullModel.genroomairlocks(self, shipsize)
        roomlist.append(ShipRoomType("Airlock", 0, r, shipsize))
        roomlist.append(ShipRoomType("EEV Suit Storage", 0, r, shipsize))
        return roomlist
    

    def genroommilitary(self, category, shipsize):
        rooms = []
        if category == "warship":
            if shipsize != ("xsmall" or "small"):
                rooms.append(ShipRoomType("Brig", 0, 1, shipsize))
                quant = 1
                if shipsize == ("large" or "xlarge"):
                    quant = 2
                rooms.append(ShipRoomType("Munitions Storage", 0, quant, shipsize))
        if rooms:
            return rooms

    #Not all airlocks are going to have suit storage
    def genroomairlocks(self, size):
        r =  1
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
        return r


    #Creates bunks, bathrooms, and lockers
    def genroomlivquarters(self, qtype, bodies, shipsize):
        rooms = []
        if qtype == "tight":
            split = math.ceil(bodies/6)
            rooms.append(ShipRoomType("Dorm Bunks", 0, split, shipsize))
            rooms.append(ShipRoomType("Locker Room", 1, math.ceil(split/4), shipsize))
            rooms.append(ShipRoomType("Bathroom", 1, math.ceil(split/15), shipsize))
        else:
            split = math.ceil(bodies/4)
            rooms.append(ShipRoomType("Bunks", 0, split, shipsize))
            rooms.append(ShipRoomType("Lockers", 0, math.ceil(split/4), shipsize))
            rooms.append(ShipRoomType("Bathroom", 0, math.ceil(split/10), shipsize))
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
    HullSpecs.hulls.append(HullTemplate("small", "skiff", "industrial", "none", "light", False))
    HullSpecs.hulls.append(HullTemplate("small", "dropship", "warship", "none", "light", True, "lander"))
    HullSpecs.hulls.append(HullTemplate("small", "dropship", "warship", "light", "heavy", True, "lander"))
    HullSpecs.hulls.append(HullTemplate("small", "transport", "warship", "light", "medium", True, "lander"))
    HullSpecs.hulls.append(HullTemplate("medium", "frigate", "warship", "medium", "medium", True))
    HullSpecs.hulls.append(HullTemplate("smedium", "frigate", "warship", "light", "light", False))
    HullSpecs.hulls.append(HullTemplate("smedium", "frigate", "warship", "medium", "light", True))
    HullSpecs.hulls.append(HullTemplate("medium", "frigate", "warship", "defensive", "light", True))
    HullSpecs.hulls.append(HullTemplate("smedium", "corvette", "warship", "medium", "light", True))
    HullSpecs.hulls.append(HullTemplate("smedium", "corvette", "warship", "light", "light", True))
    HullSpecs.hulls.append(HullTemplate("smedium", "corvette", "warship", "heavy", "medium", True))
    HullSpecs.hulls.append(HullTemplate("smedium", "corvette", "warship", "defensive", "light", True))
    HullSpecs.hulls.append(HullTemplate("medium", "destroyer", "warship", "heavy", "heavy", True))
    HullSpecs.hulls.append(HullTemplate("medium", "destroyer", "warship", "heavy", "heavy", True))
    HullSpecs.hulls.append(HullTemplate("medium", "cruiser", "warship", "heavy", "heavy", True))
    HullSpecs.hulls.append(HullTemplate("medium", "cruiser", "warship", "support", "medium", True))
    HullSpecs.hulls.append(HullTemplate("large", "carrier", "warship", "support", "medium", True))
    HullSpecs.hulls.append(HullTemplate("medium", "carrier", "warship", "medium", "medium", True))
    HullSpecs.hulls.append(HullTemplate("large", "carrier", "warship", "medium", "heavy", True))
    HullSpecs.hulls.append(HullTemplate("large", "battleship", "warship", "heavy", "heavy", True))
    HullSpecs.hulls.append(HullTemplate("medium", "minehunter", "warship", "support", "light", False)) 
    HullSpecs.hulls.append(HullTemplate("small", "monitor", "warship", "heavy", "heavy", False))
    HullSpecs.hulls.append(HullTemplate("smedium", "patrol", "warship", "light", "light", False))
    HullSpecs.hulls.append(HullTemplate("smedium", "patrol", "courier", "light", "light", False))
    HullSpecs.hulls.append(HullTemplate("smedium", "research", "science", "none", "light", False))
    HullSpecs.hulls.append(HullTemplate("smedium", "yacht", "luxury", "none", "light", False))
    HullSpecs.hulls.append(HullTemplate("small", "miner", "cargo", "none", "light", False))
    HullSpecs.hulls.append(HullTemplate("smedium", "freighter", "cargo", "none", "light", False))
    HullSpecs.hulls.append(HullTemplate("medium", "freighter", "cargo", "none", "light", False))
    HullSpecs.hulls.append(HullTemplate("xlarge", "transport", "colony", "none", "light", False))
    HullSpecs.hulls.append(HullTemplate("smedium", "exploration", "science", "defensive", "light", False))
    HullSpecs.hulls.append(HullTemplate("smedium", "exploration", "lander", "defensive", "light", False))
    HullSpecs.hulls.append(HullTemplate("smedium", "exploration", "luxury", "defensive", "light", False))
    HullSpecs.hulls.append(HullTemplate("large", "mobile dockyard", "industrial", "defensive", "light", False))
    HullSpecs.hulls.append(HullTemplate("xlarge", "galleon", "cargo", "defensive", "medium", False))

#initializehulls()
#for hull in HullSpecs.hulls:
    #print(hull)

#hull = HullTemplate("small", "heavy dropship", "military", "light", True, "heavy")
#print(HullModel(hull))
initializehulls()
for hull in HullSpecs.hulls:
    print(HullModel(hull))