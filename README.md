# Compare Centralized with Decentalized Non-potable Water Reuse


This repository consists of the code base for the analysis performed in the publication:
```http://pubs.acs.org/doi/abs/10.1021/acs.est.6b02386```

A description of the project can be found at: 
```https://okavvada.github.io/San_Francisco_webpage/```

If you wish to use the codebase for your own analysis please provide proper attribution by citing the work:

```Kavvada, Olga, Arpad Horvath, Jennifer R. Stokes-Draut, Thomas P. Hendrickson, William A. Eisenstein, and Kara L. Nelson. "Assessing Location and Scale of Urban Nonpotable Water Reuse Systems for Life-Cycle Energy Consumption and Greenhouse Gas Emissions." Environmental science & technology 50, no. 24 (2016): 13184-13194.```


## Background
Water reuse involves treating wastewater to an appropriate standard so it can be used again in other applications rather than being discharged into an ocean, river or other water body. Water reuse has been expanding rapidly, especially in drought-prone locations such as California. Adopters view reuse as an opportunity to enhance and diversify their water portfolio by supplementing other water sources with recycled water. Water reuse can be an efficient way to provide reliable, safe, drought-resilient, local water.

The core and integral criterion for sustainable water reuse implantation is the issue of system scale. Managing water is often an energy-intensive activity. Recycled water needs to be collected, treated and re-distributed to customers, processes that all require material and energy inputs and emit greenhouse gases (GHG) at the site of implementation and throughout the life-cycle. The current water infrastructure is based in large centralized infrastructure, that in most cases requires significant conveyance requirements as the wastewater treatment plants are located downhill and away from the cities. The system has been designed this way to take advantage of the strong "economies of scale" tha occur in large treatment plants. This conventional system however, does not promote reuse as the source and demand are highly disconnected. This tradeoff is generally understood but has been poorly analyzed because it depends on many site-specific factors: land use, water demands, population density, and topography to name a few. 

This project combines spatial analysis and a LCA methodology to develop an algorithm for the estimation of the environmental impacts of decentralized versus centralized non-potable water reuse. Two separate models are developed, one to assess a decentralized reuse scenario in multiple scales and one for the centralized reuse alternative taking into account the existing infrastructure. The models are currently developed for the city of San Francisco.

## Decentralized model

### Input Data
For this analysis the area of interest is a grid cell of 500x500 m. Each grid cell should contain aggregate data that characterizes it as described below.
- people: The number of people that are going to be served by the decentralized reuse system. This number can be any integer that would be used to estimate the system size and its conveyance requirements.
- grid_ID: The grid id is a uniquely identifiable value used to keep track of the grid cell results for mapping purposes.
- slope_index_grid: This is the average slope index of the area of interest (grid cell). It can be calculated as the average slope that can be found inside the boundaries of the grid cell.
- pop_density: This field contains information on the average population density of the grid cell.
- status: This field describes whether the analysis is run for the present time so that the current treatment should be assessed or allows for a 20% efficiency scale if the analysis is done for a future year. The valid arguments for this field are either `current` or `future`. 

This information would be passed in as arguments to the decentralization model `LCA_assessment_model_decentralized.py`. An example of this process can be found in the `Decentralized_SAN_FRANCISCO_Specific.ipynb`. In this example the decentralized algorithm was run for multiple grid cells so the arguments are being stored in a csv file and passed in one-by-one. 


### Algorithmic Process
The algorithmic process estimates the energy intensity and GHG emissions for all the stages of the decentralized reuse scenario at the appropriate scale. Given the input data, the algorithm sizes and estimates the energy and GHG emissions of each system component, namely the pipes, pumps, storage and treatment as described in the `Object_class.py`. Each system component is being sized appropriately to serve the required population and its construction and operating requirements are quantified. The entire algorithmic process is in the `LCA_assessment_model_decentralized.py` file. 

FInally, the calculated outputs refer to the energy and GHG intensity of each individual component and as a system total. All components are assessed for their material transport, construction impacts and operational requirements. Below is a description of the assessed system components. The codebase for the assessment is in the `Object_class.py` file.

* **Pipes**: 
The piping infrastructure is sized appropriately to be able to serve the defined people as passed in the input argument. One of the nominal piping diameters is chosen from the list: (50, 100, 160, 200, 350, 375, 450). 
The pipe length is estimated from the number for people served and the given population density, which will estimate the spread of the distribution of people and the amount of area that needs to be covered by piping.
PVC is assumed as piping material and the material mass is calculated based on the chosen diameter according to manufacturing widths. The construction and transportation requirements are estimated for a given lifetime of 50 years. The excavation requirements are also included in the analysis based on the chosen piping diameter for the excavation volume. Piping maintenace is included per meter length of piping and estimated as an annual requirement.

* **Pumps**:
For the pumping operational requirements, Bernoulli's equation is used to account for the velocity pressure, the consumption pressure, the elevation head and the headlosses. The piping length is estimated as described previously. The elevation head is calculated besed on the slope index input data for the specific area. From the slope index and the population density the maximum elevation difference can be calculated for a certain number of people served.
For the pump construction and material transportation, the material requirements are estimated based on the pump size. 

* **Storage Tanks**:
The storage tank would be located right after the treatment plant and with a capacity to store three days worth of water. It is modeled as a cylindrical tank made out of cement and with a lifetime of 50 years.

* **Treatment**:
The treatment train for the decentralized scenario unit involves a series of unit treatments. The treatment train involves a bar screen, a grinder pump, a grit cement chamber, a steel small equalization tank, an MBR unit, a UV disinfection tank and a chlorine contact tank. All unit processes are characterized by their material transport, construction impacts and operational requirements. The sludge is assumed to be transported and disposed off at a landfill.

### Outputs
The outputs of the decentralized algorithmic module is four arrays of values. The first two arrays describe the individual contributions of each process to energy and GHG emissions. The last two arrays contain the total energy and GHG emissions for the system at the specified scale.

## Centralized model

### Input Data
For this analysis each grid cell is supposed to be served by its closest centralized wastewater treatment plant. For each grid cell we account for the in-cell distribution requirements plus the distribution requirements for transporting the water from the centralized treatment plant to the grid cell. The required inputs for each grid cell are shown below.
- people: The number of people that are going to be served by the centralized reuse system. This number can be any integer that would be used to estimate the system size and its conveyance requirements.
- grid_ID: The grid id is a uniquely identifiable value used to keep track of the grid cell results for mapping purposes.
- slope_index_grid: This is the average slope index of the area of interest (in-grid cell requirements). It can be calculated as the average slope that can be found inside the boundaries of the grid cell.
- pop_density: This field contains information on the average population density of the grid cell.
- status: This field describes whether the analysis is run for the present time so that the current treatment should be assessed or allows for a 20% efficiency scale if the analysis is done for a future year. The valid arguments for this field are either `current` or `future`. 
- length_centralized_m: This value refers to the distance between the grid cell in question and the current location of the centralized treatment plant
- z_max_route: Is the maximum elevation difference that needs to be overcome on the route from the centralized plant to the grid cell.
- collection_energy: Is the pumping energy that is required for the wastewater collection (if applicable in units of MJ/m<sup>3</sup>sup>). In San Francisco not all sewers are gravity fed but some pumping might be required depending on the location. This field specifies the energy required for the sewer collection to reach the centralized facility.
- scenario: Two options are available for this field. 'branched' and 'unbranched'. For the branched scenario the assumption is that there exists piping infrastructure distributed through the entire area and each grid cell is only responsible for the piping infrastructure that it is responsible for. This means that the construction impacts from a main pipe that serves multiple grid cells would be distributed throughout all the grid cells that it serves. The 'unbranched' scenario refers to a case where a designated pipe is constructed that connects each individual cell with the centralized treatment plant.

This information would be passed in as arguments to the centralization model `LCA_assessment_model_centralized.py`. An example of this process can be found in the `Centralized_SAN_FRANCISCO_Specific.ipynb`. In this example the centralized algorithm was run for multiple grid cells so the arguments are being stored in a csv file and passed in one-by-one. 


### Algorithmic Process
The algorithmic process estimates the energy intensity and GHG emissions for all the stages of the centralized reuse scenario at the appropriate scale. Given the input data, the algorithm sizes and estimates the energy and GHG emissions of each system component, namely the pipes, pumps, storage and treatment as described in the `Object_class.py`. Each system component is being sized appropriately to serve the required population and its construction and operating requirements are quantified. The entire algorithmic process is in the `LCA_assessment_model_centralized.py` file. 

FInally, the calculated outputs refer to the energy and GHG intensity of each individual component and as a system total. All components are assessed for their material transport, construction impacts and operational requirements. Below is a description of the assessed system components. The codebase for the assessment is in the `Object_class.py` file.

* **Pipes**: 
The piping infrastructure is sized appropriately to be able to serve the defined people as passed in the input argument. For the in-cell piping requirements, one of the nominal piping diameters is chosen from the list: (50, 100, 160, 200, 350, 375, 450). 
The pipe length is estimated from the number for people served and the given population density, which will estimate the spread of the distribution of people and the amount of area that needs to be covered by piping.
PVC is assumed as piping material and the material mass is calculated based on the chosen diameter according to manufacturing widths. The construction and transportation requirements are estimated for a given lifetime of 50 years. The excavation requirements are also included in the analysis based on the chosen piping diameter for the excavation volume. Piping maintenace is included per meter length of piping and estimated as an annual requirement.

* **Pumps**:
For the pumping operational requirements, Bernoulli's equation is used to account for the velocity pressure, the consumption pressure, the elevation head and the headlosses. The piping length is estimated as described previously. The elevation head is calculated besed on the slope index input data for the specific area. From the slope index and the population density the maximum elevation difference can be calculated for a certain number of people served.
For the pump construction and material transportation, the material requirements are estimated based on the pump size. 

* **Storage Tanks**:
The storage tank would be located right after the treatment plant and with a capacity to store three days worth of water. It is modeled as a cylindrical tank made out of cement and with a lifetime of 50 years.

* **Treatment**:
The treatment train for the decentralized scenario unit involves a series of unit treatments. The treatment train involves a bar screen, a grinder pump, a grit cement chamber, a steel small equalization tank, an MBR unit, a UV disinfection tank and a chlorine contact tank. All unit processes are characterized by their material transport, construction impacts and operational requirements. The sludge is assumed to be transported and disposed off at a landfill.

### Outputs
The outputs of the decentralized algorithmic module is four arrays of values. The first two arrays describe the individual contributions of each process to energy and GHG emissions. The last two arrays contain the total energy and GHG emissions for the system at the specified scale.