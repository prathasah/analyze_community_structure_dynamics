import numpy as np
import matplotlib.pyplot as plt
import csv
import os
###########################################################################################
os.chdir("/home/pratha/Dropbox (Bansal Lab)/SBLab_Community_structure_dynamics/Community_Structure_Dynamics/analyze_epidemic_results/5_Results_WIPS_10Nov_2015")
##########################################################################################
Qrange = [0.0, 0.05,  0.1, .2, .3, .4, .5, .6, .7, 0.8]
####################################################################
invasion_time={}
error = {}
graph = "geometric"
T= 0.1
####################################################################

with open ('Invasion_time_7_Nov_2015.csv', 'r') as csvfile:
	fileread = csv.reader(csvfile, delimiter = ',')
	next(fileread, None) #skip header
	for row in fileread:
		graph=row[0]
		Q= float(row[1])
		T = float(row[2])
		module = int(row[3])
		invasion = float(row[4])
		err = float(row[6])
		
		if not invasion_time.has_key(graph):
			invasion_time[graph]={}
			error[graph]={}
		if not invasion_time[graph].has_key(T): 
			invasion_time[graph][T]={}
			error[graph][T]={}
		if not invasion_time[graph][T].has_key(Q):
			invasion_time[graph][T][Q]={}
			error[graph][T][Q]={}
			
		invasion_time[graph][T][Q][module] = invasion
		error[graph][T][Q][module] = err

############################################################################


plt.rc('font', family='serif')
plt.rc('xtick', labelsize='medium')
plt.rc('ytick', labelsize='medium')
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1)
NUM_COLORS = len(Qrange)
cm = plt.get_cmap('jet')
ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

xlist = [mod for mod in xrange(10)]
for Q in Qrange: 
	ylist =  [invasion_time[graph][T][Q][module] for module in xrange(10)]
	errlist = [error[graph][T][Q][module] for module in xrange(10)]
	ax.errorbar(xlist, ylist, yerr=errlist, label='Q='+str(Q))


ax.set_xlabel("Modules", fontsize=16)
ax.set_ylabel("Invasion time (threshold=20infected nodes)+-SE", fontsize= 16)
ax.set_ylim([0, 100])
ax.set_xlim([0, 10])

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
plt.legend(frameon=False)
plt.savefig("Invasion_time_geometric_T0.1.png")
#plt.show()

