#!/usr/bin/env python

from deezutils import *

from datetime import date
from pymongo import MongoClient

CHART_LIMIT = 50
CHART_NB_DAYS = 10
CHART_AT_DATE = date(2013, 8, 10)
#CHART_AT_DATE = date.today()

MONGO_HOST = 'localhost'
MONGO_PORT = 27017

if __name__ == "__main__":

	# get path of files to process
	log_files = get_log_paths(CHART_AT_DATE, CHART_NB_DAYS);
	#log_files = ['sample_20130723.log']

	# step1: aggregates song count for each daily file
	print "Processing log files"
	for log_file in log_files:
		print "- %s" % log_file
		tmp_charts = {}
		aggregate(tmp_charts, log_file, key_idx=1, value_idx=0)
		# store daily aggregate in temp file
		store_to_file(tmp_charts, "aggr_%s" % log_file)
	
	# step2: open each sub aggregate file for final aggregate
	charts = {}
	aggr_log_files = [ "aggr_%s" % file for file in log_files]
	print "Processing aggregated log files"
	for log_file in aggr_log_files:
		print "- %s" % log_file
		aggregate(charts, log_file, key_idx=0, value_idx=1, weight_idx=2)
	
	#store_to_file(charts, "top_50_user", CHART_LIMIT)

	print "Saving charts to database"
	client = MongoClient(MONGO_HOST, MONGO_PORT);
	db = client.deezer_charts
	store_to_mongodb(charts, db.user_charts, CHART_LIMIT)