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