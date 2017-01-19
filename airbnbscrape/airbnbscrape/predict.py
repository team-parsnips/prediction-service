import json
import os
import numpy as np
import pandas as pd
import datetime as dt
from pprint import pprint
from sklearn import linear_model
from sklearn import metrics
from sklearn import ensemble
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

class Predict():

  def predict_price(self, params):
    cols = ['accuracy_rating',
            'amenities',
            'bed_type',
            'cancel_policy',
            'host_id',
            'hosting_id',
            'instant_book',
            'name',
            'nightly_price',
            'person_capacity',
            'price',
            'rating_checkin',
            'rating_cleanliness',
            'rating_communication',
            'response_rate',
            'response_time',
            'rev_count',
            'room_type',
            'satisfaction_guest',
            'url']

    # read scraped csv and then delete the csv
    df = pd.read_csv('./airbnb.csv', usecols=cols)
    # os.remove('./airbnb.csv')

    # filter for person_capacity
    df = df[df.person_capacity == params['person_capacity']]
    # filter for listings with 5+ reviews
    df = df[df.rev_count > 5]

    # get feature encoding for categorical variables
    bt_dummies = pd.get_dummies(df.bed_type)
    rt_dummies = pd.get_dummies(df.room_type)

    # replace the old columns with new one-hot encoded ones and drop unused columns
    # alldata = pd.concat((df.drop(['accuracy_rating', 'bed_type', 'room_type', 'url', 'host_id', 'hosting_id', 'nightly_price', 'amenities', 'response_time', 'name'], axis=1), bt_dummies.astype(int), rt_dummies.astype(int)), axis=1)
    alldata = df.drop(['accuracy_rating', 'bed_type', 'room_type', 'url', 'host_id', 'hosting_id', 'nightly_price', 'amenities', 'response_time', 'name'], axis=1)
    allcols = alldata.columns

    # printing a single row of data from the read data
    # print alldata.loc[3, :]

    # split data to training set
    X_train, X_test, y_train, y_test = train_test_split(alldata.drop(['price'], axis=1), alldata.price, test_size=0.4, random_state=20)

    n_est = 300

    tuned_parameters = {
        "n_estimators": [ n_est ],
        "max_depth" : [ 4 ],
        "learning_rate": [ 0.01 ],
        "min_samples_split" : [ 1.0 ],
        "loss" : [ 'ls', 'lad' ]
    }

    gbr = ensemble.GradientBoostingRegressor()
    clf = GridSearchCV(gbr, cv=3, param_grid=tuned_parameters,
            scoring='neg_median_absolute_error')
    preds = clf.fit(X_train, y_train)
    best = clf.best_estimator_

    # predict price based on characteristics
    raw_input = [params['instant_book'], 
                params['satisfaction_guest'], 
                params['person_capacity'], 
                params['rating_communication'], 
                params['rev_count'], 
                params['cancel_policy'], 
                params['rating_cleanliness'], 
                params['response_rate'], 
                params['rating_checkin']
                ]
    input_data = np.array(raw_input).reshape(1, -1)
    best_predicted = best.predict(input_data)
    print (np.array_str(best_predicted))
    return np.array_str(best_predicted)
