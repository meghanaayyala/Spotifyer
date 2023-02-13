import pandas as pd
import numpy as np
import re
df=pd.read_csv('tomvdata.csv')

##filtering title column in df

marks_list = df['title'].tolist()
artist=[]
track=[]
for title in marks_list:
    
    splittitle=title.split(' - ')
    print(splittitle)
    if(len(splittitle)>1):
        artist.append(splittitle[0])
        track.append(splittitle[1])
    

newdf= pd.DataFrame(list(zip(artist, track)),
               columns =['artist', 'track'])

newdf.to_csv('artisttrack.csv')