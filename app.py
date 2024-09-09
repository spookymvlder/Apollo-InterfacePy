import sys, random, os

from factions import Faction, FactionList, initializeall
initializeall()
from gennpc import Npc, statlist
from location import Location
from genmeow import Cat
from genstar import Star
from genplanet import Planet
from genmoon import Moon
from hulls import HullTemplate, HullSpecs, HullModel, HullModels, HullType
from genship import Ship
from namelists import NationNameTable


from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)



def idtoname(id):
    return Faction.idtoname(id)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.jinja_env.globals.update(idtoname=idtoname)

Session(app)



#Generate initial location to save any potential NPCs
#defaultplace = Location("Unassigned", "Default")

npclist = []


#Break out posts so a banner appears if invalid combination attempted to be saved. Or warning that invalid combinations will be automatically resolved
@app.route("/", methods=["GET", "POST"])
def index():
    sexes = ["M", "F"]
    types = ["HUMAN", "SYNTH"]
    #factionnames = []
    #for faction in FactionList.factionlist:
    #    factionnames.append(faction.name)
    if request.method == "GET":
        npc = Npc()
    if request.method =="POST":
        sex = request.form.get("sex")
        postfaction = request.form.get("faction")
        pstat = request.form.get("pstat")
        type = request.form.get("type")
        nation = request.form.get("namelist")
        postfaction = Faction.nametoid(postfaction)
        '''if postfaction not in factionnames:
            postfaction = ""'''
        '''if pstat not in statlist:
            pstat = ""
        else:'''
        for x in range(len(statlist)):
            if pstat == statlist[x]:
                pstat = x
                break
        '''if type not in types:
            type = ""
        if nation not in nationlist:
            nation = ""'''
        npc = Npc(sex=sex, factionid=postfaction, pstat=pstat, type=type, nation=nation)
    npcfactionname = Faction.idtoname(npc.factionid)
    pstat = statlist[npc.pstat]
    return render_template("index.html", namelist=NationNameTable.nationlist, sexes=sexes, factions=FactionList.factionlist, types=types, statlist=statlist, npc=npc, npcfaction=npcfactionname, pstat=pstat)
            

@app.route("/validatenpc", methods=["POST"])
def validatenpc():
        sex = request.form.get("gensex")
        pstat = request.form.get("genpstat")
        for x in range(len(statlist)):
            if pstat == statlist[x]:
                pstat = x
                break
        type = request.form.get("gentype")
        #nation = request.form.get("namelist")
        postfaction = request.form.get("genfaction")
        postfaction = Faction.nametoid(postfaction)
        forename = request.form.get("genforename")
        surname = request.form.get("gensurname")
        job = request.form.get("genjob")
        type = request.form.get("gentype")
        stats = [request.form.get("genstr"), request.form.get("genagl"), request.form.get("genwit"), request.form.get("genemp"), request.form.get("genhp")]
        npclist.append(Npc(sex=sex, factionid=postfaction, pstat=pstat, type=type, forename=forename, surname=surname, job=job, stats=stats))
        return redirect("/npcs")

@app.route("/npcs", methods=["GET", "POST"])
def npcs():
    if request.method == "GET" or "POST":
        npcstrings = []
        for x in range(len(npclist)):
            npcstrings.append(npclist[x])
    return render_template("npcs.html", npcstrings=npcstrings)

@app.route("/cats")
def cats():
    cat = Cat()
    return render_template("cats.html", cat=cat)

@app.route("/solar")
def solar():
    sun = Star()
    planets = []
    moons = []
    if sun.pcount != 0:
        for planet in sun.solarobjects:
            planets.append(planet)
            if planet.mooncount > 0:
                for moon in planet.moons:
                    moons.append(moon)
    return render_template("solar.html", sun=sun, planets=planets, moons=moons)

@app.route("/ships")
def ships():
    hulltype = HullType()
    ship = Ship(HullModel(HullTemplate(hulltype.size, hulltype.type, hulltype.category, hulltype.ordenance, hulltype.armor, hulltype.troops, hulltype.priority)))
    return render_template("ships.html", ship=ship)



