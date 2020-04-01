# -*- coding: utf-8 -*-
"""
Created on Tue May 28 18:16:27 2019

@author: DevonKohler
"""

import pandas as pd
import numpy as np
import os, time
from urllib.request import urlopen
from bs4 import BeautifulSoup


def main():
    
    ids = pd.read_csv('master.csv' , encoding='latin-1').loc[:, 'fg_id']
    strings = list()
    nums = list()
    
    ids = [x for x in ids if not isinstance(x, float)]
    
    for x in ids:

        print(x)
        if 's' in x:
            strings.append(x)
        elif x == '':
            print('blank')
        else:
            nums.append(x)
            
    nums = [int(x) for x in nums]
    all_ids = [x for x in range(max(nums))]
    [all_ids.append(x) for x in strings]
    
    
    con_list = list()
    broken = list()
    
    ## Loop over all player ids
    for id in all_ids:
        
        ## Some dont exist
        try:
            
            ## Connect to page
            page = urlopen(r'https://www.fangraphs.com/statsd.aspx?playerid={0}&position=PB&type=1&gds=&gde=&season=all'.format(str(id)))
            soup = BeautifulSoup(page, 'html.parser')
            
            ## Find table
            table = soup.find('div', attrs={'id' : 'DailyStats1_dgSeason1'})
            table_body = table.find('tbody')
            
            ## Loop over table and collect data
            data = list()
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            
            ## Create dataframe
            try:
                
                df = pd.DataFrame(data[2:], columns=data[1])
    
                df.loc[:, 'pid'] = id
    
                ## Update datatypes
                df = df.loc[df['Date'] != 'Date']
                df['Date'] = pd.to_datetime(df['Date'])
                for col in df.iloc[:, 5:].columns:
                    df[col] = pd.to_numeric(df[col])
    
                df['BO'] = pd.to_numeric(df['BO'])
    
                ## Append for concat
                con_list.append(df)
    
                if id % 100 == 0:
                    print(id, len(df))
                
            except:
                print(id, data)
                    
        except:
            print(id)
            broken.append(id)
            
        time.sleep(2)
     
    
    df = pd.concat(con_list)
    
    df.to_csv('batter_raw.csv')
    
if __name__ == '__main__':
    main()