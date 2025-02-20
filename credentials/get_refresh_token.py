from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    """Shows basic usage of the Gmail API.
    Gets refresh token for Gmail API.
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    
    print("\nRefresh Token:", creds.refresh_token)
    print("\nSave this refresh token in your .env file!")

if __name__ == '__main__':
    main() 