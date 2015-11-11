import numpy as np
import matplotlib.pyplot as plt
import csv
import os
###########################################################################################
os.chdir("/home/pratha/Dropbox (Bansal Lab)/SBLab_Community_structure_dynamics/Community_Structure_Dynamics/analyze_epidemic_results/5_Results_WIPS_10Nov_2015")
##########################################################################################
########################################################################
Qrange = [0.0, 0.1, .2, .3, .4, .5,.6,.7, .8]
####################################################################
epidurdict={}
error = {}
with open ("Epidemic_duration.csv", 'r') as csvfile:
	fileread = csv.reader(csvfile, delimiter = ',')
	next(fileread, None) #skip header
	for row in fileread:
		graph=row[0]
		Q= float(row[2])
		T = float(row[3])
		peaktime = float(row[4])
		sd = float(row[5])
		if not epidurdict.has_key(T): epidurdict[T]={}
		if not epidurdict[T].has_key(graph): epidurdict[T][graph]={}
		if not error.has_key(T): error[T]={}
		if not error[T].has_key(graph): error[T][graph]={}
		epidurdict[T][graph][Q] = peaktime
		error[T][graph][Q] = sd	/np.sqrt(50.0)	
    

plt.rc('font', family='serif')
plt.rc('xtick', labelsize='medium')
plt.rc('ytick', labelsize='medium')
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(1, 1, 1)

graphtype = ["poisson", "geometric"]
Trange = [0.2, 0.1]
for graph, T in zip(graphtype, Trange):
	val = [epidurdict[T][graph][Q] for Q in Qrange]
	err = [error[T][graph][Q] for Q in Qrange]
	ax.errorbar(Qrange, val, yerr = err, label = "graph="+str(graph)+", T="+str(T))


ax.set_xlabel("Modularity, Q", fontsize=24)
ax.set_ylabel("Epidemic duration", fontsize=24)
#ax.set_xticks((0.1, 0.8))
#ax.set_xticklabels(modularity)
ax.set_xlim([-0.1, 0.9])
ax.set_ylim([100, 200])
ax.legend(loc='upper right', frameon=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
plt.savefig("Epidemic_duration_all_graphtype.png")
#plt.show()
	
