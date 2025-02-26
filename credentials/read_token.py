import pickle

# Read the token.pickle file
with open('token.pickle', 'rb') as token:
    creds = pickle.load(token)

# Print the refresh token
print("\nRefresh Token:", creds.refresh_token)
print("\nSave this refresh token in your .env file!") 