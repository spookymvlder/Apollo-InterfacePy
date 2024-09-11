

class NpcList:
    npclist = []
    npcid = 0


    @staticmethod
    def savenpc(npc):
        NpcList.npclist.append(npc)
        npc.id = NpcList.npcid
        NpcList.npcid += 1

    @staticmethod
    def removenpc(npcid):
        found = False
        for npc in NpcList.npclist:
            if npcid == npc.id:
                NpcList.npclist.remove(npc)
                found = True
                break
        return found

class ShipList:
    shiplist = []
    shipid = 0

    @staticmethod
    def saveship(ship):
        ShipList.shiplist.append(ship)
        ship.id = ShipList.shipid
        ShipList.shipid += 1

    @staticmethod
    def removenpc(shipid):
        found = False
        for ship in ShipList.shiplist:
            if shipid == ship.id:
                ShipList.shiplist.remove(ship)
                found = True
                break
        return found