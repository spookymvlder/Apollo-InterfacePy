from pathlib import Path
import random

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

#TODO add support for appending lists
class AnimalName:
    namelist = []
    newnamelist = []
    
    def __init__(self):
        AnimalName.namelist = initializetxt(Path(r'static\other_names\animals.txt'))

class MythicalName:
    namelist = []
    newnamelist = []
    
    def __init__(self):
        MythicalName.namelist = initializetxt(Path(r'static\other_names\mythical.txt'))

class FantasyJobs:
    namelist = []
    newnamelist = []
    
    def __init__(self):
        FantasyJobs.namelist = initializetxt(Path(r'static\other_names\fantasyjobs.txt'))

class PredatorName:
    namelist = []
    newnamelist = []
    
    def __init__(self):
        PredatorName.namelist = initializetxt(Path(r'static\other_names\predators.txt'))

class WeatherName:
    namelist = []
    newnamelist = []
    
    def __init__(self):
        WeatherName.namelist = initializetxt(Path(r'static\other_names\weather.txt'))

class CargoName:
    namelist = []
    newnamelist = []
    
    def __init__(self):
        CargoName.namelist = initializetxt(Path(r'static\other_names\cargo.txt'))

class YachtName:
    namelist = []
    newnamelist = []
    
    def __init__(self):
        YachtName.namelist = initializetxt(Path(r'static\other_names\yachts.txt'))

class ExplorerName:
    namelist = []
    newnamelist = []
    
    def __init__(self):
        ExplorerName.namelist = initializetxt(Path(r'static\other_names\explorers.txt'))

class CourierName:
    namelist = []
    newnamelist = []
    
    def __init__(self):
        CourierName.namelist = initializetxt(Path(r'static\other_names\couriers.txt'))

class AdjectiveName:
    namelist = []
    newnamelist = []

    def __init__(self):
        AdjectiveName.namelist = initializetxt(Path(r'static\other_names\adjectives.txt'))

class ColorName:
    namelist = []
    newnamelist = []

    def __init__(self):
        ColorName.namelist = initializetxt(Path(r'static\other_names\colors.txt'))


class USName:
    namelist = []
    newnamelist = []

    def __init__(self):
        USName.namelist = initializetxt(Path(r'static\other_names\USnames.txt'))

class TWEName:
    namelist = []
    newnamelist = []

    def __init__(self):
        TWEName.namelist = initializetxt(Path(r'static\other_names\TWEnames.txt'))

class UPPName:
    namelist = []
    newnamelist = []

    def __init__(self):
        UPPName.namelist = initializetxt(Path(r'static\other_names\UPPnames.txt'))

class TerrainName:
    namelist = []
    newnamelist = []

    def __init__(self):
        TerrainName.namelist = initializetxt(Path(r'static\other_names\terrain.txt'))

def returnNameList(category):
    tlist = ""
    match category:
        case "animal":
            AnimalName()
            tlist = AnimalName.namelist
        case "mythical":
            MythicalName()
            tlist = MythicalName.namelist
        case "fantasy":
            FantasyJobs()
            tlist = FantasyJobs.namelist
        case "predator":
            PredatorName()
            tlist = PredatorName.namelist
        case "weather":
            WeatherName()
            tlist = WeatherName.namelist
        case "cargo":
            CargoName()
            tlist = CargoName.namelist
        case "yacht":
            YachtName()
            tlist = YachtName.namelist
        case "explorer":
            ExplorerName()
            tlist = ExplorerName.namelist
        case "courier":
            CourierName()
            tlist = CourierName.namelist
        case "adjective":
            AdjectiveName()
            tlist = AdjectiveName.namelist
        case "color":
            ColorName()
            tlist = ColorName.namelist
        case "usname":
            USName()
            tlist = USName.namelist
        case "3wename":
            TWEName()
            tlist = TWEName.namelist
        case "uppname":
            UPPName()
            tlist = UPPName.namelist
        case "terrain":
            TerrainName()
            tlist = TerrainName.namelist

    return tlist

def returnNeutCategory():
    tlist = ["animal", "mythical", "fantasy", "predator", "weather", "cargo", "yacht", "explorer", "courier", "terrain"]
    return random.choice(tlist)

def returnPrefix():
    tlist = ["color", "adjective"]
    return random.choice(tlist)

#Doubles as both a list of nation based name tables that are populated and a list that can be populated. When retrieving a name table
#will build that name table if it isn't already populated.
class NationNameTable:
    namelist = []
    #Countries that have name tables built out. Need a list of possible countries separate from the list of countries that have had names loaded.
    nationlist = [
        "AFG",
        "ARG",
        "AUS",
        "AZE",
        "CHL",
        "CHN",
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

    # Loads country names as needed. As list of available names may grow, doesn't store them all if not needed, but also won't require regenerating each time.
    def nametable(nation):
        tables = []
        match nation:
            case "AFG":
                if nation not in NationNameTable.namelist:
                    AFG()
                tables.append(AFG.sur)
                tables.append(AFG.fem)
                tables.append(AFG.mal)
            case "ARG":
                if nation not in NationNameTable.namelist:
                    ARG()
                tables.append(ARG.sur)
                tables.append(ARG.fem)
                tables.append(ARG.mal)
            case "AUS":
                if nation not in NationNameTable.namelist:
                    AUS()
                tables.append(AUS.sur)
                tables.append(AUS.fem)
                tables.append(AUS.mal)
            case "AZE":
                if nation not in NationNameTable.namelist:
                    AZE()
                tables.append(AZE.sur)
                tables.append(AZE.fem)
                tables.append(AZE.mal)
            case "CHL":
                if nation not in NationNameTable.namelist:
                    CHL()
                tables.append(CHL.sur)
                tables.append(CHL.fem)
                tables.append(CHL.mal)
            case "CHN":
                if nation not in NationNameTable.namelist:
                    CHN()
                tables.append(CHN.sur)
                tables.append(CHN.fem)
                tables.append(CHN.mal)
            case "DEU":
                if nation not in NationNameTable.namelist:
                    DEU()
                tables.append(DEU.sur)
                tables.append(DEU.fem)
                tables.append(DEU.mal)
            case "EGY":
                if nation not in NationNameTable.namelist:
                    EGY()
                tables.append(EGY.sur)
                tables.append(EGY.fem)
                tables.append(EGY.mal)
            case "ESP":
                if nation not in NationNameTable.namelist:
                    ESP()
                tables.append(ESP.sur)
                tables.append(ESP.fem)
                tables.append(ESP.mal)
            case "FJI":
                if nation not in NationNameTable.namelist:
                    FJI()
                tables.append(FJI.sur)
                tables.append(FJI.fem)
                tables.append(FJI.mal)
            case "FRA":
                if nation not in NationNameTable.namelist:
                    FRA()
                tables.append(FRA.sur)
                tables.append(FRA.fem)
                tables.append(FRA.mal)
            case "IDN":
                if nation not in NationNameTable.namelist:
                    IDN()
                tables.append(IDN.sur)
                tables.append(IDN.fem)
                tables.append(IDN.mal)
            case "IND":
                if nation not in NationNameTable.namelist:
                    IND()
                tables.append(IND.sur)
                tables.append(IND.fem)
                tables.append(IND.mal)
            case "IRN":
                if nation not in NationNameTable.namelist:
                    IRN()
                tables.append(IRN.sur)
                tables.append(IRN.fem)
                tables.append(IRN.mal)
            case "JPN":
                if nation not in NationNameTable.namelist:
                    JPN()
                tables.append(JPN.sur)
                tables.append(JPN.fem)
                tables.append(JPN.mal)
            case "RUS":
                if nation not in NationNameTable.namelist:
                    RUS()
                tables.append(RUS.sur)
                tables.append(RUS.fem)
                tables.append(RUS.mal)
            case "USA":
                if nation not in NationNameTable.namelist:
                    USA()
                tables.append(USA.sur)
                tables.append(USA.fem)
                tables.append(USA.mal)
        return tables


        
class AFG:
    sur = []
    fem = []
    mal = []
    factions = []
    def __init__(self):
        AFG.sur = initializetxt(Path(r'static\names\SURAFG.txt'))
        AFG.fem = initializetxt(Path(r'static\names\FAFG.txt'))
        AFG.mal = initializetxt(Path(r'static\names\MAFG.txt'))
        NationNameTable.namelist.append("AFG")

class ARG():
    sur = []
    fem = []
    mal = []
    factions = []
    def __init__(self):
        ARG.sur = initializetxt(Path(r'static\names\SURARG.txt'))
        ARG.fem = initializetxt(Path(r'static\names\FARG.txt'))
        ARG.mal = initializetxt(Path(r'static\names\MARG.txt'))
        NationNameTable.namelist.append("ARG")

class AUS():
    sur = []
    fem = []
    mal = []
    factions = []
    def __init__(self):
        AUS.sur = initializetxt(Path(r'static\names\SURAUS.txt'))
        AUS.fem = initializetxt(Path(r'static\names\FAUS.txt'))
        AUS.mal = initializetxt(Path(r'static\names\MAUS.txt'))
        NationNameTable.namelist.append("AUS")

class AZE():
    sur = []
    fem = []
    mal = []
    factions = []
    def __init__(self):
        AZE.sur = initializetxt(Path(r'static\names\SURAZE.txt'))
        AZE.fem = initializetxt(Path(r'static\names\FAZE.txt'))
        AZE.mal = initializetxt(Path(r'static\names\MAZE.txt'))
        NationNameTable.namelist.append("AZE")

class CHL():
    sur = []
    fem = []
    mal = []
    factions = []
    def __init__(self):
        CHL.sur = initializetxt(Path(r'static\names\SURCHL.txt'))
        CHL.fem = initializetxt(Path(r'static\names\FCHL.txt'))
        CHL.mal = initializetxt(Path(r'static\names\MCHL.txt'))
        NationNameTable.namelist.append("CHL")

class CHN():
    sur = []
    fem = []
    mal = []
    factions = []
    def __init__(self):
        CHN.sur = initializetxt(Path(r'static\names\SURCHN.txt'))
        CHN.fem = initializetxt(Path(r'static\names\FCHN.txt'))
        CHN.mal = initializetxt(Path(r'static\names\MCHN.txt'))
        NationNameTable.namelist.append("CHN")

class DEU():
    sur = []
    fem = []
    mal = []
    def __init__(self):
        DEU.sur = initializetxt(Path(r'static\names\SURDEU.txt'))
        DEU.fem = initializetxt(Path(r'static\names\FDEU.txt'))
        DEU.mal = initializetxt(Path(r'static\names\MDEU.txt'))
        NationNameTable.namelist.append("DEU")

class EGY():
    sur = []
    fem = []
    mal = []
    def __init__(self):
        EGY.sur = initializetxt(Path(r'static\names\SUREGY.txt'))
        EGY.fem = initializetxt(Path(r'static\names\FEGY.txt'))
        EGY.mal = initializetxt(Path(r'static\names\MEGY.txt'))
        NationNameTable.namelist.append("EGY")

class ESP():
    sur = []
    fem = []
    mal = []
    def __init__(self):
        ESP.sur = initializetxt(Path(r'static\names\SURESP.txt'))
        ESP.fem = initializetxt(Path(r'static\names\FESP.txt'))
        ESP.mal = initializetxt(Path(r'static\names\MESP.txt'))
        NationNameTable.namelist.append("ESP")

class FJI():
    sur = []
    fem = []
    mal = []
    def __init__(self):
        FJI.sur = initializetxt(Path(r'static\names\SURFJI.txt'))
        FJI.fem = initializetxt(Path(r'static\names\FFJI.txt'))
        FJI.mal = initializetxt(Path(r'static\names\MFJI.txt'))
        NationNameTable.namelist.append("FJI")

class FRA():
    sur = []
    fem = []
    mal = []
    def __init__(self):
        FRA.sur = initializetxt(Path(r'static\names\SURFRA.txt'))
        FRA.fem = initializetxt(Path(r'static\names\FFRA.txt'))
        FRA.mal = initializetxt(Path(r'static\names\MFRA.txt'))
        NationNameTable.namelist.append("FRA")

class IDN():
    sur = []
    fem = []
    mal = []
    def __init__(self):
        IDN.sur = initializetxt(Path(r'static\names\SURIDN.txt'))
        IDN.fem = initializetxt(Path(r'static\names\FIDN.txt'))
        IDN.mal = initializetxt(Path(r'static\names\MIDN.txt'))
        NationNameTable.namelist.append("IDN") 

class IND():
    sur = []
    fem = []
    mal = []
    def __init__(self):
        IND.sur = initializetxt(Path(r'static\names\SURIND.txt'))
        IND.fem = initializetxt(Path(r'static\names\FIND.txt'))
        IND.mal = initializetxt(Path(r'static\names\MIND.txt')) 
        NationNameTable.namelist.append("IND")

class IRN():
    sur = []
    fem = []
    mal = []
    def __init__(self):
        IRN.sur = initializetxt(Path(r'static\names\SURIRN.txt'))
        IRN.fem = initializetxt(Path(r'static\names\FIRN.txt'))
        IRN.mal = initializetxt(Path(r'static\names\MIRN.txt'))
        NationNameTable.namelist.append("IRN")

class JPN():
    sur = []
    fem = []
    mal = []
    def __init__(self):
        JPN.sur = initializetxt(Path(r'static\names\SURJPN.txt'))
        JPN.fem = initializetxt(Path(r'static\names\FJPN.txt'))
        JPN.mal = initializetxt(Path(r'static\names\MJPN.txt'))
        NationNameTable.namelist.append("JPN")

class RUS():
    sur = []
    fem = []
    mal = []
    def __init__(self):
        RUS.sur = initializetxt(Path(r'static\names\SURRUS.txt'))
        RUS.fem = initializetxt(Path(r'static\names\FRUS.txt'))
        RUS.mal = initializetxt(Path(r'static\names\MRUS.txt'))
        NationNameTable.namelist.append("RUS")

class USA():
    sur = []
    fem = []
    mal = []
    def __init__(self):
        USA.sur = initializetxtUSA(Path(r'static\names\SURUSA.txt'))
        USA.fem = initializetxtUSA(Path(r'static\names\FUSA.txt'))
        USA.mal = initializetxtUSA(Path(r'static\names\MUSA.txt'))  
        NationNameTable.namelist.append("USA")


class CatNames:
    fcat = []
    mcat = []
    gcat = []
    load = False

    def __init__(self):
        CatNames.fcat = initializetxt(Path(r'static\other_names\FCAT.txt'))
        CatNames.mcat = initializetxt(Path(r'static\other_names\MCAT.txt'))
        CatNames.gcat = initializetxt(Path(r'static\other_names\GENERICCAT.txt'))
        CatNames.load = True
    

    @staticmethod
    def catnametable():
        if not CatNames.load:
            CatNames()
        return [CatNames.gcat, CatNames.fcat, CatNames.mcat]
