class ShipList:
    shiplist = []
    masterid = 1
    tempship = ""

    @staticmethod
    def saveship(ship):
        ShipList.shiplist.append(ship)
        ship.id = ShipList.masterid
        ShipList.masterid += 1
        for crew in ship.crewlist.values():
            NpcList.savenpc(crew)

    @staticmethod
    def removenpc(shipid):
        found = False
        for ship in ShipList.shiplist:
            if shipid == ship.id:
                ShipList.shiplist.remove(ship)
                found = True
                break
        return found



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