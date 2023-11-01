"""
    Name: Xiuyi Feng
    Email: xiuyi.feng15@myhunter.cuny.edu
    Resources:
            https://www.digitalocean.com/community/tutorials/loss-functions-in-python
            (mse_loss and rmse loss)
            https://stackoverflow.com/questions/53690587/how-to-get-the-difference-between-first-row-and-current-row-in-pandas
            https://stackoverflow.com/questions/54573056/pandas-dataframe-groupby-apply-several-lambda-functions-at-once(diff)
"""

import pandas as pd
import numpy as np

def parse_datetime(dff, column='DATE'):
    """
        The function should return a DataFrame with three additional columns:timestamp,month,year
    """
    dff['timestamp']=pd.to_datetime(dff[column])
    dff['month']=dff['timestamp'].dt.month
    dff['year']=dff['timestamp'].dt.year
    return dff


def compute_lin_reg(xes, yes):
    """
        The function computes the slope and y-intercept of the linear regression line,
        using ordinary least squares
    """
    sd_x=np.std(xes)
    sd_y=np.std(yes)
    correlation=np.corrcoef(xes,yes)[0,1]
    theta_1 = correlation*sd_y/sd_x
    theta_0 = yes.mean()- theta_1 * xes.mean()
    return theta_0, theta_1

def predict(xes, theta_0, theta_1):
    """
        The function returns the predicted values of the dependent variable, xes,
        under the linear regression model with y-intercept theta_0 and slope theta_1.
    """
    prediction=[]
    for index in xes:
        yes=theta_1*index+theta_0
        prediction.append(yes)
    return prediction


def mse_loss(y_actual,y_estimate):
    """
        The function returns the mean square error loss function between y_actual and y_estimate
    """
    diff = y_estimate - y_actual
    differences_squared = diff ** 2
    mean_diff = differences_squared.mean()

    return mean_diff


def rmse_loss(y_actual,y_estimate):
    """
        The function returns the square root of the mean square error
        loss function between y_actual and y_estimate
    """
    diff = y_estimate - y_actual
    differences_squared = diff ** 2
    mean_diff = differences_squared.mean()
    rmse_val = np.sqrt(mean_diff)
    return rmse_val

def compute_error(y_actual,y_estimate,loss_fnc=mse_loss):
    """
        The result of computing the loss_fnc on the inputs y_actual and y_estimate is returned.
    """
    return loss_fnc(y_actual,y_estimate)

def compute_ytd(dff):
    """
        The function returns a Series with the number of
        jobs since the beginning of the year for that entry.
    """
    dff['diff']=dff.groupby("year")["USINFO"].transform(lambda x: x - x.iloc[0])
    return dff['diff']

def compute_year_over_year(df):
    """
        Computes and returns a Series with the percent change from the previous year for USINFO.
    """
    df['year_over_year']=df['USINFO'].pct_change(periods=12)*100
    return df['year_over_year']
