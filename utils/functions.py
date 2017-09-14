from __future__ import division
import math
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.optimize import bisect

from utils.Parameters import *

def pipe_length_decentralized(people, pop_density):
	pipe_length_dec = people/pop_density*street_density
	if pipe_length_dec > street_density/2:
		pipe_length_dec = street_density/2
	return pipe_length_dec

def elevation_decentralized(people, pop_density, slope_index_grid):
	if people > pop_density/2:
		elevation_dec=grid_size*slope_index_grid
	else: 
		elevation_dec=math.sqrt(people/pop_density)*slope_index_grid*1000
	if elevation_dec==0:
		elevation_dec=0.1
	return elevation_dec

def find_nearest(array,value):
	idx = (np.abs(array-value)).argmin()
	return array[idx]

def find_pipe_diameter(people, pipe_length, elevation):
	total_demand = people*demand/24
	total_dem_round=np.ceil(total_demand)
	pipe_diameter_data = pd.read_csv('data/pipe_diameter_data2.csv')
	nominal_diameter_list=(50, 100, 160, 200, 350, 375, 450)
	nominal_diameter_array = np.array(nominal_diameter_list)

	k=pipe_diameter_data.set_index('Flow_Rate_m3_h')
	pipe_diameter=k.PVC_Diameter_mm[total_dem_round]
	#pipe_diameter = find_nearest(nominal_diameter_array,pipe_diameter)
	pipe_area=math.pi*(pipe_diameter*0.001/2)**2
	pipe_velocity=total_demand/(3600*pipe_area)

	index = nominal_diameter_list.index(pipe_diameter)
	index=index+1
	pipe_diameter=nominal_diameter_array[index]

	h1=0.03*pipe_length/((pipe_diameter)*0.001)*(pipe_velocity**2)/(2*9.81)
	threshold=0.30*(elevation)

	while h1>threshold:
		index=index+1
		pipe_diameter=nominal_diameter_list[index]
		pipe_area_2=math.pi*(pipe_diameter*0.001/2)**2
		pipe_velocity=total_demand/(3600*pipe_area_2)
		h1=0.03*pipe_length/((pipe_diameter)*0.001)*(pipe_velocity**2)/(2*9.81)

	if pipe_velocity<=2.5:
		pipe_diameter=pipe_diameter
	else:
		index=index+1
	pipe_diameter=nominal_diameter_list[index]

	return pipe_diameter

def group_in_cluster(dtframe1,field):
    grouped_decentral_energy=dtframe1.groupby(dtframe1[field])
    grid_ID_decentral=[[] for i in range(len(dtframe1))]
    for gr, item in grouped_decentral_energy:
        dt=item
        grid_ID_decentral[gr].append(dt)
    return grid_ID_decentral

def interpolate(unique_grid_ID, dataframe_group_1, dataframe_group_2, field):
	grid_intersection=[]
	for i in unique_grid_ID:
		y1 = interp1d(dataframe_group_1[i][0]['People'], dataframe_group_1[i][0][field])
		y2 = interp1d(dataframe_group_2[i][0]['People'], dataframe_group_2[i][0][field])
		f = lambda x : y1(x) - y2(x)
		x1=100
		saving_decentral=(y2(10000) - y1(10000))
		saving_central=(y1(800) - y2(800))
		ysav_cen = y1(800)
		ysav_decen = y2(10000)

		for x in reversed(range(100,10000,500)):
			if f(10000)*f(x)<0:
				x1 =bisect(f, x, 10000)
				y = y1(x1)
				break

			if (y2(x) - y1(x))>saving_decentral:
				saving_decentral=(y2(x) - y1(x))
				ysav_decen = y1(x)

		grid_intersection.extend([(i,x1,ysav_decen,ysav_cen)])

		min_people=pd.DataFrame(grid_intersection)
		min_people.columns=['grid_ID','People','decentral_value','central_value']

	return min_people


