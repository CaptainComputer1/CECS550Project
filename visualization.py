import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

user_logs = pd.read_excel('Dataset/user_log_format1.xlsx')
user_profile = pd.read_excel('Dataset/user_info_format1.xlsx')
train_df = pd.read_excel('Dataset/train_format1.xlsx')
test_df = pd.read_excel('Dataset/test_format1.xlsx')

print(user_logs.head())
print(user_profile.head())
print(train_df.head())
print(test_df.head())

# Bar Charts 
plt.figure(figsize=(10, 5))
sns.countplot(x='age_range', hue='gender', data=user_profile)
plt.title('Distribution of Age Range and Gender')
plt.xlabel('Age Range')
plt.ylabel('Count')
plt.legend(['Female', 'Male', 'Unknown'])
plt.show()

plt.figure(figsize=(10, 5))
sns.countplot(x='action_type', data=user_logs)
plt.title('Distribution of Action Types')
plt.xlabel('Action Type')
plt.ylabel('Count')
plt.xticks([0, 1, 2, 3], ['Click', 'Add to Cart', 'Purchase', 'Add to Favourite'])
plt.show()

plt.figure(figsize=(5, 5))
sns.countplot(x='label', data=train_df)
plt.title('Distribution of Repeat and Non-repeat Buyers')
plt.xlabel('Label')
plt.ylabel('Count')
plt.xticks([0, 1], ['Non-repeat Buyer', 'Repeat Buyer'])
plt.show()
