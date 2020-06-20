import pygal
from pygal.style import NeonStyle
from pygal.style import DarkStyle
from pygal import Config
from __pygalconfigs__ import PygalConfigFile
import psycopg2
from datetime import datetime

config = PygalConfigFile()


def GenerateTopTenLists():
	conn = psycopg2.connect(host="localhost",user="antopher",password="4S&7Ya", dbname="NOTAmembers")
	c=conn.cursor()
	c.execute("SELECT username,combatlevel FROM members WHERE datestamp = CAST(CURRENT_DATE as varchar(10)) ORDER BY combatlevel DESC limit 10")

	combatfive = c.fetchall()
	combatname=[]
	combatlevel=[]
	combat_chart = pygal.Bar(config)
	for i in combatfive:
		combatname.append(i[0])
		combatlevel.append(i[1])
	
	combat_chart.x_labels=combatname
	combat_chart.add("Level",combatlevel)
	combat = combat_chart.render_data_uri()
	
	c.execute("SELECT username,fishing FROM members WHERE datestamp = CAST(CURRENT_DATE as varchar(10)) ORDER BY fishing DESC limit 10")
	fishingfive = c.fetchall()
	fishname=[]
	fishlevel=[]
	fish_chart = pygal.Bar(config)
	for i in fishingfive:
		fishname.append(i[0])
		fishlevel.append(i[1])
	fish_chart.x_labels=fishname
	fish_chart.add("Fishing",fishlevel)
	fish = fish_chart.render_data_uri()
	
	c.execute("SELECT username,woodcutting FROM members WHERE datestamp = CAST(CURRENT_DATE as varchar(10)) ORDER BY woodcutting DESC limit 10")
	woodfive = c.fetchall()
	woodname=[]
	woodlevel=[]
	wood_chart = pygal.Bar(config)
	for i in woodfive:
		woodname.append(i[0])
		woodlevel.append(i[1])
	wood_chart.x_labels=woodname
	wood_chart.add("Woodcutting",woodlevel)
	wood = wood_chart.render_data_uri()
	
	c.execute("SELECT username,mining FROM members WHERE datestamp = CAST(CURRENT_DATE as varchar(10)) ORDER BY mining DESC limit 10")
	minefive = c.fetchall()
	minename=[]
	minelevel=[]
	mine_chart = pygal.Bar(config)
	for i in minefive:
		minename.append(i[0])
		minelevel.append(i[1])
	mine_chart.x_labels=minename
	mine_chart.add("Mining",minelevel)
	mine = mine_chart.render_data_uri()
	
	c.execute("SELECT username,stonecutting FROM members WHERE datestamp = CAST(CURRENT_DATE as varchar(10)) ORDER BY stonecutting DESC limit 10")
	stonefive = c.fetchall()
	stonename=[]
	stonelevel=[]
	stone_chart = pygal.Bar(config)
	for i in stonefive:
		stonename.append(i[0])
		stonelevel.append(i[1])
	stone_chart.x_labels=stonename
	stone_chart.add("Stonecutting",stonelevel)
	stone = stone_chart.render_data_uri()
	
	c.execute("SELECT username,carving FROM members WHERE datestamp = CAST(CURRENT_DATE as varchar(10)) ORDER BY carving DESC limit 10")
	carvefive = c.fetchall()
	carvename=[]
	carvelevel=[]
	carve_chart = pygal.Bar(config)
	for i in carvefive:
		carvename.append(i[0])
		carvelevel.append(i[1])
	carve_chart.x_labels=carvename
	carve_chart.add("Carving",carvelevel)
	carve = carve_chart.render_data_uri()
	
	c.execute("SELECT username,crafting FROM members WHERE datestamp = CAST(CURRENT_DATE as varchar(10)) ORDER BY crafting DESC limit 10")
	craftfive = c.fetchall()
	craftname=[]
	craftlevel=[]
	craft_chart = pygal.Bar(config)
	for i in craftfive:
		craftname.append(i[0])
		craftlevel.append(i[1])
	craft_chart.x_labels=craftname
	craft_chart.add("Crafting",craftlevel)
	craft = craft_chart.render_data_uri()
	
	return(combat, fish, wood, mine, stone, carve, craft)
