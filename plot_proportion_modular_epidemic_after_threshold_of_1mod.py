import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import zipfile
import os
import re 
import epidemic_calculations as ec
##############################################################################
Qrange=[0.95]
Trange = [0.18]
sigma = 0.2
graph="geometric"
num_modules = 100
N = 10000
modsize = N/num_modules
bins=range(0,1000, 10)
cutoff_size = 0.1*modsize
#################################################################################
os.chdir("/home/pratha/Dropbox (Bansal Lab)/SBLab_Community_structure_dynamics/Community_Structure_Dynamics/analyze_epidemic_results/Epidemic_results_6July_2015")
##########################################################################################
##############################################################################
total_epi_size={}
for T in Trange:
    total_epi_size[T]={}
    for Q in Qrange:
	total_epi_size[T][Q]={}
	print ("Q="), Q
	zf=zipfile.ZipFile("Epidemic_"+graph+"N10000_m"+str(num_modules)+"_Q"+str(Q)+"_T_"+str(T)+"_sigma_"+str(sigma)+".zip", "r")
	for filecount in xrange(2):
		print Q, T, filecount
		file1="INF_"+graph+"n10000_m"+str(num_modules)+"_d10_Q"+str(Q)+"T_"+str(T)+"_iter"+str(filecount)+".txt"
                f1=(zf.open(file1))
		############################
		lines=f1.readlines()
		x=0
		infected_list={}
		for line in lines:
			data=re.split(',', line)[1:]
			data[0]=data[0][2:]
			data[-1]=data[-1][:-2]
			infected_list[x]=[int(num) for num in data]
			x+=1
		############################	    
		for x in xrange(500): 
			if ec.is_epidemic(infected_list[x], num_modules)==True:
				ordered_mod_list = ec.sort_modules_invasion_time(infected_list[x], num_modules)
				for module in xrange(num_modules):
				    
				    if not total_epi_size[T][Q].has_key(module): total_epi_size[T][Q][module]=[]
				    #look for modules according to modules in ordered module list
				    ordered_mod = ordered_mod_list[module]
				    total_epi_size[T][Q][module].append(len([num for num in infected_list[x][(ordered_mod*modsize):(ordered_mod*modsize)+modsize] if num >0]))
			        
 
 
    ##################################
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='medium')
    plt.rc('ytick', labelsize='medium')
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1)
    NUM_COLORS = len(Qrange)
    cm = plt.get_cmap('jet')
    ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
    ##################################
    modrange = [mod for mod in xrange(num_modules)]
    for Q in Qrange:
    	prop_local_epidemic=[]
    	for module in xrange(num_modules):
    		local_epidemic = (len([num for num in  total_epi_size[T][Q][module] if num>=cutoff_size])*100.)/len( total_epi_size[T][Q][module])
    		prop_local_epidemic.append(local_epidemic)
    	
    	print prop_local_epidemic
    	ax.plot(modrange, prop_local_epidemic, label='Q='+str(Q))
    		

    ax.set_ylim([0, 105])
    ax.set_xlim([-0.1, 100.2])
    ax.set_xlabel('Modules (ordered acc. invasion time)')
    ax.set_ylabel('Percentage of modules with episize>='+str(cutoff_size))
    ax.legend(frameon=False, loc= 'lower left', fontsize= 8)
    filename="Proportion_local_epidemic_after_threshold_definition_"+str(graph)+"_m_"+str(num_modules)+"T_"+str(T)+"1.png"
    plt.savefig(filename)
    
                
