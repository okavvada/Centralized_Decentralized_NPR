from __future__ import division
import csv
import pandas as pd
import math

people_range=range(100,10600,500)
grid_size = 500 #m

#user set parameters
demand=0.2 #m3/person-day
demand_npr=0.1 #m3/person-day
total_demand_central = 241920 #m3/day
total_demand_tertiary = 6048 #m3/day
Electric_Utility="SFPUC"
Electric_Utility_pipes="2010 CA Power Mix"
pipe_material="PE"
Electricity_GHG_LCA = 0.083 #SFPUC

km_to_disposal=50
km_transport=80
discount=0.04
lifetime_treatment=25
lifetime=50
lifetime_pumps = 25
street_density=8000 #m/km2
pump_operating_fraction=0.8
storage_days=3
tank_height=3
tank_thickness = 0.1
retention_time=6 #h
consumption_pressure=20 #m

Treatment_operational_energy_m3=2.4 #MJ/m3
Treatment_capital_energy_m3=0.5 #MJ/m3
Treatment_operational_GHG_m3=0.06  #kgCO2/m3
Treatment_operational_direct_GHG_m3 = 0 #kgCO2/m3
Treatment_capital_GHG_m3= 0.07  #kgCO2/m3
Tertiary_treatment_operation_energy_m3 = 0.9 #MJ/m3
Tertiary_treatment_operation_GHG_m3 = 0.02

#specify model parameters
electricity_cost=0.12 #$/kwh
specific_weight_water=9.807 #KN/m3
water_density=1000 #kg/m3
gravity=9.8 #m/s2
excavation_cost=4.6 #$/m3
excavation_energy=153 #MJ/m3
excavation_GHG=12 #kgCO2/m3
motor_efficiency=0.95

transport_energy_MJ_km=13 #MJ/km
transport_GHG_kg_km= 1 #kgCo2/km
steel_cost=0.769 #$/kg
steel_GHG=1.3 #kgCO2/kg
steel_energy=17.5
steel_sheet_mass=186.9
steel_sheet_area=3.72
cement_energy=2820 #MJ/m3
cement_GHG=330 #kgCO2/m3
cement_cost=0.00005 #$/kg
reinf_concrete_energy=190 #Mj/m3
reinf_concrete_GHG=170 #kgCo2/m3
reinf_concrete_cost=115 # $/m3
reinf_concrete_density = 2400 #kg/m3

#specify treatment parameters
MBR_GHG=0.23
sludge_mass=0.1 #kg/m3 water treated
percent_fertilizer= 0.5 #percent of sludge disposed as fertilizer
percent_landfill= (1-percent_fertilizer) 
landfill_GHG=0.04
fertilizer_GHG=0
chlorine_energy=42 #MJ/kg
chlorine_GHG=0.74 #kg/kg
chlorine_mass=15 #mg/L
chlorine_retention_time=1 #h
UV_rating=9.5 #W/m3/d
UV_capital_cost=4 #$/W 2014
UV_usage=12 #h/day
UV_lifetime= 5 #y
RO_membrane_area = 585500  #m2
RO_energy_m2 = 1.3*10**(-4) #MJ/m2
RO_GHG_m2 = 5.6 * 10**(-6) #kg/m2
RO_lifetime = 10
media_filtration_energy=0.05 #kWh/m3 (Opportunities and Economics of water reuse)
flocculation_energy=0.05 #kWh/m3 of tank volume (Lee,2010)
Screen_Filter_capital_energy=23800
Screen_Filter_capital_GHG=1632 
filter_screen_energy=0.008 #kWh/m3 (Opportunities and Economics of water reuse)
Grinder_pump_hp=2 
Grinder_pump_usage=0.2 # h/day
Grit_chamber_time=0.02 #h (small and decentralized Tchobanoglous)
retention_time=6 #h
