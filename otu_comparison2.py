#!/usr/bin/env python

import os
import re
import sys
import operator

########################---------PARSING---------------#################################
def its2_parse():
	its2={}
	#if input =='None':
	its2_file = sys.argv[1]
	fileprefix = its2_file.split(".")[0]
	#else:
	#	its2_file=input
	separator="\t"
	separator2=";size=[0-9]+;| "
	#separator2=" |,"
	#print its2_file
	with open(its2_file, "rU") as its2_file:
		for line in its2_file:
			line=line.strip()
			seqs=re.split(separator2,line)[0::2]
			reps=seqs[0]
			s=seqs[1:]
			its2[reps]=s
		#print its2
	return its2, fileprefix

def its1_parse():
	its1={}
	its1_file=sys.argv[2]
	separator="\t"
	separator2=";size=[0-9]+;| "
	#separator2=" |,"
	with open(its1_file,"rU") as its1_file:
		for line in its1_file:
			line=line.strip()
			seqs=re.split(separator2,line)[0::2]
			reps=seqs[0]
			s=seqs[1:]
			its1[reps]=s
		#print its1
	return its1

def lsu_parse():
	lsu={}
	#print len(sys.argv)
	if len(sys.argv) >3:
		lsu_file=sys.argv[3]
	else:
		return
	if lsu_file:
		separator2=";size=[0-9]+;| "
		#separator2=" |,"
		with open(lsu_file,"rU") as lsu_file:
			for line in lsu_file:
				line=line.strip()
				seqs=re.split(separator2,line)[0::2]
				reps=seqs[0]
				s=seqs[1:]
				lsu[reps]=s
	return lsu

#############################-------------Function definitions -------------------###########################
def refcomp(lst1, d1, key=None):
	if not lst1:
		#print "lst empty"
		pass
	else:
		if key == None:
			k=lst1[0]
			key_check="no"
			#print k, key_check
		else:
			k=key
			key_check="yes"
			#print k, key_check
		#If key in d1
			#print "lst1[0]",lst1[0]
		if lst1[0] in d1:
			ref=lst1
			#print "d1",d1
			comp=list(d1[lst1[0]])
			comp.insert(0,lst1[0])
			#print "comp",comp
			diff=set(ref) - set(comp)
			#print "diff",list(diff)
			symdif=set(ref) ^ set(comp)
			#print "symdiff",list(symdif)
			if diff==symdif:
				if key_check == "no": #how to get refcomp to run with both key and non-key?
					#print "no"
					#print diff
					return list(diff)
				else:
					return refcomp(list(diff), d1,k)
			else:
				if key_check=="no":
					#print "diff", diff
					return list(diff)
				else:
					#print "k",k
					return k
		#if key in d1 values
		elif lst1[0] in sum(d1.values(),[]):
			new_key=[ke for (ke, va) in d1.items() if lst1[0] in va][0]
			#print "new_key", new_key
			ref=lst1
			comp=list(d1[new_key])
			comp.insert(0,new_key)
			#print "comp",comp
			diff=set(ref) - set(comp)
			#print "diff",diff
			symdif=set(ref) ^ set(comp)
			#print "symdiff",symdif
			if diff==symdif:
				if key_check == "no": #how to get refcomp to run with both key and non-key?
					#print "no"
					#print diff
					return list(diff)
				else:
					return refcomp(list(diff), d1, k)
			else:
				if key_check =="no":
					#print "return diff" ,diff
					return list(diff)
				else:
					#print "k",k
					return k
		else:
			if key_check=="no":
				print "value not in dict:", lst1[0]
				#Try to check if other elements present?
				bad_collection=[]
				new_lst=[]
				for i in lst1:
					if i in d1 or i in sum(d1.values(),[]):
					#take all other elements in lst1 but i, put i as first and call refcomp
						#print "i",i
						#print "list1", lst1[0:5]
						new_lst=[x for x in lst1 if x != i]
						#print "new_lst", new_lst
						new_lst.insert(0,i)
						#print "calling refcomp with ", new_lst
						return refcomp(new_lst, d1)
					else:
						bad_collection.append(i)
				return bad_collection
			else:
				print "otu not in dict: ",k
				return k
	return

def comparison(d2, d1):
	chimers=[]
	passed=[]
	for key,values in d2.iteritems():
		#print "starting key", key
		if key in d1:
			#print "key in d1"
			if len(list(d2[key]))>=len(list(d1[key])):
				helplst=list(d2[key])
				helplst.insert(0,key)
				#print "calling refcomp with",helplst
				out1=refcomp(helplst, d1, key)#changed
			else:
				helplst=list(d1[key])
				helplst.insert(0,key)
				#print "calling refcomp with",helplst
				out1=refcomp(helplst, d1, key)#shanged
			if out1 != None:
				#print "out",out1
				chimers.append(out1)
			else:
				#print"key",key
				passed.append(key)
		elif key in sum(d1.values(),[]):
			#print "key in values"
			new_key=[ke for (ke, va) in d1.items() if key in va][0]
			group=list(d1[new_key])
			group.insert(0,new_key)
			if len(list(d2[key]))>=len(group): #list in d2 longer
				helplst=list(d2[key])
				helplst.insert(0,key)
				#print "calling refcomp with", helplst
				out=refcomp(helplst, d1, key) #compare d2 to d1
			else: #list in d1 longer
				helplst=group
				#print "calling refcomp with", helplst
				out=refcomp(helplst, d2, key) #compare to d2
			#if output empty, don't add
			if out != None:
				#print "out",out
				chimers.append(out)
			else:
				#print "key",key
				passed.append(key)
		else:
			print "key not found:", key
			chimers.append(key)
	return passed, chimers

def faulty_seqs(d2,d1,chimers):
	print "running faulty seqs"
	bad_seqs=[]
	good_seqs=[]
	#print "chimers", chimers
	for i in chimers:
		#print i
		#length comparison here?
		helplist=list(d2[i])
		helplist.insert(0,i)
		#print "calling refcomp with:",helplist
		seqs=refcomp(helplist,d1)
		if  seqs:
			#print "seqs",seqs
		 	bad_seqs.extend(seqs)
			pass_seqs=list(set(helplist) - set(seqs))
		else:
			pass_seqs=helplist
			#print "pass1",pass_seqs
		if pass_seqs:
			#print "pass",pass_seqs
			good_seqs.append(pass_seqs)
		#print "bad",bad_seqs
	return bad_seqs, good_seqs

###############-------------------MAIN-----------------##############################
def main():
	its2,its2out=its2_parse()
	its1=its1_parse()
	#First run, getting good and chimeric OTUs
	passed,chims=comparison(its2,its1)
	file1=open(its2out + "_passed_OTUs.txt","w")
	file2=open(its2out + "_chimeric_OTUs.txt","w")
	for i in passed:
		otu=its2[i]
		otu.insert(0,i)
		otu=','.join(otu)
		print >>file1,otu
	print >>file2,chims
	file2.close()
	#Second step: getting sequences split between OTUs
	faulty,good=faulty_seqs(its2, its1,chims)
	file3=open(its2out + "_bad_seqs.txt","w")
	print >>file3,faulty
	file3.close()
	#putting good seqs to passed OTUs as OTUs
	for l in good:
		l=','.join(l)
		#print l
		print >>file1, l
	file1.close() 
	#Third step, comparing to LSU
	#""""
	print "running third comparison..."
	lsu=lsu_parse()
	if lsu:
		#lsu_input=open(its2out + "_passed_OTUs.txt","r+")
		file2=open(its2out + "_chimeric_OTUs.txt","w")
		lsuinput={}
		lsu_input=open(its2out + "_passed_OTUs.txt","r")
		for line in lsu_input:
			line=line.strip()
			seqs=re.split(",",line)
			reps=seqs[0]
			s=seqs[1:]
			lsuinput[reps]=s
		#print lsuinput
		#print "keys",lsuinput.keys()
		lsu_input.close()
		#print "running lsu comparison with:", lsuinput
		passed2,chims2=comparison(lsuinput,lsu)
		lsu_input=open(its2out + "_passed_OTUs.txt","w")
		for i in passed2:
			#print "i",i
			l_otu=lsuinput[i]
			#print "lsuinput",l_otu
			l_otu.insert(0,i)
			l_otu=','.join(l_otu)
			#print "l-otu", l_otu
			#lsu_input.seek(0,2) #Needed to be able to write
			print >>lsu_input,l_otu
		print >>file2,chims2
		file2.close()
		faulty2,good2=faulty_seqs(lsuinput, lsu,chims2)
		#print "faulty",faulty2
		file3=open(its2out + "_bad_seqs.txt","w")
		print >>file3,faulty2
		file3.close()
		#putting good seqs to passed OTUs as OTUs
		for l in good2:
			l=','.join(l)
			#print l
			print >>lsu_input, l
		lsu_input.close() 
		#"""""
	return

main()

