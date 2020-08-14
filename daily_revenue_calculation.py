import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import defaultdict, OrderedDict
from itertools import dropwhile, takewhile
from sqlalchemy import create_engine
import pandas as pd



"Returns a list of unique userIds for each of the three groups"
def split_groups(csv):
    
    #create an empty list for each group
    control = []
    group_1 = []
    group_2 = []
    
    next(csv, None) # skip header
    for row in csv:
        # checks the abTestGroup column for the test group, and adds userId to appropriate list
        if row[1] == 'control_group' :
            control.append(row[4])
        elif row[1] == 'test_group_1' :
            group_1.append(row[4])
        elif row[1] == 'test_group_2' :
            group_2.append(row[4])
  
    # removes duplicate userIds   
    groups = {"control" : set(control), "group1" : set(group_1), "group2" : set(group_2)}
    
    return groups


'''
"Finds the total DAU for each day of the test"
def unique_active_users_total(csv):
    next(csv, None) # skip header
    dates_dict = defaultdict(list) # empty dictionary which will become lists of userIds for each date
    for row in csv:
        date = row[0]      # saves date as string
        userId = str(row[4])    # saves userId as string
        dates_dict[date].append(userId) # adds userId to respective date in dictionary 
        
    # each list of userIds becomes a set, making the list only unique userIds   
    dates_dict = {k: set(dates_dict[k]) for k in dates_dict}
    
    # the number of unique Ids is taken
    dates_dict = {k: len(dates_dict[k]) for k in dates_dict}
    
    #order dictionary by date
    #dates_dict = OrderedDict(sorted(dates_dict.items())) 
    dates_dict = sorted(dates_dict.items()) # sorts dictionary keys in chronological order
   
    return dates_dict
'''

    
"Returns a dictionary with unique userIds for each day of the test for each group"
def unique_active_users_2(csv):
    
    # empty dictionaries which will become lists of userIds for each date for each test group
    control_group = defaultdict(list)
    group1 = defaultdict(list)
    group2 = defaultdict(list)
    
    next(csv, None) # skip header
    
    for row in csv:
        date = row[0]               # saves date
        group = str(row[1])         # saves the group as a string
        userId = str(row[4])        # saves userId as string
        if group == 'control_group':    
            control_group[date].append(userId) # adds userId to respective date in control dictionary
        elif group == 'test_group_1':    
            group1[date].append(userId) # adds userId to respective date in group1 dictionary
        elif group == 'test_group_2':    
            group2[date].append(userId) # adds userId to respective date in group2 dictionary
        
    # each list of userIds becomes a set, making the list only unique userIds   
    control_group = {k: set(control_group[k]) for k in control_group}
    group1 =        {k: set(group1[k]) for k in group1}
    group2 =        {k: set(group2[k]) for k in group2}

    
    return control_group, group1, group2



"Returns a chronologically ordered dictionary containing the daily total revenue for each group"
def tot_purchases_per_group(csv,c,g1,g2):
    
    # create an empty dictionary with each group as a key
    control_totals = {k: 0. for k in c}
    group1_totals =  {k: 0. for k in g1}
    group2_totals =  {k: 0. for k in g2}

    next(csv, None) # skip header
    
    for row in csv:
        cost = float(row[2]) # name item in cost colum 'cost' and make float
        date = row[1]   # save date from dateActivity
        user_id = row[3]     # name item in userUd column 'userId'
        # adds cost of product to total revenue of appropriate group
        if user_id in c[date]:
            control_totals[date] = control_totals[date] + cost
        elif user_id in g1[date]:
            group1_totals[date] = group1_totals[date] + cost
        elif user_id in g2[date]:
            group2_totals[date] = group2_totals[date] + cost
            
    control_totals = sorted(control_totals.items()) # sorts dictionary keys in chronological order
    group1_totals = sorted(group1_totals.items()) # sorts dictionary keys in chronological order
    group2_totals = sorted(group2_totals.items()) # sorts dictionary keys in chronological order
            
         
    return control_totals, group1_totals, group2_totals


    
"Returns the means and standard deviations of three lists"
def mean_sd(a,b,c):
     # calculate mean of list
     am, bm, cm = np.mean(a), np.mean(b), np.mean(c)
     
     # calculate standard deviation of list
     asd, bsd, csd = np.sqrt(np.var(a)), np.sqrt(np.var(b)), np.sqrt(np.var(c))
     
     # returns a list of mean and standard deviation for a, b and c
     return [[am, asd], [bm, bsd], [cm, csd]]




"************"

"Open and read both csv files"
f = open('data_daily_activity.csv')
csv_activity = csv.reader(f)
#csv_activity = pd.read_csv('data_daily_activity.csv', parse_dates = ['dateActivity'])

f2 = open('data_in_app_purchases.csv')
csv_purchases = csv.reader(f2)
#csv_purchases = pd.read_csv('data_in_app_purchases.csv', parse_dates = ['dateActivity'])



'''Seperate the userIds into the three respective groups, then calculate the
daily revenue for each group'''
Ids_c, Ids_1, Ids_2 = unique_active_users_2(csv_activity)
tot_c, tot_1, tot_2 = tot_purchases_per_group(csv_purchases, Ids_c, Ids_1, Ids_2)




"unzips tuples in ordered dictionaries, ready for math and plots"
xc,yc = zip(*tot_c)
x1,y1 = zip(*tot_1)
x2,y2 = zip(*tot_2)



averages = mean_sd(yc, y1, y2) # returns averages and std devs





"PLOTS"
x = range(1,15) # quick way of relabelling xticks in this case
plt.plot(x,yc, label = 'Control Group') # plot DAU against date
plt.plot(x,y1, label = 'Test Group 1') # plot DAU against date
plt.plot(x,y2, label = 'Test Group 2') # plot DAU against date
#plt.title('Number of DAU for Each Test Group over the 14-Day Test Period')
plt.xticks(range(1,15))
plt.ylabel('Total Revenue ($)')
plt.xlabel('Test Day')
plt.legend()
plt.show()
plt.savefig("tot_revenue_graph.png")

