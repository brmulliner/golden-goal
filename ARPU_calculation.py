import matplotlib.pyplot as plt
import numpy as np
import csv
import collections
from itertools import dropwhile, takewhile
from sqlalchemy import create_engine
import pandas


"creates a list of unique userIds for each of the three groups"
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



"determines total revenue for each group"
def tot_purchases_per_group(csv,g):
    
    # create an empty dictionary with each group as a key
    totals = {"control" : 0. , "group1" : 0. , "group2" : 0.}
    
    next(csv, None) # skip header
    for row in csv:
        cost = float(row[2]) # name item in cost colum 'cost' and make float
        user_id = row[3]     # name item in userUd column 'userId'
    
        # adds cost of product to total revenue of appropriate group
        if user_id in g["control"]:
            totals["control"] = totals["control"] + cost
        elif user_id in g["group1"]:
            totals["group1"] = totals["group1"] + cost
        elif user_id in g["group2"]:
            totals["group2"] = totals["group2"] + cost
            
    return totals



"determines ARPU for each group"
def av_revenue_per_user(csv,csv2):
    
    # returns a list of lists of all userIds
    groups = split_groups(csv)
    print(len(groups['control']))
    # returns dictionary with total revenue for each group
    total_revenue = tot_purchases_per_group(csv2,groups)
    print(total_revenue)
    #divides total revenue by total unique active users
    arpu = {k: total_revenue[k] / len(groups[k]) for k in groups.keys() & total_revenue}
    
    return arpu


'''
"Add test group identifier to purchases spreadsheet"
def add_group_identifier(csv,csv2):
    
    # returns a list of lists of all userIds
    control,group1,group2 = split_groups(csv)
    
    next(csv2, None) # skip header
    
    # add appropriate group identifier to the end of each row
    for row in csv2:
        if row[1] in control:
            row.append('control_group')
        elif row[1] in group1:
            row.append('test_group_1')
        elif row[1] in group2:
            row.append('test_group_2')
            
    return csv2
'''


"******"


"Open and read both csv files"

f = open('data_daily_activity.csv')
csv_activity = csv.reader(f)

f2 = open('data_in_app_purchases.csv')
csv_purchases = csv.reader(f2)



"determine ARPU for each group"
ARPU = av_revenue_per_user(csv_activity,csv_purchases)
print(ARPU) # print dictionary
 

"PLOTS"
#plt.title('ARPU over 14 Day Test Period')
plt.ylabel('ARPU')
plt.xlabel('Test Group')
plt.bar(range(len(ARPU)), list(ARPU.values()), align='center', color = ('b','orange','g'))
plt.xticks(range(len(ARPU)), list(ARPU.keys()))
#plt.savefig("ARPU_graph1.png")















def getstuff(filename, criterion):
    with open(filename, "rb") as csvfile:
        datareader = csv.reader(csvfile)
        yield next(datareader)  # yield the header row
        # first row, plus any subsequent rows that match, then stop
        # reading altogether
        yield from takewhile(lambda r: r[3] == criterion, dropwhile(lambda r: r[3] != criterion, datareader))
        return





#getstuff('data_daily_activity.csv', 'control_group')


"""
with open('data_daily_activity.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['abTestGroup'] == 'control_group':
            control = np.append(control,row['userId'])
        elif row['abTestGroup'] == 'test_group_1':
            group1 = np.append(group1,row['userId'])
        else:
            group2 = np.append(group2,row['userId'])

#print(control,group1,group2)
"""