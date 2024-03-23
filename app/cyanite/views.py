import json
import requests
from flask import current_app, request, jsonify, abort
from . import cyanite
from .utils import is_signature_valid, request_file_upload, upload_file_to_cyanite, create_library_track
from .tasks import asynchronously_fetch_library_track_result


@cyanite.route('/enqueue/<library_track_id>', methods=['POST'])
def enqueue_analysis(library_track_id):
    mutation_document = """
        mutation LibraryTrackEnqueue($input: LibraryTrackEnqueueInput!) {
          libraryTrackEnqueue(input: $input) {
            __typename
            ... on LibraryTrackEnqueueError {
              message
            }
            ... on LibraryTrackEnqueueSuccess {
              enqueuedLibraryTrack {
                id
              }
            }
          }
        }
    """
    response = requests.post(current_app.config['API_URL'], json={
        'query': mutation_document,
        'variables': {'input': {'libraryTrackId': library_track_id}}
    }, headers={
        'Authorization': f'Bearer {current_app.config["ACCESS_TOKEN"]}',
        'Content-Type': 'application/json'
    })

    result = response.json()
    print("[info] libraryTrackEnqueue response: ")
    print(result)

    if result.get('data', {}).get('libraryTrackEnqueue', {}).get('__typename', '').endswith('Error'):
        return jsonify({'error': result['data']['libraryTrackEnqueue']['message']}), 400

    return jsonify(result['data']), 200


@cyanite.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_upload_request = request_file_upload()
        upload_response = upload_file_to_cyanite(file, file_upload_request['uploadUrl'])
        if upload_response.status_code == 200:
            library_track = create_library_track(file_upload_request['id'])
            return jsonify(library_track), 200
        else:
            return jsonify({'error': 'Failed to upload file to Cyanite'}), upload_response.status_code


@cyanite.route('/webhook', methods=['POST'])
def handle_webhook():
    if not request.json:
        return abort(422)  # Unprocessable Entity

    print('[info] incoming event:')
    print(json.dumps(request.json, indent=2))

    if request.json.get('type') == 'TEST':
        return '', 200  # OK

    signature = request.headers.get('Signature')
    if not is_signature_valid(current_app.config['SECRET'], signature, request.data.decode()):
        print('[info] signature is invalid')
        return abort(400)  # Bad Request

    print('[info] signature is valid')

    event = request.json.get('event', {})
    if event.get('type') == 'AudioAnalysisV6' and event.get('status') == 'finished':
        asynchronously_fetch_library_track_result(request.json.get('resource', {}).get('id'))
        # Implement asynchronously_fetch_library_track_result to handle the async task

    return '', 200  # OK
