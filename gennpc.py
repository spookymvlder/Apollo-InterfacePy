import random
from helpers import coin
from load_initial import nationlist, factioncountry, factionlist, nametable, Faction

strjob = ['Marine', 'Soldier', 'Mercenary', 'Security Guard', 'Bounty Hunter', 'Roughneck', 'Miner', 'Factory Worker', 'Machinist', 'Mechanic', 'Engineer', 'Farmer', 'Technician']
agljob = ['Pilot', 'Smuggler', 'Wildcatter', 'Prospector', 'Surveyor']
witjob = ['Colonial Marshal', 'Security Chief', 'Marshal', 'Deputy', 'Sheriff', 'Bounty Hunter', 'Guard', 'Company Agent', 'Executive', 'Junior Executive', 'Manager', 'Division Head', 'Supervisor', 'Journalist', 'Researcher', 'Inventor', 'Scientist', 'Biologist', 'Chemist']
empjob = ['Medic', 'Paramedic', 'Doctor', 'Combat Medic', 'Officer', 'Captain', 'Bridge Officer', 'Inspector', 'Facility Manager', 'Counselor', 'Quartermaster','Performer', 'Club Owner', 'Waiter', 'Bartender']
statlist = ["Strength", "Agility", "Wits", "Empathy"]


class Npc():
    def __init__(self, forename="", surname="", type="", sex="", factionid="", job="", stats="", pstat="", nation=""):
        self.sex = sex
        '''if not factionid:
            if not nation:
                factionid = Npc.genfactionrand()
            else:
                factionid = Npc.genfactioninformed(nation)'''
        #If faction is empty or invalid, check if nation exists.
        if not bool(Faction.idtoname(factionid)):
            if bool(Npc.validatenation):
                factionid = Npc.genfactioninformed(nation)
            else:
                factionid = Npc.genfactionrand()
        self.factionid = factionid
        self.nation = nation
        self.forename = forename
        self.surname = surname
        self.type = type
        self.pstat = pstat
        self.job = job
        self.stats = stats
    
    @staticmethod
    def gensexrand():
        flip = coin()
        if flip == 0:
            sex = "M"
        else:
            sex = "F"
        return sex
    
    @property
    def sex(self):
        return self._sex
    
    @sex.setter
    def sex(self, sex):
        if not sex:
            sex = Npc.gensexrand()
        else:
            sex = sex[0]
            sex = sex.upper()
            if sex != ("M" or "F"):
                sex = Npc.gensexrand()
        self._sex = sex
    
    @staticmethod
    def genfactioninformed(nation=""):
        if not nation:
            faction = Npc.genfactionrand()
        else:
            try:
                faction = factioncountry[nation]
            except:
                faction = Npc.genfactionrand()
        return faction

    @staticmethod
    def genfactionrand():
        faction = random.choice(factionlist)
        return faction.id
    
    @staticmethod
    def validatenation(nation):
        if nation in nationlist:
            return True
        else:
            return False
        
    @property
    def factionid(self):
        return self._factionid
    
    @factionid.setter
    def factionid(self, factionid):
        if not bool(Faction.idtoname(factionid)):
            factionid = Npc.genfactionrand()
        self._factionid = factionid
    
    @staticmethod
    def gennationrand():
        return random.choice(nationlist)

    @staticmethod
    def gennationinformed(faction=""):
        if not faction:
            return Npc.gennationrand()  
        for fact in factionlist:
            if fact.id == faction:
                if fact.nations:
                    templist = []
                    for lang in fact.nations:
                        if lang in nationlist:
                            templist.append(lang)
                    if templist:
                        return random.choice(templist)
                    else:
                        break
                else:
                    break
        return Npc.gennationrand()
    
    @property
    def nation(self):
        return self._nation
    
    @nation.setter
    def nation(self, nation):
        if not Npc.validatenation(nation):
            faction = self.factionid
            if not faction:
                nation = Npc.gennationrand()
            else:
                nation = Npc.gennationinformed(faction)
        self._nation = nation

    @staticmethod
    def gennametable(nation=""):
        if not nation or nation not in nationlist:
            nation = Npc.gennationrand()
        return nametable(nation)

    @staticmethod
    def genname(namelist):
        name = random.randint(0, Npc.chance(namelist))
        name = namelist[name]
        return name

    @property
    def forename(self):
        return self._forename
    
    @forename.setter
    def forename(self, forename):
        if not forename:
            tables = Npc.gennametable(self.nation)
            if self.sex == "F":
                self._forename = Npc.genname(tables[1])
            else:
                self._forename = Npc.genname(tables[2])
        else:
            self._forename = forename

    @property
    def surname(self):
        return self._surname
    
    @surname.setter
    def surname(self, surname):
        if not surname:
            tables = Npc.gennametable(self.nation)
            self._surname = Npc.genname(tables[0])
        else:
            self._surname = surname

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
    
    @staticmethod
    def gentype():
        rand = random.randint(1,100)
        if rand >= 95:
            type = "SYNTH"
        else:
            type = "HUMAN"
        return type

    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type):
        if not type or type.upper != ("HUMAN" or "SYNTH"):
            self._type = Npc.gentype()
        else:
            self._type = type.upper()

    @staticmethod
    def genprimarystat():
        stat = random.randint(0,3)
        return stat
    
    @property
    def pstat(self):
        return self._pstat
    
    @pstat.setter
    def pstat(self, pstat):
        if not pstat or not (pstat >= 0 and pstat <= 3):
            pstat = Npc.genprimarystat()
        self._pstat = pstat

    @staticmethod
    def getjob(stat):
        if not stat or not (stat >= 0 and stat <= 3):
            stat = Npc.genprimarystat()
        match statlist[stat]:
            case "Strength":
                jlist = strjob
            case "Agility":
                jlist = agljob
            case "Wits":
                jlist = witjob
            case "Empathy":
                jlist = empjob
        return random.choice(jlist)

    @property
    def job(self):
        return self._job
    
    @job.setter
    def job(self, job):
        if not job or not isinstance(job, str):
            job = Npc.getjob(self.pstat)
        self._job = job

    @staticmethod
    def genstatsrand(pstat="", type="HUMAN"):
        if not pstat:
            pstat = Npc.genprimarystat()
        stats = [1, 1, 1, 1]
        stats[pstat] += 2
        tstats = 6
        while tstats < 14:
            rand = random.randint(0,3)
            if stats[rand] < 5:
                stats[rand] += 1
                tstats += 1
        if type == "SYNTH":
            stats[pstat] += 3
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
    

    @property
    def stats(self):
        return self._stats
    
    @stats.setter
    def stats(self, stats=""):
        if not Npc.validatestats(stats) or not stats:
            stats = Npc.genstatsrand(self.pstat, self.type)
        self._stats = stats

    def __str__(self):
        return f"Name: {self.forename} {self.surname}\nType: {self.type}\nFaction: {Faction.idtoname(self.factionid)}\nJob: {self.job}\nStats: {self.stats}\n"

#character = genchar()
#printcharacter(character)
#npc = Npc()
#print(npc)
