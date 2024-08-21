import csv, string
from pathlib import Path

factioncountry = {}
factionlist = []
entitycat = []
surafg = []
fafg = []
mafg = []
surarg = []
farg = []
marg = []
suraus = []
faus = []
maus = []
suraze = []
faze = []
maze = []
surchl = []
fchl = []
mchl = []
surdeu = []
fdeu = []
mdeu = []
suregy = []
fegy = []
megy = []
suresp = []
fesp = []
mesp = []
surfji = []
ffji = []
mfji = []
surfra = []
ffra = []
mfra = []
suridn = []
fidn = []
midn = []
surind = []
find = []
mind = []
surirn = []
firn = []
mirn = []
surjpn = []
fjpn = []
mjpn = []
surrus = []
frus = []
mrus = []
surusa = []
fusa = []
musa = []
gcat = []
fcat = []
mcat = []


#Countries that have name tables built out.
nationlist = [
    "AFG",
    "ARG",
    "AUS",
    "AZE",
    "CHL",
    "DEU",
    "EGY",
    "ESP",
    "FJI",
    "FRA",
    "IDN",
    "IRN",
    "JPN",
    "RUS",
    "USA"
]

def initializefactionlist():
    with open('static/FactionList.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        x = 0
        for row in reader:
            '''factionlist[int(row['FactionId'])] = {
                "FactionName" : row['FactionName'],
                "Abbr" : row['Abbr'],
                "Type" : row['EntityType']
                }'''
            factionlist.append(Faction(row['FactionName'], row['FactionId'], row['EntityType']))
            #if row['EntityType'] not in entitycat:
               # entitycat[row['EntityId']] = row['EntityType']
            if x == 0:
                entitycat.append(Entity(row['EntityType'], row['EntityId']))
            else:
                if not Entity.nametoid(row['EntityType']):
                    entitycat.append(Entity(row['EntityType'], row['EntityId']))
            x += 1

def initializefactioncountry():
    with open('static/faction_country.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            factioncountry[row['Country']] = int(row['FactionId'])
            factionlist[int(row['FactionId']) - 1].addnamelist(row['Country'])

class Faction:
    def __init__(self, name, id, type):
        self.name = name
        self.id = id
        self.type = type
        self.nations = []

    @classmethod
    def idtoname(cls, id):
        if id=="":
            return False
        if factionlist[int(id)-1].id == id:
            return factionlist[int(id)-1].name
        for x in range(len(factionlist)):
            if factionlist[x].id == id:
                return factionlist[x].name
        return False
            
    @classmethod
    def nametoid(cls, name):
        if name == "":
            return False
        for x in range(len(factionlist)):
            if factionlist[x].name == name:
                return factionlist[x].id
        return False
    
    def addfaction(self, name, type):
        if bool(Faction.nametoid(name)):
            raise ValueError("Name exists")
        #Come back to entities if they ever mean anything after creation
        if not bool(Entity.nametoid(type)):
            raise ValueError("Missing type")
        id = len(factionlist)
        factionlist.append(Faction(name, id, type))

    def addnamelist(self, nation):
        if nation not in self.nations:
            self.nations.append(nation)
    
    def removenamelist(self, nation):
        if nation in self.nations:
            self.nations.remove(nation)
    
    def __str__(self):
        return f"Name: {self.name}\nId: {self.id}\nType: {self.type}\nName Lists: {self.nations}"

class Entity:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    @classmethod
    def idtoname(self, id):
        for x in range(len(entitycat)):
            if entitycat[x].id == id:
                return entitycat[x].name
        return False
    @classmethod
    def nametoid(self, name):
        for x in range(len(entitycat)):
            if entitycat[x].name == name:
                return entitycat[x].id
        return False
        
def initializeall():
    initializefactionlist()
    initializefactioncountry()
    

def initializetxt(filepath):
    f = open(filepath, "r", encoding="utf8")
    tempname = []
    for x in f:
        x = x.replace('\n','')
        tempname.append(x)
    return tempname

#A note on names, at least the USA files are from the 1990 US census and the census bureau strips spaces and punctuation
def initializetxtUSA(filepath):
    f = open(filepath, "r", encoding="utf8")
    tempname = []
    for x in f:
        x = x.replace('\n','')
        tempname.append(x.title())
    return tempname
    
def catnametable():
    table = []
    if not bool(gcat):
        loadCat()
        table.append(gcat)
        table.append(fcat)
        table.append(mcat)
    return table

#Returns a list of three name lists for the entered language. Initializes names from that country if not already initialized.
def nametable(nation):
    table = {}
    match nation:
        case "AFG":
            if not bool(surafg):
                loadAFG()
            table[0] = surafg
            table[1] = fafg
            table[2] = mafg
        case "ARG":
            if not bool(surarg):
                loadARG()
            table[0] = surarg
            table[1] = farg
            table[2] = marg
        case "AUS":
            if not bool(suraus):
                loadAUS()
            table[0] = suraus
            table[1] = faus
            table[2] = maus
        case "AZE":
            if not bool(suraze):
                loadAZE()
            table[0] = suraze
            table[1] = faze
            table[2] = maze
        case "CHL":
            if not bool(surchl):
                loadCHL()
            table[0] = surchl
            table[1] = fchl
            table[2] = mchl
        case "DEU":
            if not bool(surdeu):
                loadDEU()
            table[0] = surdeu
            table[1] = fdeu
            table[2] = mdeu
        case "EGY":
            if not bool(suregy):
                loadEGY()
            table[0] = suregy
            table[1] = fegy
            table[2] = megy
        case "ESP":
            if not bool(suresp):
                loadESP()
            table[0] = suresp
            table[1] = fesp
            table[2] = mesp
        case "FJI":
            if not bool(surfji):
                loadFJI()
            table[0] = surfji
            table[1] = ffji
            table[2] = mfji
        case "FRA":
            if not bool(surfra):
                loadFRA()
            table[0] = surfra
            table[1] = ffra
            table[2] = mfra
        case "IDN":
            if not bool(suridn):
                loadIDN()
            table[0] = suridn
            table[1] = fidn
            table[2] = midn
        case "IND":
            if not bool(surind):
                loadIND()
            table[0] = surind
            table[1] = find
            table[2] = mind
        case "IRN":
            if not bool(surirn):
                loadIRN()
            table[0] = surirn
            table[1] = firn
            table[2] = mirn
        case "JPN":
            if not bool(surjpn):
                loadJPN()
            table[0] = surjpn
            table[1] = fjpn
            table[2] = mjpn
        case "RUS":
            if not bool(surrus):
                loadRUS()
            table[0] = surrus
            table[1] = frus
            table[2] = mrus
        case "USA":
            if not bool(surusa):
                loadUSA()
            table[0] = surusa
            table[1] = fusa
            table[2] = musa
    return table
        

'''def initializeallnames():
    loadAFG()
    loadARG()
    loadAUS()
    loadAZE()
    loadCHL()
    loadDEU()
    loadEGY()
    loadESP()
    loadFJI()
    loadFRA()
    loadIDN()
    loadIND()
    loadIRN()
    loadJPN()
    loadRUS()
    loadUSA()'''

def loadAFG():
    global surafg
    global fafg
    global mafg
    surafg = initializetxt(Path(r'static\names\SURAFG.txt'))
    fafg = initializetxt(Path(r'static\names\FAFG.txt'))
    mafg = initializetxt(Path(r'static\names\MAFG.txt'))

def loadARG():
    global surarg
    global farg
    global marg
    surarg = initializetxt(Path(r'static\names\SURARG.txt'))
    farg = initializetxt(Path(r'static\names\FARG.txt'))
    marg = initializetxt(Path(r'static\names\MARG.txt'))

def loadAUS():
    global suraus
    global faus
    global maus
    suraus = initializetxt(Path(r'static\names\SURAUS.txt'))
    faus = initializetxt(Path(r'static\names\FAUS.txt'))
    maus = initializetxt(Path(r'static\names\MAUS.txt'))

def loadAZE():
    global suraze
    global faze
    global maze
    suraze = initializetxt(Path(r'static\names\SURAZE.txt'))
    faze = initializetxt(Path(r'static\names\FAZE.txt'))
    maze = initializetxt(Path(r'static\names\MAZE.txt'))

def loadCHL():
    global surchl
    global fchl
    global mchl
    surchl = initializetxt(Path(r'static\names\SURCHL.txt'))
    fchl = initializetxt(Path(r'static\names\FCHL.txt'))
    mchl = initializetxt(Path(r'static\names\MCHL.txt'))

def loadDEU():
    global surdeu
    global fdeu
    global mdeu
    surdeu = initializetxt(Path(r'static\names\SURDEU.txt'))
    fdeu = initializetxt(Path(r'static\names\FDEU.txt'))
    mdeu = initializetxt(Path(r'static\names\MDEU.txt'))

def loadEGY():
    global suregy
    global fegy
    global megy
    suregy = initializetxt(Path(r'static\names\SUREGY.txt'))
    fegy = initializetxt(Path(r'static\names\FEGY.txt'))
    megy = initializetxt(Path(r'static\names\MEGY.txt'))

def loadESP():
    global suresp
    global fesp
    global mesp
    suresp = initializetxt(Path(r'static\names\SURESP.txt'))
    fesp = initializetxt(Path(r'static\names\FESP.txt'))
    mesp = initializetxt(Path(r'static\names\MESP.txt'))

def loadFJI():
    global surfji
    global ffji
    global mfji
    surfji = initializetxt(Path(r'static\names\SURFJI.txt'))
    ffji = initializetxt(Path(r'static\names\FFJI.txt'))
    mfji = initializetxt(Path(r'static\names\MFJI.txt'))

def loadFRA():
    global surfra
    global ffra
    global mfra
    surfra = initializetxt(Path(r'static\names\SURFRA.txt'))
    ffra = initializetxt(Path(r'static\names\FFRA.txt'))
    mfra = initializetxt(Path(r'static\names\MFRA.txt'))

def loadIDN():
    global suridn
    global fidn
    global midn
    suridn = initializetxt(Path(r'static\names\SURIDN.txt'))
    fidn = initializetxt(Path(r'static\names\FIDN.txt'))
    midn = initializetxt(Path(r'static\names\MIDN.txt'))

def loadIND():
    global surind
    global find
    global mind
    surind = initializetxt(Path(r'static\names\SURIND.txt'))
    find = initializetxt(Path(r'static\names\FIND.txt'))
    mind = initializetxt(Path(r'static\names\MIND.txt'))

def loadIRN():
    global surirn
    global firn
    global mirn
    surirn = initializetxt(Path(r'static\names\SURIRN.txt'))
    firn = initializetxt(Path(r'static\names\FIRN.txt'))
    mirn = initializetxt(Path(r'static\names\MIRN.txt'))

def loadJPN():
    global surjpn
    global fjpn
    global mjpn
    surjpn = initializetxt(Path(r'static\names\SURJPN.txt'))
    fjpn = initializetxt(Path(r'static\names\FJPN.txt'))
    mjpn = initializetxt(Path(r'static\names\MJPN.txt'))

def loadRUS():
    global surrus
    global frus
    global mrus
    surrus = initializetxt(Path(r'static\names\SURRUS.txt'))
    frus = initializetxt(Path(r'static\names\FRUS.txt'))
    mrus = initializetxt(Path(r'static\names\MRUS.txt'))

def loadUSA():
    global surusa
    global fusa 
    global musa   
    fusa = initializetxtUSA(Path(r'static\names\FUSA.txt'))
    musa = initializetxtUSA(Path(r'static\names\MUSA.txt'))
    surusa = initializetxtUSA(Path(r'static\names\SURUSA.txt'))

def loadCat():
    global fcat
    global mcat
    global gcat
    fcat = initializetxt(Path(r'static\other_names\FCAT.txt'))
    mcat = initializetxt(Path(r'static\other_names\MCAT.txt'))
    gcat = initializetxt(Path(r'static\other_names\GENERICCAT.txt'))

initializeall()

#from sys import getsizeof
#print(getsizeof(firn) + getsizeof(fjpn) + getsizeof(frus) + getsizeof(fusa) + getsizeof(surjpn) + getsizeof(mirn) + getsizeof(mjpn) + getsizeof(mrus) + getsizeof(musa) + getsizeof(surrus)+ getsizeof(surusa))