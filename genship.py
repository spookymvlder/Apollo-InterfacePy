import random
from helpers import coin
from gennpc import Npc
import namelists, genmeow
from factions import FactionList, Faction
from savedobjects import ShipList, CatList, NpcList
from shipparts import ModuleList, ShipRooms

# Formed by hulls.py components. Thought was to have a hull template used to create multiple models. Then those models could be used to generate ships.
# Ship building is a three step process, allows for future functionality to let users create and save ship types that are similar, but different.
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
        factionid = Ship.genfaction(category).id
        name = Ship.genname(factionid)
        crewsize = Ship.getcrewsize(crew)
        cat = Ship.genshipcat(category)
        crewlist = Ship.gencrewmembers(crewsize, eqmodules, factionid)
        prefix = FactionList.getprefix(factionid)
        id = 0
        return Ship(size, hulltype, category, hardpoints, signature, crew, hullen, hullval, armorval, modules, manufacturer, shipmodel, 
        eqmodules, availmodules, squads, thrusters, eqweapons, rooms, ftl, factionid, name, crewsize, cat, crewlist, prefix, id)
        
    @staticmethod
    def unpackshipsfromload(ships):
        ShipList.shiplist.clear()
        for ship in ships:
            eqmodules = ModuleList()
            for module in ship["eqmodules"]:
                ModuleList.addmodule(eqmodules, module["type"], module["lvl"], module["quantity"])
            cat = ship["cat"]
            if cat != "None":
                cat = CatList.findcatfromid(cat)
            rooms = ShipRooms()
            for room in ship["rooms"]:
                ShipRooms.addroom(rooms, room["type"], room["lvl"], room["quantity"], room["size"])
            crewlist = {}
            for job, crew in ship["crewdict"].items():
                crewlist[job] = NpcList.findnpcfromid(crew)
            ShipList.shiplist.append(Ship(ship["size"], ship["hulltype"], ship["category"], ship["hardpoints"], ship["signature"], ship["crew"], ship["hullen"], 
            ship["hullval"], ship["armorval"], ship["modules"], ship["manufacturer"], ship["shipmodel"], eqmodules, ship["availmodules"], ship["squads"], 
            ship["thrusters"], ship["eqweapons"], rooms, ship["ftl"], ship["factionid"], ship["name"], ship["crewsize"], cat, crewlist, ship["prefix"], ship["id"]))
            if ShipList.masterid <= ship["id"]:
                ShipList.masterid = ship["id"] + 1

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise ValueError(f"Ship id invalid.")
        self._id = id


    def genfaction(category):
        if category == "colony":
            found = False
            while found == False:
                faction = random.choice(FactionList.factionshiplist)
                if faction.colony == True:
                    found = True
        else:
            faction = random.choice(FactionList.factionshiplist)
        return faction
        
    # An unfortunate hardcoding based on factions.
    @staticmethod
    def genname(faction):
        name = ""
        factionname = Faction.idtoname(faction)
        if factionname in ("United Americas", "Three World Empire", "Union of Progressive Peoples", "United Americas Military", "United States Military", "UPP Military", "3WE Military"):
            flip = coin()
            if flip == 1:
                match factionname:
                    case "United Americas" | "United Americas Military" | "United States Military":
                        search = "usname"
                    case "Three World Empire" | "3WE Military":
                        search = "3wename"
                    case "Union of Progressive Peoples" | "UPP Military":
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
            crewlist["pilot"] = Npc.genrandomnpc(factionid=faction, job="Pilot", pstat="Agility")
            i += 1
        if i < crewsize:
            crewlist["captain"] = Npc.genrandomnpc(factionid=faction, job="Captain", pstat="Empathy")
            i += 1
        if i < crewsize:
            crewlist["engineer"] = Npc.genrandomnpc(factionid=faction, job="Engineer", pstat="Strength")
            i += 1
        if i < crewsize:
            crewlist["technician"] = Npc.genrandomnpc(factionid=faction, job="Technician", pstat="Strength")
            i += 1
        if i < crewsize:
            for module in eqmodules.modulelist:
                if module.type == "Medlab":
                    crewlist["medic"] = Npc.genrandomnpc(factionid=faction, job="Medic", pstat="Empathy")
                    i += 1
                    break
        if i < crewsize:
            for module in eqmodules.modulelist:
                if module.type == "Science Lab":
                    crewlist["scientist"] = Npc.genrandomnpc(factionid=faction, job="Scientist", pstat="Wits")
                    i += 1
                    break
        return crewlist
    
    def __str__(self):
        description = f"This is a {self.manufacturer} {self.shipmodel}, a {self.category} {self.hulltype} ship named the {self.prefix} {self.name}. \n"
        description += f"Length: {self.hullen}m \nSignature: {self.signature} \nHull: {self.hullval} \nArmor: {self.armorval} \nFTL: {self.ftl} \nThrusters: {self.thrusters} \n"
        description += f"Crew Capacity: {self.crew[0]}-{self.crew[1]} \nCrew Size: {self.crewsize} \nFaction: {Faction.idtoname(self.factionid)} \n"
        description += "Hardpoints: \n" 
        count = 1
        for hardpoint in self.hardpoints:
            description += f"{count}: {hardpoint} "
            count += 1
        description += "\nEmpty Modules: \n"
        count = 1
        for module in self.availmodules:
            description += f"{count}: {module} "
            count += 1
        description += "\nOriginal Modules: \n"
        count = 1
        for module in self.modules:
            description += f"{count}: {module} "
            count += 1
        description += "\nEquiped Modules: \n"
        for module in self.eqmodules.modulelist:
            description += f"Module: {module.name} Quantity: {module.quantity} Capacity: {module.capacity} \n"
        description += f"\nWeapons: \n"
        count = 1
        for weapon in self.eqweapons:
            description += f"{weapon}, "
        description += f"\nRooms: \n"
        count = 1
        for room in self.rooms.shiproomlist:
            description += f"Room: {room.type} Size: {room.size} Quantity: {room.quantity} \n"
        description += "\n Crew Members: \n"
        for role, crew in self.crewlist.items():
            description += f"{role.title()} - {crew.forename} {crew.surname} \n"
        if self.cat != "None":
            description += f"Cat: {self.cat.name}, a very good kitty "
        description += "\n"
        return description