import csv, random
# Place to save everything related to primary stats, such as jobs, talents, skills, and items.

class JobList:
    statlist = ["strength", "agility", "wits", "empathy"]
    abbrstats = ["str", "agl", "wit", "emp"]

    # Holds class references
    jobclasslist = []
    # Easy to reference string lists
    strjoblist = []
    agljoblist = []
    witjoblist = []
    empjoblist = []
    # Compiled list of string lists for name validation
    tjoblist = []
    masterid = 1
    #def addjobtolist

    # Populates a stat specific job list to allow easy lookup based on name, but also jobclasslist to store actual reference to class.
    @staticmethod
    def addjobtolist(job):
        match job.stat:
            case "str":
                joblist = JobList.strjoblist
            case "agl":
                joblist = JobList.agljoblist
            case "wit":
                joblist = JobList.witjoblist
            case "emp":
                joblist = JobList.empjoblist
        if job.jobname in joblist:
            raise ValueError(f"Invalid job, job already present in list.")
        joblist.append(job.jobname)
        JobList.tjoblist.append(job.jobname)
        if job.id <= JobList.masterid:
            JobList.masterid += 1
        JobList.jobclasslist.append(job)
        

class Job:
    def __init__(self, job, stat, jobtypes, id=""):
        self.jobname = job
        if id == 0 or id == "":
            id = JobList.masterid
        self.id = id
        self.jobtypes = Job.buildtypelist(jobtypes)
        self.stat = stat
        self.itemdict = Job.checkitemdicts(self.jobtypes)


    @property
    def jobname(self):
        return self._jobname
    
    @jobname.setter
    def jobname(self, jobname):
        if not isinstance(jobname, str):
            raise ValueError(f"Invalid job name {jobname}.")
        self._jobname = jobname

    @property
    def stat(self):
        return self._stat

    @stat.setter
    def stat(self, stat):
        if stat not in JobList.abbrstats:
            raise ValueError(f"Invalid job stat of {stat}.")
        self._stat = stat

    @property
    def jobtypes(self):
        return self._jobtypes
    
    @jobtypes.setter
    def jobtypes(self, jobtypes):
        if not isinstance(jobtypes, list):
            raise ValueError(f"Jobtype list for job must be a list.")
        self._jobtypes = jobtypes

    # Given 
    @staticmethod
    def buildtypelist(jobtypes):
        typelist = []
        for ttype in jobtypes:
            for jtype in JobTypeList.jobtypelist:
                if ttype == jtype.type:
                    typelist.append(jtype)
                    break
        return typelist

    # Checks if more than one job type exists for job. If so, merges the item list dictionaries for each so that the character can spawn the correct number of items. Skips this check if only one job type present.
    @staticmethod
    def checkitemdicts(jobtypes):
        if len(jobtypes) > 1:
            itemdictlist = []
            for jobtype in jobtypes:
                itemdictlist.append(jobtype.itemdict)
            itemdict = JobType.mergeitemdict(itemdictlist)
        else:
            itemdict = jobtypes[0].itemdict
        return itemdict

    @property
    def itemdict(self):
        return self._itemdict

    @itemdict.setter
    def itemdict(self, itemdict):
        for type in Item.typelist:
            if type not in itemdict.keys():
                raise ValueError(f"Missing item types from {self.jobname} item dictionary.")
        for value in itemdict.values():
            if not isinstance(value, list):
                raise ValueError(f"Item dictionary for {self.jobname} is not list based.")
        if itemdict["substance"] == 0:
            raise ValueError(f"Likely issue with {self.jobname} item dictionary.")
        self._itemdict = itemdict
    

# Job types are used to define what type of items should be available to npcs of a specific job.
# TODO rename to Job Tags so type doesn't get confusing.
class JobType:
    def __init__(self, jobtype, itemdict, id=""):
        self.type = jobtype
        self.itemdict = itemdict
        if id == "" or id == 0:
            id = JobTypeList.masterid
        self.id = id
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type):
        if not isinstance(type, str):
            raise ValueError(f"Invalid job type {type}.")
        self._type = type

    @property
    def itemdict(self):
        return self._itemdict

    @itemdict.setter
    def itemdict(self, itemdict):
        if not isinstance(itemdict,dict):
            raise ValueError(f"Invalid itemdict for {self.type}.")
        if not ('rifle' or 'sidearm' or 'heavyweapon' or 'armor' or 'melee' or 'explosive' or 'suit' or 'technical' or 'accessory' or 'tool' or 
        'medical' or 'food' or 'substance') in itemdict:
            raise ValueError(f"Itemdict missing item key.")
        if itemdict["substance"] == 0:
            raise ValueError(f"Likely issue with {self.type} item dictionary.")
        self._itemdict = itemdict


    # Creates a new dictionary and updates the min and max value for each starting type based on all item count dictionaries passed in.
    @staticmethod
    def mergeitemdict(itemdictlist):
        newdict = {
            'rifle': [0, 0],
            'sidearm': [0,0],
            'heavy weapon': [0, 0],
            'armor': [0, 0],
            'melee': [0, 0],
            'explosive': [0, 0],
            'suit': [0, 0],
            'technical': [0, 0],
            'accessory': [0, 0],
            'tool': [0, 0],
            'medical': [0, 0],
            'food': [0, 0],
            'substance': [0, 0]
        }
        for itemdict in itemdictlist:
            for key in itemdict:
                if itemdict[key][0] > newdict[key][0]:
                    newdict[key][0] = itemdict[key][0]
                if itemdict[key][1] > newdict[key][1]:
                    newdict[key][1] = itemdict[key][1]
        return newdict

# Container for job types
class JobTypeList:
    jobtypelist = []
    masterid = 1

    # TODO Add logic to ensure id is valid
    @staticmethod
    def addjobtype(jobtype):
        JobTypeList.jobtypelist.append(jobtype)
        if jobtype.id > JobTypeList.masterid:
            JobTypeList.masterid = jobtype.id + 1

class ItemList:
    itemlist = []
    masterid = 1
    riflelist = []
    sidearmlist = []
    hweaponlist = []
    armorlist = []
    meleelist = []
    explosivelist = []
    suitlist = []
    techlist = []
    acclist = []
    toollist = []
    medlist = []
    foodlist = []
    sublist = []
    
    @staticmethod
    def additem(item):
        ItemList.itemlist.append(item)
        if item.id >= ItemList.masterid:
            ItemList.masterid = item.id + 1
            # May be a more efficient way to do this, but useful for getitems()
            # Item may have multiple types so second list is needed.
            typelist = []
            for type in item.types:
                typelist.append(ItemList.getitemtypelist(type))
            for list in typelist:
                list.append(item)
    
    # For each key in dict, choose a number of random items for each key.
    # TODO Add handling to prevent duplicates of some item types. Ok to have more than one ration, but not ok to have 2 smart guns.
    @staticmethod
    def getitems(itemdict):
        itemlist = []
        for key in itemdict.keys():
            for x in range(random.randint(itemdict[key][0], itemdict[key][1])):
                itemlist.append(random.choice(ItemList.getitemtypelist(key)))
        return itemlist
    
    @staticmethod
    def getitemtypelist(itemtype):
        typelist = ""
        match itemtype:
            case "rifle": 
                typelist = ItemList.riflelist
            case "sidearm":
                typelist = ItemList.sidearmlist
            case "heavy weapon":
                typelist = ItemList.hweaponlist
            case "armor":
                typelist = ItemList.armorlist
            case "melee":
                typelist = ItemList.meleelist
            case "explosive":
                typelist = ItemList.explosivelist
            case "suit":
                typelist = ItemList.suitlist
            case "technical":
                typelist = ItemList.techlist
            case "accessory":
                typelist = ItemList.acclist
            case "tool":
                typelist = ItemList.toollist
            case "medical":
                typelist = ItemList.medlist
            case "food":
                typelist = ItemList.foodlist
            case "substance":
                typelist = ItemList.sublist
        return typelist

    @staticmethod
    def getitemids(itemlist):
        itemids = []
        for item in itemlist:
            itemids.append(item.id)
        return itemids

    @staticmethod
    def builditemlistfromids(itemids):
        titemlist = []
        for item in itemids:
            for citem in ItemList.itemlist:
                if citem.id == item:
                    titemlist.append(citem)
                    break
        return titemlist


class Item:
    typelist = ["rifle", "sidearm", "heavy weapon", "armor", "melee", "explosive", "suit", "technical", "accessory", "tool", 
    "medical", "food", "substance"]
    
    def __init__(self, name, types, value, id="", manufacturer=""):
        self.name = name
        self.types = types
        self.value = value
        self.manufacturer = manufacturer
        if id == "" or id == 0:
            id = ItemList.masterid
        self.id = id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if name == "" or not isinstance(name, str):
            raise ValueError(f"Invalid item name {name}.")
        self._name = name
    
    @property
    def types(self):
        return self._types

    @types.setter
    def types(self, types):
        for type in types:
            if type not in Item.typelist:
                raise ValueError(f"Invalid item type {type}.")
        self._types = types
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Invalid item value {value}.")
        self._value = value
    
    @property
    def manufacturer(self):
        return self._manufacturer
    
    @manufacturer.setter
    def manufacturer(self, manufacturer):
        if manufacturer != "" and not isinstance(manufacturer, str):
            raise ValueError(f"Invalid item manufacturer {manufacturer}.")
        self._manufacturer = manufacturer


def initializeitemlist():
    with open(r'static\jobsitems\items.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            typelist = list((row['Type'].split(",")))
            ItemList.additem(Item(row['Name'], typelist, int(row['Value']), int(row['Id'])))

def initializejobtypes():
    with open(r'static\jobsitems\JobTypes.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            itemdict = {
                "rifle": list(row['rifle'].split(",")),
                "sidearm": list((row['sidearm'].split(","))),
                "heavy weapon": list((row['heavy weapon'].split(","))),
                "armor": list((row['armor'].split(","))),
                "melee": list((row['melee'].split(","))),
                "explosive": list((row['explosive'].split(","))),
                "suit": list((row['suit'].split(","))),
                "technical": list((row['technical'].split(","))),
                "accessory": list((row['accessory'].split(","))),
                "tool": list((row['tool'].split(","))),
                "medical": list((row['medical'].split(","))),
                "food": list((row['food'].split(","))),
                "substance": list((row['substance'].split(",")))
                }
            for value in itemdict.values():
                for x in range(len(value)):
                    value[x] = int(value[x])
            JobTypeList.addjobtype(JobType(row['Job Type'], itemdict, int(row['id'])))
            
def initializejoblist():
    with open(r'static\jobsitems\Jobs.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            typelist = list((row['Type'].split(",")))
            JobList.addjobtolist(Job(row['Job'], row['Stat'], typelist, int(row['id'])))

# Called from app.py
def initializestats():
    initializeitemlist()
    initializejobtypes()
    initializejoblist()




#initializestats()