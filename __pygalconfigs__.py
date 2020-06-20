import pygal
from pygal.style import NeonStyle
from pygal.style import DarkStyle
from pygal import Config

def PygalConfigFile():
	config = Config()
	config.human_readable=True
	config.height=250
	config.width=700
	config.style=NeonStyle
	config.show_minor_y_labels=True
	config.x_label_rotation=25
	config.value_font_size=8
	config.title_font_size=8
	config.legend_font_size = 8
	config.legend_box_size=12
	config.label_font_size=6
	
	return(config)
	
def PygalConfigFileBlue():
	configB = Config()
	configB.human_readable=True
	configB.height=250
	configB.width=700
	configB.style=NeonStyle
	configB.show_minor_y_labels=True
	configB.x_label_rotation=25
	configB.value_font_size=8
	configB.title_font_size=8
	configB.legend_font_size = 8
	configB.legend_box_size=12
	configB.label_font_size=6
	configB.colors=['#000099','#009999']
	
	return(configB)
