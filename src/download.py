from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import json
import os
import io

# ID of the Google Drive folder with student files
FOLDER_ID = "1miPu8Nr2etjOZrdKe99cepMRZkCHo4ZZYDLKZvZdTs-1_JIozTBTAPvRJlj13PD8MUIrDKHJ"
SCOPES = ['https://www.googleapis.com/auth/drive']

# Read credentials from GitHub Secret
creds_json = os.getenv("DRIVE")

if creds_json:
    creds_dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
else:
    raise Exception("Google Credentials Not Available! Set up Secret 'DRIVE'.")
  
def drive():
    """Download files from Google Drive folder and save to repository."""
    service = build('drive', 'v3', credentials=creds)
    
    # Get list of files in folder
    results = service.files().list(q=f"'{FOLDER_ID}' in parents", fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        print("No Files Available.")
        return
    
    # Create folder for student files
    os.makedirs("assignments/students", exist_ok=True)
    
    for file in files:
        file_id = file['id']
        file_name = file['name']
        request = service.files().get_media(fileId=file_id)
        
        file_path = os.path.join("homework/students", file_name)
        with open(file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Downloading {file_name}: {int(status.progress() * 100)}%")

if __name__ == "__main__":
    drive()
