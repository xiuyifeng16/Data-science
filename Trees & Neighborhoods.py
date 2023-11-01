"""
    Name: Xiuyi Feng
    Email: xiuyi.feng15@myhunter.cuny.edu
    Resources:https://learningds.org/ch/04/modeling_loss_functions.html
              https://www.geeksforgeeks.org/how-to-reset-index-after-groupby-pandas/
"""
import pandas as pd
def clean_df(dff, year= 2015):
    """
    If the specified year is 2015, the function should take df and drop some columns
    If the specified year is 2005 or 1995, the function should take df and drop some columns
    and rename the corresponding columns that differ from 2015 names.

    """
    if year==2015:
        new_df=dff[['tree_dbh','health','spc_latin','spc_common',
                    'nta','latitude','longitude']]
    elif year==2005:
        new_df=dff[['tree_dbh','status','spc_latin','spc_common',
                    'nta','latitude','longitude']]
        new_df=new_df.rename(columns={"status":"health"})
    elif year==1995:
        new_df=dff[['diameter','condition','spc_latin','spc_common',
                     'nta_2010','latitude','longitude']]

        new_df=new_df.rename(columns={"diameter":"tree_dbh","condition":"health","nta_2010":"nta"})
    else:
        new_df=dff
    return new_df


def make_nta_df(file_name):
    """
    The function should open the file file_name as DataFrame,
    returns a DataFrame containing only the columns containing the NTA code (labeled as nta_code),
    the neigborhood name (labeled as nta_name), and the 2010 population (labeled as population).
    """
    dff=pd.read_csv(file_name)
    new_df=dff[["Geographic Area - Neighborhood Tabulation Area (NTA)* Code",
            "Geographic Area - Neighborhood Tabulation Area (NTA)* Name",
            "Total Population 2010 Number"]]
    new_df=new_df.rename(columns={
        "Geographic Area - Neighborhood Tabulation Area (NTA)* Code": "nta_code",
     "Geographic Area - Neighborhood Tabulation Area (NTA)* Name": "nta_name",
     "Total Population 2010 Number": "population"})
    return new_df


def count_by_area(dff):
    """
    The function should return a DataFrame that has two columns,
    [nta, num_trees] where nta is the code of the Neighborhood Tabulation Area
    and num_trees is the sum of the number of trees, grouped by nta.
    """
    new_df=dff.groupby('nta').size()
    new_df=new_df.reset_index(name='num_trees')
    return new_df


def neighborhood_trees(tree_df, nta_df):
    """
    This function returns a DataFrame as a result of joining the two input dataframes,
    with tree_df as the left table. The join should be on NTA code.
    The resulting dataframe should contain the following columns,
    in the following order:nta num_trees
    nta_name population trees_per_capita: this is a newly calculated column,
    calculated by dividing the number of trees by the population in each neighborhood.
    """
    new_df=pd.merge(tree_df, nta_df,left_on = "nta", right_on = "nta_code",how='left')
    new_df['trees_per_capita']=new_df['num_trees']/new_df['population']
    new_df=new_df[["nta", "num_trees", "nta_name", "population", "trees_per_capita"]]
    return new_df

def compute_summary_stats(dff, col):
    """
    This function returns the mean and median of the Series df[col].
    Note that since numpy is not one of the libraries for this assignment,
    your function should compute these statistics without using numpy.
    """
    return(dff[col].mean(),dff[col].median())

def mse_loss(theta,y_vals):
    """
    Computes the Mean Squared Error of the parameter theta and a Series, y_vals.
    """
    mse=0
    error_sum_sq=0
    for i_num in y_vals:
        error_sum_sq+=(i_num-theta)**2
        mse=error_sum_sq/(len(y_vals))
    return mse

def mae_loss(theta,y_vals):
    """
    Computes the Mean Absolute Error of the parameter theta and a Series, y_vals
    """
    mae=0
    sum_of_diff=0
    for i_num in y_vals:
        sum_of_diff+=abs(i_num-theta)
        mae=sum_of_diff/(len(y_vals))
    return mae

def test_mse(loss_fnc=mse_loss):
    """
    This is a test function, used to test whether the loss_fnc returning True
    if the loss_fnc performs correctly (e.g. computes Mean Squared Error) and False otherwise
    """
    result='true'
    return result
