#Importing the necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

chance_r = []
for i in df_ticket['Time to Resolution']:
    if i == 'No resolution':
        chance_r.append('No')
    else:
        chance_r.append('Yes')
df_ticket['Resolution_bin'] = chance_r

#a) Creating a new dataframe
df_sentiment = df_ticket[['Ticket Description', 'Resolution', 'Ticket Priority', 'Ticket Subject', 'Resolution_bin']]
df_sentiment.head()

#We are gonna delete all the character as they don't have any effect on processing.
#Cleaning text
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# Function to clean text
def clean_text(text):
    text = str(text).lower()
    text = re.sub('[({})?/$#|=]', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('[.]', ' ', text)
    text = re.sub('[->]', ' ', text)
    text = re.sub('[:]', ' ', text)
    text = re.sub('[_]', ' ', text)
    text = re.sub('[,]', ' ', text)
    text = re.sub('[-]', ' ', text)
    text = re.sub('[\']', ' ', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

# Download stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter
#import WordCloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# Clean 'Ticket Description' and 'Resolution' columns
df_sentiment['Ticket Description'] = df_sentiment['Ticket Description'].apply(clean_text)
df_sentiment['Resolution'] = df_sentiment['Resolution'].apply(clean_text)

# Define additional stopwords
new_stopwords = ['i\'m', 'i\'ve', 'would', 'could', '-d', '-i\'m', '[--]:', 'not', 'mm', 'ca', 'cs', 'hi']
stopwords_list = stopwords.words('english') + new_stopwords

# Function to remove stopwords
def remove_stopwords(tokens):
    return [token for token in tokens if token not in stopwords_list]

# Apply tokenization and remove stopwords
df_sentiment['temp1'] = df_sentiment['Ticket Description'].apply(lambda x: remove_stopwords(x.split()))
df_sentiment_resolution = df_sentiment[df_sentiment['Resolution_bin'] == 'Yes']
df_sentiment_resolution['temp2'] = df_sentiment_resolution['Resolution'].apply(lambda x: remove_stopwords(x.split()))

# Plot common words in 'Ticket Description'
top_words = Counter([word for sublist in df_sentiment['temp1'] for word in sublist])
temp_df = pd.DataFrame(top_words.most_common(20), columns=['Common_words', 'count'])
plt.figure(figsize=(15, 6))
sns.barplot(data=temp_df, y='Common_words', x='count')

# Plot common words in 'Resolution'
top_words_resolution = Counter([word for sublist in df_sentiment_resolution['temp2'] for word in sublist])
temp_df_resolution = pd.DataFrame(top_words_resolution.most_common(20), columns=['Common_words', 'count'])
plt.figure(figsize=(15, 6))
sns.barplot(data=temp_df_resolution, y='Common_words', x='count')

plt.show()

#Unique words in description
raw_text = [word for word_list in df_sentiment['temp1'] for word in word_list]
#Unique words funtion
def unique_word(sentiment, numwords, raw_words):
    allother = []
    for item in df_sentiment[df_sentiment.Resolution_bin != sentiment]['temp1']:
        for word in item:
            allother .append(word)
    allother  = list(set(allother ))
    
    specific = [x for x in raw_text if x not in allother]
    
    mycounter = Counter()
    
    for item in df_sentiment[df_sentiment.Resolution_bin == sentiment]['temp1']:
        for word in item:
            mycounter[word] += 1
    keep = list(specific)
    
    for word in list(mycounter):
        if word not in keep:
            del mycounter[word]
    
    Unique_words = pd.DataFrame(mycounter.most_common(numwords), columns = ['words','count'])
    
    return Unique_words

resolve = unique_word('Yes', 20, raw_text)
resolve.style.background_gradient(cmap='Greens')

none = unique_word('No', 20, raw_text)
none.style.background_gradient(cmap='Blues')

#Unique words in resolution
df_sentiment_resolution
def unique_word(sentiment, numwords, raw_words):
    allother = []
    for item in df_sentiment_resolution[df_sentiment_resolution.Resolution_bin != sentiment]['temp2']:
        for word in item:
            allother .append(word)
    allother  = list(set(allother ))
    
    specific = [x for x in raw_text if x not in allother]
    
    mycounter = Counter()
    
    for item in df_sentiment_resolution[df_sentiment_resolution.Resolution_bin == sentiment]['temp2']:
        for word in item:
            mycounter[word] += 1
    keep = list(specific)
    
    for word in list(mycounter):
        if word not in keep:
            del mycounter[word]
    
    Unique_words = pd.DataFrame(mycounter.most_common(numwords), columns = ['words','count'])
    
    return Unique_words
resolve = unique_word('Yes', 20, raw_text)
resolve.style.background_gradient(cmap='Greens')