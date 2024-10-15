import csv
# Place to save everything related to primary stats, such as jobs, talents, skills, and items.

class JobList:
    statlist = ["strength", "agility", "wits", "empathy"]
    strjob = ['Marine', 'Soldier', 'Mercenary', 'Security Guard', 'Bounty Hunter', 'Roughneck', 'Miner', 'Factory Worker', 'Machinist', 'Mechanic', 'Engineer', 'Farmer', 'Technician']
    agljob = ['Pilot', 'Smuggler', 'Wildcatter', 'Prospector', 'Surveyor']
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

# Jobs should have associated items and similar things to make NPC generation interesting.
class Job:
    jobtypes = ['military', 'enforcement', 'admin', 'intrigue', 'labor', 'research', 'health', 'tech']

    def __init__(self, job):
        self.job = job

class ItemList:
    weaponlist = []
    itemlist = []
    masterid = 1
    
    @staticmethod
    def additem(item):
        ItemList.itemlist.append(item)
        if item.id >= ItemList.masterid:
            ItemList.masterid = item.id + 1
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
    with open(r'static\items.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            typelist = list((row['Type'].split(",")))
            ItemList.additem(Item(row['Name'], typelist, int(row['Value']), int(row['Id'])))
            