# all the epidemic time series calculations
import matplotlib.pyplot as plt
#import community as cm
#import igraph as ig
import networkx as nx
from operator import itemgetter
import time as tm
import numpy as np
import random as rnd
import itertools
import scipy.stats
import math
########################################################################################################################
def calculate_incidence (infected_list):
    """Counts the number of infected at each time point and stores the data as a list"""
    time=max(infected_list)
    incidence=[infected_list.count(step) for step in range(1, time+1)] #time point 1 is stored as the zeroth element
    return incidence

########################################################################################################################
def calculate_infected_degree (infected_list, G):
    """Counts the average degree of infected at each time point and stores the data as a list"""
    time=max(infected_list)
    infected_degree=[]
    for step in range(1, time+1):
    	#time point 1 is stored as the zeroth element
    	degree=[G.degree(node) for node in xrange(len(infected_list)) if infected_list[node]==step] 
    	if len(degree)>0:infected_degree.append(np.mean(degree))
    	else: infected_degree.append(0)
 
    return infected_degree

######################################################################################################################## 

def calculate_module_incidence (infected_list, module):
    """Counts the number of infected at each time point and stores the data as a list"""
    infected_mod_list=infected_list[(module*1000):(module*1000)+1000]
    time=max(infected_mod_list)
    incidence=[infected_mod_list.count(step) for step in range(1, time+1)] #time point 1 is stored as the zeroth element
    return incidence

########################################################################################################################

def modules_infected_unit_time(infected_list, recovered_list):
    """counts the number of infected modules at each time step"""
    endtime=max(recovered_list)
    modules_infected=[len([x for x in range(0,10) if time in infected_list[x*1000:x*1000+1000]]) for time in range(1, endtime+1)]
    #print modules_infected
    return modules_infected
    
########################################################################################################################
    

def reproduction_number_modules_over_time(infected_list):
    """Returns reproduction number of each module at each time step starting from time = t when all modules are infected """
    repr_mod={}
    #start time is the maximum time step when at lease one node is infected in every module
    start_time = max([min([num for num in infected_list[x:x+1000] if num >0]) for x in range(0,10000,1000) if len([num for num in infected_list[x:x+1000] if num >0])>0])
    #end time is the minimum time when at last node was infected in every module
    end_time =  min([max([num for num in infected_list[x:x+1000] if num >0]) for x in range(0,10000,1000) if len([num for num in infected_list[x:x+1000] if num >0])>0])
    for module in xrange(10):
    	infected_mod_list=infected_list[(module*1000):(module*1000)+1000]
    	incidence_mod=[infected_mod_list.count(step) for step in range(start_time, end_time+1)]
    	repr_mod[module] = [incidence_mod[num]/(1.0 * incidence_mod[num-1]) if incidence_mod[num-1] >0  else 0 for num in range(2, len(incidence_mod)-1)]
    
    ##################sort modules according to infection times
    ordered_mod_list = sort_modules_invasion_time(infected_list)
    ordered_repr_list =[]
    for module in ordered_mod_list: ordered_repr_list.append(repr_mod[module])
    
    #################################################################
    
    return ordered_repr_list
    

########################################################################################################################
def incidence_modwise_over_time(infected_list, num_modules):
    """Returns reproduction number of each module at each time step starting from time = t when all modules are infected """
    N = len(infected_list)
    modsize = N/num_modules
    incid_mod={}
    #start time is the maximum time step when at lease one node is infected in every module
    start_time = 1
    #end time is the minimum time when at last node was infected in every module
    end_time =  min([max([num for num in infected_list[x:x+modsize] if num >0]) for x in range(0, N, modsize) if len([num for num in infected_list[x:x+modsize] if num >0])>0])
    for module in xrange(num_modules):
    	infected_mod_list=infected_list[(module*modsize):(module*modsize)+modsize]
    	incid_mod[module]=[infected_mod_list.count(step) for step in range(start_time, end_time+1)]
    	
    ##################sort modules according to infection times
    ordered_mod_list = sort_modules_invasion_time(infected_list, num_modules)
    ordered_incid_list =[]
    for module in ordered_mod_list: ordered_incid_list.append(incid_mod[module])
    
    #################################################################
    
    return ordered_incid_list
    
########################################################################################################################	

    
def calculate_prevalence(infected_list, recovered_list):
    """counts prevalence at each time step and stores the data as a list"""
    prevalence_counts=[range(infected_list[count],recovered_list[count]) for count in xrange(len(infected_list))]
    prevalence_list=[item for sublist in prevalence_counts for item in sublist]
    time=max(recovered_list)
    prevalence=[prevalence_list.count(step) for step in range(1, time+1)]
    return prevalence

########################################################################################################################

def calculate_invasion_time (infected_list):
    """returns invasion time in each module sorted in order of 1st module invaded to last"""
    invasion_time=[find_invasion_minimum(infected_list[x:x+1000]) for x in range(0,10000,1000)]
    invasion_time_sort=sorted(invasion_time)
    #remove all the invasion time when module was not infected
    invasion_time_sort = [num for num in invasion_time_sort if num!=10000]
   
    return invasion_time_sort
    
########################################################################################################################
    
def average_invasion_time(infected_list):
	"""returns average invasion time"""
	invasion_time=[find_invasion_minimum(infected_list[x:x+1000]) for x in range(0,10000,1000)]
	invasion_time_sort=sorted(invasion_time)
	#invasion_duration= time to invasion of current infected community - time to invasion of last infected community
	invasion_duration=[invasion_time_sort[x]-invasion_time_sort[x-1] for x in range(1, len(invasion_time_sort))]
	invasion_duration=[invasion_time_sort[0]]+invasion_duration # invasion_duration of 1st community to get infected = invastion_time-0
	return np.mean(invasion_duration)
	
########################################################################################################################
	

def sort_modules_invasion_time(infected_list, num_modules):
    """returns a list of modules sorted in order of their invasion time"""
    N = len(infected_list)
    mod_size = N/num_modules
    module_invasion_time=[(find_minimum(infected_list[x:x+mod_size]),(x/mod_size)) for x in range(0, N,mod_size)]
    sort_list= sorted(module_invasion_time)
    return [x[1] for x in sort_list]
    
    
########################################################################################################################
	

def sort_modules_threshold_crossover_time(infected_list):
    """returns a list of modules sorted in order of time when they cross threshold of 100 infected individuals"""
    modlist = []
    raw_modlist =[mod for mod in xrange(10)]
    cumsum={}
    for mod in raw_modlist:cumsum[mod]=0
    for time in range(1,max(infected_list)):
    	for mod in raw_modlist:cumsum[mod]+= infected_list[mod*1000:mod*1000+1000].count(time)
    	for mod in raw_modlist: 
    		if cumsum[mod]>=100:
    			raw_modlist.remove(mod)
    			modlist.append(mod)
    		
    return modlist
    
########################################################################################################################
def find_seeding_events_by_modules(G, mod, infected_list, recovered_list):

	seeding = 0
	for node in range(mod*1000,mod*1000+1000):
		infection_time = infected_list[node]
		if infection_time>0:
			infected_neighbors =  [node_i for node_i in G.neighbors(node) if infected_list[node_i]< infection_time and infected_list[node_i]>0 and recovered_list[node]>infection_time]
			is_same_module = [1 if node_i/1000 == node/1000 else 0 for node_i in infected_neighbors]
			# a node is assumed to be seeded when none of its infected neighbors are in the same module
			if sum(is_same_module)==0: seeding+=1
	return seeding
########################################################################################################################

def most_common(infected_list):
    """returns the most frequent element in a list"""
    lst=[x for x in infected_list if x>0] # removes zero from list (which indicates unifected nodes)
    return max(set(lst), key=lst.count)
    
########################################################################################################################
    
def find_invasion_minimum(sequence):
    """find minimum invasion time in a module when there are more than (or equal to
    20 infected individuals in the module"""
    if sum(sequence)>0:
        list_seq=[x for x in sequence if x!=0 and len([num for num in sequence if num!=0 and num<x])>=20]
	if len(list_seq)==0:list_seq=[10000]
        return min(list_seq)
        
    # if the module is not infected return a aburdly large number
    else: return 10000   

########################################################################################################################
    
def find_minimum(sequence):
    """find minimum invasion time in a module """
    if sum(sequence)>0:
        list_seq=[x for x in sequence if x!=0]
	if len(list_seq)==0: return 100
        return min(list_seq)
    
    #else return a large number    
    else: return 100   
    
########################################################################################################################

def is_epidemic(infected_list, num_modules):
    """an infection spread is considered an epidemic if at least 10% individuals in 1 modules are infected"""
    N = len(infected_list)
    modsize = N/num_modules
    cutoff_size = 0.1*modsize
    is_epidemic_magnitude=len([x for x in infected_list if x>0])>= cutoff_size #tests if minimum 100 indivduals are infected
    is_epidemic_scale=False
    
    if is_epidemic_magnitude==True:
        infection_count=[len([num for num in infected_list[x:x+modsize] if num>0]) for x in range (0, N, modsize)]
        infected_modules=len([infections for infections in infection_count if infections >= cutoff_size])
        is_epidemic_scale=infected_modules>=1 #i.e minimum infected modules is atleast 1
    
    return is_epidemic_magnitude and is_epidemic_scale
    #return is_epidemic_magnitude 
########################################################################################################################

def synced_epidemic_duration(infected_list, recovered_list):
	"""calculates epidemic duration starting from when 5% of the population is infected"""
	end_point=max(recovered_list) # end of epidemic
	total_infected=[]
	for time in range (1, end_point+1):
		infected= len([infected_list[x] for x in xrange(len(infected_list)) if infected_list[x]<=time and infected_list[x]>0])
		if infected>=0.05*len(infected_list):total_infected.append((time,infected))

	start_point=  min(total_infected,key=lambda x:x[1])[0]
	return end_point-start_point
	
########################################################################################################################    
    
def find_infected_modules(infected_list):
    """find the number of modules infected"""
    infection_count=[len([num for num in infected_list[x:x+1000] if num>0]) for x in range (0,10000,1000)]
    return len([infections for infections in infection_count if infections>=200])

########################################################################################################################
def track_modularity(G, recovered_list):
	"""returns a new graph with the recovered nodes removed"""
	end_time=max(recovered_list)
	modularity_values=[]
	for time in range(10,end_time+1, 10):
		GI=G.copy()
		GI.delete_vertices([x for x in xrange(len(recovered_list)) if recovered_list[x]<=time and recovered_list[x]!=0])
		partition=GI.community_multilevel(weights=None, return_levels=False)
                modularity_values.append(GI.modularity(partition))
        
	return modularity_values
########################################################################################################################

def track_infected_degree(infected_list, G):
	"""returns a dictionary of proportion infected degree over time. Key=time, Values= list of proportion infected degree
	For example [0,1,10] 10% individuals for degree 2, and 1% individual of degree 1 out of the total infected were infected at time
	t"""
	max_degree=(sorted(G.degree_iter(),key=itemgetter(1),reverse=True))[0][1]
	degree_list=G.degree().values()
	degree_count={}
	for degree in xrange(max_degree+1):
		degree_count[degree]=degree_list.count(degree)
	end_time=max(infected_list)
	infected_degree={}
	for time in xrange (end_time+1):
		# list of degree of all the nodes infected at the time
		infected_degrees=[G.degree(x) for x in xrange(len(infected_list)) if infected_list[x]==time] 
		infected_degree[time]=[infected_degrees.count(degree)/(1.0*degree_count[degree])*100.0 if degree_count[degree]>0 else 0 for degree in xrange(max_degree+1)]
	return infected_degree
		
########################################################################################################################
def estimated_wd_by_d_ratio(infected_list, G):
	"""estimates the ratio of within-degree to total degree of infected nodes
	over the course of infection duration. Assumes that the network has 10,000 nodes
	with 1000 nodes in each module"""
	end_time=max(infected_list)
	ratio_list=[]
	degree_list=[]
	for time in xrange (end_time+1):
		infected_nodes=[x for x in xrange(len(infected_list)) if infected_list[x]==time] #all the nodes infected at the time
                #print [within_degree(node, G)/(1.0* G.degree(node)) for node in infected_nodes]
                if len(infected_nodes)>0:
                    ratio_list.append(np.mean([within_degree(node, G)/(1.0* G.degree(node)) for node in infected_nodes]))
                    degree_list.append (np.mean([G.degree(node) for node in infected_nodes]))
		else:
                    ratio_list.append(0)
                    degree_list.append(0)
	return ratio_list, degree_list

########################################################################################################################

def within_degree(node, G):
	"""finds within module degree of a node. Assumes that the network has 10,000 nodes
	with 1000 nodes in each module"""
	module= node/1000 # finds module id of the node
	aii=(G.neighbors(node))# total degree of a node
        a_set=set(aii)
        mod_set=set(range(module*1000, module*1000+1000)) # list of nodes in the module
        return len(list(a_set.intersection(mod_set)))
	
########################################################################################################################
	
def track_inter_intra_incidence(infected_list, recovered_list, G):

	
	  time=max(infected_list)
	  #first time step--> infection was introduced
	  inter_infection =[0]
	  intra_infection = [0]
	  for timestep in range(2, time+1):
	  	#initialize inter-module and intra-module infection at 0 for each time-step
	  	inter_infection.append(0)
	  	intra_infection.append(0)
	  	#select nodes that were infected at timestep
	  	nodes_infected = [node for node in xrange(len(infected_list)) if infected_list[node]==timestep]
	  	
	  	recovered_nodes = [node for node in nodes_infected if recovered_list[node]>timestep]
	  	for node in nodes_infected:
	  		#select neighbors of "node" that were infected before "node" --> they act as potential infection source
	  		#also do not consider recovered nodes (select nodes that recovered in a later time-step)
			infected_neighbors =  [node_i for node_i in G.neighbors(node) if infected_list[node_i]< timestep and infected_list[node_i]>0 and recovered_list[node]>timestep]
			
			module_infected_nbrs = [x/1000 for x in infected_neighbors]  
			source = [0 if node/1000==mod else 1 for mod in  module_infected_nbrs]
			intra_source = source.count(0)
			inter_source = source.count(1)
			if  intra_source > inter_source: intra_infection[timestep-1]+=1
			elif  intra_source < inter_source: inter_infection[timestep-1]+=1
			else: 
				a = rnd.choice([0,1])
				if a==0: intra_infection[timestep-1]+=1
				else: inter_infection[timestep-1]+=1
	  return inter_infection, intra_infection
			
########################################################################################################################
def count_inter_intra_edges(G):
	
	"""returns percentage of total inter and intra edges"""
	inter_edges=0
	intra_edges = 0
	total_edges = len(G.edges())
	for node1, node2 in G.edges():
		if node1/1000 == node2/1000: intra_edges+=1
		else: inter_edges+=1
	
	return (inter_edges/(1.0*total_edges))*100., (intra_edges/(1.0*total_edges))*100.
########################################################################################################################
def calculate_between_patch_synchrony(infected_list):
	"""calculate synchrony between patches using modified formula by Jesse 2008. Assumes each patch size=1000"""
	
	#end_time = max(infected_list)
	end_time = 300
	start_time = 50
	S = {}
	I={}
	num_patches = 10
	count=-1
	
	#############
	for iterations in xrange(500):
		if is_epidemic(infected_list[iterations])==True:
			count+=1
			I[count]={}
			#order modules according to infection times
			ordered_mod_list = sort_modules_invasion_time(infected_list[iterations])
			for module in xrange(num_patches): I[count][module]={}
		
			for time in range(start_time, end_time):
				for module in xrange(num_patches):
					#count number of infected
					raw_module = ordered_mod_list[module]
					infected_count = len([num for num in infected_list[iterations][raw_module*1000:(raw_module*1000)+1000] if num==time])
					I[count][module][time] = infected_count
					
			for module in xrange(num_patches): 
				if sum(I[count][module].values())>1000: print ("check!!!"), module, sum(I[count][module])
	#############
	
	
	total_count = len(I.keys())
	#############
	module_combination = [x for x in itertools.combinations([num for num in xrange(10)],2)]
	##sum iteratior of 1 component of numerator
	num1_component = sum([np.mean([[I[count][moda][time]*I[count][modb][time] for time in range(start_time, end_time)] for count in xrange(total_count)]) for moda, modb in module_combination])
	num1 = (2./(num_patches*(num_patches-1))) * num1_component
	fac_2 = sum([np.mean([I[count][module].values() for count in xrange(total_count)]) for module in xrange(num_patches)])
	fac = (1./num_patches**2)  * fac_2**2
	denom1 = (1./num_patches) * sum([np.mean([[I[count][module][time]**2 for time in range(start_time, end_time)] for count in xrange(total_count)]) for module in xrange(num_patches)])
	denominator = denom1 - fac
	numerator = num1 - fac
	##############
	
	#print numerator, denominator, num1, denom1, fac, (1.*numerator)/denominator
	return (1.*numerator)/denominator
	
########################################################################################################################
def calculate_pairwise_pearson_correlation(infected_list, recovered_list):

	end_time =[] 
	num_patches = 10
	I={}
	ordered_mod_list = sort_modules_invasion_time(infected_list)
	
	for module in xrange(num_patches): I[module] =[0]
	for module in xrange(num_patches):
		raw_module = ordered_mod_list[module]
		I[module]= calculate_prevalence(infected_list[raw_module*1000:(raw_module*1000)+1000], recovered_list[raw_module*1000:(raw_module*1000)+1000])
		end_time.append(len(I[module]))
		
			
	N={}
	Z={}
	end_time = min(end_time) -1
	#for module in xrange(10): N[module] = [np.log(I[module][num])  if I[module][num]>0 else 0 for num in range(10, end_time) ]
	#for module in xrange(10): Z[module] = [N[module][num+1] - N[module][num] for num in xrange(len(I[module])-1)]
	for module in xrange(10): Z[module] = [I[module][num] for num in range(10, end_time)]
	
	
	module_combination = [x for x in itertools.combinations([num for num in xrange(10)],2)]

	sync = []
	
	for moda, modb in module_combination:
		rho = (scipy.stats.pearsonr(Z[moda], Z[modb])[0])	
		if not math.isnan(rho): sync.append(rho)
	
	return np.mean(sync)
			
########################################################################################################################	
def calculate_pearson_correlation_with_seeded_module(infected_list, recovered_list):

	end_time =[] 
	num_patches = 10
	I={}
	ordered_mod_list = sort_modules_invasion_time(infected_list)
	
	for module in xrange(num_patches): I[module] =[0]
	for module in xrange(num_patches):
		raw_module = ordered_mod_list[module]
		I[module]= calculate_prevalence(infected_list[raw_module*1000:(raw_module*1000)+1000], recovered_list[raw_module*1000:(raw_module*1000)+1000])
		end_time.append(len(I[module]))
		
			
	N={}
	Z={}
	end_time = min(end_time) -1
	#for module in xrange(10): N[module] = [np.log(I[module][num])  if I[module][num]>0 else 0 for num in range(10, end_time) ]
	#for module in xrange(10): Z[module] = [N[module][num+1] - N[module][num] for num in xrange(len(I[module])-1)]
	for module in xrange(10): Z[module] = [I[module][num] for num in range(10, end_time)]
	
	
	module_combination = [x for x in itertools.combinations([num for num in xrange(10)],2)]

	sync = []
	
	for moda in range(2,10):
		rho = (scipy.stats.pearsonr(Z[0], Z[moda])[0])	
		if not math.isnan(rho): sync.append(rho)
	
	return np.mean(sync)
			
########################################################################################################################	
		
		

	
		
	


 
