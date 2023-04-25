import pandas as pd

user_logs = pd.read_csv('Dataset/user_log.csv')
user_info = pd.read_csv('Dataset/user_info.csv')

# Merge Data Frames
df = user_logs.merge(user_info, on='user_id')

# Total Number of Purchased
user_actions = df.groupby(['user_id', 'action_type']).size().unstack(fill_value=0)
user_actions.columns = ['clicks', 'add_to_cart', 'purchases', 'add_to_favorite']
user_actions.drop(columns=['clicks', 'add_to_cart', 'add_to_favorite'], inplace=True)
df = df.merge(user_actions, on='user_id', how='left')

# User's favorite merchant, category, and brand
favorite_merchant = user_logs.groupby('user_id')['seller_id'].agg(lambda x: x.value_counts().index[0]).reset_index(name='favorite_merchant')
favorite_category = user_logs.groupby('user_id')['cat_id'].agg(lambda x: x.value_counts().index[0]).reset_index(name='favorite_category')

def get_favorite_brand(x):
    if x.value_counts().size == 0:
        return None
    return x.value_counts().index[0]

favorite_brand = user_logs.groupby('user_id')['brand_id'].agg(get_favorite_brand).reset_index(name='favorite_brand')

df = df.merge(favorite_merchant, on='user_id', how='left')
df = df.merge(favorite_category, on='user_id', how='left')
df = df.merge(favorite_brand, on='user_id', how='left')

# Average Interactions Per Merchant
average_interactions_per_merchant = user_logs.groupby('seller_id')['action_type'].count() / user_logs['seller_id'].nunique()
df['avg_interactions_per_merchant'] = df['seller_id'].map(average_interactions_per_merchant)

# User Interaction Per Category
user_category_interactions = user_logs.groupby(['user_id', 'cat_id']).size().groupby('user_id').sum().reset_index(name='total_category_interactions')
df = df.merge(user_category_interactions, on='user_id', how='left')

# User Interaction Per Merchant
total_merchant_interactions = user_logs.groupby(['user_id', 'seller_id']).size().groupby('user_id').sum().reset_index(name='total_merchant_interactions')
df = df.merge(total_merchant_interactions, on='user_id', how='left')

# User Interaction Per Brand
user_brand_interactions = user_logs.groupby(['user_id', 'brand_id']).size().groupby('user_id').sum().reset_index(name='total_brand_interactions')
df = df.merge(user_brand_interactions, on='user_id', how='left')

# Unqiue Items Iteracted w/ Per User
unique_items = user_logs.groupby('user_id')['item_id'].nunique().reset_index(name='unique_items_interacted')
df = df.merge(unique_items, on='user_id', how='left')

# Unique Catgories Interacted w/ Per User
unique_categories = user_logs.groupby('user_id')['cat_id'].nunique().reset_index(name='unique_categories_interacted')
df = df.merge(unique_categories, on='user_id', how='left')

# Unique Brands Interacted w/ Per User
unique_brands = user_logs.groupby('user_id')['brand_id'].nunique().reset_index(name='unique_brands_interacted')
df = df.merge(unique_brands, on='user_id', how='left')

# Days Since First Interaction
user_logs['time_stamp'] = pd.to_datetime(user_logs['time_stamp'], format='%m%d')
first_interaction = user_logs.groupby('user_id')['time_stamp'].min().reset_index(name='first_interaction')
max_date = user_logs['time_stamp'].max()
first_interaction['days_since_first_interaction'] = (max_date - first_interaction['first_interaction']).dt.days
df = df.merge(first_interaction.drop(columns=['first_interaction']), on='user_id', how='left')

# Fill Empty
df['age_range'].fillna(0, inplace = True)
df['gender'].fillna(2, inplace = True)

# Pandas Display Options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print(df)