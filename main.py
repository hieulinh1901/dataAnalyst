import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# read csv file
raw_data_path = os.getcwd() + "/rawData.csv"
df = pd.read_csv(raw_data_path, encoding="latin-1")

# checking if there are any null values in the winspeed column
df["windSpeed"].isnull().value_counts()

# checking if there are any null values in the windGust column
df["windGust"].isnull().value_counts()

# checking if there are any null values in the pressure column
df["pressure"].isnull().value_counts()

# checking if there are any null values in the temperature column
df["temperature"].isnull().value_counts()

# Transform date and time
df['datetime'] = pd.to_datetime(df['date'] + " " + df['time'], format="%d-%m-%y %I:%M %p")



# Group by hour and average data
df['windSpeed'] = pd.to_numeric(df['windSpeed'], errors='coerce').fillna(0)
df['windGust'] = pd.to_numeric(df['windGust'], errors='coerce').fillna(0)
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce').fillna(0)
df['pressure'] = pd.to_numeric(df['pressure'], errors='coerce').fillna(0)
df['Solar'] = pd.to_numeric(df['Solar'], errors='coerce').fillna(0)
df.set_index('datetime', inplace=True)
time_grouper = pd.Grouper(freq='1H')
new_df = df.groupby(time_grouper)['windSpeed','windGust','temperature','pressure','Solar'].mean()
new_df['aveWindSpeed'] = ((new_df['windGust'] + new_df['windSpeed']) / 2)

# Create a column power production
sweptArea = 3421
powerProduction = []

new_df['airDensity'] = (new_df['pressure'] * 3386.39) / (287.058 * ((new_df['temperature'] - 32) * 5 / 9 + 273.15))


# Checking if the winspeed reach cut-out and cut-in point
new_df['power'] = np.where(((new_df['aveWindSpeed'] > 55.9234) & (new_df['windGust'] > 55.9234)) | ((new_df['aveWindSpeed'] < 7.82928) & (new_df['windGust'] < 7.82928)), 0, (0.5 * new_df['airDensity'] * ((new_df['aveWindSpeed'] / 2.237 ) ** 3) * sweptArea))/1000
new_df = new_df.round()

#Group windPower by day
day_grouper = pd.Grouper(freq='1D')
new_df_2= new_df.groupby(day_grouper)['power'].sum().to_frame()

#Split date time of Df
new_df['date'] = new_df.index.date
new_df['time'] = new_df.index.time

# Creat a cleanedData file
new_df.to_csv('cleanedData.csv', index=True, encoding='utf-8')

# Creat a analystData File
new_df_2.to_csv('analystData.csv', index=True, encoding='utf-8')

#Solar power distribution based on time
sns.set_theme()
# solar_long = sns.load_dataset(new_df)
solar = new_df.pivot("date", "time", "Solar")

# Draw a heatmap with the numeric values in each cell
f, ex = plt.subplots(figsize=(25, 15))
sns.heatmap(solar, annot=True, fmt=".1f", linewidths=1, ax=ex)
ex.set_title("Solar irradiance in March 2022",fontdict={'size':26})
ex.xaxis.set_label_text("Time",fontdict= {'size':18})
ex.yaxis.set_label_text("Date in March",fontdict= {'size':18})
# plt.show()
# saving the plot
f.savefig("solarmap.png")


#Wind power production in March 2022
# Show the results of a linear regression within each dataset
new_df_2['date'] = new_df_2.index.strftime("%d")
g = sns.catplot(data=new_df_2, kind="bar", x="date", y="power")
g.fig.set_size_inches(22, 15)
g.fig.subplots_adjust(top=0.85, right=0.86)


# extract the matplotlib axes_subplot objects from the FacetGrid
ax = g.facet_axis(0, 0)
ax.xaxis.set_label_text("Date in March",fontdict= {'size':14})
ax.yaxis.set_label_text("Power (Kwh) ",fontdict= {'size':14})
ax.set_title("Wind power production per turbine in March 2022",fontdict= {'size':22})
# iterate through the axes containers
for c in ax.containers:
    labels = [f'{(v.get_height()):.1f}' for v in c]
    ax.bar_label(c, labels=labels, label_type='edge')
#plt.show()
# saving the plot
g.savefig("windpower.png")

