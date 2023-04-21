import pandas as pd

# Data Allocation

# Format 1 Data Frames
user_log = pd.read_csv('Dataset/user_log_format1.csv')

# Group 3 Range
user_log = user_log[user_log['item_id'].between(321, 480)]

user_log.to_csv('Dataset/user_log.csv', index=False)