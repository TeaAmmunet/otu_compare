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
	else:
		k=key
	#print "k=", k
	if not lst1:
		pass
	else:
		#If key in d1
		if lst1[0] in d1:
			ref=lst1
			comp=list(d1[lst1[0]])
			comp.insert(0,lst1[0])
			diff=set(ref) - set(comp)
			symdif=set(ref) ^ set(comp)
			if diff==symdif:
				return refcomp(list(diff), d1,k)
			else:
				return k
		#if key in d1 values
		elif lst1[0] in sum(d1.values(),[]):
			new_key=[ke for (ke, va) in d1.items() if lst1[0] in va][0]
			ref=lst1
			comp=list(d1[new_key])
			comp.insert(0,new_key)
			diff=set(ref) - set(comp)
			symdif=set(ref) ^ set(comp)
			if diff==symdif:
				return refcomp(list(diff), d1, k)
			else:
				return k
		else:
			out="value not in dict"
			return out
	return

def comparison(its2, its1):
	chimers=[]
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
	return chimers

####MAIN
def main():
	chims=[]
	its2=its2_parse()
	its1=its1_parse()
	chims=comparison(its2,its1)
	print chims
	return

main()

