import pandas as pd

# Data Allocation

# Format 1 Data Frames
user_log = pd.read_excel('Dataset/user_log_format1.xlsx')

# Format 2 Data Frames
format2_train_data = pd.read_excel('Dataset/train_format2.xlsx')
format2_test_data = pd.read_excel('Dataset/test_format2.xlsx')

# Group 3 Range
item_ids = list(range(321, 481))

# Remove item_id from format 1
user_log = user_log[user_log['item_id'].isin(item_ids)]
user_log.to_excel('Dataset/updated_user_log_format1.xlsx', index=False)

# Remove item_id from format 2 activity logs
format2_train_data['activity_log'] = format2_train_data['activity_log'].fillna('').apply(lambda x: '#' + '#'.join([s for s in x.split('#') if len(s.split(':')) > 1 and int(s.split(':')[0]) in item_ids]) + '#')
format2_train_data = format2_train_data[format2_train_data['activity_log'] != '##']
format2_train_data.to_excel('Dataset/update_train_format2.xlsx', index=False)

format2_test_data['activity_log'] = format2_test_data['activity_log'].fillna('').apply(lambda x: '#' + '#'.join([s for s in x.split('#') if len(s.split(':')) > 1 and int(s.split(':')[0]) in item_ids]) + '#')
format2_test_data = format2_test_data[format2_test_data['activity_log'] != '##']
format2_test_data.to_excel('Dataset/update_test_format2.xlsx', index=False)

print(user_log.head(5))
print(format2_train_data.head(5))
print(format2_test_data.head(5))