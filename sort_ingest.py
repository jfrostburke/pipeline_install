import lsc
import os
from glob import glob

dir_dic = {'fs': 'fts',
           'fa': 'lsc',
           'fl': 'lsc',
           'kb': '0m4'}

fullpaths = []
for filename in glob('*.fits'):
	date = filename.split('-')[2]
	instrument = dir_dic[filename.split('-')[1][:2]]
	filepath = os.path.join('/supernova','data',instrument,date,'')
	if not os.path.isdir(filepath): 
		os.makedirs(filepath)
	print "Moving {0} to {1}".format(filename,filepath)
	os.system("mv {0} {1}".format(filename,filepath))
	fullpaths.append(filepath+filename)

print "Ingesting into database"
lsc.mysqldef.ingestredu(fullpaths)
