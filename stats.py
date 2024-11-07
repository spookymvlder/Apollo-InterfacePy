import csv
# Place to save everything related to primary stats, such as jobs, talents, skills, and items.

class JobList:
    statlist = ["strength", "agility", "wits", "empathy"]
    strjob = ['Marine', 'Soldier', 'Mercenary', 'Security Guard', 'Bounty Hunter', 'Roughneck', 'Miner', 'Factory Worker', 'Machinist', 'Mechanic', 'Engineer', 'Farmer', 'Technician']
    agljob = ['Pilot', 'Military Pilot', 'Smuggler', 'Wildcatter', 'Prospector', 'Surveyor']
    witjob = ['Colonial Marshal', 'Security Chief', 'Marshal', 'Deputy', 'Sheriff', 'Bounty Hunter', 'Guard', 'Company Agent', 'Executive', 'Junior Executive', 'Manager', 'Division Head', 'Supervisor', 'Journalist', 'Researcher', 'Inventor', 'Scientist', 'Biologist', 'Chemist']
    empjob = ['Medic', 'Paramedic', 'Doctor', 'Combat Medic', 'Officer', 'Captain', 'Bridge Officer', 'Inspector', 'Facility Manager', 'Counselor', 'Quartermaster','Performer', 'Club Owner', 'Waiter', 'Bartender']
    joblist = strjob + agljob + witjob + empjob
    


    #empty lists for saving new jobs to, which can then be exported.
    newstrjoblist = []
    newagljoblist = []
    newwitjoblist = []
    newempjoblist = []


    strjoblist = strjob + newstrjoblist
    agljoblist = agljob + newagljoblist
    witjoblist = witjob + newwitjoblist
    empjoblist = empjob + newempjoblist
    #def addjobtolist

    @staticmethod
    def addjobtolist(job, stat):
        match stat:
            case "strength":
                joblist = JobList.strjoblist
                newlist = JobList.newstrjoblist
            case "agility":
                joblist = JobList.agljoblist
                newlist = JobList.newagljoblist
            case "wits":
                joblist = JobList.witjoblist
                newlist = JobList.newwitjoblist
            case "empathy":
                joblist = JobList.empjoblist
                newlist = JobList.newempjoblist
        if job in joblist:
            raise ValueError(f"Invalid job, job already present in list.")
        newlist.append(job)

class Job:
    def __init__(self, job, id, stat, jobtypes):
        self.job = job
        self.id = id
        self.jobtypes = Job.buildtypelist(jobtypes)
        self.stat = stat
        self.itemdict = Job.checkitemdicts(self.jobtypes)


    @staticmethod
    def buildtypelist(jobtypes):
        typelist = []
        for type in jobtypes:
            for jtype in JobTypeList.jobtypelist:
                if type == jtype.jobtype:
                    typelist.append(jtype)
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
    

# Job types are used to define what type of items should be available to npcs of a specific job.
class JobType:
    def __init__(self, jobtype, id, itemdict):
        self.jobtype = jobtype
        self.itemdict = itemdict
        self.id = id

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
    weaponlist = []
    itemlist = []
    masterid = 1
    
    @staticmethod
    def additem(item):
        ItemList.itemlist.append(item)
        if item.id >= ItemList.masterid:
            ItemList.masterid = item.id + 1
            # May not be worth it, but create a secondary list that is just weapons.
            for type in item.types:
                if type in ["rifle", "sidearm", "heavy weapon", "melee", "explosive"]:
                    ItemList.weaponlist.append(item)

class Item:
    typelist = ["rifle", "sidearm", "heavy weapon", "armor", "melee", "explosive", "suit", "technical", "accessory", "tool", "medical", "food", "substance"]
    
    def __init__(self, name, types, value, id="", manufacturer=""):
        self.name = name
        self.types = types
        self.value = value
        self.manufacturer = manufacturer
        if id == "":
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
            JobTypeList.addjobtype(JobType(row['Job Type'], int(row['id']), itemdict))
            
def initializejoblist():
    with open(r'static\jobsitems\Jobs.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            typelist = list((row['Type'].split(",")))
            if row['Stat'] == "str":
                joblist = JobList.newstrjoblist
            elif row['Stat'] == 'agl':
                joblist = JobList.newagljoblist
            elif row['Stat'] == 'wit':
                joblist = JobList.newwitjoblist
            elif row['Stat'] == 'emp':
                joblist = JobList.newempjoblist
            joblist.append(Job(row['Job'], int(row['id']), row['Stat'], typelist))

# Called from app.py
def initializestats():
    initializeitemlist()
    initializejobtypes()
    initializejoblist()




