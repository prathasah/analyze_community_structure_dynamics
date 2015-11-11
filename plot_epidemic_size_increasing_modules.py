import numpy as np
import matplotlib.pyplot as plt
import csv
import os
###########################################################################################
os.chdir("/home/pratha/Dropbox (Bansal Lab)/SBLab_Community_structure_dynamics/Community_Structure_Dynamics/analyze_epidemic_results/5_Results_WIPS_10Nov_2015")
##########################################################################################
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
		episize = float(row[4])
		sd = float(row[5])
		if not episizedict.has_key(num_modules): episizedict[num_modules]={}
		if not episizedict[num_modules].has_key(T): episizedict[num_modules][T]={}
		if not episizedict[num_modules][T].has_key(graph): episizedict[num_modules][T][graph]={}
		if not error.has_key(num_modules): error[num_modules]={}
		if not error[num_modules].has_key(T): error[num_modules][T]={}
		if not error[num_modules][T].has_key(graph): error[num_modules][T][graph]={}
		episizedict[num_modules][T][graph][Q] = episize
		error[num_modules][T][graph][Q] = sd		
    


plt.rc('font', family='serif')
plt.rc('xtick', labelsize='medium')
plt.rc('ytick', labelsize='medium')
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(1, 1, 1)


print episizedict
graph = "geometric"
T = 0.1
Qrange = [0.0, 0.8, 0.88]
num_module_range= [10,10,100]
xlist = [1,2,3]

for Q, num_modules,x in zip(Qrange, num_module_range,xlist):
	ax.errorbar(x, episizedict[num_modules][T][graph][Q], yerr = error[num_modules][T][graph][Q], fmt="o", label = "Q="+str(Q)+", mod="+str(num_modules))
	
ax.set_xlabel("Modularity, Q", fontsize=24)
ax.set_ylabel("Epidemic size (%)", fontsize=24)
ax.set_xlim([0, 3.4])
ax.set_ylim([0, 60])
ax.legend(loc='upper right', frameon=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
a=ax.get_xticks().tolist()
print a
a[0] =""
a[1] = ""
a[2] = "Null"
a[3] = ""
a[4] = "Qrel=0.88,m10"
a[5] = ""
a[6] = "Qrel=0.88,m100"
ax.set_xticklabels(a)
plt.savefig("Epidemic_size_diff_module.png")
#plt.show()
	
