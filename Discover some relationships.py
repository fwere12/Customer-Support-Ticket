import pandas as pd

df = pd.read_csv(r"C:\Users\Faith\Documents\GitHub\Customer-Support-Ticket\customer_support_tickets.csv")
df.head(5)

#Cleaning our data

#Convert to datetime
df['Date of Purchase'] = pd.to_datetime(df['Date of Purchase'], format = '%Y-%m-%d')
df['First Response Time'] = pd.to_datetime(df['First Response Time'], format = '%Y-%m-%d %H:%M:%S')
df['Time to Resolution'] = pd.to_datetime(df['Time to Resolution'], format = '%Y-%m-%d %H:%M:%S') 

#Droping the null values
df_ticket = df.drop(columns = ['Ticket ID'], axis = 1)
#Because Ticket ID column is similar to index of the table, we drop it.

#We replace the following missing values
df_ticket['Resolution'] = df_ticket['Resolution'].fillna('None')
df_ticket['First Response Time'] = df_ticket['First Response Time'].fillna('No response')
df_ticket['Time to Resolution'] = df_ticket['Time to Resolution'].fillna('No resolution')
df_ticket['Customer Satisfaction Rating'] = df_ticket['Customer Satisfaction Rating'].fillna('No rating')

import matplotlib.pyplot as plt
import seaborn as sns

#Ticket channel and Ticket priority
plt.figure(figsize = (15,6))
sns.histplot(df_ticket, hue = 'Ticket Channel', x = 'Ticket Priority',multiple = 'dodge', shrink = 0.8)
plt.title('Distribution of ticket channel by priority', loc = 'center', pad = 10, size = 20)
plt.show()

#Ticket status
ticket_st = df_ticket['Ticket Status'].unique()
print(f'Ticket status: {list(ticket_st)}')

#plot
import matplotlib.pyplot as plt
import seaborn as sns

# Check the column names in your DataFrame
print(df_ticket.columns)

chance_r = []
for i in df_ticket['Time to Resolution']:
    if i == 'No resolution':
        chance_r.append('No')
    else:
        chance_r.append('Yes')
df_ticket['Resolution_bin'] = chance_r

# Plot Ticket status and response, Ticket status and resolution
try:
    fig, axes = plt.subplots(1, 2, figsize=(20, 6))
    sns.histplot(df_ticket, x='Ticket Status', hue='Ticket Priority', multiple='dodge', shrink=0.5, ax=axes[0])
    sns.histplot(df_ticket, x='Ticket Status', hue='Resolution_bin', multiple='dodge', shrink=0.5, ax=axes[1])
    axes[0].set_title('Ticket status and ticket priority', loc='center', pad=10, size=15)
    axes[1].set_title('Ticket status and resolution', loc='center', pad=10, size=15)
    plt.show()
except ValueError as e:
    print(f"Error plotting: {e}")

#Ticket priority and solution
#Create a pivot table for caculating
priority = pd.pivot_table(df_ticket, index = ['Ticket Priority'], values = ['Customer Name'], columns = ['Resolution_bin'], aggfunc = len).reset_index()
priority = priority.rename(columns = {'Customer Name': 'Chance of Solution'})
priority['Percent'] = (priority['Chance of Solution']['Yes']/priority['Chance of Solution']['No'])*100
priority
#Plot
plt.figure(figsize = (8,6))
sns.barplot(priority, x = 'Ticket Priority', y = 'Percent')
plt.title('Chance of solution per ticket priority', loc = 'center', pad = 10, size = 15)
plt.show()

#Customer satistaction rating
rating = pd.pivot_table(df_ticket, index = ['Customer Satisfaction Rating'], values= ['Customer Name'], columns = ['Resolution_bin'], aggfunc = len).reset_index()
rating = rating.rename(columns = {'Customer Name': 'Resolution'})
rating

#Create new dataframe
df_resolution = df_ticket[df_ticket['Resolution_bin'] =='Yes']
df_resolution.head()
#Distribution of ticket priority in case resolution
chart_reprio = df_resolution['Ticket Priority'].value_counts()
plt.pie(chart_reprio, labels = chart_reprio.index, autopct = '%.2f')
plt.title('Distribution of ticket priority in case resolution', loc = 'center', pad = 10, size = 15)
plt.show()

rating = []
for i in df_resolution['Customer Satisfaction Rating']:
    if i<=2:
        rating.append('Low')
    elif i==3:
        rating.append('Medium')
    else:
        rating.append('High')
df_resolution['Type of rating'] = rating
#Customer satisfaction rating and ticket priority
fig, axes = plt.subplots(1,2, figsize = (20,6))
sns.histplot(df_resolution, x = 'Ticket Priority', hue = 'Type of rating' ,multiple = 'dodge', shrink = 0.5, ax = axes[0])
sns.histplot(df_resolution['Ticket Priority'], shrink = 0.5, ax = axes[1])
axes[0].set_title('Customer satisfaction rating per ticket priority', loc = 'center', pad = 10, size = 15)
axes[1].set_title('Distribution of ticket priority in case resolution', loc = 'center', pad = 10, size = 15)
plt.show()

#Customer satisfaction rating and ticket type
fig, axes = plt.subplots(1,2, figsize = (15,6))
sns.histplot(df_resolution['Ticket Type'], shrink = 0.8, ax = axes[0])
sns.histplot(hue = df_resolution['Type of rating'], x = df_resolution['Ticket Type'], multiple = 'dodge', shrink = 0.8, stat = 'percent', ax = axes[1])
axes[0].tick_params(labelrotation = 90)
axes[1].tick_params(labelrotation = 90)
axes[0].set_title('Distribution of ticket type', loc = 'center', pad = 10, size = 15)
axes[1].set_title('Customer satisfaction rating per ticket type', loc = 'center', pad = 10, size = 15)
plt.show()