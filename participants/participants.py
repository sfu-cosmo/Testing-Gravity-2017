#!/usr/bin/env python
# -*- coding: utf8 -*-

import re, csv
import itertools

participants = [
	# invited speakers
	["Adelberger", "Eric", "University of Washington"],
	["Allen", "Bruce", "MPI & LIGO"],
	["Brax", "Philippe", "Université Paris Saclay"],
	["Burgess", "Cliff", "McMaster/Perimeter"],
	["Burrage", "Clare", "University of Nottingham"],
	["Ferreira", "Pedro", "University of Oxford"],
	["Hui", "Lam", "Columbia University"],
	["Jain", "Bhuvnesh", "University of Pennsylvania"],
	["Joyce", "Austin", "Columbia University"],
	["Khoury", "Justin", "University of Pennsylvania"],
	["Maartens", "Roy", "University of Western Cape"],
	["Muller" ,"Holger", "University of California, Berkeley"],
	["Percival", "Will", "ICG, Portsmouth"],
	["Pospelov", "Maxim", "Victoria/Perimeter"],
	["Pretorius", "Frans", "Princeton University"],
	["Rham", "Claudia de", "Imperial College"],
	["Sasaki", "Misao", "Yukawa Institute for Theoretical Physics"],
	["Trodden", "Mark", "University of Pennsylvania"],
	["White", "Martin", "University of California, Berkeley"],
  	# LOC
  	["Frolov", "Andrei", "Simon Fraser University"],
  	["Pogosian", "Levon", "Simon Fraser University"],
]

table = []

def mangle(affiliation):
	affiliation = re.sub(r"Royal Astronomical Society", 'RASC', affiliation)
	affiliation = re.sub(r"University of British Columbia", 'UBC', affiliation)
	affiliation = re.sub(r"Simon Fraser (U|u)niversity", 'SFU', affiliation)
	affiliation = re.sub(r"Canadian Institute for Theoretical Astrophysics", 'CITA', affiliation)
	affiliation = re.sub(r"Memorial University of Newfoundland", 'Memorial', affiliation)
	affiliation = re.sub(r"California Institut?e of Technology", 'Caltech', affiliation)
	affiliation = re.sub(r"California State University", 'CSU', affiliation)
	affiliation = re.sub(r"University of California(,|\s+at)?", 'UC', affiliation)
	affiliation = re.sub(r"(The\s+)?University of Texas(,|\s+at)?", 'UT', affiliation)
	affiliation = re.sub(r"University of Pennsylvania", 'UPenn', affiliation)
	affiliation = re.sub(r"Case Western Reserve", 'Case Western', affiliation)
	affiliation = re.sub(r"Perimeter.*", 'Perimeter', affiliation)
	affiliation = re.sub(r"ONERA, France", 'ONERA', affiliation)
	affiliation = re.sub(r"Yukawa Institute for Theoretical Physics", 'YITP', affiliation)
	affiliation = re.sub(r"Tokyo University of Science", 'TUS', affiliation)
	affiliation = re.sub(r"National Astronomical Observatory of Japan", 'NAOJ', affiliation)
	affiliation = re.sub(r"Lebedev.*", 'Lebedev', affiliation)
	affiliation = re.sub(r".*\(IKI\).*", 'IKI', affiliation)
	affiliation = re.sub(r"ITA - Aeronautics Institute of Technology", 'ITA', affiliation)
	affiliation = re.sub(r"Universidad Austral de Chile", 'UACh', affiliation)
	affiliation = re.sub(r"American University of Afghanistan", 'AUAF', affiliation)
	affiliation = re.sub(r"Prince Mohammad Bin Fahd University", 'PMU', affiliation)
	affiliation = re.sub(r"\s*Universit(y|é)(\s+(of|at|de))?(\s+(the))?\s*", '', affiliation)
	affiliation = re.sub(r"\s*Observatory(\s+(of|at|de))?(\s+(the))?\s*", '', affiliation)
	affiliation = re.sub(r",?\s*Dep(ar)?t(ment)?\s+of\s+.*", '', affiliation)
	return affiliation

def grouper(n, iterable, padvalue=None):
	"grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
	return itertools.izip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

def chunker(n, array, padvalue=None):
	"chunker(3, 'abcdefg', 'x') --> ('a','d','g'), ('b','e','x'), ('c','f','x')"
	l = len(array); m = (l+n-1)/n
	chunks = [array[i:min(i+m,l)] for i in range(0,l,m)]
	return itertools.izip_longest(*chunks, fillvalue=padvalue)

with open('participants.csv', 'rU') as csvfile:
	for row in csv.reader(csvfile, dialect=csv.excel):
		if row[27].lower() != 'yes': continue
		if row[3].lower() in [p[0].lower() for p in participants]: continue
		participants.append(row[3:6])

participants.sort(key = lambda p: p[0])

for p in itertools.groupby(participants):
	last,first,affiliation = p[0]
	
	# fix stuff for people who cannot spell
	if last == "Lebed": affiliation = "University of Arizona"
	if last == "Afshordi": affiliation = "Perimeter Institute"
	if last == "Baryakhtar": affiliation = "Perimeter Institute"
	if last == "Halenka": affiliation = "University of Michigan"
	if last == "Steer": affiliation = "APC, Paris"
	if last == "Ottewill": affiliation = "UCD"
	if last == "Saida": affiliation = "Daido University"
	if last == "Tsujikawa": affiliation = "Tokyo University of Science"
	if last == "Tanahashi": affiliation = "DAMTP"
	if last == "Nielsen": affiliation = "MPI"
	if last == "Menary": affiliation = "York University"
	if last == "Galvez": affiliation = "Simon Fraser University"
	if last == "Kunstatter": affiliation = "University of Winnipeg"
	if last == "Vikman": affiliation = "FZU"
	if last == "Rapetti": affiliation = "Boulder/NASA Ames"
	if last == "Deffayet": affiliation = "CNRS"
	if last == "JULIÉ": last = "Julié"
	if last == "SACHDEVA":
		first = "Tarun";last = "Sachdeva"
		affiliation = "Thapar University"
	if last == "de Rham": continue
	
	
	# abbreviate name if it is too long
	if (len(first+last) > 24):
		first = re.sub(r'([A-Z])[a-z]+', r'\1.', first)

	table.append("%s %s (%s)" % (first, last, mangle(affiliation)))

print """<meta charset="UTF-8">
<font face="PT Sans Caption" size="6">Registered Participants:
</font>
<table>
<tbody style="vertical-align: top;">
<tr>
"""

#for row in chunker(3, table, ""):
#	print "<tr>"
#	for name in row:
#		print "<td style=\"width: 48ex;\">%s" % name

for column in grouper((len(table)+2)/3, table):
	print "<td style=\"width: 30%;\"><ul>"
	for name in column:
		if name != None: print "<li>" + name
	print "</ul></td>"

print """
</tr>
</tbody>
</table>
"""
