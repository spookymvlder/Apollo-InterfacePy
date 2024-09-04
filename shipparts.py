import random

#Collection of rooms for a ship
class ShipRooms:
    roomlist = []

class ShipRoomType:
    roomtypes = ["Bridge", "AI Access", "Air Scrubbers", "Engine Room", 
                 "Reactor Core", "Cryo Deck", "Quarantine Bunk", "Quarantine Rec", 
                 "Decontamination", "AI Core", "Workroom", "Coolant Tanks", 
                 "Admin Office", "Briefing Room", "Cryo Storage", "Cryo Pods", 
                 "Comm Array", "Quarantine Bunk", "Cargo Bay", "Hangar", "Brig", 
                 "Munitions Storage", "Armory", "Airlock", "EEV Suit Storage", "Vehicle Bay", 
                 "Ready Room", "Vehicle Workshop", "Parts Storage", "Science Lab", "Medlab", 
                 "Infirmary", "Med Pods", "Dorm Bunks", "Private Quarters", "Bunks", "EEV Access", 
                 "Locker Room", "Storage", "Bathroom", "Elevator", "Docking Tube", "Salvage Station",
                 "Galley", "Mess Hall", "Science Stores", "Stores", "Rec Room", "Corporate Suite", "Meeting Room",
                 "Engineering", "Officer's Galley", "Emergency Wash Station", "Lavatory", "Sensor Station", "Lockers"]
    cascaderooms = ["AI Access", "Hangar", "Vehicle Bay", "Science Lab", "Bunks"]
    roomsizes = ["S", "M", "L", "XL", "XXL"]

    def __init__(self, type, lvl, quantity, shipsize):
        self.type = type
        self.size = ShipRoomType.assesssize(type, lvl, shipsize)
        self.quantity = quantity

    def __str__(self):
        return f"Type: {self.type} Size: {self.size} Quantity: {self.quantity}\n"

    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type):
        if type not in ShipRoomType.roomtypes:
            raise ValueError(f"Invalid room type not on type list {type}.")
        self._type = type

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size):
        if size not in ShipRoomType.roomsizes:
            raise ValueError(f"Invalid size {size} for room.")
        self._size = size
    
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity):
        if not isinstance(quantity, int):
            raise ValueError(f"Invalid room quantity {quantity}.")
        self._quantity = quantity

    #Split from here for the varied list. Also needs ship size brought in.
    @classmethod
    def assesssize(cls, type, lvl, shipsize):
        slist = ["Airlock", "EEV Suit Storage", "Dorm Bunks", "Private Quarters", "Lavatory", "Elevator", "Sensor Station", 
                 "AI Access", "Med Pods", "Docking Tube", "Salvage Station", "Science Stores", "Quarantine Bunk", 
                 "Quarantine Rec", "Decontamination", "Admin Office", "Comm Array", "Lockers"]
        mlist = ["Bridge", "Engine Room", "Bunks", "Locker Room", "Storage", "Air Scrubbers", "Cryo Pods", "Munitions Storage",
                 "Ready Room", "Vehicle Workshop", "Parts Storage", "Science Lab", "Medlab", "Galley", "Corporate Suite", 
                 "Workroom", "Coolant Tanks", "Briefing Room", "Stores", "Rec Room", "Meeting Room", "Brig", "Officer's Galley"]
        llist = ["Cryo Deck", "Infirmary", "Mess Hall", "Engineering", "AI Core"]
        xxllist = ["Cryo Storage"]
        varlist = ["Cargo Bay", "Hangar", "Vehicle Bay", "Reactor Core", "EEV Access", "Bathroom"]
        if type in slist:
            size = "S"
        elif type in mlist:
            size = "M"
        elif type in varlist:
            size = ShipRoomType.varroom(type, lvl, shipsize)
        elif type in llist:
            size = "L"
        elif type in xxllist:
            size = "XXL"
        else:
            raise ValueError(f"Room type {type} not in room list.")
        return size

    @classmethod
    def varroom(cls, type, lvl, shipsize):
        if type == "Reactor Core":
            if shipsize == ("medium", "large", "xlarge"):
                size = "L"
            else:
                size = "M"
        elif type == ("EEV Access" or "Bathroom"):
            match lvl:
                case 0:
                    size = "S"
                case 1 | 2:
                    size = "M"
                case 3 | 4:
                    size = "L"
        else:
            match lvl:
                case 0 | 1:
                    size = "M"
                case 2:
                    size = "L"
                case 3:
                    size = "XL"
                case 4:
                    size = "XXL"
        return size


#Pass in modules and then spit out which rooms should be added. For each room pass that room to ShipRoomType.
#Then collect in room lists.
class Module:
    cargolvls = [.5, 10, 250, 5000, 100000]
    poplvls = [1, 10, 50, 500, 2500]
    airlvls = [10, 50, 500, 2500]
    eevlvls = [1, 4, 5, 20, 20]
    vehiclelvls = [1, 2, 3, 4, 5]
    #TODO separate vehicle and ship lvls for dropship
    all = ["AI", "Docking", "Medlab", "Science Lab", "Corp Suite", "Tractor", "Crane", 
           "Cargo Bay", "Hangar", "Vehicle Bay", "EEV", "Galley", "Air Scrubbers", "Cryo"]
    #Maybe move module build to this section.
    #Module will take in slot used. Slot used will determine what gets added for rooms. 
    # Like science lab that's in a big module gets extra labs. - Actually, have extra labs as a modifier for later

    def __init__(self, module, lvl, quantity):
        self.type = module
        self.lvl = lvl
        self.name = self.type + " " + str(self.lvl)
        self.capacity = Module.getcapacity(self.type, self.lvl)
        self.rooms = Module.associatedrooms(self.type, self.lvl)
        self.quantity = quantity

    def __str__(self):
        return f"Module Name: {self.name} Quantity: {self.quantity}\n"

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity):
        if quantity < 0:
            return ValueError(f"Invalid module quantity {quantity}.")
        self._quantity = quantity

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            return ValueError(f"Invalid module name {name}.")
        self._name = name

    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type):
        if type not in Module.all:
            raise ValueError(f"Invalid module type {type}.")
        self._type = type

    @property
    def lvl(self):
        return self._lvl
    
    @lvl.setter
    def lvl(self, lvl):
        if lvl < 0 or lvl > 4:
            raise ValueError(f"Invalid module level {lvl}.")
        self._lvl = lvl

    @property
    def capacity(self):
        return self._capacity
    
    @capacity.setter
    def capacity(self, capacity):
        if not isinstance(capacity, int):
            raise ValueError(f"Invalid capacity {capacity}.")
        self._capacity = capacity
    
    #These are just the rooms associated with a module not the actual rooms themselves.
    @property
    def rooms(self):
        return self._rooms
    
    @rooms.setter
    def rooms(self, rooms):
        for room in rooms:
            if room not in ShipRoomType.roomtypes:
                raise ValueError(f"Invalid room {room}.")
        self._rooms = rooms
    
    @classmethod
    def getcapacity(cls, module, lvl):
        match module:
            case "Cargo Bay":
                capacity = Module.cargolvls[lvl]
            case "Cryo" | "Galley":
                capacity = Module.poplvls[lvl]
            case "Air":
                capacity = Module.airlvls[lvl]
            case "EEV":
                capacity = Module.eevlvls[lvl]
            case "Hangar" | "Vehicle Bay":
                capacity = Module.vehiclelvls[lvl]
            case __:
                capacity = 0
        return capacity
    
    @classmethod
    def associatedrooms(cls, module, lvl):
        rooms = []
        match module:
            case "AI":
                rooms.append("AI Access")
            case "Docking":
                rooms.append("Docking Tube")
            case "Medlab":
                if lvl < 2:
                    rooms.append("Medlab")
                else:
                    rooms.append("Infirmary")
                    rooms.append("Med Pods")
            case "Science Lab":
                rooms.append("Science Lab")
                rooms.append("Science Stores")
            case "Corp Suite":
                rooms.append("Corporate Suite")
                if lvl > 2:
                    rooms.append("Meeting Room")
            case "Crane":
                rooms.append("Salvage Station")
            case "Cargo Bay":
                rooms.append("Cargo Bay")
                rooms.append("Parts Storage")
            case "Hangar":
                rooms.append("Hangar")
                if lvl > 2:
                    rooms.append("Vehicle Workshop")
                    rooms.append("Parts Storage")
                    rooms.append("Ready Room")
            case "Vehicle Bay":
                rooms.append("Vehicle Bay")
                if lvl > 2:
                    rooms.append("Vehicle Workshop")
                    rooms.append("Parts Storage")
            case "EEV":
                rooms.append("EEV Access")
            case "Galley":
                if lvl < 2:
                    rooms.append("Galley")
                elif lvl <= 3:
                    rooms.append("Mess Hall")
                else:
                    rooms.append("Mess Hall")
                    rooms.append("Mess Hall")
            case "Air Scrubbers":
                rooms.append("Air Scrubbers")
                if lvl > 2:
                    rooms.append("Air Scrubbers")
            case "Cryo":
                if lvl <= 2:
                    rooms.append("Cryo Pods")
                if lvl < 4:
                    rooms.append("Cryo Deck")
                else:
                    rooms.append("Cryo Pods")
                    rooms.append("Cryo Storage")
        return rooms
            
            

class ModuleList:
    modulelist = []