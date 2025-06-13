"""
Module: graph.py

Communication with the Microsoft Graph API to manage Teams chats and messages.

Classes:
    ChatList: Represents a list of chats for a user.
    ChatMessage: Represents a chat message in a chat, used to send messages.

Dependencies:
    - requests: For making HTTP requests to the Microsoft Graph API.
    - logging: For logging messages and errors.
"""

# Standard library imports
import requests
import logging


BASE_URL = "https://graph.microsoft.com/v1.0"


class ChatList:
    """
    Used to retrieve and parse the list of chats for a service account.

    Args:
        user_upn (str): The user principal name of the service account.
        access_token (str): The access token for authentication.
    """

    def __init__(
        self,
        user_upn: str,
        access_token: str
    ) -> None:
        """
        Initializes the ChatList with user principal name and access token.

        Args:
            user_upn (str): The user principal name of the service account.
            access_token (str): The access token for authentication.

        Returns:
            None
        """

        self.user_upn = user_upn
        self.access_token = access_token
        self.raw_chat_list = []
        self.chat_list = []

        # Get the user chats from the API
        self.get_user_chats()

        # Parse the chat list to extract relevant information
        if len(self.raw_chat_list) > 0:
            self.parse_chat_list()

    def __enter__(
        self
    ) -> 'ChatList':
        """
        Context manager entry method.

        Args:
            None

        Returns:
            ChatList: The instance itself.
        """

        return self

    def __exit__(
        self,
        exc_type: type,
        exc_value: Exception,
        traceback: object
    ) -> None:
        """
        Context manager exit method.

        Args:
            exc_type (type): The exception type.
            exc_value (Exception): The exception value.
            traceback (object): The traceback object.

        Returns:
            None
        """

        if exc_type is not None:
            logging.error(
                f"ChatList: An error occurred: {exc_value}",
                exc_info=True
            )

    def get_user_chats(
        self,
    ) -> None:
        """
        Retrieves the list of chats for the service account.
        The chat list is stored in the class variable `raw_chat_list`.

        Args:
            None

        Returns:
            None
        """

        # Build request
        url = f"{BASE_URL}/users/{self.user_upn}/chats?$expand=members"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json"
        }

        chat_list = []
        try:
            response = requests.get(url, headers=headers)

        except Exception as e:
            logging.error(
                "ChatList.get_user_chats: "
                f"An error occurred while retrieving user chats: {e}",
                exc_info=True
            )
            return

        # Handle an unauthorized response
        if response.status_code == 403:
            logging.error(
                "Access denied. Ensure the service account has logged in."
            )

        # A good response
        elif response.status_code == 200:
            logging.info(
                "ChatList.get_user_chats: "
                "Successfully retrieved user chats."
            )

            # List of chats
            for chat in response.json().get('value', []):
                chat_list.append(chat)

            logging.info(
                "ChatList.get_user_chats: "
                f"Retrieved {len(chat_list)} chats."
            )

        # Handle other response codes
        else:
            logging.error(
                "ChatList.get_user_chats: "
                f"Failed to retrieve user chats.Response: {response.text}"
            )

        # Store the raw chat list in the class
        self.raw_chat_list = chat_list

    def parse_chat_list(
        self,
    ) -> None:
        """
        Parses the chat list to extract relevant information.

        Gets:
            - id: The chat ID
            - topic: The chat topic
            - members: A list of members in the chat, excluding the user
            - chat_type: The type of chat (e.g., one-on-one, group)
            - web_url: The web URL for the chat

        Information is stored in the class variable `chat_list`.

        Args:
            None

        Returns:
            None
        """

        chat_list = []

        # Loop through the raw chat list and extract relevant information
        for chat in self.raw_chat_list:
            member_list = []

            # Loop through the members in the chat
            for member in chat.get('members', []):
                # Skip the service account user
                if member['email'] == self.user_upn:
                    continue

                # Add member information to the list
                member_list.append({
                    'display_name': member['displayName'],
                    'email': member['email'],
                })

            # Append the chat information to the chat list
            chat_list.append({
                'id': chat.get('id'),
                'topic': chat.get('topic'),
                'members': member_list,
                'chat_type': chat.get('chatType'),
                'web_url': chat.get('webUrl'),
            })

        # Store the parsed chat list in the class
        self.chat_list = chat_list


class ChatMessage:
    """
    Represents a chat message in a chat.
        Used to send messages to a chat.

    Args:
        chat_id (str): The ID of the chat to send the message to.
        access_token (str): The access token for authentication.
    """

    def __init__(
        self,
        chat_id: str,
        access_token: str,
    ) -> None:
        """
        Initializes the ChatMessage.

        Args:
            chat_id (str): The ID of the chat to send the message to.
            access_token (str): The access token for authentication.

        Returns:
            None
        """

        self.chat_id = chat_id
        self.access_token = access_token

    def __enter__(
        self
    ) -> 'ChatMessage':
        """
        Context manager entry method.

        Args:
            None

        Returns:
            ChatMessage: The instance itself.
        """

        return self

    def __exit__(
        self,
        exc_type: type,
        exc_value: Exception,
        traceback: object
    ) -> None:
        """
        Context manager exit method.

        Args:
            exc_type (type): The exception type.
            exc_value (Exception): The exception value.
            traceback (object): The traceback object.

        Returns:
            None
        """

        if exc_type is not None:
            logging.error(
                f"ChatMessage: An error occurred: {exc_value}",
                exc_info=True
            )

    def send_message(
        self,
        message: str
    ) -> bool:
        """
        Sends a message to the chat.

        Args:
            message (str): The message to send.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """

        # Build the request
        url = f"{BASE_URL}/chats/{self.chat_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "body": {
                "content": message
            }
        }

        # API call to Graph API to send the message
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload
            )

        except Exception as e:
            logging.error(
                "ChatMessage.send_message: "
                f"An error occurred while sending the message: {e}",
                exc_info=True
            )
            return False

        # Check the response status code (should be 201 for success)
        if response.status_code == 201:
            logging.info(
                "ChatMessage.send_message: "
                "Message sent successfully."
            )
            return True

        else:
            logging.error(
                "ChatMessage.send_message: "
                f"Failed to send message. Response: {response.text}"
            )
            return False
