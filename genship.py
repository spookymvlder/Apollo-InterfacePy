import random
from hulls import HullModel, HullModels, initializehulls, initializemodels
from helpers import coin
import namelists, genmeow, gennpc
from factions import FactionList

class Ships:
    shiplist = []

class Ship:
    def __init__(self, model):
        self.size = model.size
        self.hulltype = model.hulltype
        self.category = model.category
        self.hardpoints = model.hardpoints
        self.signature = model.signature
        self.crew = model.crew
        self.hullen = model.hullen
        self.hullval = model.hullval
        self.armorval = model.armorval
        self.modules = model.modules
        self.manufacturer = model.manufacturer
        self.shipmodel = model.shipmodel
        self.eqmodules = model.eqmodules
        self.availmodules = model.availmodules
        self.squads = model.squads
        self.thrusters = model.thrusters
        self.eqweapons = model.eqweapons
        self.rooms = model.rooms
        self.ftl = model.ftl
        self.faction = Ship.genfaction()
        self.name = Ship.genname(self.faction)
        self.crewsize = Ship.getcrewsize(self, self.crew)
        self.cat = Ship.genshipcat(self, self.category)
        self.crewlist = Ship.gencrewmembers(self, self.crewsize, self.eqmodules, self.faction.id)


    def genfaction():
            return random.choice(FactionList.factionlist)
        
    @staticmethod
    def genname(faction):
        name = ""
        if faction.name in ("United Americas", "Three World Empire", "Union of Progressive Peoples"):
            flip = coin()
            if flip == 1:
                match faction.name:
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

    def getcrewsize(self, crew):
        min = crew[0]
        max = crew[1]
        return random.randint(min, max)
    
    def genshipcat(self, category):
        r = random.randint(0, 100)
        if category == "warship" or r < 70:
            return "None"
        return genmeow.Cat()

    def gencrewmembers(self, crewsize, eqmodules, faction):
        crewlist = {}
        i = 0
        if i < crewsize:
            crewlist["pilot"] = gennpc.Npc(forename="", surname="", type="", sex="", factionid=faction, job="pilot", stats="", pstat=1, nation="")
            i += 1
        if i < crewsize:
            crewlist["captain"] = gennpc.Npc(forename="", surname="", type="", sex="", factionid=faction, job="captain", stats="", pstat=3, nation="")
            i += 1
        if i < crewsize:
            crewlist["engineer"] = gennpc.Npc(forename="", surname="", type="", sex="", factionid=faction, job="engineer", stats="", pstat=0, nation="")
            i += 1
        if i < crewsize:
            crewlist["technician"] = gennpc.Npc(forename="", surname="", type="", sex="", factionid=faction, job="technician", stats="", pstat=0, nation="")
            i += 1
        if i < crewsize:
            for module in eqmodules.modulelist:
                if module.type == "Medlab":
                    crewlist["medic"] = gennpc.Npc(forename="", surname="", type="", sex="", factionid=faction, job="medic", stats="", pstat=3, nation="")
                    i += 1
                    break
        if i < crewsize:
            for module in eqmodules.modulelist:
                if module.type == "Science Lab":
                    crewlist["scientist"] = gennpc.Npc(forename="", surname="", type="", sex="", factionid=faction, job="scientist", stats="", pstat=2, nation="")
                    i += 1
                    break
        return crewlist
    
    def __str__(self):
        description = f"This is a {self.manufacturer} {self.shipmodel}, a {self.category} {self.hulltype} ship named {self.name}.\n"
        description += f"Crew size: {self.crewsize} \nLength: {self.hullen} \nSignature: {self.signature} \nHull: {self.hullval} \nArmor: {self.armorval} \nFTL: {self.ftl}\n"
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
        description += "\n Crew Members: \n"
        for role, crew in self.crewlist.items():
            description += f"{role} {crew.forename} {crew.surname}\n"
        description += "\n"
        return description

'''initializehulls()
initializemodels()
for model in HullModels.models:
    print(Ship(model))'''