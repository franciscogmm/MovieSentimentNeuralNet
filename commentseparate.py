from apiclient.discovery import build
import json
import pprint
import sys
import csv
import pandas as pd
from time import time, sleep
import numpy as np
import nltk
import string
import ast
import re
from os import listdir
from os.path import isfile, join

year = 2006
mypath = 'C:\\Users\\fmendoza6\\Documents\\fmendoza6\\Classes\\Big Data\\' + str(year) + ' fin\\'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
csv.field_size_limit(sys.maxsize)

def getcomments(file):
	filename = 'C:\\Users\\fmendoza6\\Documents\\fmendoza6\\Classes\\Big Data\\' + str(file) + ' fin\\'

	rowlist = []
	dflist = []
	with open(filename, 'rb') as csv_in:
	    myreader2 = csv.reader(csv_in, delimiter = ',')
	    next(myreader2) #skips column headers    

	    for row in myreader2:
	        vid_id = row[0]
	        commenttotallist = row[13]
	        commenttotallist = ast.literal_eval(commenttotallist)
	        # newlist = []
	        # for i in commenttotallist:
	        # 	i = i.decode('unicode_escape').encode('ascii','ignore')
	        # 	i = i.translate(None, string.punctuation)
	        # 	newlist.append(i)
	        rc=0
	        for j in commenttotallist:
	        	text = j
	        	if isinstance(text, list):
	        		if text == []:
	        			pass
	        		else:
	        			#print text
	        			for reply in text:
	        				
	        				if reply.startswith("20"):
	        					pass
	        				else:
	        					
	        					reply = reply.replace('\\','')
					        	reply = reply.decode('unicode_escape').encode('ascii','ignore')
					        	reply = reply.strip()
					        	if reply == 'TZ':
					        		pass
					        	elif reply == ' ':
					        		pass
					        	elif reply == '':
					        		pass
					        	elif reply == '[]':
					        		pass
					        	else:
					        		rc += 1
					        		
					        		#print reply
					       			# rowlist.append(vid_id)
					        		# rowlist.append(reply)
					        		print str(vid_id) + ' - reply - ' + str(rc)
					        		#print rowlist
					        		# dflist.append(rowlist)
					        		# rowlist = []
					        		with open('allcomments.txt', 'a') as csvfile:
										csvfile.write(str(vid_id) + '\t' + str(text) + '\n')
					        		
		        elif text.startswith("20"):
		        	pass
	        	else:
		        	#text = cleanhtml(text)
		        	text = text.replace('\\','')
		        	text = text.decode('unicode_escape').encode('ascii','ignore')
		        	text = text.strip()
		        	if text == 'TZ':
		        		pass
		        	elif text == ' ':
		        		pass
		        	elif text == '':
		        		pass
		        	elif text == '[]':
		        		pass
		        	else:
		        		#print text
		        		rc +=1
		        		
		       			rowlist.append(vid_id)
		        		rowlist.append(text)
		        		print str(vid_id) + ' - thread - ' + str(rc)
		        		#print rowlist
		        		# dflist.append(rowlist)
		        		# rowlist = []
		        		with open('allcomments.txt', 'a') as csvfile:
							csvfile.write(str(vid_id) + '\t' + str(text) + '\n')
	return 
aa = 1
for movie in onlyfiles:
	print movie
	if movie.startswith('._'):
		pass
	else:
		print aa
		getcomments(movie)
		aa += 1
		#dataz.append(commentlist)
		# moviesave = movie.replace('trailer','comments')
# df = pd.DataFrame.from_records(dataz)
# df.to_csv('allcomments.csv', index = False)
