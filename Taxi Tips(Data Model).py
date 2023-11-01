"""
    Name: Xiuyi Feng
    Email: xiuyi.feng15@myhunter.cuny.edu
    Resources:
                https://stackoverflow.com/questions/71254492/how-to-delete-any-row-
                for-which-a-corresponding-column-has-a-negative-value-usin
                https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
                https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html
                https://www.sharpsightlabs.com/blog/pandas-get-dummies/
                https://medium.com/@maziarizadi/pickle-your-model-in-python-2bbe7dba2bbb
                https://www.analyticsvidhya.com/blog/2021/08/quick-hacks-to-save-machine-learning-model-using-pickle-and-joblib/
"""
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def import_data(file_name):
    """
        The data in the file is read into a DataFrame.The columns: VendorID,RatecodeID,
        store_and_fwd_flag,payment_type,extra,mta_tax,tolls_amount,improvement_surcharge,
        congestion_surcharge are dropped. Any rows with non-positive total_amount are dropped.
    """
    dff=pd.read_csv(file_name)
    dff=dff.drop(columns=["VendorID","RatecodeID","store_and_fwd_flag","payment_type","extra",
                         "mta_tax","tolls_amount","improvement_surcharge","congestion_surcharge"])
    dff=dff.drop(dff.index[dff['total_amount']<=0])
    return dff


def add_tip_time_features(dff):
    """
        percent_tip: which is 100*tip_amount/(total_amount-tip_amount)
        duration: the time the trip took in seconds.
        dayofweek: the day of the week that the trip started
    """
    dff['percent_tip']=100*dff['tip_amount']/dff['total_amount']-dff['tip_amount']
    dff['timestamp1']=pd.to_datetime(dff['tpep_pickup_datetime'])
    dff['timestamp2']=pd.to_datetime(dff['tpep_dropoff_datetime'])
    dff["duration"] =(dff['timestamp2'] - dff['timestamp1']).dt.total_seconds()
    dff['dayofweek']=dff['timestamp1'].dt.dayofweek
    dff=dff.drop(columns=['timestamp1','timestamp2'])
    return dff


def impute_numeric_cols(dff):
    """
        Missing data in the numeric columns passenger_count,trip_distance,fare_amount,
        tip_amount,total_amount,duration,dayofweek are replaced with the median
        of the respective column.
    """
    dff['passenger_count']=dff['passenger_count'].fillna((dff['passenger_count'].median()))
    dff['trip_distance']=dff['trip_distance'].fillna((dff['trip_distance'].median()))
    dff['fare_amount']=dff['fare_amount'].fillna((dff['fare_amount'].median()))
    dff['tip_amount']=dff['tip_amount'].fillna((dff['tip_amount'].median()))
    dff['total_amount']=dff['total_amount'].fillna((dff['total_amount'].median()))
    dff['duration']=dff['duration'].fillna((dff['duration'].median()))
    dff['dayofweek']=dff['dayofweek'].fillna((dff['dayofweek'].median()))
    return dff


def add_boro(dff, file_name) -> pd.DataFrame:
    """
        Makes a DataFrame, using file_name, to add pick up and drop off boroughs to df.
        In particular, adds two new columns to the df:
    """
    zones_df = pd.read_csv(file_name)
    dff = pd.merge(dff, zones_df[["LocationID", "borough"]], left_on =
    "PULocationID", right_on = "LocationID", how = "left")
    dff.rename(columns={"borough": "PU_borough"}, inplace = True)
    dff = pd.merge(dff, zones_df[["LocationID", "borough"]],
    left_on = "DOLocationID", right_on = "LocationID", how = "left")
    dff.rename(columns={"borough": "DO_borough"}, inplace = True)
    dff.drop(columns = ['LocationID_x', 'LocationID_y'], inplace=True)
    return dff


def encode_categorical_col(col,prefix):
    """
        Takes a column of categorical data and uses categorical encoding to
        create a new DataFrame with the k-1 columns,
        where k is the number of different nomial values for the column.
        Your function should create k columns,one for each value, labels by the prefix
        concatenated with the value.The columns should be sorted and the DataFrame
        restricted to the first k-1 columns returned.
    """
    sub = pd.get_dummies(col, prefix = prefix, prefix_sep="")
    return sub.iloc[:, :-1]


def split_test_train(dff, xes_col_names, y_col_name, test_size=0.25, random_state=1870):
    """
        Calls sklearn's train_test_split function to split the data
        set into a training and testing subsets:
        x_train, x_test, y_train, y_test. The resulting 4 subsets are returned.
    """
    xes = dff[xes_col_names]
    yes = dff[y_col_name]
    x_train, x_test, y_train, y_test = train_test_split(xes, yes,
                                                        test_size, random_state)
    return x_train, x_test, y_train, y_test


def fit_linear_regression(x_train, y_train):
    """
    Fits a linear model to x_train and y_train, using sklearn.linear_model.LinearRegression
    The resulting model should be returned as bytestream, using pickle
    """
    reg = LinearRegression().fit(x_train, y_train)
    reg_pickle = pickle.dumps(reg)
    return reg_pickle

def predict_using_trained_model(mod_pkl, xes, yes):
    """
        Computes and returns the mean squared error and r2 score
        between the values predicted by the model
        (mod_pkl on x) and the actual values (y).
    """
    with open(mod_pkl, 'rb') as model_f:
        lr1 = pickle.load(model_f)
    prediction = lr1.predict(xes)
    mse = mean_squared_error(yes, prediction)
    r2_s = r2_score(yes, prediction)
    return mse, r2_s
