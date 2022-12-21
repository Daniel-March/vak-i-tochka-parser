import io
import os

import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class GoogleAPI:
    credential_path = "/".join(__file__.split("/")[:-1] + ["GOOGLE_APPLICATION_CREDENTIALS.json"])

    @staticmethod
    def download_file(real_file_id: str, save_to: str) -> bool:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GoogleAPI.credential_path
        creds, _ = google.auth.default()

        try:
            service = build('drive', 'v3', credentials=creds)

            file_id = real_file_id
            name = service.files().get(fileId=file_id).execute().get("name")
            request = service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            with open(save_to + f"/{name}", "wb") as f:
                f.write(file.getvalue())
            return True
        except:
            return False

    @staticmethod
    def get_folder_files(real_folder_id) -> list[str]:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GoogleAPI.credential_path
        creds, _ = google.auth.default()

        try:
            service = build('drive', 'v3', credentials=creds)
            files = []
            page_token = None
            while True:
                response = service.files().list(q=f"'{real_folder_id}' in parents",
                                                spaces='drive',
                                                fields='nextPageToken, '
                                                       'files(id)',
                                                pageToken=page_token).execute()
                files.extend([file.get("id") for file in response.get('files', [])])
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
            return files
        except:
            return []
