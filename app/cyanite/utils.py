import requests
import hmac
import hashlib
from . import API_URL, ACCESS_TOKEN


def is_signature_valid(secret, signature, message):
    hmac_signature = hmac.new(secret.encode(), msg=message.encode(), digestmod=hashlib.sha512)
    return hmac.compare_digest(hmac_signature.hexdigest(), signature)


def request_file_upload():
    mutation = """
        mutation fileUploadRequest {
            fileUploadRequest {
                id
                uploadUrl
            }
        }
    """
    response = requests.post(API_URL, json={
        'query': mutation
    }, headers={
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    })
    return response.json()['data']['fileUploadRequest']


def upload_file_to_cyanite(file, upload_url):
    response = requests.put(upload_url, data=file.read(), headers={
        'Content-Length': str(file.content_length)
    })
    return response


def create_library_track(file_upload_request_id):
    mutation = """
        mutation LibraryTrackCreate($input: LibraryTrackCreateInput!) {
            libraryTrackCreate(input: $input) {
                ... on LibraryTrackCreateError {
                    message
                }
                ... on LibraryTrackCreateSuccess {
                    createdLibraryTrack {
                        __typename
                        id
                    }
                }
            }
        }
    """
    response = requests.post(API_URL, json={
        'query': mutation,
        'variables': {
            'input': {
                'title': 'Uploaded via Flask',
                'uploadId': file_upload_request_id
            }
        }
    }, headers={
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    })
    return response.json()['data']['libraryTrackCreate']
