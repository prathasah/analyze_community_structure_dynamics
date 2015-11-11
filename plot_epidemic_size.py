import numpy as np
import matplotlib.pyplot as plt
import csv
import os
###########################################################################################
os.chdir("/home/pratha/Dropbox (Bansal Lab)/SBLab_Community_structure_dynamics/Community_Structure_Dynamics/analyze_epidemic_results/5_Results_WIPS_10Nov_2015")
##########################################################################################
Qrange = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
####################################################################
episizedict={}
error = {}
with open ("Epidemic_size.csv", 'r') as csvfile:
	fileread = csv.reader(csvfile, delimiter = ',')
	next(fileread, None) #skip header
	for row in fileread:
		graph=row[0]
		num_modules = int(row[1])
		Q= float(row[2])
		T = float(row[3])
		peaktime = float(row[4])
		sd = float(row[5])
		if not episizedict.has_key(num_modules): episizedict[num_modules]={}
		if not episizedict[num_modules].has_key(T): episizedict[num_modules][T]={}
		if not episizedict[num_modules][T].has_key(graph): episizedict[num_modules][T][graph]={}
		if not error.has_key(num_modules): error[num_modules]={}
		if not error[num_modules].has_key(T): error[num_modules][T]={}
		if not error[num_modules][T].has_key(graph): error[num_modules][T][graph]={}
		episizedict[num_modules][T][graph][Q] = peaktime
		error[num_modules][T][graph][Q] = sd		
    


plt.rc('font', family='serif')
plt.rc('xtick', labelsize='medium')
plt.rc('ytick', labelsize='medium')
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(1, 1, 1)


print episizedict
graphtype = ["poisson", "geometric"]
Trange = [0.2, 0.1]
num_modules = 10
for graph, T in zip(graphtype, Trange):
	val = [episizedict[num_modules][T][graph][Q] for Q in Qrange]
	err = [error[num_modules][T][graph][Q] for Q in Qrange]
	ax.errorbar(Qrange, val, yerr = err, label = "graph="+str(graph)+", T="+str(T))
	
ax.set_xlabel("Modularity, Q", fontsize=24)
ax.set_ylabel("Epidemic size (%)", fontsize=24)
ax.set_xlim([-0.1, 0.9])
ax.set_ylim([0, 100])
ax.legend(loc='upper right', frameon=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
plt.savefig("Epidemic_size.png")
#plt.show()
	
