# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:42:16 2020

@author: DevonKohler
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np
import smtplib

import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm
from scipy.interpolate import interp1d

from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

def main():
    
    
    page = urlopen(r'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Massachusetts')
    soup = BeautifulSoup(page, 'html.parser')
    
    table = soup.find('table', attrs = {'class' : 'wikitable mw-datatable sortable'})
    table_body = table.find('tbody')
    
    soup.find(lambda tag: tag.name=='table' and tag.has_attr('class'))
    
    data = list()
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    
    ## Transform into usable data
    df = pd.DataFrame(data[2:], columns=['Date', 'Confirmed', 'Cases',4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    df = df.loc[:, ['Date', 'Cases']]
    df = df.loc[~df['Date'].isin(['...', 'February 1', 'March 2'])]
    df = df.loc[~pd.isnull(df['Date'])]
    df.loc[:, 'Cases'] = df.loc[:, 'Cases'].apply(lambda x: int(x.replace('+', '')))
    df.loc[:, 'Date'] = pd.to_datetime(df.loc[:, 'Date'].apply(lambda x: x + ', 2020'))
    df.set_index('Date', inplace = True)
    
    ## Model with LOWESS
    lowess = sm.nonparametric.lowess(df.loc[:, 'Cases'], np.arange(0, len(df)), frac = .33)
    lowess_x = list(list(zip(*lowess))[0])
    lowess_y = list(list(zip(*lowess))[1])

# =============================================================================
#     ## Quadratic Regression
#     poly = PolynomialFeatures(degree=3)
#     X_ = poly.fit_transform(np.arange(len(df)).reshape(-1, 1))
#     predict_ = poly.fit_transform(np.arange(60).reshape(-1, 1))
# 
#     clf = linear_model.LinearRegression(fit_intercept = True)
#     clf.fit(X_, df.loc[:, 'Cases'])
#     pred = clf.predict(predict_)
# =============================================================================

    ## Plot
    fig, ax = plt.subplots(figsize = (12,8))
    
    true = ax.plot(df['Cases'], label = 'True Cases')
    ax.scatter(df.index, df['Cases'])

    pred = ax.plot(df.index, lowess_y, color = 'red', label = 'Trend')

# =============================================================================
#     ## Plot
#     fig, ax = plt.subplots(figsize = (12,8))
#     
#     true = ax.plot(np.arange(len(df)), df['Cases'], label = 'True Cases')
#     ax.scatter(np.arange(len(df)), df['Cases'])
# 
#     pred = ax.plot(np.arange(60), pred, color = 'red', label = 'Trend')
# =============================================================================
    
    fig.autofmt_xdate()
    plt.grid()
    ax.legend(loc="upper left", fontsize= 16)
    
    ax.set_title('Massachusetts Corona Cases')
    ax.set_ylabel('Cases')
    ax.set_xlabel('Date')
    plt.savefig('MA_Corona.png')
    
# =============================================================================
#     ## Connect to gmail
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     
#     gmail_user = 'devonjkohler@gmail.com'
#     gmail_password = 'ZenyattaOmnic69'
#     
#     server.login(gmail_user, gmail_password)
# =============================================================================
    
    
if __name__ == '__main__':
    main()