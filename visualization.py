# -*- coding: utf-8 -*-
"""EM_PR Final_DataVis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mZbQRuamwVqa8jBuJeqKxV1A1B5ayg5q
"""

from google.colab import drive
drive.mount('/content/drive')

"""# Repeat Buyers Prediction for E-Commerce

### Problem Statement
Merchants often gain many new customers through promotions, but a significant portion of these customers are only interested in one-time deals. Therefore, the impact of promotions on long-term sales may be limited. To maximize return on investment (ROI) and reduce promotion costs, it is crucial for merchants to distinguish between one-time buyers and potential loyal customers and focus their efforts on converting the latter group.

In this project, you are provided a dataset with information on promotional shopping event from e-commerce platform. Your task is to design a system which will increase the ROI (in other words, you need to predict the probability that these new buyers would purchase items from the same merchants again within 6 months), reduce promotional cost, and identify one-time buyers. 


"""

import pandas as pd

user_logs = pd.read_csv('/content/drive/MyDrive/PR_Final/user_log.csv')
user_info = pd.read_csv('/content/drive/MyDrive/PR_Final/user_info.csv')
train = pd.read_csv('/content/drive/MyDrive/PR_Final/train.csv')
test = pd.read_csv('/content/drive/MyDrive/PR_Final/test.csv')

"""# New Section"""

user_logs.head(5)

user_logs.shape

"""# Data Visualization

4 Data Frames 

**User Behavior**, with 6 columns, *user_id*: a unique id for the shopper, *item_id*: a unique id for the item, *cat_id*, a unique id for the category that the item belongs to, *merchant_id*: a unique id for the merchant, *brand_id*: a unique id for the brand of the item, *time_stamp*: date the action took place (format: mmdd), and *action_type*: it is an enumerated type {0, 1, 2, 3}, where 0 is for click, 1 is for add-to-cart, 2 is for purchase and 3 is for add-to-favorite. 

**User Profile**, with 3 columns, *user_id*: a unique id for the shopper, *age_range*: user's age range, 1 for younger than 18, 2 for 18-24, 3 for 25-29, 4 for 30-34, 5 for 35-39, 6 for 40-49, 7 and 8 for older than 50, and 0 and Null for unknown, and *gender*: user's gender, 0 for female, 1 for male, and 2 for Null or unknown. 

**Training and Testing**, *user_id*: a unique id for the shopper, *merchant_id*: a unqiue id for the merchant, and *label*: it is an enumerated type{0, 1}, where 1 means repeat buyer, 0 is for non-repeat buyer. This field is blank for test data.

"""

import matplotlib.pyplot as plt
import seaborn as sns

"""### User Behavior Data Visualization

"""

# Map the number action_type labels to word action_type labels
action_type_mapping = {0: "Clicks", 1: "Add to Cart", 2: "Purchases", 3: "Favorites"}

# Replace the number action_type labels with the word labels
user_logs["action_type"] = user_logs["action_type"].replace(action_type_mapping)

plt.figure(figsize=(10, 5))
sns.countplot(x='action_type', data=user_logs)
plt.title('Distribution of Action Types by count')
plt.xlabel('Action Type')
plt.ylabel('Count')

plt.show()

# Merge user logs and info
merged_data = pd.merge(user_logs, user_info, on='user_id', how='left')
merged_data.head()

# Pie chart - to show action types distribution
action_type_counts = merged_data['action_type'].value_counts()
action_type_percentages = 100 * action_type_counts / len(merged_data)

plt.figure(figsize=(8,8))
plt.pie(action_type_percentages, labels=action_type_percentages.index, autopct='%1.1f%%', textprops={'fontsize': 14})
plt.title('Distribution of Action Types by percentage', fontsize=16)
plt.legend(title='Action Types', loc='best', bbox_to_anchor=(1, 0.5, 0.5, 0.5))

plt.show()

# Pivot table - to aggregate the number of actions by category and action type
pivot_table = user_logs.pivot_table(index="cat_id", columns="action_type", values="user_id", aggfunc="count")

# Stacked Bar Chart - to visualize the distributions of actions across different merchants or brands
pivot_table.plot(kind="bar", stacked=True, figsize=(14, 8))

plt.title("Distribution of Actions Types by Category")
plt.xlabel("Category")
plt.ylabel("Count of Actions")


plt.show()

# Convert time_stamp to datetime format: mmdd
user_logs["time_stamp"] = pd.to_datetime(user_logs["time_stamp"], format="%m%d")

# Pivot table - to aggregate the number of actions by date and action type
pivot_table = user_logs.pivot_table(index="time_stamp", columns="action_type", values="user_id", aggfunc="count")

# Line chart - to visualize the trend of user actions over time
pivot_table.plot(kind="line", figsize=(14, 8))

plt.title("Trend of User Actions over Time")
plt.xlabel("Time Stamp")
plt.ylabel("Count of Actions")

plt.show()

"""## User Profile Data Visualization"""

# Bar - to visualize distribution of age range and gender
plt.figure(figsize=(10, 5))
sns.countplot(x='age_range', hue='gender', data=user_info)
plt.title('Distribution of Age Range and Gender')
plt.xlabel('Age Range')
plt.ylabel('Count')
plt.legend(['Female', 'Male', 'Unknown'])

plt.show()

# Violin plot - to show age range distribution by action type
plt.figure(figsize=(10, 6))
sns.violinplot(x='action_type', y='age_range', data=merged_data)
plt.title("Distribution of Age Range by Action Type")

plt.show()

# Create age and gender purchase data
age_purchase_data = merged_data[merged_data['action_type'] == 2].groupby(['age_range', 'time_stamp']).size().reset_index(name='num_purchases')
gender_purchase_data = merged_data[merged_data['action_type'] == 2].groupby(['gender', 'time_stamp']).size().reset_index(name='num_purchases')

# Heatmap - to visualize the action type frequency by age range and gender
age_gender_action = merged_data.groupby(['age_range', 'gender', 'action_type']).size().unstack()
age_gender_action.fillna(0, inplace=True)

# Normalize the data
age_gender_action = age_gender_action.div(age_gender_action.sum(axis=1), axis=0)

sns.heatmap(age_gender_action, annot=True, cmap='coolwarm')
plt.title("Frequency of Action Type by Age Range and Gender")

plt.show()

"""## Training Data Visualization"""

# Map the number number labels to word labels
buyer_mapping = {0: "Non-repeat Buyer", 1: "Repeat Buyer"}

# Replace the number labels with the word labels
train["label"] = train["label"].replace(buyer_mapping)

# Bar - to visualize distribution of repeat and non-repeat buyers
plt.figure(figsize=(5, 5))
sns.countplot(x='label', data=train)
plt.title('Distribution of Repeat and Non-repeat Buyers')
plt.xlabel('Label')
plt.ylabel('Count')

plt.show()

# Create a scatter plot to show the relationship between user_id and merchant_id in the training data
sns.scatterplot(x='user_id', y='merchant_id', hue='label', data=train)
plt.title('Relationship between User ID and Merchant ID')
plt.xlabel('User ID')
plt.ylabel('Merchant ID')

plt.show()

# Group and count the data by merchant_id and label
merchant_counts = train.groupby(["merchant_id", "label"]).size().reset_index(name="count")

# Bar chart - to show the top 20 merchants with the most repeat buyers
repeat_buyers = train[train['label'] == "Repeat Buyer"]
merchant_counts = repeat_buyers['merchant_id'].value_counts().head(20)

plt.bar(range(len(merchant_counts)), merchant_counts.values)
plt.xticks(range(len(merchant_counts)), merchant_counts.index, rotation=45)

plt.title('Top 20 Merchants with the Most Repeat Buyers')
plt.xlabel('Merchant ID')
plt.ylabel('Count of Repeat Buyers')

plt.show()

# Bar chart - to show the top 20 merchants with the most non-repeat buyers
non_repeat_buyers = train[train['label'] == "Non-repeat Buyer"]
merchant_counts = non_repeat_buyers['merchant_id'].value_counts().head(20)

plt.bar(range(len(merchant_counts)), merchant_counts.values)
plt.xticks(range(len(merchant_counts)), merchant_counts.index, rotation=45)

plt.title('Top 20 Merchants with the Most Non-Repeat Buyers')
plt.xlabel('Merchant ID')
plt.ylabel('Count of Non-Repeat Buyers')

plt.show()

# Bar chart - to show the top 20 users with the most repeat buyers
repeat_buyers = train[train['label'] == "Repeat Buyer"]
user_counts = repeat_buyers['user_id'].value_counts().head(20)

plt.bar(range(len(user_counts)), user_counts.values)
plt.xticks(range(len(user_counts)), user_counts.index, rotation=45)

plt.title('Top 20 Users with the Most Repeat Purchases')
plt.xlabel('User ID')
plt.ylabel('Count of Repeat Purchases')

plt.show()

# Bar chart - to show the top 20 users with the most non-repeat buyers
repeat_buyers = train[train['label'] == "Non-repeat Buyer"]
user_counts = repeat_buyers['user_id'].value_counts().head(20)

plt.bar(range(len(user_counts)), user_counts.values)
plt.xticks(range(len(user_counts)), user_counts.index, rotation=45)

plt.title('Top 20 Users with the Most Non-repeat Purchases')
plt.xlabel('User ID')
plt.ylabel('Count of Non-repeat Purchases')

plt.show()

# Heatmap - to show the correlation matrix of the training data
corr_matrix = train.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')

plt.title('Correlation Matrix of Training Data')

plt.show()

