"""
    Name: Xiuyi Feng
    Email: xiuyi.feng15@myhunter.cuny.edu
    Resources:
            https://www.geeksforgeeks.org/capitalize-first-letter-of-a-column-in-pandas-dataframe/
            (capitalized)
            https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html(drop)
            https://www.tutorialsteacher.com/python/string-isnumeric(isnumeric())
            https://www.geeksforgeeks.org/python-program-to-check-if-string-is-empty-or-not/
            (string empty or not)
            https://favtutor.com/blogs/capitalize-first-letter-python(str.title format)
            https://stackoverflow.com/questions/18689823/pandas-dataframe-replace-nan-values-with-average-of-columns
            (fill null value with mean of that column)
            https://stackoverflow.com/questions/466345/convert-string-jun-1-2005-133pm-into-datetime
"""

import pandas as pd

def make_dog_df(license_file,zipcode_file):
    "The function opens the two inputted files and do some change to these two file and merge them"
    df1=pd.read_csv(license_file)
    df2=pd.read_csv(zipcode_file)

    df1['AnimalName']=df1['AnimalName'].str.capitalize()
    df1=df1.drop(columns=['LicenseExpiredDate','Extract Year'])
    new_df=pd.merge(df1,df2,left_on="ZipCode",right_on="zip",how="left")
    new_df=new_df.rename(columns={'borough':'Borough'})
    new_df=new_df.dropna(subset=['Borough'])
    new_df=new_df[["AnimalName", "AnimalGender", "AnimalBirthYear",
                     "BreedName", "ZipCode", "LicenseIssuedDate", "Borough"]]

    return new_df

def make_bite_df(file_name):
    """
    The function should open the file file_name as DataFrame,
    dropping the Species column. The resulting DataFrame is returned.
    """

    dff=pd.read_csv(file_name)
    dff=dff.drop(columns=['Species'])
    return dff


def clean_age(age_str):
    """
    age_strage_str ends in a M, return the rest of the string as a number in years.
    age_strage_strends in a Y, return the rest of the string as a number
    age_str contains only a number, return it as a number.
    For all other values, return None
    """
    if age_str[-1]=='Y':
        return float(age_str[:-1])
    if age_str[-1]=='M':
        return float(age_str[:-1])/12.0
    if age_str.isnumeric():
        return float(age_str)
    return None

def clean_breed(breed_str):
    """
    If breed_str is empty, return "Unknown".Otherwise,return the string in title
    format with each word in the string capitalized and all other letters lower case
    """
    if len(breed_str)==0:
        return "Unknown"

    return str.title(breed_str)


def impute_age(dff):
    """
    Function should replace any missing values in the df['Age Num']
    column with the median of the values of the column
    """
    dff['Age Num']=dff['Age Num'].fillna((dff['Age Num'].mean()))

    return dff


def impute_zip(boro, zipcode):
    """
    If the zipcode column is empty, impute the value with the zip code
    of the general delivery post office based on value of boro
    """
    if zipcode=="" or pd.isnull(zipcode):
        if boro=='Bronx':
            zipcode='10451'
        elif boro=='Brooklyn':
            zipcode='11201'
        elif boro=='Manhattan':
            zipcode='10001'
        elif boro=='Queens':
            zipcode='11431'
        elif boro=='Staten Island':
            zipcode='10341'
        else:
            zipcode=None
    return zipcode


def parse_datetime(dff, column='LicenseIssuedDate'):
    """
    The function should return a DataFrame with three additional columns:timestamp,month,day_of_week
    """
    dff['timestamp']=pd.to_datetime(dff[column])
    dff['month']=dff['timestamp'].dt.month
    dff['day_of_week']=dff['timestamp'].dt.dayofweek
    return dff
