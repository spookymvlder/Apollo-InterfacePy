from load_initial import initializetxt
from pathlib import Path

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

def returnNamelist(category):
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
    return tlist

