# dataAnalyst
This is a small data analyst project of wind power production and solar irradiance in Marrawah, 7330, Tas based on the weather record in March 2022
(https://www.wunderground.com/dashboard/pws/IMARRA24/table/2022-03-1/2022-03-1/daily)

**Dataset Overview**
- The Dataset is taken from wunderground contain weather data in Marrawah area in March 2022
- The raw dataset is not cleaned. There are some missing values. The data of wind speed and wind gust need to be caculated. The wind power need to be calcualated.
-  The wind power will be calculated according to the paper from The royal academic of engineering (https://www.raeng.org.uk/publications/other/23-wind-turbine)
- Turbine detail is calculated base on Vestas V66-1.77 model. Using Vestas V66-1.75 model detail.
- The dataset is cleaned and stored in a cleanData folder which contains the entire cleaned dataset plus analyst dataset named as cleanedData.csv and analystData.csv

### More Info
The main folder contains 
- main.py - execute code
- raw dataset
- clean dataset folder
- plots
***
### Analysis 1
- This analysis describe the wind power production hourly in March 2022 
- The highest power produced from wind is from the ealier of the month and hardly dropped.
- The power produced from wind is regularly, consistent most of the days except if there was a storm
- The wind turbine will be cut off if the wind is too strong or too weak to prevent damages(cut-in: 4.0 m/s and cut-out: 25m/s) 

![alt text](dataAnalyst/windower.png "Logo Title Text 1")

