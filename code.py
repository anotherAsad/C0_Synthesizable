#! /usr/bin/python

# CAUTION: Better to understand and improve than to start all over
import asm
import sys

x, count = 0, 0
labels = {}
infile = open("stub.asm", "r").readlines()
outfile = ""

# Label collecting pass
while x < len(infile):
	# Remove new lines and whitespaces
	commentIndex = infile[x].find(";")
	if commentIndex > -1:
		infile[x] = infile[x][:commentIndex]
	if infile[x].isspace() or len(infile[x]) == 0:
		infile.pop(x)
		continue
	# Split to words
	infile[x] = infile[x].split()
	# Handle Label
	if infile[x][0][-1] == ":":
		labels[infile[x][0][:-1]] = count
		infile[x].pop(0)
		# If left with an empty string after removal, pop it and come again, else increase count because you have a valid line
		if len(infile[x]) == 0:
			infile.pop(x)
			continue
	count += 1
	x += 1

x = 0
# Civilize the instr, remove labelish anarchy
while x < len(infile):
	if (infile[x][-1][0] != 'R' or not infile[x][-1][1].isdigit()) and infile[x][-1][0] != '#' and len(infile[x]) > 1:
		infile[x][-1] = "#"+str(labels[infile[x][-1]]-1)
	infile[x] = " ".join(infile[x])
	# Translate the string to machine code
	infile[x] = asm.assemble(infile[x])+";"
	x += 1

count = 0
for x in infile:
	num = hex(count)[2:].upper()
	print '\t\t\t8\'d'+(2-len(num))*'0'+num+": instr = "+x
	count += 1
