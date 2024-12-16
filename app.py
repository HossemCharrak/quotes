from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ast
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Define request schema
class RecommendationRequest(BaseModel):
    username: str
    liked_quotes: list

# Load and process data (sample size and confidence threshold can be modified)
def load_data():
    """Load the data."""
    users_df = pd.read_csv('users.csv')
    users_df['likes'] = users_df['likes'].apply(ast.literal_eval)
    return users_df

def process_transactions(users_df):
    """Transform transactions into a one-hot encoded DataFrame."""
    transactions = users_df['likes'][:150].tolist()
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    return pd.DataFrame(te_ary, columns=te.columns_)

def generate_association_rules(df_onehot, min_support=0.01, min_confidence=0.7):
    """Generate association rules."""
    frequent_itemsets = apriori(df_onehot, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets,frequent_itemsets.shape[0], metric="confidence", min_threshold=min_confidence)
    return rules

def recommend_quotes_association(user_likes, rules):
    """Recommend quotes based on association rules."""
    recommendations = []
    for _, rule in rules.iterrows():
        if set(rule['antecedents']).issubset(user_likes):
            recommendations.extend(rule['consequents'])
    recommendations = set(recommendations) - set(user_likes)
    return list(recommendations)

# Load and process data at startup
users_df = load_data()
df_onehot = process_transactions(users_df)
rules = generate_association_rules(df_onehot)

@app.post("/recommend")
def recommend(request: RecommendationRequest):
    """
    API endpoint to recommend quotes.
    - username: str
    - liked_quotes: list[int]
    """
    username = request.username
    user_likes = request.liked_quotes

    # Check if the user exists
    if username not in users_df['name'].values:
        raise HTTPException(status_code=404, detail=f"User {username} not found.")

    # Generate recommendations
    recommendations = recommend_quotes_association(user_likes, rules)

    # Return recommendations
    return {"username": username, "recommendations": recommendations}

# Run the app with `uvicorn` when this script is executed directly
if __name__ == "__main__":
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
