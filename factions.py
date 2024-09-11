from namelists import NationNameTable, NationNameTable
from savedobjects import NpcList, ShipList
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
                    for faction in FactionList.factionlist:
                        if faction.id == int(parent):
                            parentlist.append(faction)
            FactionList.addfaction(row['FactionName'], row['EntityType'], namelist, parentlist, row['Abbr'])

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
    def addfaction(name, type, nameset, parents, abbr):
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
                    if int(faction.id) == parent:
                        parentlist.append(faction)
        FactionList.factionlist.append(Faction(name, type, nameset, parentlist, abbr))
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
            for ship in ShipList.shiplist:
                if ship.factionid == id:
                    ship.factionid = 0
                    for crew in ship.crewlist:
                        crew.factionid = id
            for parent in faction.parents:
                if parent.id == id:
                    faction.parents.remove(parent)
        for faction in FactionList.factionlist: #Have to loop twice because if a faction is removed before the loop finished can no longer validate remaining data.
            if faction.id == id:
                FactionList.factionlist.remove(faction)
                found = True
        return found

class Faction:
    typelist = ['gov', 'corp', 'settlement', 'religion', 'outlaw', 'guild', 'military', 'alliance', 'agency', 'ngo', 'cooperative', 'none']
    masterid = 0
    ordenancelevel = ['none', 'security', 'black ops', 'military']

    def __init__(self, name, type, nameset=[], parents=[], abbr=""):
        self.name = name
        self.id = Faction.genfactionid()
        self.type = type
        self.nameset = nameset
        self.parents = parents
        self.abbr = abbr
        self.notes = ""


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
        if nameset != ['']:
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
            for parent in parents:
                if parent.id == self.id:
                    raise ValueError(f"Unable to assign same faction parent {parent.name} multiple times.")
        self._parents = parents

    @property
    def abbr(self):
        return self._abbr

    @abbr.setter
    def abbr(self, abbr):
        if len(abbr) > 4:
            raise ValueError(f"Faction abbreviation length too long {abbr}.")
        self._abbr = abbr

    def __str__(self):
        return f"Name: {self.name}\nId: {self.id}\nType: {self.type}\nName Lists: {self.nameset}"

def initializeall():
    CountryList()
    initializefactionlist()