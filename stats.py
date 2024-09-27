# Place to save everything related to primary stats, such as jobs, talents, skills, and items.

class JobList:
    strjob = ['Marine', 'Soldier', 'Mercenary', 'Security Guard', 'Bounty Hunter', 'Roughneck', 'Miner', 'Factory Worker', 'Machinist', 'Mechanic', 'Engineer', 'Farmer', 'Technician']
    agljob = ['Pilot', 'Smuggler', 'Wildcatter', 'Prospector', 'Surveyor']
    witjob = ['Colonial Marshal', 'Security Chief', 'Marshal', 'Deputy', 'Sheriff', 'Bounty Hunter', 'Guard', 'Company Agent', 'Executive', 'Junior Executive', 'Manager', 'Division Head', 'Supervisor', 'Journalist', 'Researcher', 'Inventor', 'Scientist', 'Biologist', 'Chemist']
    empjob = ['Medic', 'Paramedic', 'Doctor', 'Combat Medic', 'Officer', 'Captain', 'Bridge Officer', 'Inspector', 'Facility Manager', 'Counselor', 'Quartermaster','Performer', 'Club Owner', 'Waiter', 'Bartender']
    joblist = strjob + agljob + witjob + empjob


    #empty lists for saving new jobs to, which can then be exported.
    newstrjoblist = []
    newagljoblist = []
    newwitjoblist = []
    newempjoblist = []


    strjoblist = strjob + newstrjoblist
    agljoblist = agljob + newagljoblist
    witjoblist = witjob + newwitjoblist
    empjoblist = empjob + newempjoblist
    #def addjobtolist

class Job:
    jobtypes = ['military', 'enforcement', 'admin', 'intrigue', 'labor', 'research', 'health', 'tech']

    def __init__(self, job):
        self.job = job

class ItemList:
    ...

