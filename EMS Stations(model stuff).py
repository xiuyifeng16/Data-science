"""
    Name: Xiuyi Feng
    Email: xiuyi.feng15@myhunter.cuny.edu
    Resources:
            https://www.geeksforgeeks.org/select-rows-that-contain-specific-text-using-pandas/
            https://stackoverflow.com/questions/17071871/how-do-i-select-rows-from-
            a-dataframe-based-on-column-values
            https://www.gradescope.com/courses/403327/assignments/2825519/submissions/176501909?view=files
            
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.cluster import AgglomerativeClustering

def make_df(file_name):
    """
       The data is read into a DataFrame. Rows that are have null
       values for the type description, incident date, incident time,
       latitute and longitude are dropped. Only rows that contain AMBULANCE
       as part of the TYP_DESC are kept. The resulting DataFrame is returned. 
    """
    dff = pd.read_csv(file_name)
    dff = dff.dropna(subset=["TYP_DESC", "INCIDENT_DATE", "INCIDENT_TIME", "Latitude", "Longitude"])
    dff = dff[dff["TYP_DESC"].str.contains("AMBULANCE")]
    return dff


def add_date_time_features(dff):
    """
        An additional column WEEK_DAY is added with the day of the week
        (0 for Monday, 1 for Tuesday, ..., 6 for Sunday) of the date in
        INCIDENT_DATE is added. Another column, INCIDENT_MIN, that takes
        the time from INCIDENT_TIME and stores it as the number of minutes
        since midnight. The resulting DataFrame is returned.
    """
    dff["INCIDENT_DATE"] = pd.to_datetime(dff["INCIDENT_DATE"])
    dff["WEEK_DAY"] = dff["INCIDENT_DATE"].dt.dayofweek
    dff["INCIDENT_TIME"] = pd.to_timedelta(dff["INCIDENT_TIME"])
    dff["INCIDENT_MIN"] = dff["INCIDENT_TIME"].dt.total_seconds() / 60
    return dff

def filter_by_time(dff, days=None, start_min=0, end_min=1439):
    """
        Returns a DataFrame with entries restricted to weekdays in days
        (or all weekdays if None is given) and incident times in [start_min, end_min]
        inclusive (e.g. contains the endpoints).

    """
    if days is None:
        days = [0,1,2,3,4,5,6]
    dff = dff[dff["WEEK_DAY"].isin(days)]
    dff = dff[(dff["INCIDENT_MIN"] >= start_min) & (dff["INCIDENT_MIN"] <= end_min)]
    return dff

def compute_kmeans(dff, num_clusters = 8, n_init = 'auto', random_state = 2022):
    """
        Runs the KMeans model with num_clusters on the latitude and
        longitude data of the provided DataFrame. Returns the cluster
        centers and predicted labels computed via the model.
    """
    kmx = dff[["Latitude", "Longitude"]].values
    kmeans = KMeans(n_clusters=num_clusters, random_state=random_state, n_init=n_init).fit(kmx)
    return kmeans.cluster_centers_,kmeans.labels_

def compute_gmm(dff, num_clusters = 8, random_state = 2022):
    """
        Runs the GaussianMixture model with num_clusters on the
        latitude and longitude data of the provided DataFrame.
        Returns the array of the predicted labels computed via the model.
    """
    gmx = dff[["Latitude", "Longitude"]].values
    gmm = GaussianMixture(n_components=num_clusters, random_state=random_state).fit(gmx)
    return gmm.predict(gmx)

def compute_agglom(dff, num_clusters = 8, linkage='ward'):
    """
        Runs the Agglomerative model with num_clusters on the
        latitude and longitude data of the provided DataFrame
        and default linkage (i.e. ward). Returns the array of
        the predicted labels computed via the model.
    """
    agx = dff[["Latitude", "Longitude"]].values
    agg=AgglomerativeClustering(n_clusters=num_clusters, linkage = linkage).fit(agx)
    return agg.labels_

def compute_explained_variance(dff, K =[1,2,3,4,5], random_state = 55):
    """
        Returns a list of the sum of squared distances of samples
        to their closest cluster center for each value of K. This
        can be computed manually or via the inertia_ attribute of
        the KMeans model.
    """
    variances = []
    vax = dff[["Latitude", "Longitude"]].values
    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=random_state).fit(vax)
        variances.append(kmeans.inertia_)
    return variances
     