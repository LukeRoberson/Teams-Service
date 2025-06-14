'''
Module: teams_token.py

Manages the bearer token for the Teams user.
This module does not handle the actual authentication. This is done by the
    security service.
The token represents the Teams service account.

Classes:
    - TeamsToken: Handles the retrieval, storage, and refresh of the
        Teams token.

Dependencies:
    - requests: For making HTTP requests to the security service.
    - logging: For logging messages and errors.
'''

# Standard library imports
from time import time
import requests
import logging


TOKEN_URL = "http://security:5100/api/token"


class TeamsToken:
    """
    Manage the Teams user token.
        Retrieve, store, and refresh the token as needed.

    Args:
        None
    """

    def __init__(
        self,
    ) -> None:
        '''
        Creates variables to store the token and its validity.
        The validity is the epoch time the cache expires.
            When the cache expires, the token will need to be refreshed.
            Note, this is not the same as the token expiration time.

        Args:
            None

        Returns:
            None
        '''

        self.token = None
        self.validity = None

    def get_token(
        self,
    ) -> bool:
        """
        Get the Teams token from the security service.
        Store the token for later use.

        1. Set the token and validity to None, to clear any previous token.
        2. Get the token from the security service.

        Args:
            None

        Returns:
            - bool: True if the token was retrieved successfully,
                False if there was an error
        """

        # Reset values
        self.token = None
        self.validity = None

        # API call to the security service
        response = requests.get(TOKEN_URL, timeout=3)
        if response.status_code == 200:
            data = response.json()

        else:
            logging.error(
                f"TeamsToken.get_token: "
                f"Failed to get Teams token from security service.\n"
                f"Error: {response.text}"
            )

            return False

        # Check if the response contains the expected data
        if (
            not data or
            'result' not in data or
            data['result'] == 'error' or
            'token' not in data or
            'validity' not in data
        ):
            logging.error(
                "Failed to get Teams token from security service"
            )

            return False

        # Check the token validity
        if data["validity"] < time():
            logging.error(
                "The Teams token is not valid. Invalid validity time"
            )

            return False

        # Store the token and validity
        self.token = data["token"]
        self.validity = data["validity"]

        logging.debug("Teams token retrieved successfully")
        return True

    def request_token(
        self,
    ) -> str | bool:
        """
        Return the token to the caller.
        This would be used before making API calls to Teams.

        1. Check if the token is available.
        2. Check if the token is still valid.
        3. If needed, request the token again
        4. Return the token or an error

        Args:
            None

        Returns:
            - str: The Teams token if available
            - bool: False if no valid token is available
        """

        # If there is no cached token, request one
        if self.token is None:
            logging.debug(
                "No cached Teams token available, requesting a new one"
            )
            self.get_token()

        # If the token cache has expired, request a new one
        elif self.validity is not None and self.validity < time():
            logging.debug(
                "Cached Teams token has expired, requesting a new one"
            )
            self.get_token()

        # Otherwise, use the cached token
        else:
            logging.debug("Using cached Teams token")

        # Check that the token is available
        if self.token is None:
            logging.error("No valid Teams token available")
            return False

        # If all is ok, return the token and its validity
        return self.token
