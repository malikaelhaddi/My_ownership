# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from datetime import date
import csv
import os
import glob
import zipfile
import gdal
from collections import defaultdict

#uses the event ids stored for eq from a file in JAPAN_EQ Folder to download intensity shapefiles
input_file = "C:\\Users\\kumar.shivam\\Desktop\\27-05-2018\\Loss_History_Japan_EQ.csv" 
output_file = "C:\\Users\\kumar.shivam\\Desktop\\27-05-2018\\output3.csv"

row_inp = []
with open(input_file) as f:
    reader = csv.reader(f)
    for row in reader:
        row_inp.append(row)
              
row_data = []
with open('\\output.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        row_data.append(row)

row_data = row_data[1:]
        
row_inp = row_inp[1:]

selected_unique_id = {}
count = 0 
  
date_found = []
all_entered = []
      
for i in row_inp:
    dateraw = (i[3])
    dateraw = dateraw.split("/")
    dateraw0 = int(dateraw[0])
    dateraw1 = int(dateraw[1])
    dateraw2 = int(dateraw[2])
    all_entered.append(i[0])
    datetocheck = date(dateraw2,dateraw0,dateraw1)    
    for j in row_data:
        dateagainst = j[12]
        dateagainst = dateagainst.split("T")
        dateagainst = dateagainst[0]
        dateagainst = dateagainst.split("-")
        dateagainst0 = int(dateagainst[1])
        dateagainst1 = int(dateagainst[2])
        dateagainst2 = int(dateagainst[0])
        dateagainst = date(dateagainst2,dateagainst0,dateagainst1)
        deltadays = ((datetocheck - dateagainst).days) 
               
        if deltadays >=-10 and deltadays <= 2:
            selected_unique_id[count] = [j[92],i[0],j[12].split("T")[0].split("-")[0],i[1],i[2],j[12].split("T")[0]]
            date_found.append(i[0])
            count = count +1
            
datenotfound = list(set(all_entered) - (set(date_found) & set(all_entered)))
                                   
all_folders = os.listdir("C:\\Users\\kumar.shivam\\Desktop\\Yogesh\\EQ_datapicking")
all_folders = all_folders[0:8]

min_max_folder = []

for i in all_folders:
    min_max = i.split("_")
    min_max_folder.append([i,min_max[0],min_max[1]])
    
eq_raster_data = {}
              
for i in selected_unique_id:
    unique_id = selected_unique_id[i][0]
    year = selected_unique_id[i][2]
    if year >= min_max_folder[0][1] and year <= min_max_folder[0][2]:
        ypath = (min_max_folder[0][0])
    elif year >= min_max_folder[1][1] and year <= min_max_folder[1][2]:
        ypath = (min_max_folder[1][0])
    elif year >= min_max_folder[2][1] and year <= min_max_folder[2][2]:
        ypath = (min_max_folder[2][0])
    elif year >= min_max_folder[3][1] and year <= min_max_folder[3][2]:
        ypath = (min_max_folder[3][0])
    elif year >= min_max_folder[4][1] and year <= min_max_folder[4][2]:
        ypath = (min_max_folder[4][0])
    elif year >= min_max_folder[5][1] and year <= min_max_folder[5][2]:
        ypath = (min_max_folder[5][0])
    elif year >= min_max_folder[6][1] and year <= min_max_folder[6][2]:
        ypath = (min_max_folder[6][0])
    elif year >= min_max_folder[7][1] and year <= min_max_folder[7][2]:
        ypath = (min_max_folder[7][0])
    else:
        ypath = "nothing"
        
    final_path = "\\EQ_datapicking\\"+ypath+"\\"+unique_id+""
    if os.path.isdir(final_path):
        print(final_path)
        os.chdir(final_path)
        zip_path = (glob.glob(final_path+"//*.zip"))
        if len(zip_path) != 0:
            coord = (float(selected_unique_id[i][4]),float(selected_unique_id[i][3]))
            print(coord)
            with zipfile.ZipFile(zip_path[0],"r") as zip_ref:
                zip_ref.extractall(final_path)
            driver = gdal.GetDriverByName('GTiff')
            raster_files = ["\\mi.fit","\\pga.fit","\\pgv.fit","\\psa03.fit","\\psa10.fit","\\psa30.fit"]
            for rf in raster_files:
                data_id = unique_id +":"+ rf[1:len(rf)-4] + ":" + selected_unique_id[i][1] +":"+ selected_unique_id[i][5]
                filename = final_path+rf #path to raster
                dataset = gdal.Open(filename)
                band = dataset.GetRasterBand(1)
                
     
# picking up data on the coordinates defined by the input files
                            
                cols = dataset.RasterXSize
                rows = dataset.RasterYSize
                unique_id
                transform = dataset.GetGeoTransform()
                try:
                
                    xOrigin = transform[0]
                    yOrigin = transform[3]
                    pixelWidth = transform[1]
                    pixelHeight = -transform[5]
                    
                    data = band.ReadAsArray(0, 0, cols, rows)
                
                    
                    points_list = [ coord ] #list of X,Y coordinates
                    
                    for point in points_list:
                        col = int((point[0] - xOrigin) / pixelWidth)
                        row = int((yOrigin - point[1]) / pixelHeight)            
                        print(row,col, data[row][col])
                        eq_raster_data[data_id] = (data[row][col])
                except Exception as e:
                    eq_raster_data[data_id] = "NA"

sorted_data = defaultdict(list)

for i in eq_raster_data:
    sorted_data[i.split(":")[2]].append([i,eq_raster_data[i]])
    
    

lengthi = 0
for i in sorted_data.keys():
    length_f = (len(sorted_data[i]))
    if length_f > lengthi:
        stored = i
        
 
column = ['ID', 'Lat', 'Lon', 'Date','Event_ID','Event_Date']  
     
for i in range(len(sorted_data[stored])):
    
    if sorted_data[stored][i][0].split(":")[1] in column and sorted_data[stored][i][0].split(":")[1] == 'mi':
        column.append('Event_ID')
        column.append('Event_Date')
    column.append(sorted_data[stored][i][0].split(":")[1])
    
    
no_date = [] 
check =[]
    
with open(input_file,'r') as csvinput:
    with open(output_file, 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        writer.writerow(column)
        for row in csv.reader(csvinput):
            
            print(row)
            for keyi in sorted_data.keys():
                if row[0] == keyi:
                    final_rows = []
                    
                    for z in range(len(sorted_data[keyi])):
                        id_sort = sorted_data[keyi][z][0].split(":")[0]
                        date_sorted1 = sorted_data[keyi][z][0].split(":")[3]
                        if id_sort not in final_rows:
                            final_rows.append(id_sort)
                            final_rows.append(date_sorted1)
                        final_rows.append(sorted_data[keyi][z][1])   
                    writer.writerow(row+final_rows)  
                    
                else:
                    for i in datenotfound:
                        if i == row[0]:                            
                            if row not in check:
                                check.append(row)
                                writer.writerow(row)
                            

                    
