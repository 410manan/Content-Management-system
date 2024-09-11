import io
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import boto3
from googleapiclient.http import MediaIoBaseDownload



SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CLIENT_SECRET_FILE = ''
TOKEN_PICKLE_FILE = 'token.pickle'
MIME_TYPE_WORD = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_REGION_NAME = 'us-east-1'
S3_BUCKET_NAME = ''

def authenticate_google_drive():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(TOKEN_PICKLE_FILE, 'wb') as token:
        pickle.dump(creds, token)

def download_word_file(file_id):
    creds = None
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        authenticate_google_drive()
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    service = build('drive', 'v3', credentials=creds)
    request = service.files().export_media(fileId=file_id, mimeType=MIME_TYPE_WORD)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download progress: {int(status.progress() * 100)}%")
    return file

def upload_to_s3(file, filename):
    s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION_NAME)
    s3.Object(S3_BUCKET_NAME, filename).put(Body=file.getvalue())
    print(f"File uploaded to S3 bucket: {filename}")

def main():
    file_id = ''
    filename = ''

    word_file = download_word_file(file_id)

    upload_to_s3(word_file, filename)

    if os.path.exists(TOKEN_PICKLE_FILE):
        os.remove(TOKEN_PICKLE_FILE)


if __name__ == '__main__':
    main()
