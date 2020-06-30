from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
import pygal
from pygal.style import NeonStyle
from pygal.style import DarkStyle
from pygal import Config
import json
import psycopg2
from datetime import datetime, timedelta, date
from displayGemList import generate_recipe
import pandas as pd
import matplotlib.pyplot as plt
import gc
import os
from __clanhighlevelgraphs__ import ParseClanAndRenderData
from __pygalconfigs__ import PygalConfigFile, PygalConfigFileBlue
from __MemberTopTens__ import GenerateTopTenLists
#db connaction info
from super_secret_stuff import conn, notaconn,activesconn

config = PygalConfigFile()
configB = PygalConfigFileBlue()

app = Flask(__name__)
app.secret_key = os.urandom(32)


#set pg2/postgres connection info and define URLs
#conn = psycopg2.connect(host="localhost",user=",password="redacted", dbname="testone")
#notaconn = psycopg2.connect(host="localhost",user="redacted",password="redacted", dbname="NOTAmembers")
#activesconn = psycopg2.connect(host="localhost",user="redacted",password="redacted", dbname="actives")
c = conn.cursor()
nc = notaconn.cursor()
ac = activesconn.cursor()

##prepare lists for the different equipment types and their limitations
List_of_all_gems=['Strength','Health', 'Coordination','Agility','Retaliation','Restoration','Dueling','Sniping','Sorcery','Brawling','Elusion','Normalizing','Hunting','Taming','Destruction','Slaying',
		'Weathering','Murdering','Solidifying','Weedwhacking','Charm','Exterminating','Swiftness','Potency','Recklessness','Resilience','Retribution','Recovery','Smithing','Etching','Harvesting','Wisdom',
		'Greed','Luck','Mastery','Endurance','Celerity','Piercing','Chronokinesis']

List_of_boot_gems=['Strength','Health', 'Coordination','Agility','Retaliation','Restoration','Dueling','Sniping','Sorcery','Brawling','Elusion','Normalizing','Hunting','Taming','Destruction','Slaying',
		'Weathering','Murdering','Solidifying','Weedwhacking','Charm','Exterminating','Swiftness','Potency','Recklessness','Resilience','Retribution','Recovery','Smithing','Etching','Harvesting',
		'Celerity','Chronokinesis']

List_of_glove_gems=['Strength','Health', 'Coordination','Agility','Retaliation','Restoration','Dueling','Sniping','Sorcery','Brawling','Elusion','Normalizing','Hunting','Taming','Destruction','Slaying',
		'Weathering','Murdering','Solidifying','Weedwhacking','Charm','Exterminating','Swiftness','Potency','Recklessness','Resilience','Retribution','Recovery','Smithing','Etching','Harvesting',
		'Luck']

List_of_breastplate_gems=['Strength','Health', 'Coordination','Agility','Retaliation','Restoration','Dueling','Sniping','Sorcery','Brawling','Elusion','Normalizing','Hunting','Taming','Destruction','Slaying',
		'Weathering','Murdering','Solidifying','Weedwhacking','Charm','Exterminating','Swiftness','Potency','Recklessness','Resilience','Retribution','Recovery','Smithing','Etching','Harvesting',
		'Mastery','Endurance']

List_of_helmet_gems=['Strength','Health', 'Coordination','Agility','Retaliation','Restoration','Dueling','Sniping','Sorcery','Brawling','Elusion','Normalizing','Hunting','Taming','Destruction','Slaying',
		'Weathering','Murdering','Solidifying','Weedwhacking','Charm','Exterminating','Swiftness','Potency','Recklessness','Resilience','Retribution','Recovery','Smithing','Etching','Harvesting','Wisdom']

List_of_weapon_gems=['Strength','Health', 'Coordination','Agility','Retaliation','Restoration','Dueling','Sniping','Sorcery','Brawling','Elusion','Normalizing','Hunting','Taming','Destruction','Slaying',
		'Weathering','Murdering','Solidifying','Weedwhacking','Charm','Exterminating','Swiftness','Potency','Recklessness','Resilience','Retribution','Recovery','Smithing','Etching','Harvesting',
		'Greed','Piercing']

List_of_offhand_gems=['Strength','Health', 'Coordination','Agility','Retaliation','Restoration','Dueling','Sniping','Sorcery','Brawling','Elusion','Normalizing','Hunting','Taming','Destruction','Slaying',
		'Weathering','Murdering','Solidifying','Weedwhacking','Charm','Exterminating','Swiftness','Potency','Recklessness','Resilience','Retribution','Recovery','Smithing','Etching','Harvesting']


##start assigning routes
@app.route('/gems/',)
def showgembasicss():
	recipies = generate_recipe()
	try:
		return render_template('Gem_costs.html', recipies=recipies)
	except psycopg2.DatabaseError as e:
		print("error: ",e)

@app.route('/market/')
def showmarketfunction():
	try:
		c.execute("SELECT * FROM ingr WHERE time_stamp = (SELECT MAX(time_stamp) FROM ingr) ORDER BY time_stamp DESC, ingredient_type ASC, price ASC")
		currentlistings = c.fetchall()
		return render_template('ingredient_market_table.html', currentlistings=currentlistings)
	except psycopg2.DatabaseError as e:
		print("error: ",e)

@app.route('/orders/', methods=["GET","POST"])
def function_ordersGenerator():
	TotalBank = 0
	recipies = generate_recipe()
	ingr_dict = {}
	if request.method == "POST":
		PrimaryBoots = request.form.get("bootsprimgem")
		SecondaryBoots = request.form.get("bootssecgem")
		PrimaryHelmet = request.form.get("helmetprimgem")
		SecondaryHelmet = request.form.get("helmetsecgem")
		PrimaryBreast = request.form.get("boobsprimgem")
		SecondaryBreast = request.form.get("boobssecgem")
		PrimaryGloves = request.form.get("glovesprimgem")
		SecondaryGloves = request.form.get("glovessecgem")
		PrimaryOffhand = request.form.get("shieldprimgem")
		SecondaryOffhand = request.form.get("shieldsecgem")
		PrimaryWeapon = request.form.get("weps_primgem")
		SecondaryWeapon = request.form.get("weps_secgem")

		NeededGems60 = (PrimaryWeapon,SecondaryWeapon,PrimaryBoots,SecondaryBoots,PrimaryHelmet,SecondaryHelmet,PrimaryBreast,SecondaryBreast,PrimaryGloves,SecondaryGloves,PrimaryOffhand,SecondaryOffhand,)
		TierIngr =(int(request.form.get("select_tier")))
		session['boots_primary'] = PrimaryBoots
		session['boots_secondary'] = SecondaryBoots
		session['helmet_primary'] = PrimaryHelmet
		session['helmet_secondary'] = SecondaryHelmet
		session['breastplate_primary'] = PrimaryBreast
		session['breastplate_secondary'] = SecondaryBreast
		session['gloves_primary'] = PrimaryGloves
		session['gloves_secondary'] = SecondaryGloves
		session['offhand_primary'] = PrimaryOffhand
		session['offhand_secondary'] = SecondaryOffhand
		session['weapon_primary'] = PrimaryWeapon
		session['weapon_secondary'] = SecondaryWeapon

		TieredIngr=(TierIngr//3)+1

		for this_gem in NeededGems60:
			if this_gem == "none":
				pass
			else:
				for this_ingr in recipies[this_gem]:
					if this_ingr not in ingr_dict:
						ingr_dict[this_ingr]=(5*TieredIngr)
					else:
						ingr_dict[this_ingr]=(ingr_dict[this_ingr]+(5*TieredIngr))
		'''InvIngString = request.form.get("inventoryingrs")
		InvIngString = InvIngString.split('[Market] [Send]')
		get_rid_of_turkeys = []
		for line in InvIngString:
			if line[0:8] == " Turkey ":
				line = line[23:]
			if line[0:1] == " ":
				line = line[1:]
			get_rid_of_turkeys.append(line)
		list_of_list = []
		for line in get_rid_of_turkeys:
			zline = line.split('\t')
			list_of_list.append(zline)
		zz = pd.DataFrame(list_of_list, columns=['ingr','stock','price','blank'])
		zz = zz[['ingr','stock','price']]
		df = zz.set_index('ingr')
		df = df.replace(',', "", regex=True)
		df= df.drop(df.tail(1).index)
		df = df.drop(df[df['price'] == 'N/A'].index)
		df['stock'] = df['stock'].astype(int)
		df['price'] = df['price'].astype(int)
		df['total_bank'] =df['stock'] * df['price']
		TotalBank = df['total_bank'].sum()
		'''
		return render_template('order_configuration.html', List_of_all_gems=List_of_all_gems, ingr_dict=ingr_dict,List_of_boot_gems=List_of_boot_gems,List_of_offhand_gems=List_of_offhand_gems,List_of_weapon_gems=List_of_weapon_gems,List_of_helmet_gems=List_of_helmet_gems,List_of_breastplate_gems=List_of_breastplate_gems,List_of_glove_gems=List_of_glove_gems, TotalBank=TotalBank)
	try:
		return render_template('order_configuration.html', List_of_all_gems=List_of_all_gems, ingr_dict=ingr_dict,List_of_boot_gems=List_of_boot_gems,List_of_offhand_gems=List_of_offhand_gems,List_of_weapon_gems=List_of_weapon_gems,List_of_helmet_gems=List_of_helmet_gems,List_of_breastplate_gems=List_of_breastplate_gems,List_of_glove_gems=List_of_glove_gems, TotalBank=TotalBank)
	except psycopg2.DatabaseError as e:
		print("error: ",e)

@app.route('/orderstesting/', methods=["GET","POST"])
#was testing copy&paste of ingredient inventory
def function_ordersGenerator2():
	TotalBank = 0
	recipies = generate_recipe()
	ingr_dict = {}
	if request.method == "POST":
		if request.form['btn'] == 'gemsbutton':
			PrimaryBoots = request.form.get("bootsprimgem")
			SecondaryBoots = request.form.get("bootssecgem")
			PrimaryHelmet = request.form.get("helmetprimgem")
			SecondaryHelmet = request.form.get("helmetsecgem")
			PrimaryBreast = request.form.get("boobsprimgem")
			SecondaryBreast = request.form.get("boobssecgem")
			PrimaryGloves = request.form.get("glovesprimgem")
			SecondaryGloves = request.form.get("glovessecgem")
			PrimaryOffhand = request.form.get("shieldprimgem")
			SecondaryOffhand = request.form.get("shieldsecgem")
			PrimaryWeapon = request.form.get("weps_primgem")
			SecondaryWeapon = request.form.get("weps_secgem")
			'''try:
				InvIngString = request.form.get("inventoryingrs")
			except:
				InvIngString = False'''

			NeededGems60 = (PrimaryWeapon,SecondaryWeapon,PrimaryBoots,SecondaryBoots,PrimaryHelmet,SecondaryHelmet,PrimaryBreast,SecondaryBreast,PrimaryGloves,SecondaryGloves,PrimaryOffhand,SecondaryOffhand,)
			TierIngr =(int(request.form.get("select_tier")))
			TieredIngr=(TierIngr//3)+1

			for this_gem in NeededGems60:
				if this_gem == "none":
					pass
				else:
					for this_ingr in recipies[this_gem]:
						if this_ingr not in ingr_dict:
							ingr_dict[this_ingr]=(5*TieredIngr)
						else:
							ingr_dict[this_ingr]=(ingr_dict[this_ingr]+(5*TieredIngr))
		'''elif request.form['btn'] == 'inventorybutton':

			InvIngString = InvIngString.split('[Market] [Send]')
			get_rid_of_turkeys = []
			for line in InvIngString:
				if line[0:8] == " Turkey ":
					line = line[23:]
				if line[0:1] == " ":
					line = line[1:]
				get_rid_of_turkeys.append(line)
			list_of_list = []
			for line in get_rid_of_turkeys:
				zline = line.split('\t')
				list_of_list.append(zline)
			zz = pd.DataFrame(list_of_list, columns=['ingr','stock','price','blank'])
			zz = zz[['ingr','stock','price']]
			df = zz.set_index('ingr')
			df = df.replace(',', "", regex=True)
			df= df.drop(df.tail(1).index)
			df = df.drop(df[df['price'] == 'N/A'].index)
			df['stock'] = df['stock'].astype(int)
			df['price'] = df['price'].astype(int)
			df['total_bank'] =df['stock'] * df['price']
			TotalBank = df['total_bank'].sum()
			'''

		return render_template('order_configuration_test.html', List_of_all_gems=List_of_all_gems, ingr_dict=ingr_dict,List_of_boot_gems=List_of_boot_gems,List_of_offhand_gems=List_of_offhand_gems,List_of_weapon_gems=List_of_weapon_gems,List_of_helmet_gems=List_of_helmet_gems,List_of_breastplate_gems=List_of_breastplate_gems,List_of_glove_gems=List_of_glove_gems, TotalBank=TotalBank)
	try:
		return render_template('order_configuration_test.html', List_of_all_gems=List_of_all_gems, ingr_dict=ingr_dict,List_of_boot_gems=List_of_boot_gems,List_of_offhand_gems=List_of_offhand_gems,List_of_weapon_gems=List_of_weapon_gems,List_of_helmet_gems=List_of_helmet_gems,List_of_breastplate_gems=List_of_breastplate_gems,List_of_glove_gems=List_of_glove_gems, TotalBank=TotalBank)
	except psycopg2.DatabaseError as e:
		print("error: ",e)


@app.route('/updateGemOrder',methods=['POST'])
def update_order():
	ingr_dict = {}
	# PrimaryBoots = request.form.get("bootsprimgem")
	# SecondaryBoots = request.form.get("bootssecgem")
	# PrimaryHelmet = request.form.get("helmetprimgem")
	# SecondaryHelmet = request.form.get("helmetsecgem")
	# PrimaryBreast = request.form.get("boobsprimgem")
	# SecondaryBreast = request.form.get("boobssecgem")
	# PrimaryGloves = request.form.get("glovesprimgem")
	# SecondaryGloves = request.form.get("glovessecgem")
	# PrimaryOffhand = request.form.get("shieldprimgem")
	# SecondaryOffhand = request.form.get("shieldsecgem")
	# PrimaryWeapon = request.form.get("weps_primgem")
	# SecondaryWeapon = request.form.get("weps_secgem")
	#TierIngr =(int(request.form.get("select_tier")))
	NeededGems60 = (PrimaryBoots, SecondaryBoots)
	#NeededGems60 = (PrimaryWeapon,SecondaryWeapon,PrimaryBoots,SecondaryBoots,PrimaryHelmet,SecondaryHelmet,PrimaryBreast,SecondaryBreast,PrimaryGloves,SecondaryGloves,PrimaryOffhand,SecondaryOffhand,)
	TieredIngr=(TierIngr//3)+1
	#some_html = "<thead><tr><th> &nbsp;&nbsp; </th><th style='min-width:230px;'>click here to sort</th></tr></thead><tbody>"

	for this_gem in NeededGems60:
		if this_gem == "none":
			continue
		else:
			for this_ingr in recipies[this_gem]:
				if this_ingr not in ingr_dict:
					ingr_dict[this_ingr]=(5*TieredIngr)
				else:
					ingr_dict[this_ingr]=(ingr_dict[this_ingr]+(5*TieredIngr))

	#for thing in ingr_dict:
	#	some_html = some_html+"<tr><td>"+ingr_dict[thing]+"</td><td>"+thing+"</td></tr>"
	#some_html = some_html+"<tr><td>7</td><td>Monkeys</td></tr>"
	#some_html = some_html+"</tbody>"
	return ("success")


@app.route('/cheapestgems/')
#used for determining cheapest gem to make based on current market prices (not used since introduction of Training Gems)
def make_list_of_cheap_gems():
	prices={}
	try:
		recipies = generate_recipe()
		c.execute("SELECT ingredient_type,price FROM ingr WHERE time_stamp = (SELECT MAX(time_stamp) FROM ingr) ORDER BY ingredient_type ASC, price ASC")
		currentlistings = c.fetchall()
		df = pd.DataFrame(currentlistings, columns=['ingredient_type','price'])

		for gemrecipe in recipies:
			cost=0
			for ingr_item in recipies[gemrecipe]:
				cost=cost+(df.loc[df['ingredient_type']==ingr_item,['price']].iloc[0])*21
			prices[gemrecipe]= list(cost)
		pricedf = pd.DataFrame(prices)
		prices_df = pricedf.transpose()
		prices_df.columns = ['price']
		target_name = prices_df.idxmin().item()
		target_price = prices_df.min().item()

		# valiums = prices.values()
		# targetprice = min(valiums)
		# targetgem = min(prices.items(), key=lambda x: x[1])
		#targetgem = prices.keys
		return render_template('cheapgems.html', target_name = target_name, target_price = target_price)
		#return render_template('cheapgems.html')

	except psycopg2.DatabaseError as e:
		print("error: ",e)

#############################################################################
# # # #  NOTA CLAN TRACKING # # # #
#############################################################################
@app.route('/test/')
def test():
	return ("Hello Princess")

@app.route('/nota/')
def clanstats():
	nc.execute("SELECT * FROM clan ORDER BY datestamp DESC LIMIT 14")
	clandata=nc.fetchall()

	#charts for front page's 3 pills.  Python logic done in __clanhighlevelgraphs__ to reduce __init__ clutter.
	chart, xpchart, dailyxpchart, goldchart, crychart, platchart = ParseClanAndRenderData(clandata)

	return render_template('tracker/Index.html', chart = chart, xpchart=xpchart, dailyxpchart = dailyxpchart, goldchart = goldchart, crychart=crychart, platchart=platchart)

@app.route('/memberlevels/')
def clanmemeberlevels():
	# datestamp, username, combatlevel, fishing, woodcutting,mining,stonecutting,crafting,carving

	nc.execute("SELECT datestamp, username, carving FROM members ORDER BY datestamp DESC")
	leveldata=c.fetchall()
	datelabel=[]
	membername=[]
	chartingnames={}
	subdata = {}

	for i in leveldata:
		if i[1] not in membername:
			membername.append(i[1])
		if i[0] not in datelabel:
			datelabel.append(i[0])

	for h,i,j in leveldata:
		if i not in subdata:
			subdata.update({i:{}})
		if h not in subdata[i]:
			subdata[i].update({h:{}})
		subdata[i][h].update({'Carving Level':j})

	for name in membername:
		levels=[]
		variablename = pygal.Bar(config)
		variablename.x_labels=datelabel

		for date_ in subdata[name]:
			levels.append(subdata[name][date_]['Carving Level'])
		variablename.add('Carving Level',tuple(levels))
		tommy=variablename.render_data_uri()
		chartingnames.update({name:tommy})
	return render_template('tracker/memberlevels.html',  membername=membername, chartingnames=chartingnames)


@app.route('/memberactions/')
def clanmemeberactions():
	todaysdatadate = datetime.utcnow().date()
	previous1week =todaysdatadate - timedelta(7)
	previous2week = todaysdatadate - timedelta(14)
	previous3week = todaysdatadate - timedelta(21)
	previous4week = todaysdatadate - timedelta(28)
	todaysdatadate = str(todaysdatadate)
	previous1week = str(previous1week)
	previous2week = str(previous2week)
	previous3week = str(previous3week)
	previous4week = str(previous4week)
	nc.execute("SELECT datestamp, username, stats, kills, deaths, harvests, craftingacts, carvingacts, quests FROM members WHERE datestamp = %s or datestamp =%s or datestamp =%s or datestamp =%s or datestamp =%s ORDER BY datestamp ASC",[todaysdatadate,previous1week,previous2week,previous3week,previous4week])
	leveldata=c.fetchall()
	datelabel=[]
	membername=[]
	chartingnames={}
	subdata = {}

	for identifiers in leveldata:
		if identifiers[1] not in membername:
			membername.append(identifiers[1])
		if identifiers[0] not in datelabel:
			datelabel.append(identifiers[0])

	for h,i,j,k,l,m,n,o,p in leveldata:
		if i not in subdata:
			subdata.update({i:{}})
		if h not in subdata[i]:
			subdata[i].update({h:{}})
		subdata[i][h].update({'stats':j})
		subdata[i][h].update({'kills':k})
		subdata[i][h].update({'deaths':l})
		subdata[i][h].update({'harvests':m})
		subdata[i][h].update({'craftingacts':n})
		subdata[i][h].update({'carvingacts':o})
		subdata[i][h].update({'quests':p})

	for name in membername:
		statsnumbers=[]
		killsnumbers=[]
		deathsnumbers=[]
		harvestsnumbers=[]
		craftingactsnumbers=[]
		carvinnumbers=[]
		questsnumbers=[]

		variablename = pygal.Line(config)
		variablename.x_labels=datelabel

		for date_ in subdata[name]:
			statsnumbers.append(subdata[name][date_]['stats'])
			killsnumbers.append(subdata[name][date_]['kills'])
			deathsnumbers.append(subdata[name][date_]['deaths'])
			harvestsnumbers.append(subdata[name][date_]['harvests'])
			craftingactsnumbers.append(subdata[name][date_]['craftingacts'])
			carvinnumbers.append(subdata[name][date_]['carvingacts'])
			questsnumbers.append(subdata[name][date_]['quests'])

		variablename.add('stats',tuple(statsnumbers))
		variablename.add('kills',tuple(killsnumbers))
		variablename.add('deaths',tuple(deathsnumbers))
		variablename.add('harvests',tuple(harvestsnumbers))
		variablename.add('craftingacts',tuple(craftingactsnumbers))
		variablename.add('carvingacts',tuple(carvinnumbers))
		variablename.add('quests',tuple(questsnumbers))

		renderedchart = variablename.render_data_uri()
		chartingnames.update({name:renderedchart})

	gc.collect()
	return render_template('tracker/memberactions.html',  membername=membername, chartingnames=chartingnames)

@app.route('/memberdonations/')
def clanmemeberdonats():

	return render_template('tracker/memberlevels.html')

@app.route('/kicklist/')
def kicklist():
	return render_template('kick.html')

@app.route('/toptens/')
def todaystop10listsbyaction():
	#all SQL queries and python logic handled in __MemberTopTens__ to reduce __init__ clutter.
	combat, fish, wood, mine, stone, carve, craft = GenerateTopTenLists()

	return render_template('tracker/top10lists.html',  fish=fish, combat=combat, wood=wood, mine=mine, stone=stone, craft=craft, carve=carve)

@app.route('/memberxps/', methods=["GET","POST"])
def zDexxajustwantstextforthis():
#if date fields submitted, use those dates, otherwise (including initial page load) use today and yesterday.
#based on stats acquired at 00:01 UTC, so roughly 20:00 server time.  which means daily actions won't 100% match game's daily totals
	if request.method == "POST":

		startdate = request.form["startdate"]
		enddate = request.form["enddate"]

	else:
		enddate = datetime.utcnow().date()
		startdate =enddate - timedelta(1)

	enddate=str(enddate)
	startdate = str(startdate)

	nc.execute("SELECT datestamp, username, totalxp, kills, totalacts FROM members WHERE datestamp = %s or datestamp = %s ORDER BY datestamp", [startdate,enddate])

	xpdata = nc.fetchall()
	membername=[]
	subdata = {}

	for date_,name,xp, kill,acts in xpdata:
		if name not in membername:
			membername.append(name)
		if name not in subdata:
			subdata.update({name:{}})
		subdata[name].update({date_:(int(xp),int(kill),int(acts))})

	return render_template('tracker/memberxps.html', subdata=subdata, startdate=startdate, enddate=enddate)

@app.route('/tiptouchtuesday/', methods=["GET","POST"])
def recruit():
#if date fields submitted, use those dates, otherwise (including initial page load) use today and yesterday.
#based on stats acquired at 00:01 UTC, so roughly 20:00 server time.  which means daily actions won't 100% match game's daily totals

	if request.method == "POST":

		startdate = request.form["startdate"]
		enddate = request.form["enddate"]

	else:
		enddate = datetime.utcnow().date()
		startdate =enddate - timedelta(1)
	#timedeltachange = enddate - startdate
	#dayschange = timedeltachange.days

	enddate=str(enddate)
	startdate = str(startdate)

	ac.execute("SELECT datestamp, username, totalacts, clanname, totalxp, highmonsterkill FROM members WHERE datestamp = %s or datestamp = %s ORDER BY datestamp DESC", [startdate,enddate])

	activedata = ac.fetchall()

	subdata2 = {}

	for dateP,name,acts,someclan, xp, mob in activedata:

		if name not in subdata2:
			subdata2.update({name:{"clan":someclan, "highmob":mob }})
		subdata2[name].update({dateP:(int(acts), int(xp))})

	return render_template('tracker/activestool.html', subdata2=subdata2, startdate=startdate, enddate=enddate)


@app.route('/carvingdonations/')
#def showZthedonations():
#	return render_template('carvingdonations.html')
def PlatinumDonationsForGemCarving():
	nc.execute("SELECT * FROM platforgems ORDER BY date DESC")
	results = nc.fetchall()

	platAPI = pd.DataFrame(data=results, columns=['Username','Amount','Date'])
	chuckchuck = platAPI.groupby('Username', as_index=False)[['Amount']].sum()
	chuckchuck['Amount'] = chuckchuck.apply(lambda x: "{:,}".format(x['Amount']), axis=1)
	platAPI['Amount'] = platAPI.apply(lambda x: "{:,}".format(x['Amount']), axis=1)
	return render_template('tracker/plats.html', donationtable=platAPI.to_html(classes="table table-sm table-hover table-inverted table-striped table-dark"), chuckchuck=chuckchuck.to_html(classes="table table-sm table-hover table-inverted table-striped table-dark"))

@app.route('/addinfo/', methods=["GET","POST"])
#webpage for adding daily clan stats until API is finished
#manually adding info was abanded, info now well out of date
def addinfo():

	if request.method =="POST":
		adddate = request.form["date"]
		addexp = int(request.form["exp"])
		addgold = int(request.form["gold"])
		addcry = int(request.form["cry"])
		addplat = int(request.form["plat"])
		addfish = int(request.form["fish"])
		addwood = int(request.form["wood"])
		addiron  = int(request.form["iron"])
		addstone = int(request.form["stone"])
		try:
			nc.execute("INSERT INTO clan (datestamp, xp, gold, crystals, platinum, food, wood, iron, stone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (adddate,addexp,addgold,addcry,addplat,addfish,addwood,addiron,addstone))
			successalert = "Successfully added"
			notaconn.commit()


			return render_template('tracker/ClanUpdatePageV2.html', successalert = successalert)
		except Exception as e:
			notaconn.rollback()
			nc.close()
			notaconn.close()
			raise RuntimeError("An error occured while storing fetched data: {}".format(repr(e)))
			return render_template('tracker/ClanUpdatePageV2.html', successalert = repr(e))
	else:
		return render_template('tracker/ClanUpdatePageV2.html')

@app.route('/add_donation/', methods=["GET","POST"])
#webpage for adding platinum donations
def adddonation():

	if request.method =="POST":
		adddate = request.form["date"]
		adduser = request.form["username"]
		addamount = int(request.form["amount"])
		try:
			nc.execute("INSERT INTO platforgems (Username, platinum_amount, date) VALUES (%s,%s,%s)", (adduser,addamount,adddate))
			successalert = "Successfully added"
			notaconn.commit()


			return render_template('tracker/addplatinumdonation.html', successalert = successalert)
		except Exception as e:
			notaconn.rollback()
			nc.close()
			notaconn.close()
			raise RuntimeError("An error occured while storing fetched data: {}".format(repr(e)))
			return render_template('tracker/addplatinumdonation.html', successalert = repr(e))
	else:
		return render_template('tracker/addplatinumdonation.html')



@app.route('/chunchunling')
def chinchungsgems():
	return render_template('chinsOrder.html')

@app.route('/zdexxa')
def dexgems():
	return render_template('zdexxaOrder.html')

@app.route('/backgroundimageforlyrania')
#just an image I'm storing for background of my custom Lyrania theme
def lyrania():
	return render_template('lyrania-image.html')

@app.route('/weeble')
def weeblegems():
	return render_template('weebleOrder.html')

@app.route('/dash/')
#only works when I've started the stand-alone dash app which is not configured to load at boot currently.
def makethedashappviewable():

	return redirect("http://165.227.64.83:8050")


if __name__ == "__main__":
	#app.secret_key = os.urandom(32)
	app.run()
