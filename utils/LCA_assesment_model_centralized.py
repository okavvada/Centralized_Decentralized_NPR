from __future__ import division
import csv
import numpy as np
import pandas as pd
import math
from utils.Parameters import *
from utils.functions import *
from utils.Object_class import Pipes, Pumps, Tanks_cement, Treatment

def LCA_assesment_model_centralized(people, scenario, status, grid_ID, slope_index_grid, length_centralized_m, z_max_route, pop_density, collection_energy, length_centralized_const):
	process_energy_array = []
	process_GHG_array = []
	total_energy_array = []
	total_GHG_array = []

	people_npr = demand/demand_npr*people

	pipe_length_dec = pipe_length_decentralized(people_npr, pop_density)

	elevation_dec = elevation_decentralized(people_npr, pop_density, slope_index_grid)

	if scenario == 'branched':
		pipe_length = pipe_length_dec + length_centralized_const
	elif scenario == 'unbranched':
		pipe_length = pipe_length_dec + length_centralized_m
	    
	elevation = elevation_dec + z_max_route
	elevation_length = pipe_length_dec + length_centralized_m


	#Calculate pipe diameter
	total_demand = people*demand/24 #m3/h
	total_demand_s = total_demand/3600 #m3/s
	demand_day = people*demand #m3/day
	total_dem_round=round(total_demand)

	pipe_diameter = find_pipe_diameter(people, pipe_length, elevation)
	if scenario == 'branched':
		pipe_diameter = 100

	#Pipes        
	Pipe_centralized = Pipes(pipe_diameter, total_demand_s, pipe_length)
	Pipe_energy_construction_kWh_m3, PVC_GHG_m3 = Pipe_centralized.PVC_construction()
	Pipe_excavation_energy_kWh_m3, Pipe_excavation_GHG_m3 = Pipe_centralized.PVC_excavation()
	Pipe_transport_energy_kWh_m3, Pipe_transport_GHG_m3 = Pipe_centralized.PVC_transportation()
	pipe_maint_energy_kWh_m3, pipe_maint_GHG_m3 = Pipe_centralized.PVC_maintenance()

	#Pipes Totals
	Pipe_capital_energy_KWh_m3 = (Pipe_energy_construction_kWh_m3+Pipe_excavation_energy_kWh_m3+Pipe_transport_energy_kWh_m3)
	Pipe_operat_energy_KWh_m3 = pipe_maint_energy_kWh_m3  

	Pipe_capital_GHG_m3 = PVC_GHG_m3+Pipe_excavation_GHG_m3+Pipe_transport_GHG_m3
	Pipe_operat_GHG_m3 = pipe_maint_GHG_m3

	#Pumps
	Pump_centralized = Pumps(pipe_diameter, total_demand_s, elevation, consumption_pressure, elevation_length)
	Pump_energy_operation_kWh_m3, Pump_GHG_operation_m3 = Pump_centralized.pump_operational()
	Pump_energy_construction_kWh_m3, Pump_GHG_construction_m3 = Pump_centralized.pump_construction()
	Pump_energy_transportation_kWh_m3, Pump_GHG_transportation_m3 = Pump_centralized.pump_transportation()

	#Pumps Totals 
	Pump_capital_energy_KWh_m3 = Pump_energy_construction_kWh_m3+Pump_energy_transportation_kWh_m3
	Pump_operat_energy_KWh_m3 = Pump_energy_operation_kWh_m3

	Pump_capital_GHG_m3 = Pump_GHG_construction_m3+Pump_GHG_transportation_m3
	Pump_operat_GHG_m3 = Pump_GHG_operation_m3

	#Tank
	Tank_centralized = Tanks_cement(total_demand_tertiary)
	Tank_energy_construction_kWh_m3, Tank_GHG_construction_m3 = Tank_centralized.tank_construction()
	Tank_energy_transportation_kWh_m3, Tank_GHG_transportation_m3 = Tank_centralized.tank_transportation()

	#Tank Totals
	Tank_capital_energy_kWh_m3 = Tank_energy_construction_kWh_m3+Tank_energy_transportation_kWh_m3
	Tank_capital_GHG_m3 = Tank_GHG_construction_m3+Tank_GHG_transportation_m3


	###Treatment
	Secondary_treatment_operational_energy_KWh_m3 = Treatment_operational_energy_m3/3.6
	Secondary_treatment_operational_GHG_m3 = Treatment_operational_GHG_m3
	Secondary_treatment_capital_energy_KWh_m3 = Treatment_capital_energy_m3/3.6
	Secondary_treatment_capital_GHG_m3 = Treatment_capital_GHG_m3

	Tertiary_treatment_operational_energy_KWh_m3 = Tertiary_treatment_operation_energy_m3/3.6
	Tertiary_treatment_operational_GHG_m3 = Tertiary_treatment_operation_GHG_m3


	#Capitals for Recycling
	Treatment_capital = Treatment(total_demand_tertiary, status)
	#RO
	RO_Construction_energy_KWh_m3, RO_Construction_GHG_m3 = Treatment_capital.RO_construction()
	RO_transport_energy_kWh_m3, RO_transport_GHG_m3 = Treatment_capital.RO_transportation()
	RO_Capital_energy_KWh_m3 = RO_Construction_energy_KWh_m3+RO_transport_energy_kWh_m3
	RO_Capital_GHG_m3 = RO_Construction_GHG_m3+RO_transport_GHG_m3

	#UV
	UV_Operation_energy_KWh_m3, UV_Operation_GHG_m3 = Treatment_capital.UV_operation()
	UV_Construction_energy_KWh_m3, UV_Construction_GHG_m3 = Treatment_capital.UV_construction()
	UV_transport_energy_kWh_m3, UV_transport_GHG_m3 = Treatment_capital.UV_transportation()
	UV_Capital_energy_KWh_m3 = UV_Construction_energy_KWh_m3+UV_transport_energy_kWh_m3
	UV_Capital_GHG_m3 = UV_Construction_GHG_m3+UV_transport_GHG_m3

	#Chlorination
	Chlorine_Tank_energy_KWh_m3, Chlorine_Tank_GHG_m3 = Treatment_capital.Chlorine_Tank_construction()
	Chlorine_Operation_energy_KWh_m3, Chlorine_Operation_GHG_m3 = Treatment_capital.Chlorine_operation()
	Chlorine_transport_energy_kWh_m3, Chlorine_transport_GHG_m3 = Treatment_capital.Chlorine_transportation()
	Chlorine_Capital_energy_KWh_m3 = Chlorine_Tank_energy_KWh_m3+Chlorine_transport_energy_kWh_m3
	Chlorine_Capital_GHG_m3 = Chlorine_Tank_GHG_m3+Chlorine_transport_GHG_m3

	#Sludge            
	Sludge_transport_energy_kWh_m3, Sludge_transport_GHG_m3 = Treatment_capital.Sludge_transportation()
	Sludge_disposal_GHG_m3 = Treatment_capital.Sludge_disposal()


	####Conveyance Totals
	Collection_pumping_energy=collection_energy/3.6 #KWh/m3
	Collection_pumping_GHG=Collection_pumping_energy*Electricity_GHG_LCA

	Total_conveyance_capital_energy_m3 = Pipe_capital_energy_KWh_m3+Pump_capital_energy_KWh_m3+Tank_capital_energy_kWh_m3
	Total_conveyance_operational_energy_m3 = Pipe_operat_energy_KWh_m3+Pump_operat_energy_KWh_m3

	Total_conveyance_capital_GHG_m3 = Pipe_capital_GHG_m3+Pump_capital_GHG_m3+Tank_capital_GHG_m3
	Total_conveyance_operational_GHG_m3 = Pipe_operat_GHG_m3+Pump_operat_GHG_m3

	####Treatment Totals
	Total_Treatment_Capital_energy = (Secondary_treatment_capital_energy_KWh_m3+UV_Capital_energy_KWh_m3+ RO_Capital_energy_KWh_m3+Chlorine_Capital_energy_KWh_m3)
	Total_Treatment_Operational_energy = (Secondary_treatment_operational_energy_KWh_m3+Tertiary_treatment_operational_energy_KWh_m3+UV_Operation_energy_KWh_m3+
											Chlorine_Operation_energy_KWh_m3+Sludge_transport_energy_kWh_m3)

	Total_Treatment_Capital_GHG = Secondary_treatment_capital_GHG_m3+RO_Capital_GHG_m3+UV_Capital_GHG_m3+Chlorine_Tank_GHG_m3
	Total_Treatment_Operational_GHG = (Secondary_treatment_operational_GHG_m3+Tertiary_treatment_operational_GHG_m3+
	                                   UV_Operation_GHG_m3+Chlorine_Operation_GHG_m3+Sludge_transport_GHG_m3+
	                                   Sludge_disposal_GHG_m3)
	        
	Total_Energy_m3=(Total_Treatment_Capital_energy+Total_Treatment_Operational_energy+Total_conveyance_capital_energy_m3+
	                 Total_conveyance_operational_energy_m3+Collection_pumping_energy)
	Total_GHG_m3= (Total_Treatment_Capital_GHG+Total_Treatment_Operational_GHG+Total_conveyance_operational_GHG_m3+
	               Total_conveyance_capital_GHG_m3+Collection_pumping_GHG)

	process_energy_array.append((people, int(grid_ID), Pipe_capital_energy_KWh_m3, Pipe_operat_energy_KWh_m3, 
	                      Pump_capital_energy_KWh_m3, Pump_operat_energy_KWh_m3, Tank_capital_energy_kWh_m3, 
	                            Collection_pumping_energy, Secondary_treatment_operational_energy_KWh_m3, Secondary_treatment_capital_energy_KWh_m3,
	                            Tertiary_treatment_operational_energy_KWh_m3, RO_Capital_energy_KWh_m3,
	                            UV_Operation_energy_KWh_m3, UV_Capital_energy_KWh_m3, Chlorine_Operation_energy_KWh_m3,
	                            Chlorine_Capital_energy_KWh_m3, Sludge_transport_energy_kWh_m3))

	process_GHG_array.append((people, int(grid_ID), Pipe_capital_GHG_m3, Pipe_operat_GHG_m3, 
	                      Pump_capital_GHG_m3, Pump_operat_GHG_m3, Tank_capital_GHG_m3, 
	                            Collection_pumping_GHG, Secondary_treatment_operational_GHG_m3, Secondary_treatment_capital_GHG_m3,
	                            Tertiary_treatment_operational_GHG_m3, RO_Capital_GHG_m3,
	                            UV_Operation_GHG_m3, UV_Capital_GHG_m3, Chlorine_Operation_GHG_m3,
	                            Chlorine_Capital_GHG_m3, Sludge_transport_GHG_m3, Sludge_disposal_GHG_m3))

	total_energy_array.append((people, int(grid_ID), Total_Energy_m3))

	total_GHG_array.append((people, int(grid_ID), Total_GHG_m3))

	return process_energy_array, process_GHG_array, total_energy_array, total_GHG_array                      