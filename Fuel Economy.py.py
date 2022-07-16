##Investigate a more challenging dataset on fuel economy and learn more about problems and strategies in data analysis.
##The fuel economy of an automobile is the fuel efficiency relationship between the distance traveled and the amount of fuel consumed by the vehicle.
#Consumption can be expressed in terms of volume of fuel to travel a distance, or the distance travelled per unit volume of fuel consumed.

#Assessing
import pandas as pd
% matplotlib inline
df_08 = pd.read_csv('all_alpha_08.csv')
df_18 = pd.read_csv('all_alpha_18.csv')

#Find the correct count for each of the following in the 2008 and 2018 dataset
df_08.count()
df_18.count()

#what are the data types of each feature in the datasets
df_08.dtypes
df_18.dtypes

#unique values for each feature
df_08.nunique()

#Cleaning column labels
#Drop Extraneous columns
# drop columns from 2008 dataset
df_08.drop(['Stnd', 'Underhood ID', 'FE Calc Appr', 'Unadj Cmb MPG'], axis=1, inplace=True)

# confirm changes
df_08.head(1)

# drop columns from 2018 dataset
df_18.drop(['Stnd', 'Stnd Description', 'Underhood ID', 'Comb CO2'], axis=1, inplace=True )

# confirm changes
df_18.head(1)

#Rename columns
# rename Sales Area to Cert Region
df_08.rename(columns={'Sales Area':'Cert Region'}, inplace= True)

# confirm changes
df_08.head(1)

# replace spaces with underscores and lowercase labels for 2008 dataset
df_08.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)

# confirm changes
df_08.head(1)

# replace spaces with underscores and lowercase labels for 2018 dataset
df_18.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)


# confirm changes
df_18.head(1)

# confirm column labels for 2008 and 2018 datasets are identical
df_08.columns == df_18.columns

# make sure they're all identical like this
(df_08.columns == df_18.columns).all()

# save new datasets for next section
df_08.to_csv('data_08_v1.csv', index=False)
df_18.to_csv('data_18_v1.csv', index=False)

##Filter, Drop Nulls, Dedupe
# view dimensions of dataset
df_08.shape
df_18.shape


#Filter by Certification Region
# filter datasets for rows following California standards
df_08 = df_08.query('cert_region =="CA"')
df_18 = df_18.query('cert_region =="CA"')

# confirm only certification region is California
df_08['cert_region'].unique()

# confirm only certification region is California
df_18['cert_region'].unique()


# drop certification region columns form both datasets
df_08.drop('cert_region', axis=1, inplace=True)
df_18.drop('cert_region', axis=1, inplace=True)

df_08.shape
df_18.shape

#Drop rows with missing values
# view missing value count for each feature in 2008
df_08.isnull().sum()

# view missing value count for each feature in 2018
df_18.isnull().sum()

# drop rows with any null values in both datasets
df_08.dropna(inplace=True)
df_18.dropna(inplace=True)

# checks if any of columns in 2008 have null values - should print False
df_08.isnull().sum().any()
# checks if any of columns in 2018 have null values - should print False
df_18.isnull().sum().any()

# print number of duplicates in 2008 and 2018 datasets
df_08.duplicated().sum()
df_18.duplicated().sum()

# drop duplicates in both datasets
df_08.drop_duplicates(inplace=True)
df_18.drop_duplicates(inplace=True)

# print number of duplicates again to confirm dedupe - should both be 0
df_08.duplicated().sum()
df_18.duplicated().sum()

# save progress for the next section
df_08.to_csv('data_08_v2.csv', index=False)
df_18.to_csv('data_18_v2.csv', index=False)

# check value counts for the 2008 cyl column
df_08['cyl'].value_counts()

# Extract int from strings in the 2008 cyl column
df_08['cyl'] = df_08['cyl'].str.extract('(\d+)').astype(int)

# Check value counts for 2008 cyl column again to confirm the change
df_08['cyl'].value_counts()

# convert 2018 cyl column to int
df_18['cyl'] = df_18['cyl'].astype(int)

df_08.to_csv('data_08_v3.csv', index=False)
df_18.to_csv('data_18_v3.csv', index=False)

# try using pandas' to_numeric or astype function to convert the
# 2008 air_pollution_score column to float -- this won't work
df_08['air_pollution_score']= df_08['air_pollution_score'].astype[float]

##Figuring out the issue
##Looks like this isn't going to be as simple as converting the datatype.
##According to the error above, the air pollution score value in one of the rows is "6/4"
df_08[df_08.air_pollution_score == '6/4']

"""It's not just the air pollution score!
The mpg columns and greenhouse gas scores also seem to have the same problem - maybe that's why these were all saved as strings! According to this link, which I found from the PDF documentation:

"If a vehicle can operate on more than one type of fuel, an estimate is provided for each fuel type."
Ohh... so all vehicles with more than one fuel type, or hybrids, like the one above (it uses ethanol AND gas) will have a string that holds two values - one for each. This is a little tricky,
so I'm going to show you how to do it with the 2008 dataset, and then you'll try it with the 2018 dataset."""

# First, let's get all the hybrids in 2008
hb_08 = df_08[df_08['fuel'].str.contains('/')]
hb_08

"""Looks like this dataset only has one! The 2018 has MANY more - but don't worry -
 the steps I'm taking here will work for that as well!"""

 # hybrids in 2018
hb_18 = df_18[df_18['fuel'].str.contains('/')]
hb_18

"""We're going to take each hybrid row and split them into two new rows - one with values for the first fuel type (values before the "/"), and the other with values for the second fuel type (values after the "/").
Let's separate them with two dataframes!"""

# create two copies of the 2008 hybrids dataframe
df1 = hb_08.copy()  # data on first fuel type of each hybrid vehicle
df2 = hb_08.copy()  # data on second fuel type of each hybrid vehicle

# Each one should look like this
df1

# columns to split by "/"
split_columns = ['fuel', 'air_pollution_score', 'city_mpg', 'hwy_mpg', 'cmb_mpg', 'greenhouse_gas_score']

# apply split function to each column of each dataframe copy
for c in split_columns:
    df1[c] = df1[c].apply(lambda x: x.split("/")[0])
    df2[c] = df2[c].apply(lambda x: x.split("/")[1])

# this dataframe holds info for the FIRST fuel type of the hybrid
# aka the values before the "/"s
df1

# this dataframe holds info for the SECOND fuel type of the hybrid
# aka the values after the "/"s
df2

# combine dataframes to add to the original dataframe
new_rows = df1.append(df2)

# now we have separate rows for each fuel type of each vehicle!
new_rows

# drop the original hybrid rows
df_08.drop(hb_08.index, inplace=True)

# add in our newly separated rows
df_08 = df_08.append(new_rows, ignore_index=True)

# check that all the original hybrid rows with "/"s are gone
df_08[df_08['fuel'].str.contains('/')]

df_08.shape

#Repeat this process for the 2018 dataset
# create two copies of the 2018 hybrids dataframe, hb_18
df1 = hb_18.copy()
df2 = hb_18.copy()

"""Split values for fuel, city_mpg, hwy_mpg, cmb_mpg
You don't need to split for air_pollution_score or greenhouse_gas_score
here because these columns are already ints in the 2018 dataset."""

# list of columns to split
split_columns = ['fuel', 'city_mpg', 'hwy_mpg', 'cmb_mpg']

# apply split function to each column of each dataframe copy
for c in split_columns:
    df1[c] = df1[c].apply(lambda x: x.split("/")[0])
    df2[c] = df2[c].apply(lambda x: x.split("/")[1])

    # append the two dataframes
new_rows = df1.append(df2)

# drop each hybrid row from the original 2018 dataframe
# do this by using pandas' drop function with hb_18's index
df_18.drop(hb_18.index, inplace=True)

# append new_rows to df_18
df_18 = df_18.append(new_rows, ignore_index=True)

# check that they're gone
df_18[df_18['fuel'].str.contains('/')]

df_18.shape

"""Now we can comfortably continue the changes needed for air_pollution_score! Here they are again:
2008: convert string to float
2018: convert int to float"""

# convert string to float for 2008 air pollution column
df_08['air_pollution']= df_08['air_pollution'].astype(float)

# convert int to float for 2018 air pollution column


df_08.to_csv('data_08_v4.csv', index=False)
df_18.to_csv('data_18_v4.csv', index=False)

# convert mpg columns to floats
mpg_columns = ['city_mpg', 'hwy_mpg', 'cmb_mpg']
for c in mpg_columns:
    df_18[c] = df_18[c].astype(float)
    df_08[c] = df_08[c].astype(float)

"""Fix greenhouse_gas_score datatype
2008: convert from float to int"""

# convert from float to int
df_08['greenhouse_gas_score'] = df_08['greenhouse_gas_score'].astype(int)

"""All the dataypes are now fixed! Take one last check to confirm all the changes."""
df_08.dtypes
df_18.dtypes

#to check that all columns are equal in data data types
df_08.dtypes == df_18.dtypes

# Save your final CLEAN datasets as new files!
df_08.to_csv('clean_08.csv', index=False)
df_18.to_csv('clean_18.csv', index=False)

#Exploring with visuals
df_08.hist(figsize=(8,8));
df_18.hist(figsize=(8,8));

combined_mpg_08= df_08['city_mpg']+ df_08['cmb_mpg']+ df_08['hwy_mpg']
combined_mpg_18= df_18['city_mpg']+ df_18['cmb_mpg']+ df_18['hwy_mpg']

combined_mpg_08.hist();
combined_mpg_18.hist();

df_08.plot(x='displ', y='cmb_mpg', kind='scatter');
df_18.plot( x='displ', y='cmb_mpg', kind='scatter');

df_08.plot(x='greenhouse_gas_score', y='cmb_mpg', kind='scatter');
df_18.plot(x='greenhouse_gas_score', y='cmb_mpg', kind='scatter');

#Q1: Are more unique models using alternative sources of fuel? By how much?
df_08.fuel.value_counts()
df_18.fuel.value_counts()
alt_08 = df_08.query('fuel in [\"CNG\", \"ethanol\"]').model.nunique()
alt_08
alt_18 = df_18.query('fuel in [\"Ethanol\", \"Electricity\"]').model.nunique()
alt_18

#Q2: How much have vehicle classes improved in fuel economy?
veh_08 = df_08.groupby('veh_class').cmb_mpg.mean()
veh_08
veh_18 = df_18.groupby('veh_class').cmb_mpg.mean()
veh_18

inc = veh_18 - veh_08
inc

#Q3: What are the characteristics of SmartWay vehicles? Have they changed over time?
df_08.smartway.unique()
smart_08 = df_08.query('smartway == \"yes\"')
smart_08.describe()
smart_18 = df_18.query('smartway in [\"Yes\", \"Elite\"]')
smart_18.describe()

#Q4: What features are associated with better fuel economy?
top_08 = df_08.query('cmb_mpg > cmb_mpg.mean()')
top_08.describe()
op_18 = df_18.query('cmb_mpg > cmb_mpg.mean()')
top_18.describe()

#Create combined dataset
# rename 2008 columns
df_08.rename(columns=lambda x: x[:10] + "_2008", inplace=True)
# view to check names
df_08.head()

# merge datasets
df_combined = df_08.merge(df_18, left_on= 'model_2008_2008',right_on= 'model', how='inner')

# view to check merge
df_combined.head()

#save the combined dataset
df_combined.to_csv('combined_dataset.csv', index=False)
df_combined.shape

#Q5: For all of the models that were produced in 2008 that are still being produced now,
# how much has the mpg improved and which vehicle improved the most?

"""1. Create a new dataframe, model_mpg, that contain the mean combined mpg values in 2008 and 2018 for each unique model
To do this, group by model and find the mean cmb_mpg_2008 and mean cmb_mpg for each."""

model_mpg = df.groupby('model').mean()[['cmb_mpg_20_2008', 'cmb_mpg']]
model_mpg.head()

"""2. Create a new column, mpg_change, with the change in mpg
Subtract the mean mpg in 2008 from that in 2018 to get the change in mpg"""

model_mpg['mpg_change'] = model_mpg['cmb_mpg'] - model_mpg['cmb_mpg_20_2008']
model_mpg.head()

"""3. Find the vehicle that improved the most
Find the max mpg change, and then use query or indexing to see what model it is!"""

max_change = model_mpg['mpg_change'].max()
max_change

model_mpg[model_mpg['mpg_change'] == max_change]
idx = model_mpg.mpg_change.idxmax()
idx
