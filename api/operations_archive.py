import os
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
from datetime import datetime
from apiclient import errors
from apiclient.http import MediaIoBaseUpload
from io import BytesIO
import magic
import base64 
'''
DRIVE = None

def connect_to_drive():
    '''
SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE =  build('drive', 'v2', http=creds.authorize(Http()))

def get_children_folder_id_by_name(parentFolderId,nameToMatch,shouldCreate):
    childrenResponse = None
    try:
        childrenResponse = DRIVE.children().list(q="mimeType='application/vnd.google-apps.folder' and trashed=False", folderId=parentFolderId).execute()
    except:
        childrenResponse = {'items':[]}
    childrenClientId = ""
    for folder in childrenResponse.get('items', []):
        response = DRIVE.files().get(fileId=folder['id']).execute()
        clientName = response['title']
        if clientName == nameToMatch:
            print('Found folder %s!' % (nameToMatch))
            childrenClientId = response['id']
            break
    if childrenClientId == "":
        print('The folder %s wasn\'t found.' % (nameToMatch))
        if shouldCreate:
            print('Creating folder...')
            metadata = {
                'title': nameToMatch,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [{'id': parentFolderId}],
            }
            createdFolder = DRIVE.files().insert(body=metadata,
                 fields='id').execute()
            print('Folder created successfully.')
            childrenClientId = createdFolder['id']
        else:
            print('Check input parameters and try again.')
            return None
    return childrenClientId
        
def setup_client(clientName, client_label):
    #connect_to_drive()
    with open('clientes.json') as json_file:
        clientDirs = json.load(json_file)
    clientsFolderId = clientDirs['ClientsFolder']
    clientFolderId = get_children_folder_id_by_name(clientsFolderId,clientName,False)
    if clientFolderId is not None:
        operationsFolderId = get_children_folder_id_by_name(clientFolderId,"Operaciones",True)
        historyFolderId = get_children_folder_id_by_name(operationsFolderId, "Historico", True)
        print("Client added successfully! Folder Id " + historyFolderId)
        clientDirs[client_label] = historyFolderId
        with open('clientes.json', 'w') as fp:
            json.dump(clientDirs, fp)
        return "Client added sucessfully.", 200
    else:
        return "Client base folder doesn't exist", 400

def get_client_folder_id(client_label):
    with open('clientes.json') as json_file:
        clientDirs = json.load(json_file)
    try:
        folderId = clientDirs[client_label]
        return folderId
    except:
        print("Client doesn't exist.")
        return None

def archive_file(file, file_name, client_label):
    #connect_to_drive()
    print("Trying to archive file " + file_name + " on client " + client_label)
    file_content=base64.b64decode(s=file)
    yearMonth = datetime.now().strftime("%Y%m")
    yearMonthDay = datetime.now().strftime("%Y%m%d")
    clientFolderId = get_client_folder_id(client_label)
    if clientFolderId is None:
        return "Client doesn't exist. Please set it up first.", 400
    yearMonthId = get_children_folder_id_by_name(clientFolderId,yearMonth,True)
    yearMonthDayId = get_children_folder_id_by_name(yearMonthId,yearMonthDay,True)
    insert_response = insert_file(service=DRIVE, title=file_name, parent_id=yearMonthDayId, file_content = file_content)
    if insert_response:
        print('Created file %s/Operaciones/Historico/%s/%s/%s' % (client_label, yearMonth, yearMonthDay, file_name))
    return insert_response


def insert_file(service, title, parent_id, file_content):
    file_bytes = BytesIO(file_content)
    mime_type = magic.from_buffer(file_bytes.read(),mime=True)
    print('Detected mimetype: ' +  mime_type)
    media_body = MediaIoBaseUpload(file_bytes, resumable=False, mimetype=mime_type)
    body = {
        'title': title,
    }
    if parent_id:
        body['parents'] = [{'id': parent_id}]

    try:
        service.files().insert(
            body=body,
            media_body=media_body).execute()
        print("File succesfully uploaded.")
        return "File succesfully uploaded.", 200
    except errors.HttpError:
        print('The file couldn\'t be uploaded')
        return 'The file couldn\'t be uploaded', 400