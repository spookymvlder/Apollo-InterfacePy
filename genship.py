import random


class Ship:
    #types = ["lifeboat", "pinnacle", "shuttle", "skiff",  "research", "yacht", "miner", "cargo freighter", "colony ship", "exploration", "transport", "patrol"]
    def __initial__(self):
        self.shiptype = ""
        self.shipcategory = "MILITARY"
    '''size
        TYPE (based on size)
        role
        faction
        crew max
        crew size
        components
        shape
        number of rooms
        floor count
        engines'''
    
    
    def gensize(self):
        sizes = ["small", "medium", "large", "xlarge"]
        return random.choice(sizes)

    @property
    def size(self):
        return self.__size
    
    @size.setter
    def size(self, size):
        sizes = ["xsmall", "small", "medium", "large", "xlarge"]
        if size:
            if size not in sizes:
                raise ValueError("Invalid ship size.")
        else:
            size = Ship.gensize(self)
        self._size = size

    @property
    def shipcategory(self):
        return self._shipcategory
    
    @shipcategory.setter
    def shipcategory(self, shipcategory):
        shipcategories = ["COURIER", "CARGO", "MILITARY", "SCIENCE", "CIVILIAN", "GOVERNMENT"]
        if shipcategory:
            if shipcategory not in shipcategories:
                raise ValueError("Invalid ship category.")
        else:
            shipcategory = random.choice(shipcategories)
        self._shipcategory = shipcategory

    @property
    def shiptype(self):
        return self._shiptype
    
    @shiptype.setter
    def shiptype(self, shiptype, shipcategory, shipsize):
        shiptypes =  ["lifeboat", "pinnacle", "shuttle", "skiff",  "research", "yacht", "miner", "cargo freighter", "colony ship", "exploration", "transport", "patrol"]
        if self.shipcategory == "MILITARY":
            shiptypes = ["lifeboat", "shuttle", "skiff", "fighter", "dropship", "heavy dropship", "frigate", "light frigate", "escort frigate", "heavy frigate", "carrier frigate", "corvette", "light corvette", "heavy corvette", 
                     "stealth corvette", "destroyer", "heavy destroyer", "cruiser", "surveillance cruiser", "heavy cruiser", "carrier", "assualt carrier", "heavy carrier", "battleship", "mobile dockyard",
                      "minehunter", "galleon", "monitor", "transport", "patrol"]
            if shiptype != "" and shiptype not in shiptypes:
                raise ValueError("Invalid Military ship type")
            if shipsize == "xsmall":
                shiptypes = ["lifeboat", "shuttle", "fighter", ]
                if shiptype and shiptype not in shiptypes:
                    raise ValueError("Ship size and type mismatch")
                
