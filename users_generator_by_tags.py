import pandas as pd
import random

LIKES = 20
# Read the CSV file into a pandas DataFrame
quotes_df = pd.read_csv('quotes.csv')

# Extract unique tags from the 'tags' column
tags_set = set()
for tags in quotes_df['tags']:
    tags_set.update(tags.split(';'))

# Create 300 users
users = [f"User{i+1}" for i in range(300)]

# Initialize a list to store user data
user_tag_data = []

# Assign quotes to users based on tags
for user in users:
    # Select a random tag for the user
    tag = random.choice(list(tags_set))
    
    # Filter quotes that contain the selected tag
    tag_quotes = quotes_df[quotes_df['tags'].str.contains(tag)]
    
    # Initialize list of quotes for the current user
    selected_quotes = tag_quotes.sample(n=min(LIKES, len(tag_quotes)), random_state=random.randint(0, 1000))
    
    # Keep adding quotes until we reach 30
    while len(selected_quotes) < LIKES:
        remaining_count = LIKES - len(selected_quotes)
        
        # Exclude already used tag
        other_tags = list(tags_set - {tag})
        
        # Select a second tag
        second_tag = random.choice(other_tags)
        second_tag_quotes = quotes_df[quotes_df['tags'].str.contains(second_tag)]
        
        # Adjust sample size to not exceed available quotes
        sample_size = min(remaining_count, len(second_tag_quotes))
        
        # Sample the remaining quotes from the second tag
        second_tag_quotes_sample = second_tag_quotes.sample(n=sample_size, random_state=random.randint(0, 1000))
        
        # Add the quotes from the second tag
        selected_quotes = pd.concat([selected_quotes, second_tag_quotes_sample])
    
    # Create a list of quote indices for the user (likes)
    user_likes = selected_quotes.index.tolist()

    # Append user data
    user_tag_data.append({'name': user, 'likes': user_likes})

# Create a DataFrame to save the data
users_tags_df = pd.DataFrame(user_tag_data)

# Save to users_tags.csv
users_tags_df.to_csv('users_tags.csv', index=False, quoting=1)

print("User data saved to users_tags.csv")
