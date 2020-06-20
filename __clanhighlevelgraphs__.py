import pygal
from pygal.style import NeonStyle
from pygal.style import DarkStyle
from pygal import Config
from __pygalconfigs__ import PygalConfigFile, PygalConfigFileBlue

config = PygalConfigFile()
configB = PygalConfigFileBlue()



def ParseClanAndRenderData(clandata):
#parse data from the DB query into usable form.	
	xlabels=[]
	xpvalues=[]
	dailyxp=[]
	goldvalues=[]
	cryvalues=[]
	platvalues=[]
	foodvalue=[]
	woodvalue=[]
	ironvalue=[]
	stonevalue=[]
	for i in clandata:
		xlabels.append(i[0])
		xpvalues.append(i[1]/1000000)
		goldvalues.append(i[4]/1000000000)
		cryvalues.append(i[2])
		platvalues.append(i[3])
		foodvalue.append(i[5])
		woodvalue.append(i[6])
		ironvalue.append(i[7])
		stonevalue.append(i[8])
	
	for i in range(1,len(xpvalues)):
		if xpvalues[i-1]-xpvalues[i] > 0:
			dailyxp.append((xpvalues[i-1]-xpvalues[i]))
		else:
			dailyxp.append(0)
			
		
#Clan XP Chart
	xp_line_chart = pygal.Line(config)
	xp_line_chart.title = 'Experience (In Millions)'
	xp_line_chart.add('Experience',tuple(reversed(xpvalues)))
	xp_line_chart.x_labels=tuple(reversed(xlabels))
	xpchart = xp_line_chart.render_data_uri()
	
	dailyxp_chart = pygal.Line(configB)
	dailyxp_chart.title = "Daily XP Gains (In Millions)"
	dailyxp_chart.add('Experience', tuple(reversed(dailyxp)))
	dailyxp_chart.x_labels=tuple(reversed(xlabels))
	dailyxpchart = dailyxp_chart.render_data_uri()
		
		
#3 Clan curriencies Charts
	gold_chart = pygal.Bar(config)
	gold_chart.title = 'GOLD (in Billions)'
	gold_chart.add('Gold', tuple(reversed(goldvalues)))
	gold_chart.x_labels=tuple(reversed(xlabels))
	goldchart = gold_chart.render_data_uri()

	cry_chart = pygal.Bar(config)
	cry_chart.title = 'Crystals'
	cry_chart.x_labels=tuple(reversed(xlabels))
	cry_chart.add('Crystals',tuple(reversed(cryvalues)))
	crychart = cry_chart.render_data_uri()
		
	plat_chart = pygal.Bar(config)
	plat_chart.title = 'Platinum'
	plat_chart.add('Platinums',tuple(reversed(platvalues)))
	plat_chart.x_labels=tuple(reversed(xlabels))
	platchart = plat_chart.render_data_uri()
	
#Clan Resource Chart	
	line_chart = pygal.Line(config)
	line_chart.title = 'Clan Resources'
	line_chart.x_labels = tuple(reversed(xlabels))
	line_chart.add('Food', tuple(reversed(foodvalue)))
	line_chart.add('Wood', tuple(reversed(woodvalue)))
	line_chart.add('Iron', tuple(reversed(ironvalue)))
	line_chart.add('Stone', tuple(reversed(stonevalue)))
	chart = line_chart.render_data_uri()
	
	return( chart, xpchart, dailyxpchart, goldchart, crychart, platchart)
	
