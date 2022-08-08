#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 21:22:37 2022

@author: julianballrodriguez
"""

import pandas as pd

import statsmodels.api as sm

#Data Preparation
df = pd.read_csv (r'/Users/julianballrodriguez/Documents/Take Home Assignment/fake_orders_test.csv', 
                  names=['order_id', 'activation_time_local', 'country_code', 
                         'store_address', 'final_status', 'payment_status', 
                         'products', 'products_total', 'purchase_total_price'])


#1 What percent of orders are under-authorized?
# def authorisation(df):
def authorization_calc(df,primary_column,comparison_column):
    '''
    This function calculates creates labels based on whether an order is 
    authorized or under-authorized
    
    Parameters
    ----------
    df : Pandas Dataframe
        Dataframe for authorisation comparison
    primary_column : String
        The total amount at checkout in the app.
    comparison_column : String
        What the courier pays at the store.

    Returns
    -------
    str
        If the products total is larger than what is paid at the store then it 
        is labeled as "Under" otherwise it is labeled as "Authorized".

    '''
    p = df[primary_column]
    c = df[comparison_column]
    if p < c:
        return "Under"
    else:
        return "Authorized" 

df['authorization'] = df.apply(lambda df : authorization_calc(df,'products_total','purchase_total_price'), axis=1)
under = len(df[(df['authorization']=='Under')])
total = df['purchase_total_price'].count()
print(under/total)


#2 What percent of orders would be correctly authorized w/ incremental authorisation (+20%) on
#the amount at checkout?
df['products_total_20'] = df['products_total']*1.2
df['authorization_20'] = df.apply(lambda df : authorization_calc(df,'products_total_20','purchase_total_price'), axis=1)
authorization_20 = len(df[(df['authorization_20']=='Authorized')])
print(authorization_20/total)


#3 Are there differences when split by country?
countries = pd.DataFrame(df.groupby(['country_code'])['country_code'].count())
countries = countries.rename(columns={"country_code": "total"})
#Count of under authorised orders by country
countries2 = df.groupby('country_code')['authorization'].apply(lambda x: (x=='Under').sum()).reset_index(name='under')
#Rate per country
countries2 = pd.merge(countries, countries2, on="country_code", how="left")
countries2['rate'] =  countries2['under']/countries2['total']
countries2.sort_values(by='rate', ascending=False)

#4 For the remainder of orders that would be outside of incremental auth what values would be
#necessary to capture the remaining amount?
df['authorization_20'] = df.apply(lambda df : authorization_calc(df,'products_total_20','purchase_total_price'), axis=1)
remaining_orders = df[df["authorization_20"] == "Under"]
remaining_orders = remaining_orders[["order_id", "store_address", "authorization_20", "final_status", "purchase_total_price", "products_total_20"]]
remaining_orders['difference'] = remaining_orders['purchase_total_price']-remaining_orders['products_total_20']
sum(remaining_orders['difference'])


#5a Which stores are the most problematic in terms of monetary value?
stores = df[["store_address", "order_id", "final_status", "authorization", "purchase_total_price", "products_total"]]
stores = stores[stores["authorization"] == "Under"]
stores1 = stores.groupby(by=["store_address"]).sum()
stores1['difference'] = stores1['purchase_total_price']-stores1['products_total']
stores1 = stores1.sort_values(by='difference', ascending=False)
stores1.head(10)


#5b Which stores are the most problematic in terms of orders?
stores2 = stores.groupby(by=["store_address"]).count()
stores2 = stores2[["order_id"]]
stores2 = stores2.sort_values(by='order_id', ascending=False)
stores2.head(10)


#6 For under-auth orders is there a correlation between the difference in the prices and the 
#cancellation of the order? In other words: Is an order more likely to be cancelled as the price
#difference increases?
stores['difference'] = stores['purchase_total_price']-stores['products_total']
df2 = stores[['difference', 'final_status']]
df2 = df2.replace({'final_status':{'DeliveredStatus':1, 'CanceledStatus':0}})
df2 =  df2[df2["difference"] < 150]
df2.dtypes
df2.shape

#Logistical Regression model
model = sm.GLM.from_formula("final_status ~ difference", family=sm.families.Binomial(), data=df2)
result = model.fit()
result.summary()