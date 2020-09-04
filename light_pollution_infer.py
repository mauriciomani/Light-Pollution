# -*- coding: utf-8 -*-
"""
@author: MauricioMani
"""

#This script helps infer long coordinates.

from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
import numpy as np

luminosity = pd.read_csv('your_luminosity.csv')
luminosity = luminosity[(luminosity.light>5) & (luminosity.light<=350)]
luminosity['nano_centroid']= luminosity.latitud.apply(lambda x: str(round(x,5))) + luminosity.longitud.apply(lambda x: str(round(x,5)))

_lat_lon_train = np.array(luminosity[['latitud', 'longitud']])
_lum_train = np.array(luminosity['light'])

knn = KNeighborsRegressor(n_neighbors=3, metric='haversine')
knn.fit(X =_lat_lon_train, y= _lum_train)

#change _lat_lon_train for your numpy array with latitutde and longitude.
light_predictions = knn.predict(_lat_lon_train)

