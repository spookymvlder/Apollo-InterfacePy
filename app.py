import sys, random, os, json, io
from datetime import datetime



from factions import Faction, FactionList, initializeall
initializeall()
from gennpc import Npc
from location import Location
from genmeow import Cat
from genstar import Star
from genplanet import Planet
from genmoon import Moon
from hulls import HullTemplate, HullSpecs, HullModel, HullModels, HullType
from genship import Ship
from namelists import NationNameTable
from savedobjects import ShipList, NpcList, StarList, CatList
from helpers import convertbool




from flask import Flask, flash, redirect, render_template, request, session, send_file, jsonify
from flask_session import Session

app = Flask(__name__)



def idtoname(id):
    return Faction.idtoname(id)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.jinja_env.globals.update(idtoname=idtoname)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

Session(app)



# TODO Break out posts so a banner appears if invalid combination attempted to be saved. Or warning that invalid combinations will be automatically resolved.
# Generates a random npc to be displayed in the form. Also takes input for creating a new random npc based on desired traits.
# TODO make job list a list.
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        npc = Npc.genrandomnpc()

    if request.method =="POST":
        sex = request.form.get("sex")
        postfaction = request.form.get("faction")
        if postfaction != "":
            postfaction = int(postfaction)
        pstat = request.form.get("pstat")
        type = request.form.get("type")
        nation = request.form.get("namelist")
        for x in range(len(Npc.statlist)):
            if pstat == Npc.statlist[x]:
                pstat = x
                break
        npc = Npc.genrandomnpc(sex=sex, factionid=postfaction, pstat=pstat, type=type, nation=nation)

    return render_template("index.html", namelist=NationNameTable.nationlist, sexes=Npc.sexlist, factions=FactionList.factionlist, types=Npc.typelist, statlist=Npc.statlist, npc=npc)
            
# Saves user form data as a new NPC.
@app.route("/validatenpc", methods=["POST"])
def validatenpc():
        sex = request.form.get("gensex")
        pstat = request.form.get("genpstat")
        for x in range(len(Npc.statlist)):
            if pstat == Npc.statlist[x]:
                pstat = x
                break
        type = request.form.get("gentype")
        postfaction = int(request.form.get("genfaction"))
        forename = request.form.get("genforename")
        surname = request.form.get("gensurname")
        job = request.form.get("genjob")
        type = request.form.get("gentype")
        stats = [request.form.get("genstr"), request.form.get("genagl"), request.form.get("genwit"), request.form.get("genemp"), request.form.get("genhp")]
        NpcList.savenpc(Npc.genrandomnpc(forename, surname, type, sex, postfaction, job, stats, pstat))
        return redirect("/saved")

# Displays class strings for each saved object.
# TODO allow objects to be edited.
@app.route("/saved", methods=["GET", "POST"])
def saved():

    return render_template("npcs.html", npcstrings=NpcList.npclist, starstrings=StarList.starlist, shipstrings=ShipList.shiplist)

# Generates a random cat. Currently not saved as there's no functionality to manually attach a cat to a ship/location.
@app.route("/cats")
def cats():
    cat = Cat.genrandcat()
    return render_template("cats.html", cat=cat)

# Generates a new star. Each star generates relevant planet and moon data. Saves star to temp star as some data isn't shown to user, but needed for editing.
@app.route("/solar")
def solar():
    sun = Star.genrandomstar()
    StarList.tempstar = sun
    return render_template("solar.html", sun=sun, factionlist=FactionList.factionlist)

@app.route("/editstar", methods=["POST"])
def editstar():
    sun = int(request.form["savestar"]) # Star id
    if sun == 0:
        sun = StarList.tempstar
    else:
        sun = StarList.findstarfromid(sun)
    name = request.form.get("starname")
    pcount = int(request.form.get("planetcount"))
    starclass = request.form.get("starclass")
    spectype = int(request.form.get("spectype"))
    notes = request.form.get("notes")
    Star.editstar(sun, name, pcount, starclass, spectype, notes)
    StarList.savestar(sun)
    return render_template("solar.html", sun=sun, factionlist=FactionList.factionlist)

# Functionality for the delete button, should only appear for a star that has already been saved.
@app.route("/delstar", methods=["POST"])
def delstar():
    sun = int(request.form["delstar"])
    if sun != 0:
        StarList.removestar(sun)
    else:
        raise ValueError("Unable to delete a star that hasn't already been saved.")
    return redirect("/solar")
    

@app.route("/editplanet", methods=["POST"])
def editplanet():
    sun = int(request.form.get("sunid"))
    if sun == 0:
        sun = StarList.tempstar
    else:
        sun = StarList.findstarfromid(sun)
    id = int(request.form['saveplanet'])
    planet=""
    for obj in sun.solarobjects: # Find planet id from star
        if obj.id == id:
            planet = obj
            break
    pname = request.form.get('planetname')
    distance = float(request.form.get('planetdistance'))
    ptype = request.form.get('planettype')
    atmo = request.form.get('planetatmo')
    mass = float(request.form.get('planetsize'))
    radius = float(request.form.get('planetradius'))
    basetemp = float(request.form.get('planettemp'))
    pressure = request.form.get('planetpressure')
    mooncount = int(request.form.get('mooncount') or 0)
    faction1 = request.form.get("faction1")
    faction2 = request.form.get("faction2")
    factions = Faction.factionstolist(faction1, faction2)
    lwater = convertbool(request.form.get('lwater'))
    rings = convertbool(request.form.get('rings'))
    life = convertbool(request.form.get('life'))
    notes = request.form.get('notes')
    surveyed = float(request.form.get('planetsurvey'))
    Planet.editplanet(planet, pname, distance, ptype, atmo, mass, radius, basetemp, pressure, mooncount, factions, lwater, rings, life, notes, surveyed, sun)
    return render_template("solar.html", sun=sun, factionlist=FactionList.factionlist)

# Replaces one of a star's saved planets with a new planet in the same relative position. Planet will have a new distance from star, but will still be in a similar range band.
@app.route("/randplanet", methods=["POST"])
def randplanet():
    sun = int(request.form.get("sunid"))
    if sun == 0:
        sun = StarList.tempstar
    else:
        sun = StarList.findstarfromid(sun)
    id = int(request.form["rollbtn"])
    sun.solarobjects[id] = Planet.genplanetfromstar(sun.inzone, sun.outzone, Planet.randomdistance(sun, id), sun.startemp, sun.mass, sun.lum, Planet.randomdistancelimit(sun, id), id)
    return render_template("solar.html", sun=sun, factionlist=FactionList.factionlist)


# Planet's delete button
@app.route("/delplanet", methods=["POST"])
def delplanet():
    sun = int(request.form.get("sunid"))
    if sun == 0:
        sun = StarList.tempstar
    else:
        sun = StarList.findstarfromid(sun)
    id = int(request.form["delbtn"])
    Star.delplanet(sun, id)
    return render_template("solar.html", sun=sun, factionlist=FactionList.factionlist)

@app.route("/editmoon", methods=["POST"])
def editmoon():
    sun = int(request.form.get("sunid"))
    if sun == 0:
        sun = StarList.tempstar
    else:
        sun = StarList.findstarfromid(sun)
    planet = int(request.form.get("planetid"))
    moon = int(request.form["savemoon"]) # Moon id.
    for planetc in sun.solarobjects: # First find planet in a star and then find the moon for that planet.
        if planetc.id == planet:
            for moonc in planetc.moons:
                if moonc.id == moon:
                    moon = moonc
                    break
    name = request.form.get("moonname")
    lwater = convertbool(request.form.get("moonlwater"))
    life = convertbool(request.form.get("moonlife"))
    mtype = request.form.get("moontype")
    atmo = request.form.get("moonatmo")
    faction1 = request.form.get("moonfaction1")
    faction2 = request.form.get("moonfaction2")
    factions = Faction.factionstolist(faction1, faction2)
    notes = request.form.get("notes")
    Moon.editmoon(moon, name, lwater, life, mtype, atmo, factions, notes)
    return render_template("solar.html", sun=sun, factionlist=FactionList.factionlist)

@app.route("/randmoon", methods=["POST"])
def randmoon():
    sun = int(request.form.get("sunid"))
    if sun == 0:
        sun = StarList.tempstar
    else:
        sun = StarList.findstarfromid(sun)
    planet = int(request.form.get("planetid"))
    moon = int(request.form["moonroll"])
    for planetc in sun.solarobjects:
        if planetc.id == planet:
            planet = planetc
    Planet.replacemoon(planet, moon)
    return render_template("solar.html", sun=sun, factionlist=FactionList.factionlist)


# TODO update names of remaining moons, requires revising name code to store a flag if name is original or compiled.
@app.route("/delmoon", methods=["POST"])
def delmoon():
    sun = int(request.form.get("sunid"))
    if sun == 0:
        sun = StarList.tempstar
    else:
        sun = StarList.findstarfromid(sun)
    planet = int(request.form.get("planetid"))
    moon = int(request.form["moondel"])
    for planetc in sun.solarobjects:
        if planetc.id == planet:
            planet = planetc
    Planet.delmoon(planet, moon) # Just needs to be id
    return render_template("solar.html", sun=sun, factionlist=FactionList.factionlist)

@app.route("/ships", methods=["GET", "POST"])
def ships():
    if request.method=='POST':
        if request.form['rollbtn']:
            return redirect("/ships")
    hulltype = HullType()
    ship = Ship.genshipfrommodel(HullModel(HullTemplate(hulltype.size, hulltype.type, hulltype.category, hulltype.ordenance, hulltype.armor, hulltype.troops, hulltype.priority)))
    ShipList.tempship = ship
    return render_template("ships.html", ship=ship)

@app.route("/saveship", methods=["POST"])
def saveship():
    shipid = int(request.form["savebtn"])
    if shipid == 0:
        ship = ShipList.tempship
    else:
        ship = ShipList.findshipfromid(shipid)
    # Put edits to ship here
    ShipList.saveship(ship)
    return redirect("/ships")

@app.route("/factions", methods=["GET", "POST"])
def factions():
    nationlist = NationNameTable.nationlist
    if request.method == "POST":  
        deleteid = request.form.get("delbtn")
        FactionList.removefaction(int(deleteid))
    return render_template("factions.html", factions=FactionList.factionlist, types=Faction.typelist, nationlist=nationlist, ordenance=Faction.ordenancelevel)

@app.route("/editfaction", methods=["POST"])
def editfaction():
    editid = request.form.get("savebtn")
    name = request.form.get("factionname")
    type = request.form.get("factiontype")
    abbr = request.form.get("abbr")
    faction1 = request.form.get("factionparent1")
    faction2 = request.form.get("factionparent2")
    faction3 = request.form.get("factionparent3")
    parentlist = Faction.factionstolist(faction1, faction2, faction3)
    nameset = request.form.getlist("getnation")
    notes = request.form.get("notes")
    shippre = request.form.get("shippre")
    ordlvl = request.form.get("ordlevel")
    science = convertbool(request.form.get("science"))
    colony = convertbool(request.form.get("colony"))
    mgmt = convertbool(request.form.get("mgmt"))
    ships = convertbool(request.form.get("ships"))
    scope = request.form.get("scope")
    FactionList.editfaction(editid, name, type, abbr, notes, shippre, ordlvl, science, colony, mgmt, ships, scope, nameset, parentlist)
    return redirect("/factions")
            


@app.route("/addfaction", methods=["POST"])
def addfaction():
    name = request.form.get("factionname")
    type = request.form.get("factiontype")
    abbr = request.form.get("abbr")
    faction1 = request.form.get("factionparent1")
    faction2 = request.form.get("factionparent2")
    faction3 = request.form.get("factionparent3")
    parentlist = Faction.factionstolist(faction1, faction2, faction3)
    nameset = request.form.getlist("getnation")
    notes = request.form.get("notes")
    shippre = request.form.get("shippre")
    ordlvl = request.form.get("ordlevel")
    science = convertbool(request.form.get("science"))
    colony = convertbool(request.form.get("colony"))
    mgmt = convertbool(request.form.get("mgmt"))
    ships = convertbool(request.form.get("ships"))
    scope = request.form.get("scope")
    FactionList.addfaction(name, type, abbr, notes, shippre, ordlvl, science, colony, mgmt, ships, scope, nameset, parentlist)
    return redirect("/factions")

@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/export", methods=["POST"])
def export():
    factions = []
    for faction in FactionList.factionlist:
        dict = {
        "name" : faction.name,
        "id" : faction.id,
        "ftype" : faction.type,
        "abbr" : faction.abbr,
        "notes" : faction.notes,
        "shippre" : faction.shippre,
        "ordlvl" : faction.ordlvl,
        "science" : faction.science,
        "colony" : faction.colony,
        "mgmt" : faction.mgmt,
        "ships" : faction.ships,
        "scope" : faction.scope,
        "nameset" : faction.nameset,
        "parentlist" : []
        }
        for parent in faction.parents:
            dict["parentlist"].append(parent.id)
        factions.append(dict)
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
    cats = []
    for cat in CatList.catlist:
        dict = {
            "mutation" : cat.mutation,
            "color1" : cat.color1,
            "color2" : cat.color2,
            "eye1" : cat.eye1,
            "eye2" : cat.eye2,
            "tort" : cat.tort,
            "tabby" : cat.tabby,
            "colorpoint" : cat.colorpoint,
            "whitespot" : cat.whitespot,
            "tipped" : cat.tipped,
            "whitespotpatt" : cat.whitespotpatt,
            "sex" : cat.sex,
            "name" : cat.name,
            "id" : cat.id
        }
        cats.append(dict)
    ships = []
    for ship in ShipList.shiplist:
        dict = {
            "size" : ship.size,
            "hulltype" : ship.hulltype,
            "category" : ship.category,
            "hardpoints" : ship.hardpoints,
            "signature" : ship.signature,
            "crew" : ship.crew,
            "hullen" : ship.hullen,
            "hullval" : ship.hullval,
            "armorval" : ship.armorval,
            "modules" : ship.modules,
            "manufacturer" : ship.manufacturer,
            "shipmodel" : ship.shipmodel,
            #"eqmodules" : ship.eqmodules,
            "availmodules" : ship.availmodules,
            "squads" : ship.squads,
            "thrusters" : ship.thrusters,
            "eqweapons" : ship.eqweapons,
            #"rooms" : ship.rooms,
            "ftl" : ship.ftl,
            "factionid" : ship.factionid,
            "name" : ship.name,
            "crewsize" : ship.crewsize,
            "prefix" : ship.prefix,
            "id" : ship.id
        }
        crewdict = {}
        for job, crew in ship.crewlist.items():
            crewdict[job] = crew.id
        dict["crewdict"] = crewdict
        if ship.cat != "None":
            dict["cat"] = ship.cat.id
        else:
            dict["cat"] = ship.cat
        modulelist = []
        for module in ship.eqmodules.modulelist:
            moduledict = {
                "type" : module.type,
                "lvl" : module.lvl,
                "quantity" : module.quantity
            }
            modulelist.append(moduledict)
        dict["eqmodules"] = modulelist
        roomlist = []
        for room in ship.rooms.shiproomlist:
            roomdict = {
                "type" : room.type,
                "lvl" : room.lvl,
                "size" : room.size,
                "quantity" : room.quantity
            }
            roomlist.append(roomdict)
        dict["rooms"] = roomlist
        ships.append(dict)
    stars = []
    for star in StarList.starlist:
        dict = {
            "name" : star.name,
            "starclass" : star.starclass,
            "spectype" : star.spectype,
            "color" : star.color,
            "mass" : star.mass,
            "radius" : star.radius,
            "lum" : star.lum,
            "startemp" : star.startemp,
            "notes" : star.notes,
            "pcount" : star.pcount,
            "inzone" : star.inzone,
            "outzone" : star.outzone,
            "id" : star.id,
            "spacing" : star.spacing
            #solarobjects
        }
        planets = []
        for planet in star.solarobjects:
            planetdict = {
            "distance" : planet.distance,
            "gzone" : planet.gzone,
            "basetemp" : planet.basetemp,
            "terrestrial" : planet.terrestrial,
            "ptype" : planet.ptype,
            "lwater" : planet.lwater,
            "atmo" : planet.atmo,
            "mass" : planet.mass,
            "radius" : planet.radius,
            "rings" : planet.rings,
            "mooncandidate" : planet.mooncandidate,
            "mooncount" : planet.mooncount,
            "gravity" : planet.gravity,
            "relativeg" : planet.relativeg,
            "notes" : planet.notes,
            "life" : planet.life,
            "populated" : planet.populated,
            "pname" : planet.pname,
            "surveyed" : planet.surveyed,
            "pressure" : planet.pressure,
            "settlements" : planet.settlements,
            "id" : planet.id
            }
            pfactions = []
            for faction in planet.factions:
                pfactions.append(faction.id)
            planetdict["factions"] = pfactions
            moonlist = []
            for moon in planet.moons:
                moondict = {
                    "pname" : moon.pname,
                    "gzone" : moon.gzone,
                    "id" : moon.id,
                    "name" : moon.name,
                    "mtype" : moon.mtype,
                    "lwater" : moon.lwater,
                    "atmo" : moon.atmo,
                    "life" : moon.life,
                    "populated" : moon.populated,
                    "systemobjects" : moon.systemobjects,
                    "surveyed" : moon.surveyed,
                    "pressure" : moon.pressure
                }
                mfactions = []
                for faction in moon.factions:
                    mfactions.append(faction.id)
                moondict["factions"] = mfactions
                moonlist.append(moondict)
            planetdict["moons"] = moonlist
            planets.append(planetdict)
        dict["solarobjects"] = planets
        stars.append(dict)

    exportlist = {
        "factions": factions,
        "npcs" : npcs,
        "cats" : cats,
        "ships" : ships,
        "stars" : stars
    }

    json_data = json.dumps(exportlist, indent=6)
    return_data = io.BytesIO()
    return_data.write(json_data.encode('utf-8'))
    return_data.seek(0)

    # Generate a filename with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file_name = f"saveapollodata_{timestamp}.json"
    response = send_file(return_data, as_attachment=True, mimetype='application/json', download_name=json_file_name)
    response.headers['X-Filename'] = json_file_name
    # Send the file as an attachment with the correct MIME type
    return response

@app.route("/import", methods=["POST"])
def import_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.json'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        loadjson(data)
        os.remove(file_path)
        return redirect("/saved")
    return jsonify({"error": "Invalid file format"}), 400


def loadjson(data):
    factions = data.get("factions")
    npcs = data.get("npcs")
    cats = data.get("cats")
    ships = data.get("ships")
    stars = data.get("stars")
    FactionList.unpackfactionsfromload(factions)
    Npc.unpacknpcsfromload(npcs)
    Cat.unpackcatsfromload(cats)
    Ship.unpackshipsfromload(ships)
    Star.unpackstarfromload(stars)

#FactionList.editfaction(1, "United Americas", "gov", "UA", "", "USCSS", "security", True, True, True, True, "pervasive", [], [FactionList.getclassfromid(4)])
#hulltype = HullType()
#ship = Ship(HullModel(HullTemplate(hulltype.size, hulltype.type, hulltype.category, hulltype.ordenance, hulltype.armor, hulltype.troops, hulltype.priority)))
#ShipList.saveship(ship)
'''star = Star()
while len(star.solarobjects) < 3:
    star = Star()
for planet in star.solarobjects:
    if planet.mooncount > 1:
        mooncount = planet.mooncount - 1
    else:
        mooncount = 0
    Planet.editplanet(planet, planet.pname, planet.distance, planet.ptype, planet.atmo, planet.mass, planet.radius, planet.basetemp, planet.pressure, mooncount, planet.factions, planet.lwater, planet.rings, planet.life, planet.notes, planet.surveyed, star)
'''
