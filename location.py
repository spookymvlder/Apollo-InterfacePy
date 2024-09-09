import random

class Location():
    types = ["Ship", "Base", "Station", "Habitat", "Planet", "Star", "Camp", "Default"]

    def __init__(self, name, type, types):
        #Split out evenutally
        
        if type not in types:
            raise ValueError("Invalid type for location")
        self.type = type
        if not name:
            name = type + "-" + random.randint(0,999)
        self.name = name
        self.inhabitants = []
        self.buildcontainers(self.type)

    def buildcontainers(self, type):
        match type:
            case "Ship" | "Station":
                self.crew = []
            case "Base" | "Camp":
                self.staff = []
            case "Planet" | "Star":
                self.places = []



    def addnpc(self, npc):
        self.inhabitants.append(npc)
    
    def removenpc(self, npc):
        self.inhabitants.remove(npc)