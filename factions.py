from namelists import NationNameTable, NationNameTable
from savedobjects import ShipList, NpcList
from helpers import convertbool
import csv

def initializefactionlist():

    with open(r'static\FactionList_new.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            namelist = list((row['NameList'].split(",")))
            parents = list((row['Parents'].split(",")))
            parentlist = []
            if parents != [""]:
                for parent in parents:
                    parentlist.append(int(parent))
            FactionList.addfaction(row['FactionName'], row['EntityType'], row['Abbr'], row['Notes'], row['ShipPre'], row['OrdLvl'], convertbool(row['Science']), convertbool(row['Colony']), convertbool(row['MGMT']), convertbool(row['Ships']), row['Scope'], namelist, parentlist)

class CountryList:
    countrylist = {}

    def __init__(self):
        fieldnames = ["Country", "Abbr", "Code"]
        with open(r'static\iso_codes.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames)
            for row in reader:
                CountryList.countrylist[row['Abbr']] = []

class FactionList:
    factionlist = []
    factionshiplist = []


    @staticmethod
    def checkfactionid(id):
        found = False
        for faction in FactionList.factionlist:
            if id == faction.id:
                found = True
                break
        return found

    @staticmethod
    def checkfactionname(name):
        found = False
        for faction in FactionList.factionlist:
            if name == faction.name:
                found = True
                break
        return found

    @staticmethod
    def getclassfromid(id):
        if id == "-" or id == "None":
            return False
        for faction in FactionList.factionlist:
            if int(id) == faction.id:
                return faction
        return False

    @staticmethod
    def getprefix(id):
        faction = FactionList.getclassfromid(id)
        return faction.shippre
    
    @staticmethod
    def addfaction(name, type, abbr, notes, shippre, ordlvl, science, colony, mgmt, ships, scope, nameset, parents):
        parentlist = []
        parentsnew = []
        try:
            for parent in parents:
                parentsnew.append(int(parent))
        except:
            parentsnew = []
        for faction in FactionList.factionlist:
            if name == faction.name:
                return False
        if parentsnew != []:
            for parent in parentsnew:
                parentlist.append(FactionList.getclassfromid(parent))
        if nameset == ['']:
            nameset = []
        if nameset == [] and parentlist != []:
            for parent in parentlist:
                for nation in parent.nameset:
                    nameset.append(nation)
            nameset = list(set(nameset))
        faction = Faction(name, type, abbr, notes, shippre, ordlvl, science, colony, mgmt, ships, scope, nameset, parentlist)
        FactionList.factionlist.append(faction)
        if faction.ships:
            FactionList.factionshiplist.append(faction)
            
        return True

    @staticmethod
    def removefaction(id):
        found = False
        if id == 0:
            raise ValueError(f"Unable to delete Unaligned faction.")
        for faction in FactionList.factionlist:
            for npc in NpcList.npclist: #Remove all saved npc references to faction and make them unaligned.
                if npc.factionid == id:
                    npc.factionid = 0
            FactionList.updateshipfaction(id)
            for parent in faction.parents:
                if parent.id == id:
                    faction.parents.remove(parent)
        for faction in FactionList.factionlist: #Have to loop twice because if a faction is removed before the loop finished can no longer validate remaining data.
            if faction.id == id:
                FactionList.factionlist.remove(faction)
                found = True
        if faction.ships == True:
            FactionList.shiplist.remove(faction)
        return found

    @staticmethod
    def editfaction(id, name, type, abbr, notes, shippre, ordlvl, science, colony, mgmt, ships, scope, nameset, parentlist):
        faction = FactionList.getclassfromid(int(id))
        if not faction:
            raise ValueError(f"Unable to find a faction for {name}.")
        if faction.name != name: #name has a duplicate check to ensure that we can't have multiple factions with the same name, so skip blind assignment.
            faction.name = name
        faction.type = type
        faction.abbr = abbr
        faction.parents = parentlist
        faction.nameset = nameset
        faction.notes = notes
        if faction.shippre != shippre:
            for ship in ShipList.shiplist:
                if ship.factionid == id:
                    ship.prefix == shippre
        faction.ordlvl = ordlvl
        faction.science = science
        faction.colony = colony
        faction.mgmt = mgmt
        if faction.ships != ships and ships != True: #Only if we are changing the value for ships.
            if ships == True:
                FactionList.shiplist.append(faction) #Going from false to true means faction can generate new ships
            else:
                FactionList.updateshipfaction(id) #Going from true to false requires an update to existing ships
        faction.ships = ships
        faction.scope = scope
        return True

    @staticmethod
    def updateshipfaction(id):
        for ship in ShipList.shiplist:
            if ship.factionid == id:
                ship.factionid = 0
                for crew in ship.crewlist.values():
                    crew.factionid == 0
                ship.prefix = "SS"



class Faction:
    typelist = ['gov', 'corp', 'settlement', 'religion', 'outlaw', 'guild', 'military', 'alliance', 'agency', 'ngo', 'cooperative', 'none']
    masterid = 0
    ordenancelevel = ['none', 'security', 'black ops', 'military']
    scopelevel = ['local', 'system', 'sector', 'pervasive', 'infiltrating', 'attached']

    def __init__(self, name, type, abbr, notes, shippre, ordlvl, science, colony, mgmt, ships, scope, nameset, parents):
        self.name = name
        self.id = Faction.genfactionid()
        self.type = type
        self.nameset = nameset
        self.parents = parents
        self.abbr = abbr
        self.notes = notes
        self.shippre = shippre
        self.ordlvl = ordlvl
        self.science = science
        self.colony = colony
        self.mgmt = mgmt
        self.ships = ships
        self.scope = scope


    @classmethod
    def idtoname(cls, id):
        if id=="":
            return False
        for faction in FactionList.factionlist:
            if id == faction.id:
                return faction.name
        return False
            
    @classmethod
    def nametoid(cls, name):
        if name == "":
            return False
        for faction in FactionList.factionlist:
            if name == faction.name:
                return faction.id
        return False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name == "" or not isinstance(name, str):
            raise ValueError(f"Invalid faction name {name}.")
        if FactionList.checkfactionname(name):
            raise ValueError(f"Faction name {name} must be unique.")
        self._name = name
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if not isinstance(id, int) or id < 0:
            raise ValueError(f"Invalid faction id {id}.")
        if FactionList.checkfactionid(id):
            raise ValueError(f"Faction id {id} must be unique.")
        self._id = id

    @staticmethod
    def genfactionid():
        id = Faction.masterid
        Faction.masterid += 1
        return id

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        if type not in Faction.typelist:
            raise ValueError(f"Invalid faction type {type}.")
        self._type = type

    @property
    def nameset(self):
        return self._nameset

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        if len(notes) > 999:
            raise ValueError(f"Faction notes are too long.")
        self._notes = notes


# For now it is only actually valuable to save the namelists that are populated. 
# Will change going forward when more namelists are available.
    @nameset.setter
    def nameset(self, nameset):
        names2 = []
        if nameset == ['']:
            nameset = []
        if nameset != []:
            for nation in nameset:
                if nation not in CountryList.countrylist.keys():
                    raise ValueError(f"Invalid name list {nation} for faction.")
                Faction.addfactioncountry(nation, self.id)
                if nation in NationNameTable.nationlist:
                    names2.append(nation)
        self._nameset = names2
        
    @classmethod
    def addfactioncountry(cls, nation, id):
        CountryList.countrylist[nation].append(id)

    def addtonamelist(self, nation):
        if nation in NationNameTable.nationlist:
            self.nameset.append(nation)
            return True
        return False
    
    def removefromnamelist(self, nation):
        if nation in NationNameTable.nationlist:
            self.nameset.remove(nation)
            return True
        return False
    
    @property
    def parents(self):
        return self._parents

    @parents.setter
    def parents(self, parents):
        if parents != ['']:
            ids = []
            for parent in parents:
                if parent.id == self.id:
                    raise ValueError(f"Unable to assign self as faction parent.")
                if parent.id in ids:
                    raise ValueError(f"Unable to assign same parent multiple times.")
                ids.append(parent.id)
                for grandparent in parent.parents:
                    if grandparent.id == self.id:
                        raise ValueError(f"Circular faction parent loop detected between {self.name} and {grandparent.name}.")
        self._parents = parents

    @property
    def abbr(self):
        return self._abbr

    @abbr.setter
    def abbr(self, abbr):
        if abbr != "":
            if len(abbr) > 4:
                raise ValueError(f"Faction abbreviation length too long {abbr}.")
        self._abbr = abbr

    @property
    def shippre(self):
        return self._shippre

    @shippre.setter
    def shippre(self, shippre):
        if not isinstance(shippre, str) or len(shippre) > 5:
            raise ValueError(f"Ship prefix {shippre} must be a string less than 5 characters.")
        self._shippre = shippre

    def __str__(self):
        return f"Name: {self.name}\nId: {self.id}\nType: {self.type}\nName Lists: {self.nameset}"

    @property
    def ordlvl(self):
        return self._ordlvl

    @ordlvl.setter
    def ordlvl(self, ordlvl):
        if ordlvl not in Faction.ordenancelevel:
            raise ValueError(f"Invalid faction ordenance level {ordlvl}.")
        self._ordlvl = ordlvl

    @property
    def science(self):
        return self._science

    @science.setter
    def science(self, science):
        science = convertbool(science)
        if not isinstance(science, bool):
            raise ValueError("Invalid science level {science}, bool value expected.")
        self._science = science
    
    @property
    def colony(self):
        return self._colony

    @colony.setter
    def colony(self, colony):
        colony = convertbool(colony)
        if not isinstance(colony, bool):
            raise ValueError("Invalid colony level, bool value expected.")
        self._colony = colony

    @property
    def ships(self):
        return self._ships

    @ships.setter
    def ships(self, ships):
        ships = convertbool(ships)
        if not isinstance(ships, bool):
            raise ValueError("Invalid ship level, bool value expected.")
        self._ships = ships

    @property
    def mgmt(self):
        return self._mgmt

    @mgmt.setter
    def mgmt(self, mgmt):
        mgmt = convertbool(mgmt)
        if not isinstance(mgmt, bool):
            raise ValueError("Invalid mgmt level, bool value expected.")
        self._mgmt = mgmt

    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self, scope):
        if scope not in Faction.scopelevel:
            raise ValueError(f"Invalid faction scope level {scope}.")
        self._scope = scope

def initializeall():
    CountryList()
    FactionList.addfaction("Unaligned", "none", abbr="", notes="", shippre="SS", ordlvl="security", science=True, colony=False, mgmt=False, ships=True, scope="pervasive", nameset=[], parents=[])
    initializefactionlist()