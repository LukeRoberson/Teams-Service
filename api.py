"""
Module: teams_api.py

API endpoints for the Teams service.

Blueprint lists routes for the Teams API. This is registered in main.py

Routes:
    - /api/health:
        Health check endpoint to ensure the service is running.
    - /api/message:
        Endpoint to send messages to MS Teams.
    - /api/chat_list:
        Endpoint to get a list of chats for the user.

Dependencies:
    - Flask: For creating the web API.
    - requests: For making HTTP requests to the Microsoft Graph API.
    - logging: For logging messages and errors.

Custom Dependencies:
    - graph: Custom module for handling Teams chats and messages.
"""

# Standard library imports
from flask import (
    Blueprint,
    Response,
    request,
    current_app,
    jsonify,
    make_response,
)
import logging

# Custom imports
from graph import ChatList, ChatMessage


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
def message() -> Response:
    """
    Enable services to send messages to MS Teams.

    Expects a JSON payload with 'chat-id' and 'message'.

    Returns a JSON response indicating success or failure.
    """

    # Get the chat-id and message from the request body
    data = request.get_json()
    if (
        not data or
        'chat-id' not in data or
        'message' not in data
    ):
        logging.error(
            "/api/message: Missing chat-id or message in request data"
        )
        return make_response(
            jsonify(
                {
                    "result": "error",
                    "error": "Missing chat-id or message"
                }
            ),
            400
        )

    token = current_app.config['TOKEN_MANAGER'].request_token()
    if not token:
        logging.error("/api/message: Failed to obtain access token")
        return make_response(
            jsonify(
                {
                    "result": "error",
                    "error": "No access token available, "
                    "check the service account is logged in."
                }
            ),
            400
        )

    with ChatMessage(
        chat_id=data['chat-id'],
        access_token=token,
    ) as chat_message:
        # Send the message
        result = chat_message.send_message(
            message=data['message']
        )

    if result:
        return make_response(
            jsonify(
                {
                    "result": "success"
                }
            ),
            200
        )

    else:
        logging.error(
            "/api/message: Failed to send message to chat "
            f"{data['chat-id']}"
        )
        return make_response(
            jsonify(
                {
                    "result": "error",
                    "error": "Failed to send message"
                }
            ),
            400
        )


@teams_api.route(
    '/api/chat_list',
    methods=['GET']
)
def chat_list() -> Response:
    '''
    Get a list of chats for the user.

    The username is the service account in the teams config.
    A bearer token is requested from the token manager.

    Returns a JSON response with the list of chats.
    '''

    # Get a list of user chats
    user = current_app.config['GLOBAL_CONFIG']['teams']['user']
    token_manager = current_app.config['TOKEN_MANAGER']
    token = token_manager.request_token()

    logging.info(f"/api/chat_list: Requesting chats for user: {user}")
    with ChatList(user, token) as chat_list:
        # Get the chats for the user
        chats = chat_list.chat_list

    return make_response(
        jsonify(
            {
                "result": "success",
                "chats": chats
            },
            200
        )
    )
