###############################################################################
#
# ETL Project - CDC Mortality Data from Kaggle
#
# Vannia Hernandez, Mark Flynn

import numpy as np
import pandas as pd
import json
import time
import os

import data_prep_utilities as utl

# Run control variables
check_codes = True   # Read JSON code files for each year and confirm known deltas
check_data  = True   # Confirm data column, code key and clean key/value validity
debug       = True   # Enable verbose print for check functions

start_yr = 2015      # Start year for data set time period
stop_yr  = 2015      # Stop year for data set period
nrows    = None      # Number of row to read for each data set. if None, all rows are read

db_block = 50000     # Block size of 50000 rows
db_chunk = 5000      # Chunk size of 5000 rows

data_path = './source_data/'

#######################################
#
# Extract ...
#
#######################################
print('\n\nEXTRACT ...')

# ### Read JSON Code files ...

# Read JSON code files for each year and confirm know deltas
# This step is not necessary if previous check passed, and no 
# further data changes have occured
print('Read JSON files ...')

if check_codes :
    codes = utl.read_codes(data_path, verbose=debug)
    if not codes : print('WARNING : Unknown discrepency in JSON code input')
        
# Otherwise, read target JSON code file for year 2015
else :
    codes = utl.read_code(data_path, '2015')


# ### Read the data for each year ...
print('Read data files ...')

# Read mortality data for each year into a data frame
data = {}
for yr in range(start_yr, stop_yr+1) :
    file = os.path.join(data_path, str(yr)+'_data.csv')
    data[yr] = pd.read_csv(file, nrows=nrows, dtype='object')

# Correct outlier column value in 2012 data set
if 2012 in range(start_yr, stop_yr) :
    data[2012].rename(columns={'icd_code_10':'icd_code_10th_revision'}, inplace=True)


#######################################
#
# Transform ...
#
#######################################
print('\nTRANSFORM ...')

# ### Check mapping between code and columns, and check validity of clean keys and values

# Check clean keys/values and data frame columns for any discrepency
# Expectation is all data frames have same columns, code keys have a
# corresponding column and clean keys/values are value code key/value
# pairs. Function calls 
print('Check data prior to clean operation ...')

clean = utl.get_clean()

if check_data :
    if not utl.check_df_columns(data, verbose=debug) :
        print('WARNING : Inconsistent columns between data frames')
    if not utl.check_replacement_codes(codes, clean, verbose=debug) :
        print('WARNING : Discrepency between code keys/values and clean keys/values')
    if not utl.check_replacement_columns(data[2015].columns, clean, verbose=debug) :
        print('WARNING : Discrepency between column names and clean keys')
        print('Check that clean operation run, if so, re-read data or ignore warning')


# ### Clean the data ...
print('Clean the data ...')

# Clean data frame data based on values in clean object
# Assumes data frames and replace values have been checked by running functions :
# check_df_columns(), check_replacement_codes() and check_replacement_columns()
#
# Build drop and fill lists (same for each data frame)
drop = [key for key in clean if clean[key][0]=='Drop']
fill = [{key:clean[key][0] for key in clean if (clean[key][0]!='Drop') and (clean[key][0]!='None')}][0]

# Apply drop and fill directives for each data frame
try :
    for yr in data.keys() :
        data[yr].drop(columns=drop, inplace=True)
        data[yr].fillna(fill, inplace=True)
        
except (KeyError) :
    print('KeyError : confirm full set of columns present in data or re-read data')

# Check for any remaining NaN values
na_cnt = [data[yr].isna().sum().sum() for yr in data.keys()]

if sum(na_cnt) != 0 :
    print(f'WARNING : Some NaN remaining in the date set : {na_cnt}')

#######################################
#
# Load ...
#
#######################################
print('\nLOAD ...')

import pymysql  #needed by sqlalchemy
from sqlalchemy import create_engine
from db_access import db_pwd
pymysql.install_as_MySQLdb()

# ### Create the tables
print('Create tables ...')

#Connect to the data base assumes "mortality" schema is present
eng = create_engine(f"mysql://root:{db_pwd}@localhost:3306/mortality?charset=utf8mb4")
eng.execute('USE mortality;')

# For this project, pick subset of columns / codes 
keepcols=['age_recode_52', 'age_recode_27', 'age_recode_12', 'infant_age_recode_22']

# Create a table per code in keepcols
for k in keepcols:
    q_cscodes= " CREATE TABLE  IF NOT EXISTS "+k+"( ckey VARCHAR(255) NOT NULL PRIMARY KEY, cvalue VARCHAR(1024) ); "
    eng.execute(q_cscodes)  

# Create the person table
q_cperson="CREATE TABLE  IF NOT EXISTS person( id INT PRIMARY KEY NOT NULL, "
for c in keepcols:
    q_cperson+=("fk_"+c+ " VARCHAR(255) DEFAULT '', ")
    q_cperson+=" CONSTRAINT cfk_"+c+" FOREIGN KEY (fk_"+c+") REFERENCES "+c+"(ckey) ON DELETE NO ACTION ON UPDATE CASCADE,"

q_cperson=q_cperson[:-1]
q_cperson+=");"

eng.execute(q_cperson)

# ### Populate the tables
print('Populate the tables')

#LOADING pcodes TABLE WITH QUERIES

for k in keepcols:
    thistable=codes.get(k)
    thiskeys=list(thistable.keys())
    thisvars=list(thistable.values())
    
    df=pd.DataFrame(thisvars,thiskeys, dtype=object)
    df.reset_index(inplace=True)
    df.columns=['ckey','cvalue']
    df.to_sql(k, eng,  if_exists='append', index=False)

#PERSON TABLE with age data

ddf = data[2015][keepcols].copy()
ddf.index.names=['id']
ddf.rename(columns={'age_recode_52':'fk_age_recode_52', 'age_recode_27':'fk_age_recode_27',
                    'age_recode_12':'fk_age_recode_12', 'infant_age_recode_22':'fk_infant_age_recode_22'},inplace=True)

start = time.time()
for i in range(0, ddf.shape[0], db_block) :
    ddf.iloc[i:i+db_block].to_sql('person', eng, if_exists='append', index=True, chunksize=db_chunk)
    print(f'Insert from {i}, {i+db_block-1} : {int(time.time()-start)} secs')
