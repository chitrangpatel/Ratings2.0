#!/usr/bin python
"""
Query the PALFA database and generate a CSV file (in the style of the ATNF
pulsar catalog) with alle known sources with period > 0 and DM > 0.
The list thus misses some X-ray and gamma-ray pulsars that are radio-quiet
and have no measured DM. It also misses some RRATs for which no period 
measurement is available.

NB This script has to be run on a machine with access to the PALFA database
located at Cornell University, e.g. 'kira' at McGill.
"""
import csv
import time
import database

# connect to the PALFA database at Cornell
db = database.Database('common3')

known_psr_query = "SELECT pulsar_name, ra_deg, dec_deg, period, dm " + \
 				  "FROM Known_Pulsars"

db.execute(known_psr_query)
known_psrs = db.cursor.fetchall()

num_psrs = len(known_psrs)

# mark-up of csv file
csv.register_dialect('palfa', delimiter=';', lineterminator=';\n')

f = open('knownpulsars.csv', 'wt')
try:
	writer = csv.writer(f, dialect='palfa')
	# write format
	writer.writerow(('NUM','NAME','RAJD','DECJD','P0','DM'))
	# write header
	today = time.strftime('%Y-%m-%d')
	f.write('# Generated ' + today + ' using PALFA Known_Pulsars database\n')
	f.write('# Contains only sources with DM > 0 and period > 0\n')
	# write pulsars
	for i in range(num_psrs):
		name, ra_deg, dec_deg, period, dm = known_psrs[i]
		# only write out pulsars with known period and dm (necessary for raters)
		if (dm > 0) and (period > 0):
			# start from 1, not 0
			writer.writerow((i+1, name, ra_deg, dec_deg, period, dm))
finally:
	f.close()
