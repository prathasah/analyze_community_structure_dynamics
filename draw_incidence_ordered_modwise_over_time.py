import re 
import csv
import numpy as np
import zipfile
import matplotlib.pyplot as plt
from pylab import *
import os
###########################################################################################
os.chdir("/home/pratha/Dropbox (Bansal Lab)/SBLab_Community_structure_dynamics/Community_Structure_Dynamics/analyze_epidemic_results/5_Results_WIPS_10Nov_2015")
##########################################################################################
#################################################################################
Qrange = [0.0]
num_modules = 100
NUM_COLORS = num_modules
cm = plt.get_cmap('jet')
incidence_dict={}
err_dict={}
graph = "geometric"
T = 0.1
num_modules = 10
####################################################################

with open ("Incidence_mean_ordered_modules_"+graph+"_T_"+str(T)+"_increasing_mod.csv", 'r') as csvfile:
	fileread = csv.reader(csvfile, delimiter = ',')
	next(fileread, None) #skip header
	for row in fileread:
		graph=row[0]
		Q= float(row[1])
		T = float(row[2])
		module = int(row[3])
		incid = row[4:]
		incid_list = [float(num) if num!="" else 0  for num in incid]
		if not incidence_dict.has_key(T): incidence_dict[T]={}
		if not incidence_dict[T].has_key(graph): incidence_dict[T][graph]={}
		if not incidence_dict[T][graph].has_key(Q):  incidence_dict[T][graph][Q]={}
		incidence_dict[T][graph][Q][module] = incid_list
	
with open ("Incidence_std_ordered_modules_"+graph+"_T_"+str(T)+"_increasing_mod.csv", 'r') as csvfile:
	fileread1 = csv.reader(csvfile, delimiter = ',')
	next(fileread1, None) #skip header
	for row in fileread1:
		graph=row[0]
		Q= float(row[1])
		T = float(row[2])
		module = int(row[3])
		err= row[4:]
		err_list = [float(num) if num!="" else 0  for num in err]
		if not err_dict.has_key(T): err_dict[T]={}
		if not err_dict[T].has_key(graph): err_dict[T][graph]={}
		if not err_dict[T][graph].has_key(Q):  err_dict[T][graph][Q]={}
		err_dict[T][graph][Q][module] = err_list


fig, ax = plt.subplots()
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
############################################################################

for Q in Qrange:
	plt.clf()
	time={}		    
	##################################
	plt.rc('font', family='serif')
	plt.rc('xtick', labelsize='medium')
	plt.rc('ytick', labelsize='medium')
	fig = plt.figure(figsize=(8, 6))
	ax = fig.add_subplot(1, 1, 1)
	NUM_COLORS = 10 # 10 is the total modules
	cm = plt.get_cmap('jet')
	ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
	##################################
	
	for mod in xrange(num_modules): time[mod] = [x for x in xrange(len(incidence_dict[T][graph][Q][mod]))]
	

	#ax.plot(xs=time, ys= Qrange, zs=  final_incidence_curve, zdir='z')

	for num in xrange(num_modules): 
		print Q, num, len( incidence_dict[T][graph][Q][num]), len(err_dict[T][graph][Q][num])
		#ax.errorbar(time[num], incidence_dict[T][graph][Q][num], yerr= err_dict[T][graph][Q][num], marker="o",  label='module='+str(num))
		ax.plot(time[num], incidence_dict[T][graph][Q][num],  marker="o",  label='module='+str(num))
	
	
	ax.set_title("time=0, start infection, endtime=min time all mod one infected", fontsize=10)
	ax.set_xlabel("Time", fontsize=24)
	ax.set_ylabel("Module incidence", fontsize=24)
	ax.set_ylim([0,6])
	ax.set_xlim([-2,300])

	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.xaxis.set_ticks_position('bottom')
	ax.yaxis.set_ticks_position('left')
	#plt.legend(frameon=False)
	plt.savefig("Incidence_modwise_"+graph+"T_"+str(T)+"_Q_"+str(Q)+".png")
		
        
