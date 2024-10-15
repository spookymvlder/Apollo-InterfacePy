import random
from helpers import coin
from namelists import NationNameTable
from factions import FactionList, CountryList, Faction
from stats import JobList
from savedobjects import NpcList


class Npc:
    # Move statlist to stats.py
    statlist = ["Strength", "Agility", "Wits", "Empathy"]
    sexlist = ["M", "F"]
    typelist = ["HUMAN", "SYNTH"]

    def __init__(self, forename, surname, type, sex, factionid, job, stats, pstat, nation, id):
        self.sex = sex
        self.factionid = factionid
        self.nation = nation
        self.forename = forename
        self.surname = surname
        self.type = type
        self.pstat = pstat
        self.job = job
        self.stats = stats
        self.id = id

    # TODO find a better spot for this, can't put in saved objects due to circular reference
    @staticmethod
    def unpacknpcsfromload(npcs):
        NpcList.npclist.clear()
        for npc in npcs:
            NpcList.npclist.append(Npc(npc["forename"], npc["surname"], npc["type"], npc["sex"], npc["factionid"], npc["job"], npc["stats"], npc["pstat"], npc["nation"], npc["id"]))
            if npc["id"] >= NpcList.masterid:
                NpcList.masterid = npc["id"] + 1

    # Packs each npc from the npc list as a dictionary to be converted to JSON later.
    @staticmethod
    def packnpcs():
        npcs = []
        for npc in NpcList.npclist:
            dict = {
                "forename" : npc.forename,
                "surname" : npc.surname,
                "type" : npc.type,
                "sex" : npc.sex,
                "factionid" : npc.factionid,
                "job" : npc.job,
                "stats" : npc.stats,
                "pstat" : npc.pstat,
                "nation" : npc.nation,
                "id" : npc.id
            }
            npcs.append(dict)
        return npcs

    @staticmethod
    def genrandomnpc(forename="", surname="", type="", sex="", factionid="", job="", stats="", pstat="", nation=""):
        if sex == "":
            sex = Npc.gensexrand()
        if factionid != "" and nation == "":
            nation = Npc.gennationinformed(factionid)
        elif factionid == "" and nation != "":
            factionid = Npc.genfactioninformed(nation)
        if factionid == "":
            factionid = Npc.genfactionrand()
        if nation == "":
            nation = Npc.gennationrand()
        if forename == "":
            forename = Npc.genforename(sex, nation)
        if surname == "":
            surname = Npc.gensurname(nation)
        if type == "":
            type = Npc.gentype()
        if pstat == "":
            pstat = Npc.genprimarystat()
        if job == "":
            job = Npc.getjob(pstat)
        if stats == "":
            stats = Npc.genstatsrand(pstat, type)
        id = 0
        return Npc(forename, surname, type, sex, factionid, job, stats, pstat, nation, id)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise ValueError(f"Invalid npc id.")
        self._id = id

    @property
    def sex(self):
        return self._sex
    
    @sex.setter
    def sex(self, sex):
        if sex not in Npc.sexlist:
            raise ValueError(f"Invalid npc sex attribute {sex}.")
        self._sex = sex

    @staticmethod
    def gensexrand():
        flip = coin()
        if flip == 0:
            sex = "M"
        else:
            sex = "F"
        return sex

    @property
    def factionid(self):
        return self._factionid
    
    @factionid.setter
    def factionid(self, factionid):
        if not bool(Faction.idtoname(factionid)):
            raise ValueError(f"Invalid NPC factionid {factionid}.")
        self._factionid = factionid
    
    @staticmethod
    def genfactioninformed(nation=""):
        if not nation:
            faction = Npc.genfactionrand()
        elif nation not in NationNameTable.nationlist:
            raise ValueError(f"Nation {nation} does not have a name table set.")
        else:
            try:
                faction = random.choice(CountryList.countrylist[nation])
            except:
                faction = Npc.genfactionrand()
        return faction

    @staticmethod
    def genfactionrand():
        faction = random.choice(FactionList.factionlist)
        return faction.id

    @property
    def nation(self):
        return self._nation
    
    @nation.setter
    def nation(self, nation):
        if nation not in NationNameTable.nationlist:
            raise ValueError(f"Invalid NPC nation {nation}.")
        self._nation = nation     

    @staticmethod
    def gennationrand():
        return random.choice(NationNameTable.nationlist)

    @staticmethod
    def gennationinformed(faction=""):
        if not faction:
            return Npc.gennationrand()  
        for fact in FactionList.factionlist:
            if fact.id == faction:
                if fact.nameset != []:
                    return random.choice(fact.nameset)
                return Npc.gennationrand()
        return Npc.gennationrand()
    
    @property
    def forename(self):
        return self._forename
    
    @forename.setter
    def forename(self, forename):
        if forename == "" or not isinstance(forename, str):
            raise ValueError(f"Invalid Npc forename {forename}.")
        self._forename = forename
    
    @property
    def surname(self):
        return self._surname
    
    @surname.setter
    def surname(self, surname):
        if surname == "" or not isinstance(surname, str):
            raise ValueError(f"Invalid Npc forename {surname}.")
        self._surname = surname

    @staticmethod
    def gennametable(nation=""):
        if not nation or nation not in NationNameTable.nationlist:
            nation = Npc.gennationrand()
        return NationNameTable.nametable(nation)

    @staticmethod
    def genname(namelist):
        name = random.randint(0, Npc.chance(namelist))
        return namelist[name]

    @staticmethod
    def genforename(sex, nation):
        tables = Npc.gennametable(nation)
        if sex == "F":
            return Npc.genname(tables[1])
        else:
            return Npc.genname(tables[2])

    @staticmethod
    def gensurname(nation):
        tables = Npc.gennametable(nation)
        return Npc.genname(tables[0])

    #While not as good as some sort of algorithm to consume the probability of each name table, this should skew name lists in favor of common names.
    def chance(list):
        chance = coin()
        if chance == 1:
            chance = len(list)
        else: 
            if len(list) > 50:
                chance = 50
            else:
                chance = int(len(list) / 2)
        return chance - 1
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type):
        if type not in Npc.typelist:
            raise ValueError(f"Invalid Npc type {type}.")
        self._type = type

    @staticmethod
    def gentype():
        rand = random.randint(1,100)
        if rand >= 95:
            type = "SYNTH"
        else:
            type = "HUMAN"
        return type

    @property
    def pstat(self):
        return self._pstat
    
    @pstat.setter
    def pstat(self, pstat):
        if pstat not in Npc.statlist:
            raise ValueError(f"Invalid primary stat {pstat}.")
        self._pstat = pstat
    
    @staticmethod
    def genprimarystat():
        return random.choice(Npc.statlist)
    
    @property
    def job(self):
        return self._job
    
    @job.setter
    def job(self, job):
        found = False
        for jobs in JobList.joblist:
            if job in jobs:
                found = True
                break
        if found == False:
            raise ValueError(f"Invalid job type {job}.")
        self._job = job

    @staticmethod
    def getjob(stat):
        if stat not in Npc.statlist:
            stat = Npc.genprimarystat()
        match stat:
            case "Strength":
                jlist = JobList.strjob
            case "Agility":
                jlist = JobList.agljob
            case "Wits":
                jlist = JobList.witjob
            case "Empathy":
                jlist = JobList.empjob
        return random.choice(jlist)

    @property
    def stats(self):
        return self._stats
    
    @stats.setter
    def stats(self, stats=""):
        if not Npc.validatestats(stats):
            raise ValueError(f"Invalid NPC stat values.")
        self._stats = stats

    @staticmethod
    def genstatsrand(pstat, type):
        # Probably can be removed.
        if not pstat:
            pstat = Npc.genprimarystat()
        position = 0
        for i, stat in enumerate(Npc.statlist):
            if pstat == stat:
                position = i
        stats = [1, 1, 1, 1]
        stats[position] += 2
        tstats = 6
        while tstats < 14:
            rand = random.randint(0,3)
            if stats[rand] < 5:
                stats[rand] += 1
                tstats += 1
        if type == "SYNTH":
            stats[position] += 3
            largest = stats
            largest.sort()
            largest = largest[2] #index 3 should be primary stat as it is at least 6
            for x in range(4):
                if stats[x] == largest:
                    stats[x] += 3
                    break
        health = stats[0]
        stats.append(health)
        return stats

    #Will need bulked up, range is -1 to ignore HP
    def validatestats(self, stats="", type=""):
        if type == "HUMAN":
            for x in range(len(stats) - 1):
                if stats[x] > 5:
                    return False
                elif stats[x] < 1:
                    return False
                total += stats[x]
            if total != 14:
                return False
            if stats[0] != stats[4]:
                return False
            else:
                return True
        elif type == "SYNTH":
            highcount = 0
            for x in range(len(stats) - 1):
                total += stats[x]
                if stats[x] > 5:
                    highcount += 1
                elif stats[x] < 1:
                    return False
            if highcount > 2:
                return False
            elif total != 20:
                return False
            elif stats[0] != stats[4]:
                return False
        return True
    

    

    def __str__(self):
        return f"Name: {self.forename} {self.surname}\nType: {self.type}\nFaction: {Faction.idtoname(self.factionid)}\nJob: {self.job}\nStats: {self.stats}\n"

#character = genchar()
#printcharacter(character)
#npc = Npc()
#print(npc)
