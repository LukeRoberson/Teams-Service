"""
API module.
    Used for communication with other services.

Blueprint lists routes for the Teams API. This is registered in main.py

Routes:
    - /api/health:
        Health check endpoint to ensure the service is running.
"""


from flask import (
    Blueprint,
    jsonify,
    request,
)

import logging


# Create a Flask blueprint for the API
teams_api = Blueprint(
    'teams_api',
    __name__
)


@teams_api.route(
    '/api/health',
    methods=['GET']
)
def health():
    """
    Health check endpoint.
    Returns a JSON response indicating the service is running.
    """

    return jsonify({'status': 'ok'})


@teams_api.route(
    '/api/message',
    methods=['POST']
)
def message():
    """
    Enable services to send messages to MS Teams.

    Expects a JSON payload with 'chat-id' and 'message'.

    Returns a JSON response indicating success or failure.
    """

    # Get the chat-id and message from the request body
    data = request.get_json()
    if not data or 'chat-id' not in data or 'message' not in data:
        logging.error("Missing chat-id or message in request data")
        return jsonify(
            {
                'result': 'error',
                'error': 'Missing chat-id or message'
            }
        ), 400

    # If everything is ok
    return jsonify(
        {
            'result': 'success'
        }
    )


@teams_api.route(
    '/api/id',
    methods=['POST']
)
def chat_id():
    """
    Lookup a chat-id for a user or group.

    Expects a JSON payload with 'user-id'
        This could represent a group as well.

    Returns a JSON response:
        - 'result': 'success' or error
        - 'chat-id': The chat-id if successful
        - 'name': The name of the user or group if successful
        - 'error': Error message if unsuccessful
    """

    # Get the user-id from the request body
    data = request.get_json()
    if not data or 'user-id' not in data:
        logging.error("Missing user-id in request data")
        return jsonify(
            {
                'result': 'error',
                'error': 'Missing user-id'
            }
        ), 400

    # If everything is ok
    return jsonify(
        {
            'result': 'success',
            'chat-id': '1234567890',  # Example chat-id
            'name': 'Example User'  # Example name
        }
    )
