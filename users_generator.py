import pandas as pd
import random

# Parameters
num_users = 300  # Number of users to generate
num_quotes = 3000  # Total number of quotes (indexed from 1 to 3000)
likes_per_user = 30  # Number of quotes liked per user (updated to less than 30)

# Grouping quotes into clusters with intersections to create focused associations
num_groups = 15  # Number of groups (clusters of quotes)
group_size = (num_quotes // num_groups) // 2  # Reduced group size to allow overlap

# Generate overlapping groups of quotes
quote_groups = []
for i in range(num_groups):
    start = i * group_size + 1
    end = start + group_size * 2  # Overlapping range
    quote_groups.append(list(range(start, min(end, num_quotes + 1))))

# Generate users and their likes
users = []
for i in range(1, num_users + 1):
    user_name = f"User{i}"

    # Select a few groups to focus the user's likes
    focused_groups = random.sample(quote_groups, k=random.randint(2, 4))

    # Collect quotes from the selected groups
    likes = []
    for group in focused_groups:
        # Ensure k is not larger than the group size
        max_sample_size = min(len(group), 30)
        if max_sample_size > 0:
            likes.extend(random.sample(group, k=random.randint(20, max_sample_size)))  # Focused likes within groups

    # Add random likes from the entire range of quotes
    remaining_likes = likes_per_user - len(likes)
    if remaining_likes > 0:
        likes.extend(random.sample(range(1, num_quotes + 1), k=remaining_likes))

    # Remove duplicates and ensure exact likes_per_user count
    likes = list(set(likes))[:likes_per_user]

    # Append user data
    users.append({"name": user_name, "likes": likes})

# Create DataFrame and save to CSV
users_df = pd.DataFrame(users)
users_df['likes'] = users_df['likes'].apply(lambda x: str(x))  # Convert list to string for CSV
users_df.to_csv('users.csv', index=False)

print("users.csv generated successfully!")