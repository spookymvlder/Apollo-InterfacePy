from namelists import NationNameTable, NationNameTable
from savedobjects import ShipList, FactionList, CountryList
from helpers import convertbool
import csv


# Factions, initially loaded via csv. Loading code underneath this class and called by app.py
class Faction:
    # Types don't currently drive anything.
    typelist = ['gov', 'corp', 'settlement', 'religion', 'outlaw', 'guild', 'military', 'alliance', 'agency', 'ngo', 'cooperative', 'none']
    # Currently scope level and ordenance level don't do anything.
    # TODO restrict types of ships and npc careers to appropriate ordenance/scope levels.
    ordenancelevel = ['none', 'security', 'black ops', 'military']
    scopelevel = ['local', 'system', 'sector', 'pervasive', 'infiltrating', 'attached']

    def __init__(self, name, type, abbr, notes, shippre, ordlvl, science, colony, mgmt, ships, scope, nameset, parents, id):
        self.name = name
        self.id = id
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

    @staticmethod
    def addfaction(name, type, abbr, notes, shippre, ordlvl, science, colony, mgmt, ships, scope, nameset, parents, id=""):
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
        if id == "":
            id = FactionList.genfactionid()
        faction = Faction(name, type, abbr, notes, shippre, ordlvl, science, colony, mgmt, ships, scope, nameset, parentlist, id)
        FactionList.factionlist.append(faction)
        if faction.ships:
            FactionList.factionshiplist.append(faction)
        return faction

    def editfaction(self, name, type, abbr, notes, shippre, ordlvl, science, colony, mgmt, ships, scope, nameset, parentlist):
        if self.name != name: # Avoid duplicate check if possible
            self.name = name
        self.type = type
        self.abbr = abbr
        self.parents = parentlist
        self.nameset = nameset
        self.notes = notes
        if self.shippre != shippre:
            for ship in ShipList.shiplist:
                if ship.factionid == id:
                    ship.prefix == shippre
        self.ordlvl = ordlvl
        self.science = science
        self.colony = colony
        self.mgmt = mgmt
        if self.ships != ships and ships != True: #Only if we are changing the value for ships.
            if ships == True:
                FactionList.shiplist.append(self) #Going from false to true means faction can generate new ships
            else:
                FactionList.updateshipfaction(self.id) #Going from true to false requires an update to existing ships
        self.ships = ships
        self.scope = scope

    # Clears entire factionlist and then rebuilds. *SHOULD* be ok since every saved list will also be getting cleared.
    # Builds all factions and then builds parent relationships in case there are order issues. Faction.parents.setter should handle any potential messes.
    @staticmethod
    def unpackfactionsfromload(factions):
        FactionList.factionlist.clear()
        FactionList.factionshiplist.clear()
        for faction in factions:
            factionc = Faction.addfaction(faction["name"], faction["ftype"], faction["abbr"], faction["notes"], faction["shippre"], faction["ordlvl"], 
            faction["science"], faction["colony"], faction["mgmt"], faction["ships"], faction["scope"], faction["nameset"], [], faction["id"])
            FactionList.editparent(factionc, faction["parentlist"])
            if faction["id"] >= FactionList.masterid:
                FactionList.masterid = faction["id"] + 1

    # Used to convert HTML form responses to a faction list for any objects that can have factions.
    @staticmethod
    def factionstolist(faction1, faction2, faction3=""):
        factions = []
        faction1 = FactionList.getclassfromid(faction1)
        faction2 = FactionList.getclassfromid(faction2)
        faction3 = FactionList.getclassfromid(faction3)
        if faction1 != False:
            factions.append(faction1)
        if faction2 != False:
            factions.append(faction2)
        if faction3 != False:
            factions.append(faction3)
        return factions

    # Returns faction name, used by classes that store a faction id.
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

    

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        if type not in Faction.typelist:
            raise ValueError(f"Invalid faction type {type}.")
        self._type = type

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        if len(notes) > 999:
            raise ValueError(f"Faction notes are too long.")
        self._notes = notes

    @property
    def nameset(self):
        return self._nameset

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

    def __str__(self):
        return self.name

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
            Faction.addfaction(row['FactionName'], row['EntityType'], row['Abbr'], row['Notes'], row['ShipPre'], row['OrdLvl'], convertbool(row['Science']), convertbool(row['Colony']), convertbool(row['MGMT']), convertbool(row['Ships']), row['Scope'], namelist, parentlist, int(row['Id']))


def initializeall():
    CountryList()
    Faction.addfaction("Unaligned", "none", abbr="", notes="", shippre="SS", ordlvl="security", science=True, colony=False, mgmt=False, ships=True, scope="pervasive", nameset=[], parents=[])
    initializefactionlist()