"""
    Name: Xiuyi Feng
    Email: xiuyi.feng15@myhunter.cuny.edu
    Resources: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html
               for rename function
               https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
               for iterate over rows in dataframe in pandas
               https://stackoverflow.com/questions/12096252/use-a-list-of-values-to-select-rows-from-a-pandas-dataframe
               for Use a list of values to select rows from a Pandas dataframe(.isin()function)
"""

def clean_df(dff, year= 2015):
    """
    If the specified year is 2015, the function should take df and drop some columns
    If the specified year is 2005 or 1995, the function should take df and drop some columns
    and rename the corresponding columns that differ from 2015 names.

    """
    if year==2015:
        new_df=dff[['tree_dbh','health','spc_latin','spc_common','address',
                    'zipcode','boroname','nta','latitude','longitude',
                    'council_district', 'census_tract']]
    elif year==2005:
        new_df=dff[['tree_dbh','status','spc_latin','spc_common','address',
                    'zipcode','boroname','nta','latitude',
                    'longitude','cncldist', 'census_tract']]
        new_df=new_df.rename(columns={"status":"health","cncldist":"council_district"})
    elif year==1995:
        new_df=dff[['diameter','condition','spc_latin','spc_common','address',
                     'zip_original','borough','nta_2010','latitude',
                     'longitude','council_district','censustract_2010']]

        new_df=new_df.rename(columns={"diameter":"tree_dbh","condition":"health",
                                       "zip_original":"zipcode","borough":"boroname",
                                       "nta_2010":"nta","censustract_2010":"census_tract"})
    else:
        new_df=dff
    return new_df

def filter_health(dff, keep):
    """
    The function returns the DataFrame with only rows that
    where the column health contains a value from the list keep.
    All rows where the health column contains a different value are dropped.

    """
    new_df=dff[dff['health'].isin(keep)]
    return new_df

def add_indicator(row):
    """
    The function should return 1 if health is not Poor and
    tree_dbh is larger than 10. Otherwise, it should return 0.

    """
    if row.tree_dbh<=10 and row.health!='poor':
        return 0
    return 1

def find_trees(dff, species):
    """
    The function should return, as a list, the address for all trees of that species in spc_latin.
    If that species does not occur in the DataFrame, then an empty list is returned.
    """
    new_df=dff[dff["spc_latin"] == species]
    a_list=new_df['address'].tolist()
    return a_list

def count_by_area(dff, area = "boroname"):
    """
    The function should return the sum of the number of trees, grouped by area.
    your function should group by boroname and
    return the number of each trees in each of the boroughs.
    """
    total_tree=dff.groupby(area).size()
    return total_tree
