class ShipList:
    shiplist = []
    masterid = 1
    tempship = ""

    # Used for saving or updating a ship, not for importing a ship.
    @staticmethod
    def saveship(ship):
        if ship.id == 0:
            ShipList.shiplist.append(ship)
            ship.id = ShipList.masterid
            ShipList.masterid += 1
            for crew in ship.crewlist.values():
                NpcList.savenpc(crew)
            if ship.cat != "None":
                CatList.savecat(ship.cat)
        else:
            for i, shipc in enumerate(ShipList.shiplist):
                if ship.id == shipc.id:
                    ShipList.shiplist[i] = ship
                    break


    @staticmethod
    def removeship(shipid):
        found = False
        for ship in ShipList.shiplist:
            if shipid == ship.id:
                ShipList.shiplist.remove(ship)
                found = True
                break
        return found

    @staticmethod
    def findshipfromid(shipid):
        for ship in ShipList.shiplist:
            if ship.id == shipid:
                return ship
        raise ValueError(f"Invalid shipid {shipid}.")


class NpcList:
    npclist = []
    masterid = 1


    @staticmethod
    def savenpc(npc):
        NpcList.npclist.append(npc)
        npc.id = NpcList.masterid
        NpcList.masterid += 1
        

    @staticmethod
    def removenpc(npcid):
        found = False
        for npc in NpcList.npclist:
            if npcid == npc.id:
                NpcList.npclist.remove(npc)
                found = True
                break
        return found
    
    @staticmethod
    def findnpcfromid(npcid):
        for npc in NpcList.npclist:
            if npcid == npc.id:
                return npc
        raise ValueError(f"Invalid npcid {npcid}.")

class StarList:
    starlist = []
    masterid = 1
    tempstar = ""

    @staticmethod
    def savestar(star):
        StarList.starlist.append(star)
        star.id = StarList.masterid
        StarList.masterid += 1

    @staticmethod
    def removestar(starid):
        found = False
        star = StarList.findstarfromid(starid)
        if star:
            StarList.starlist.remove(star)
            found = True
        return found
    
    @staticmethod
    def findstarfromid(starid):
        for star in StarList.starlist:
            if starid == star.id:
                return star
        raise ValueError(f"Invalid starid {starid}.")

# At this time I'm not certain it's necessary to add functionality to remove templates.
class HullTemplateList:
    hulltemplatelist = []
    masterid = 1

    @staticmethod
    def savehtemplate(template):
        if template.id == 0:
            HullTemplateList.hulltemplatelist.append(template)
            template.id = HullTemplateList.masterid
            HullTemplateList.masterid += 1

# At this time I'm not certain it's necessary to add functionality to remove templates.
class HullModelList:
    hullmodellist = []
    masterid = 1

    @staticmethod
    def savehmodel(model):
        if model.id == 0:
            HullModelList.hullmodellist.append(model)
            model.id = HullModelList.masterid
            HullModelList.masterid += 1
    
class CatList:
    catlist = []
    masterid = 1

    @staticmethod
    def savecat(cat):
        if cat.id == 0:
            CatList.catlist.append(cat)
            cat.id = CatList.masterid
            CatList.masterid += 1