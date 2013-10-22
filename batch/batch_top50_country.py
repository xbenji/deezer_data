#!/usr/bin/env python

from deezutils import *

from datetime import date
from pymongo import MongoClient

CHART_LIMIT = 50
CHART_NB_DAYS = 10
CHART_DATE = date(2013, 8, 10)
#CHART_DATE = date.today()

MONGO_HOST = 'localhost'
MONGO_PORT = 27017

if __name__ == "__main__":
	
	# get path of files to process
	log_files = get_log_paths(CHART_DATE, CHART_NB_DAYS);
	#log_files = ['sample_20130723.log']

	# aggregate distinct songs play by country
	charts = {}
	print "Processing log files"
	for log_file in log_files:
		print "- %s" % log_file
		aggregate(charts, log_file, key_idx=2, value_idx=0)
	
	#store_to_file(charts, "top_50_country", CHART_LIMIT)
	
	# store results in db 
	print "Saving charts to database"
	client = MongoClient(MONGO_HOST, MONGO_PORT);
	db = client.deezer_charts
	store_to_mongodb(charts, db.country_charts, CHART_LIMIT)
