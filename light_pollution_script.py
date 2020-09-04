# -*- coding: utf-8 -*-
"""
@author: MauricioMani
"""
import gdal as gd
import numpy as np
import rasterio
import pandas as pd

file = gd.Open("your_Tiff_file_here") # A GeoTiff file
dataset = rasterio.open("yourTiff_file_here")
greyscale = dataset.read(1)

def coord(file):
    padfTransform = file.GetGeoTransform()
    indices = np.indices(file.ReadAsArray().shape)
    
    pad_transform_zero = padfTransform[0]
    pad_transform_one = indices[1]*padfTransform[1]
    pad_transform_two =  indices[1]*padfTransform[2]  
    
    pad_transform_three = padfTransform[3]
    pad_transform_four = indices[0]*padfTransform[4]
    pad_transform_five = indices[0]*padfTransform[5]
    
    xp = pad_transform_zero + pad_transform_one + pad_transform_two
    yp = pad_transform_three + pad_transform_four + pad_transform_five
    
    return xp,yp

#xp: longitude
#yp: latitude
xp,yp = coord(file)

def lights_info():
    position = 0
    position2 = 0
    lights = []
    for i in greyscale:
        for e in i:
            if e > 0:
                lights.append((position, position2))
            position2 += 1
        position2 = 0
        position += 1
    return(lights)

lights = lights_info()

latitud = []
position = 0
for i in yp:
  if i[0] >= 12.211404 and i[0] <= 32.621072:
    latitud.append(position)
    position += 1
  else:
    position += 1
    
longitud = []
position = 0
for i in xp[0]:
  if i >= -119.850663 and i <= -80.355462:
    longitud.append(position)
    position += 1
  else:
    position += 1
    
lat_lon = []
for i in latitud:
  lat = yp[i][0]
  for e in longitud:
    lon = xp[0][e]
    position = [i, e]
    lat_lon.append([lat, lon, position])
  
lights = []
for i in lat_lon:
  pos = i[2]
  light = greyscale[pos[0]][pos[1]]
  lights.append(light)  

index = 0
for i in lat_lon:
  i.append(lights[index])
  index += 1

light_pollution = pd.DataFrame(lat_lon, columns = ['latitud', 'longitud', 
                                                   'position_tif', 'light'])

light_pollution.to_csv("light_pollution.csv", index = False)

#Further, you can print your locations light pollution
