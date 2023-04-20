import pandas as pd

# Data Allocation

# Format 1 Data Frames
user_log = pd.read_excel('Dataset/user_log_format1.xlsx')

# Group 3 Range
user_log = user_log[(user_log['cat_id'] >= 321) & (user_log['cat_id'] <= 480)]

user_log.to_excel('Dataset/updated_user_log_format1.xlsx', index=False)