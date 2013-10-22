import time
from datetime import timedelta, date

import fileinput
import operator

def aggregate(out_map, filepath, key_idx, value_idx, weight_idx=None):
	""" Aggregates two columns from a table into a map

		Args:
			out_map: output dict containing aggregates
			filepath: input file containing table data ('|' separated values)
			key_idx: column index for group key
			value_idx: colum index for values to count
			weigth_idx: optional colum index for value weigths

		Output object is a dict of dict mapping values to their count 
		for each key, as following:

		input:
			A | x 
			A | x
			A | z
			B | z

		output: 
			{A: {x: 2, z:1}, B: {z: 1}}
	"""	
	for line in fileinput.input(filepath):
		try:
			# parse line and get field values
			sline = line[:-1].split('|')
			key_id = sline[key_idx]
			value_id = sline[value_idx]
			weight = 1
			if weight_idx:
				weight = int(sline[weight_idx])
			
			# protect from null values
			if not key_id or not value_id:
				skip_line(line)
				continue
			
			# aggregate
			group = out_map.setdefault(key_id, {})
			group[value_id] = group.setdefault(value_id, 0) + weight
		except Exception as e:
			skip_line(line, e)


def extract_charts(charts, limit=None):
	""" Sort, truncate and tranpose an aggregated dict to a table.
		Row are sorted by descending value count

		input: 
			charts = {A: {x: 2, z:1}, B: {z: 1}}
		output:
			A | x | 2
			A | z | 1
			B | z | 1

		Args:
			charts: dict containing aggregates
			limit: optional limit size for the list of values

		Returns:
			iterator on first output table rows
	"""	
	result = []
	# sort values by count, and create list of tuples
	for key, chart in charts.iteritems():	   
		chart = sorted(chart.iteritems(), key=operator.itemgetter(1), reverse=True)
		# truncate
		if limit:
			chart = chart[:limit]
		yield key, chart


def skip_line(line, e=None):
	print "!! Skipped line %s" % line,


def get_log_paths(start_date, ndays):
	""" Return array of log filenames for a given period  
		following the pattern 'log_20120721', ... , 'log_20120723' 
	"""
	paths = []
	for n in range(ndays):
		d = start_date - timedelta(n)
		paths.append("log_%s" % d.strftime("%Y%m%d"))
	paths.reverse()
	return paths


def store_to_file(charts, path, limit=None):
	outfile = open(path, 'w')
	for key, chart in extract_charts(charts, limit):
		for c in chart:
			outfile.write('|'.join((str(key), str(c[0]), str(c[1]))) + '\n')


def store_to_mongodb(charts, table, limit=None):
	table.drop()
	for key, chart in extract_charts(charts, limit):
		c = { "key" : key, "charts" : [ { "song" : c[0], "count" : c[1] } for c in chart ]}
		table.insert(c)
	
