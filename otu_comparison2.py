#!/usr/bin/env python

import os
import re
import sys
import operator

def its2_parse():
	its2={}
	its2_file = sys.argv[1]
	separator="\t"
	separator2=";size=[0-9]+;| "
	with open(its2_file, "rU") as its2_file:
		for line in its2_file:
			line=line.strip()
			seqs=re.split(separator2,line)[0::2]
			reps=seqs[0]
			s=seqs[1:]
			its2[reps]=s
	return its2

def its1_parse():
	its1={}
	its1_file=sys.argv[2]
	separator="\t"
	separator2=";size=[0-9]+;| "
	with open(its1_file,"rU") as its1_file:
		for line in its1_file:
			line=line.strip()
			seqs=re.split(separator2,line)[0::2]
			reps=seqs[0]
			s=seqs[1:]
			its1[reps]=s
	return its1

def refcomp(lst1, d1, key=None):
	if key == None:
		k=lst1[0]
		key_check="no"
		print k, key_check
	else:
		k=key
		key_check="yes"
		print k, key_check
	if not lst1:
		pass
	else:
		#If key in d1
		if lst1[0] in d1:
			ref=lst1
			comp=list(d1[lst1[0]])
			comp.insert(0,lst1[0])
			diff=set(ref) - set(comp)
			print "diff",diff
			symdif=set(ref) ^ set(comp)
			print "symdiff",symdif
			if diff==symdif:
				if key_check == "no": #how to get refcomp to run with both key and non-key?
					print "no"
					print diff
					return refcomp(list(diff), d1 )
				else:
					return refcomp(list(diff), d1,k)
			else:
				if key_check=="no":
					return lst1
				else:
					return k
		#if key in d1 values
		elif lst1[0] in sum(d1.values(),[]):
			new_key=[ke for (ke, va) in d1.items() if lst1[0] in va][0]
			print "new_key", new_key
			ref=lst1
			comp=list(d1[new_key])
			comp.insert(0,new_key)
			diff=set(ref) - set(comp)
			print "diff",diff
			symdif=set(ref) ^ set(comp)
			print "symdiff",symdif
			if diff==symdif:
				if key_check == "no": #how to get refcomp to run with both key and non-key?
					print "no"
					print diff
					return refcomp(list(diff), d1 )
				else:
					return refcomp(list(diff), d1, k)
			else:
				if key_check =="no":
					return lst1
				else:
					return k
		else:
			out="value not in dict: {lst1[0]}"
			return out
	return

def comparison(its2, its1):
	chimers=[]
	passed=[]
	for key,values in its2.iteritems():
		#print "starting key", key
		if key in its1:
			if len(list(its2[key]))>len(list(its1[key])):
				helplst=list(its2[key])
			else:
				helplst=list(its1[key])
			helplst.insert(0,key)
			out1=refcomp(helplst, its1, key)
			if out1 != None:
				chimers.append(out1)
			else:
				passed.append(key)
		if key in sum(its1.values(),[]):
			new_key=[ke for (ke, va) in its1.items() if key in va][0]
			group=list(its1[new_key])
			group.insert(0,new_key)
			if len(list(its2[key]))>len(group):
				helplst=list(its2[key])
				helplst.insert(0,key)
			else:
				helplst=group
			#calling refcomp with helplst
			out=refcomp(helplst, its2, key)
			#if output empty, don't add
			if out != None:
				chimers.append(out)
			else:
				passed.append(key)
	return passed, chimers

def faulty_seqs(its2,its1,chimers):
	all_seqs=[]
	for i in chimers:
		print i
		helplist=its2[i]
		helplist.insert(0,i)
		print "calling refcomp with:",helplist
		seqs=refcomp(helplist,its1)
		all_seqs.append(seqs)
	return sum(all_seqs,[])


####MAIN
def main():
	chims=[]
	its2=its2_parse()
	its1=its1_parse()
	#First run, getting good and chimeric OTUs
	passed,chims=comparison(its2,its1)
	print passed
	print chims
	#Second step: getting sequences split between OTUs
	faulty=faulty_seqs(its2, its1,chims)
	print faulty
	return

main()

