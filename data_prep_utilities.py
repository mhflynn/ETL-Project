###############################################################################
#
# This module is specific Kaggle mortality data set as of 2/1/19
# link - www.kaggle.com/cdc/mortality
#

###############################################################################
#
# Functions to confirm expected input for categorical JSON files for each year.
# Identifying the differences in the JSON files was a manual process, this 
# module captures those differences for review, confirms the differences and
# returns a single JSON file, i.e. a superset, applicable to all the data input.
#
# Current result returned is JSON for year 2015. If check has been run once
# without issues, no need to re-call this function, just use 2015 JSON
#
# Differences between all JSON files are enumerate and confirmed by modifying
# the values in each file such that all files have the same data. After modification,
# then each file is checked for equivalence, if equivlent, return a single JSON
# object to be used for the data categories. 
#
# Most differences between JSON files are whitespace and typo corrections. Remaining
# changes are addition or extension of categories or descriptions. There were no 
# deletions of categorical information.
#
# Two other modifications are made :
# 1) Key 'current_data_year is deleted, as no translation for the year data is needed
#    and is obviously different between each file
# 2) Considered deletion of key 'icd_code_10th_revision' as it has no information

import json
import os

###############################################################################
#
# Function to recursively check equivalence of nested dictionary/lists
#

def compare_seq(seq1, seq2, verbose=False) :

    if type(seq1)== dict and type(seq2)==dict :   # Input sequences are dictionaires
        keys1 = list(seq1.keys())
        keys2 = list(seq2.keys())
        if len(keys1) == len(keys2) :
            for key in keys1 :
                if key in keys2 :
                    if not(compare_seq(seq1[key], seq2[key])) :
                        if verbose : print(f'Compare failed {key}:{seq1[key]} - {seq2[key]}')
                        return False
                else :
                    if verbose : print(f'Key not found {key}:{keys2}')
                    return False
            return True
        else :
            if verbose : print(f'Key length not equal {len(keys1)}, {len(keys2)}')
            return False

    elif type(seq1)== list and type(seq1)==type(seq2) :
            if len(seq1)==len(seq2) :
                for l in seq1 :
                    if not(l in seq2) :
                        if verbose : print(f'List member not found {l}')
                        return False
                return True
            else :
                if verbose : print('List length not equal {len(seq1)}, {len(seq2)}')
                return False
    else :
        if seq1==seq2 :
            return True
        elif seq1!=seq1 and seq2!=seq2 :  # To accomodate nan equivalence
            return True
        else :
            return False

#################################################
#
# Read single JSON file input
# return single JSON object
# 
def read_code (path, year) :

    # Read JSON code for year 

    with open(os.path.join(path, str(year)+'_codes.json'), 'r') as f_in:
        result = json.load(f_in)
        del(result['current_data_year'])
    return result


#################################################
#
# Read in all JSON file input, return single JSON object
# 
def read_codes (path, verbose=False) :

    # Read JSON for each year for comparison, 
    # save objects in dictionary key'd by year
  
    d_json = {}
    for yr in range(2005, 2015+1) :
        read_code(path, yr)
        d_json[yr] = read_code(path, yr)

#        with open(os.path.join(path, str(yr)+'_codes.json'), 'r') as f_in:
#            d_json[yr] = json.load(f_in)
#            del(d_json[yr]['current_data_year'])
#        pass

    # Update JSON for years 2005 - 2009 to match 2010

    yrs_to_fix = range(2005, 2009+1)

    for yr in yrs_to_fix : 
        d_json[yr]['age_recode_27']['01']='Under 1 month (includes not stated weeks, days, hours, and minutes)'   # Add '... and minutes'
        d_json[yr]['age_recode_27']['03']='1 year'   # Was 'years'
        
        d_json[yr]['place_of_injury_for_causes_w00_y34_except_y06_and_y07_']['2']='School, other institution and public administrative area'   # Add ' area'

        d_json[yr]['race']['03']='American Indian (includes Aleuts and Eskimos)'   # Whitespace

        d_json[yr]['358_cause_recode']['001']='I.  Certain infectious and parasitic diseases (A00-B99)'   # Whitespace
    #   d_json[yr]['358_cause_recode']['156']='IV.  Endocrine, nutritional and metabolic diseases (E00-E88)'   # Whitespace
        d_json[yr]['358_cause_recode']['174']='V.  Mental and behavioral disorders (F01-F99)'   # Whitespace
    #   d_json[yr]['358_cause_recode']['185']='VI.  Diseases of the nervous system (G00-G98)'   # Whitespace
    #   d_json[yr]['358_cause_recode']['195']='VII.  Diseases of the eye and adnexa (H00-H57)'   # Whitespace
    #   d_json[yr]['358_cause_recode']['196']='VIII.  Diseases of the ear and mastoid process (H60-H93)'   # Whitespace
    #   d_json[yr]['358_cause_recode']['197']='IX.  Diseases of the circulatory system (I00-I99)'   # Whitespace
        d_json[yr]['358_cause_recode']['205']='Hypertensive diseases (I10-I15)'  # Was I13
        d_json[yr]['358_cause_recode']['208']='Hypertensive renal disease (I12,I15)'  # Was (I12)
        d_json[yr]['358_cause_recode']['247']='X.  Diseases of the respiratory system (J00-J98,U04)'  # Was (J00-J98)
        d_json[yr]['358_cause_recode']['252']='Other diseases of the respiratory system (J09-J98,U04)'  # Was (J09-J98)
        d_json[yr]['358_cause_recode']['253']='Influenza (J09-J11)'  # Was (J10-J11)
        d_json[yr]['358_cause_recode']['258']='Other acute lower respiratory infections (J20-J22,U04)'   # Was (J20-J22)
        d_json[yr]['358_cause_recode']['260']='Other and unspecified acute lower respiratory infection (J22,U04)'  # Waas (J22)
    #   d_json[yr]['358_cause_recode']['279']='XI.Diseases of the digestive system (K00-K92)'   # Whitespace
    #   d_json[yr]['358_cause_recode']['307']='XII.Diseases of the skin and subcutaneous tissue (L00-L98)'   # Whitespace
    #   d_json[yr]['358_cause_recode']['310']='XIII.  Diseases of the musculoskeletal system and connective tissue (M00-M99)'   # Whitespace
    #   d_json[yr]['358_cause_recode']['319']='XIV.Diseases of the genitourinary system (N00-N98)'   # Whitespace
    #   d_json[yr]['358_cause_recode']['339']='XV.Pregnancy, childbirth and the puerperium (O00-O99)'   # Whitespace
    #   d_json[yr]['358_cause_recode']['356']='XVI.Certain conditions originating in the perinatal period (P00-P96)'   # Whitespace
    #   d_json[yr]['358_cause_recode']['365']='XVII.  Congenital malformations, deformations and chromosomal abnormalities (Q00-Q99)'   # Whitespace
    #   d_json[yr]['358_cause_recode']['375']='XVIII.Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99)'   # Whitespace
        d_json[yr]['358_cause_recode']['381']='XX.External causes of mortality (*U01-*U03,V01-Y89)'   # Whitespace
        d_json[yr]['358_cause_recode']['384']='Railway accidents (V05,V15,V80.6,V81.2-V81.9)'   # *** Need to check this
        
        d_json[yr]['113_cause_recode']['069']='Essential (primary) hypertension and hypertensive renal disease (I10,I12,I15)'   # Was (I10,I12)
        d_json[yr]['113_cause_recode']['076']='Influenza and pneumonia (J09-J18)'   # Was (J10-J18)
        d_json[yr]['113_cause_recode']['077']='Influenza (J09-J11)'   # Was (J10-J18)
        d_json[yr]['113_cause_recode']['079']='Other acute lower respiratory infections (J20-J22,U04)'   # Was (J20-J22)
        d_json[yr]['113_cause_recode']['081']='Other and unspecified acute lower respiratory infection (J22,U04)'   # Was (J22)

        d_json[yr]['130_infant_cause_recode']['053']='Diseases of the respiratory system (J00-J98,U04)'   # Was (J00-J98)
        d_json[yr]['130_infant_cause_recode']['055']='Influenza and pneumonia (J09-J18)'   # Was (J10-J18)
        d_json[yr]['130_infant_cause_recode']['056']='Influenza (J09-J11)'   # Was (J10-J11)
        d_json[yr]['130_infant_cause_recode']['062']='Other and unspecified diseases of respiratory system (J22,J30-J39,J43-J44,J47-J68,J70-J98,U04)'   # Add (,U04)
        d_json[yr]['130_infant_cause_recode']['158']='Other external causes (X60-X84,Y10-Y36)'   # Added (X60-X84,)

        d_json[yr]['39_cause_recode']['023']='Essential (primary) hypertension and hypertensive renal disease (I10,I12,I15)'   # Was (I10,I12)
        d_json[yr]['39_cause_recode']['027']='Influenza and pneumonia (J09-J18)'   # Was (J10-J18)
        d_json[yr]['39_cause_recode']['037']='All other diseases (Residual) (A00-A09,A20-A49,A54-B19,B25-B99,D00-E07, E15-G25,G31-H93,I80-J06,J20-J39,J60-K22,K29-K66,K71-K72, K75-M99,N10-N15,N20-N23,N28-N98,U04)'   # Added (,U04)

    # Update JSON for years 2005 - 2010 to match 2011

    yrs_to_fix = range(2005, 2010+1) 

    for yr in yrs_to_fix : 
        d_json[yr]['358_cause_recode']['102']='Kaposi’s sarcoma (C46)'   # Was 'Kaposi=s', typo
        d_json[yr]['358_cause_recode']['194']='All other diseases of nervous system (G10-G14,G23-G25,G31,G36-G37,G43-G44,G47-G72,G81-G98)'   # Was (G10-G12, ...)
        d_json[yr]['113_cause_recode']['111']='All other diseases (Residual) (D65-E07,E15-E34,E65-F99,G04-G14,G23-G25,G31-H93, K00-K22,K29-K31,K50-K66,K71-K72,K75-K76,K83-M99, N13.0-N13.5,N13.7-N13.9, N14,N15.0,N15.8-N15.9,N20-N23,N28-N39,N41-N64,N80-N98)'   # Was (... ,G04-G12, ...)
    

    # Update JSON for years 2005 - 2013 to match 2014
    # Additional whitespace corrections

    yrs_to_fix = range(2005, 2013+1) 

    for yr in yrs_to_fix : 
        d_json[yr]['358_cause_recode']['156']='IV. Endocrine, nutritional and metabolic diseases (E00-E88)'   # Whitespace    
        d_json[yr]['358_cause_recode']['185']='VI. Diseases of the nervous system (G00-G98)'   # Whitespace    
        d_json[yr]['358_cause_recode']['195']='VII. Diseases of the eye and adnexa (H00-H57)'   # Whitespace    
        d_json[yr]['358_cause_recode']['196']='VIII. Diseases of the ear and mastoid process (H60-H93)'   # Whitespace    
        d_json[yr]['358_cause_recode']['197']='IX. Diseases of the circulatory system (I00-I99)'   # Whitespace  
        d_json[yr]['358_cause_recode']['279']='XI. Diseases of the digestive system (K00-K92)'   # Whitespace  
        d_json[yr]['358_cause_recode']['307']='XII. Diseases of the skin and subcutaneous tissue (L00-L98)'   # Whitespace  
        d_json[yr]['358_cause_recode']['310']='XIII. Diseases of the musculoskeletal system and connective tissue (M00-M99)'   # Whitespace  
        d_json[yr]['358_cause_recode']['319']='XIV. Diseases of the genitourinary system (N00-N98)'   # Whitespace 
        d_json[yr]['358_cause_recode']['339']='XV. Pregnancy, childbirth and the puerperium (O00-O99)'   # Whitespace 
        d_json[yr]['358_cause_recode']['356']='XVI. Certain conditions originating in the perinatal period (P00-P96)'   # Whitespace 
        d_json[yr]['358_cause_recode']['365']='XVII. Congenital malformations, deformations and chromosomal abnormalities (Q00-Q99)'   # Whitespace 
        d_json[yr]['358_cause_recode']['375']='XVIII. Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99)'   # Whitespace 


    # Fix outlier key in year 2012
    d_json[2012]['icd_code_10th_revision'] = d_json[2011]['icd_code_10th_revision']
    del d_json[2012]['icd_code_10']

    # Confirm JSON for each year are equivalent, after updates
    years = range(2005, 2015) 
    eq_agg = True

    for yr in years :
        equiv = compare_seq(d_json[yr], d_json[2015]) 
        if (not equiv) and verbose : print(f'JSON for years {yr} and 2015 are not equivalent')
        eq_agg &= equiv
    
    if eq_agg :
        return d_json[2015]
    else :
        if verbose : print('WARNING : Discrepencies found in JSON code data')
        return False



###############################################################################
#
# Functions to check coherency of input data and define replacements values for 
# cleaning the data. 

###############################################################################
#
# Function to confirm relacement columns/code keys and replacement values are
# found in the codes object
#

def check_replacement_codes(codes, replace_codes, verbose=False) :
    result = True
    code = list(codes.keys())

    for key in replace_codes :
        if (replace_codes[key][-1] != 'No code') :
            
            if not (key in code) :
                if verbose : print(f'Code not found {key}')
                result = False
                
            if (replace_codes[key][0] != 'None') and (replace_codes[key][0] != 'Drop') :
                valkey = replace_codes[key][0]
                if not (valkey in codes[key].keys()) :
                    if verbose : print(f'Replacement key not found : {key} : {valkey}')
                    result = False
                else :
                    repval = replace_codes[key][-1]
                    if codes[key][valkey] != repval :
                        if verbose : print(f'Replacement value not found : {key} : {valkey} : {repval}')
                
    return result

###############################################################################
#
# Function to confirm columns/code keys in replacement object are available 
# in the data frames. Use function check_df_columns() to confirm columns in
# each data frame are the same. Then this function only needs to be called for 
# for column set from one data frame. Alternatively it can be called for each.
#

def check_replacement_columns(cols, replace_codes, verbose=False) :
    result = True
    
    for key in replace_codes :
        if not (key in cols) :
            if verbose : print(f'Replacement key not in column list {key}')
            result = False
            
    keys = replace_codes.keys()
    for col in cols :
        if not (col in keys) :
            if verbose : print(f'Column not found in replacement key list {col}')
            result = False
    return result

###############################################################################
#
# Function to confirm column headings are same for each csv file
# Currently check assumes the order of columns is the same, consider
# change to confirm equivalence
#

def check_df_columns (data_dict, verbose=False) :
    result = True
    keys   = list(data_dict.keys())
    cols   = data_dict[keys[0]].columns
    
    for key in keys[1:] :
        chk = all(cols == data_dict[key].columns)
        if not chk :
            if verbose : print(f'Column mismatch {keys[0]} : {key}')
            result = False
    return result


###############################################################################
# Clean directive table, defines fillna and drop actions for data frames
# Assumption is column names match the code keys, if code exists for that column
# Dictionary keys are data column names, 
# list [0] replacement value, if any; 'None' for no replacement, 'Drop' for column drop
# list [1] if present, expected description for replacement code value or
#         'No code' is no associated code exists

# Define function to return clean directory to avoid clutter in .py file
def get_clean() :
    return {
        'resident_status'                     : ['None'], 
        'education_1989_revision'             : ['99',       'Not stated'],
        'education_2003_revision'             : ['9',        'Unknown'],
        'education_reporting_flag'            : ['2',        'no education item on certificate'],
        'month_of_death'                      : ['None'],
        'sex'                                 : ['None'],
        'detail_age_type'                     : ['None'],
        'detail_age'                          : ['None',     'No code'],
        'age_substitution_flag'               : ['Drop'],
        'age_recode_52'                       : ['52',       'Age not stated'],
        'age_recode_27'                       : ['27',       'Age not stated'],
        'age_recode_12'                       : ['12',       'Age not stated'],
        'infant_age_recode_22'                : ['Blank',    'Age 1 year and over or not stated'],
        'place_of_death_and_decedents_status' : ['9',        'Place of death unknown'],
        'marital_status'                      : ['U',        'Marital Status unknown'],
        'day_of_week_of_death'                : ['9',        'Unknown'],
        'current_data_year'                   : ['None',     'No code'],
        'injury_at_work'                      : ['U',        'Unknown'],
        'manner_of_death'                     : ['Blank',    'Not specified'],
        'method_of_disposition'               : ['U',        'Unknown'],
        'autopsy'                             : ['U',        'Unknown'],
        'activity_code'                       : ['9',        'During unspecified activity'],
        'place_of_injury_for_causes_w00_y34_except_y06_and_y07_' : ['9', 'Unspecified place'],
        'icd_code_10th_revision'              : ['None'],
        '358_cause_recode'                    : ['None'],
        '113_cause_recode'                    : ['None'],
        '130_infant_cause_recode'             : ['158',      'Other external causes (X60-X84,Y10-Y36)'],
        '39_cause_recode'                     : ['042',      'All other external causes (Y10-Y36,Y87.2,Y89)'],
        'number_of_entity_axis_conditions'    : ['None',     'No code'],
        'entity_condition_1'                  : ['0000',     'No code'],
        'entity_condition_2'                  : ['0000',     'No code'],
        'number_of_record_axis_conditions'    : ['None',     'No code'],
        'record_condition_1'                  : ['0000',     'No code'],
        'record_condition_2'                  : ['0000',     'No code'],
        'race'                                : ['00',       'Other races'],
        'bridged_race_flag'                   : ['Blank',    'Race is not bridged'],
        'race_imputation_flag'                : ['Blank',    'Race is not imputed'],
        'race_recode_3'                       : ['2',        'Races other than White or Black'],
        'race_recode_5'                       : ['None'],
        'hispanic_origin'                     : ['996-999',  'Unknown'],
        'hispanic_originrace_recode'          : ['9',        'Hispanic origin unknown'],
        'entity_condition_3'                  : ['Drop',     'No code'],
        'entity_condition_4'                  : ['Drop',     'No code'],
        'entity_condition_5'                  : ['Drop',     'No code'],
        'entity_condition_6'                  : ['Drop',     'No code'],
        'entity_condition_7'                  : ['Drop',     'No code'],
        'entity_condition_8'                  : ['Drop',     'No code'],
        'entity_condition_9'                  : ['Drop',     'No code'],
        'entity_condition_10'                 : ['Drop',     'No code'],
        'entity_condition_11'                 : ['Drop',     'No code'],
        'entity_condition_12'                 : ['Drop',     'No code'],
        'entity_condition_13'                 : ['Drop',     'No code'],
        'entity_condition_14'                 : ['Drop',     'No code'],
        'entity_condition_15'                 : ['Drop',     'No code'],
        'entity_condition_16'                 : ['Drop',     'No code'],
        'entity_condition_17'                 : ['Drop',     'No code'],
        'entity_condition_18'                 : ['Drop',     'No code'],
        'entity_condition_19'                 : ['Drop',     'No code'],
        'entity_condition_20'                 : ['Drop',     'No code'],
        'entity_condition_20'                 : ['Drop',     'No code'],
        'record_condition_3'                  : ['Drop',     'No code'],
        'record_condition_4'                  : ['Drop',     'No code'],
        'record_condition_5'                  : ['Drop',     'No code'],
        'record_condition_6'                  : ['Drop',     'No code'],
        'record_condition_7'                  : ['Drop',     'No code'],
        'record_condition_8'                  : ['Drop',     'No code'],
        'record_condition_9'                  : ['Drop',     'No code'],
        'record_condition_10'                 : ['Drop',     'No code'],
        'record_condition_11'                 : ['Drop',     'No code'],
        'record_condition_12'                 : ['Drop',     'No code'],
        'record_condition_13'                 : ['Drop',     'No code'],
        'record_condition_14'                 : ['Drop',     'No code'],
        'record_condition_15'                 : ['Drop',     'No code'],
        'record_condition_16'                 : ['Drop',     'No code'],
        'record_condition_17'                 : ['Drop',     'No code'],
        'record_condition_18'                 : ['Drop',     'No code'],
        'record_condition_19'                 : ['Drop',     'No code'],
        'record_condition_20'                 : ['Drop',     'No code'],
    }


###############################################################################
#
# if run from terminal, call function to check JSON files as test
#

if __name__ == '__main__' :
    read_codes('./', verbose=True)
