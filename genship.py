import random
from helpers import coin
from gennpc import Npc
import namelists, genmeow
from factions import FactionList, Faction



class Ship:

    def __init__(self, size, hulltype, category, hardpoints, signature, crew, hullen, hullval, armorval, modules, manufacturer, shipmodel, 
        eqmodules, availmodules, squads, thrusters, eqweapons, rooms, ftl, factionid, name, crewsize, cat, crewlist, prefix, id):
        self.size = size
        self.hulltype = hulltype
        self.category = category
        self.hardpoints = hardpoints
        self.signature = signature
        self.crew = crew
        self.hullen = hullen
        self.hullval = hullval
        self.armorval = armorval
        self.modules = modules
        self.manufacturer = manufacturer
        self.shipmodel = shipmodel
        self.eqmodules = eqmodules
        self.availmodules = availmodules
        self.squads = squads
        self.thrusters = thrusters
        self.eqweapons = eqweapons
        self.rooms = rooms
        self.ftl = ftl
        self.factionid = factionid
        self.name = name
        self.crewsize = crewsize
        self.cat = cat
        self.crewlist = crewlist
        self.prefix = prefix
        self.id = id


    @staticmethod
    def genshipfrommodel(model):
        size = model.size
        hulltype = model.hulltype
        category = model.category
        hardpoints = model.hardpoints
        signature = model.signature
        crew = model.crew
        hullen = model.hullen
        hullval = model.hullval
        armorval = model.armorval
        modules = model.modules
        manufacturer = model.manufacturer
        shipmodel = model.shipmodel
        eqmodules = model.eqmodules
        availmodules = model.availmodules
        squads = model.squads
        thrusters = model.thrusters
        eqweapons = model.eqweapons
        rooms = model.rooms
        ftl = model.ftl
        factionid = Ship.genfaction().id
        name = Ship.genname(factionid)
        crewsize = Ship.getcrewsize(crew)
        cat = Ship.genshipcat(category)
        crewlist = Ship.gencrewmembers(crewsize, eqmodules, factionid)
        prefix = FactionList.getprefix(factionid)
        id = 0
        return Ship(size, hulltype, category, hardpoints, signature, crew, hullen, hullval, armorval, modules, manufacturer, shipmodel, 
        eqmodules, availmodules, squads, thrusters, eqweapons, rooms, ftl, factionid, name, crewsize, cat, crewlist, prefix, id)
        
        
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise ValueError(f"Ship id invalid.")
        self._id = id


    def genfaction():
            return random.choice(FactionList.factionshiplist)
        
    @staticmethod
    def genname(faction):
        name = ""
        factionname = Faction.idtoname(faction)
        if factionname in ("United Americas", "Three World Empire", "Union of Progressive Peoples"):
            flip = coin()
            if flip == 1:
                match factionname:
                    case "United Americas":
                        search = "usname"
                    case "Three World Empire":
                        search = "3wename"
                    case "Union of Progressive Peoples":
                        search = "uppname"
                return "The " + random.choice(namelists.returnNameList(search))
        flip = coin()
        if flip == 1:
            name = "The "
        flip = coin()
        if flip == 1:
            name += random.choice(namelists.returnNameList(namelists.returnPrefix())) + " "
        name += random.choice(namelists.returnNameList(namelists.returnNeutCategory()))
        return name

    @staticmethod
    def getcrewsize(crew):
        min = crew[0]
        max = crew[1]
        return random.randint(min, max)
    
    @staticmethod
    def genshipcat(category):
        r = random.randint(0, 100)
        if category == "warship" or r < 70:
            return "None"
        return genmeow.Cat.genrandcat()

    @staticmethod
    def gencrewmembers(crewsize, eqmodules, faction):
        crewlist = {}
        i = 0
        if i < crewsize:
            crewlist["pilot"] = Npc.genrandomnpc(factionid=faction, job="Pilot", pstat=1)
            i += 1
        if i < crewsize:
            crewlist["captain"] = Npc.genrandomnpc(factionid=faction, job="Captain", pstat=3)
            i += 1
        if i < crewsize:
            crewlist["engineer"] = Npc.genrandomnpc(factionid=faction, job="Engineer", pstat=0)
            i += 1
        if i < crewsize:
            crewlist["technician"] = Npc.genrandomnpc(factionid=faction, job="Technician", pstat=0)
            i += 1
        if i < crewsize:
            for module in eqmodules.modulelist:
                if module.type == "Medlab":
                    crewlist["medic"] = Npc.genrandomnpc(factionid=faction, job="Medic", pstat=3)
                    i += 1
                    break
        if i < crewsize:
            for module in eqmodules.modulelist:
                if module.type == "Science Lab":
                    crewlist["scientist"] = Npc.genrandomnpc(factionid=faction, job="Scientist", pstat=2)
                    i += 1
                    break
        return crewlist
    
    def __str__(self):
        description = f"This is a {self.manufacturer} {self.shipmodel}, a {self.category} {self.hulltype} ship named {self.name}.\n"
        description += f"Crew size: {self.crewsize} \nLength: {self.hullen} \nSignature: {self.signature} \nHull: {self.hullval} \nArmor: {self.armorval} \nFTL: {self.ftl}\n"
        description += "Hardpoints: "
        return description
        #count = 1
        ''' for hardpoint in self.hardpoints:
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
        description += "\n Crew Members: \n"
        for role, crew in self.crewlist.items():
            description += f"{role} {crew.forename} {crew.surname}\n"
        description += "\n"'''
        

'''initializehulls()
initializemodels()
for model in HullModels.models:
    print(Ship(model))'''