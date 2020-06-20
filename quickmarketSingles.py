import json
import psycopg2
from displayGemList import generate_recipe
import pandas as pd
import matplotlib.pyplot as plt
from super_secret_stuff import conn

#set pg2/postgres connection info and define URLs
#conn = psycopg2.connect(host="localhost",user="redacted",password="redacted", dbname="testone")
c = conn.cursor()
recipies = generate_recipe()
prices={}
try:
	c.execute("SELECT ingredient_type,price FROM ingr WHERE time_stamp = (SELECT MAX(time_stamp) FROM ingr) ORDER BY ingredient_type ASC, price ASC")
	currentlistings = c.fetchall()
	df = pd.DataFrame(currentlistings, columns=['ingredient_type','price'])
	for gemrecipe in recipies:
		cost=0
		for ingr_item in recipies[gemrecipe]:
			cost=cost+(df.loc[df['ingredient_type']==ingr_item,['price']].iloc[0])*10
		prices[gemrecipe]= list(cost.values)
	pricedf = pd.DataFrame(prices)
	kays = prices.keys()
	valiums = prices.values()
	plt.plot(valiums, kays)
	plt.savefig("temp.png")	
	plt.show()
	


except psycopg2.DatabaseError as e:
	print("error: ",e)

