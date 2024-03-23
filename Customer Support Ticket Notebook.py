#Importing the necessary libraries
import pandas as pd
import  numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Reading in our data
df = pd.read_csv(r"C:\Users\Faith\Documents\GitHub\Customer-Support-Ticket\customer_support_tickets.csv")
df.head(5)

#Checking on the data types
df.dtypes

#Summary statistics
df.describe().T

#Checking on the null values
df.isnull().sum()

#Checking on the duplicates
df.duplicated().sum()