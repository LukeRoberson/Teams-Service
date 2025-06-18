# Teams Service

The Teams service. Manages communications with the Teams platform, through the MS Graph API

This includes sending chats to groups, and getting known chat ID's.
</br></br>

> [!NOTE]  
> Additional documentation can be found in the **docs** folder
</br></br>



----
# Project Organization
## Python Files

| File           | Provided Function                                             |
| -------------- | ------------------------------------------------------------- |
| main.py        | Entry point to the service, load configuration, set up routes |
| api.py         | API endpoints for this service                                |
| graph.py       | Communication with GraphAPI to manage Teams chats             |
| teams_token.py | Manage the bearer token for the service account               |
</br></br>



----
# Token Management

To communicate with the Graph API, a Bearer token is required. This can be obtained from the _Security Service_.

To get this from the service, an API call is needed. This is what the **TeamsToken** class in teams_token.py is used for.

The security service will handle the authentication process, and obtain a token from Azure. It will then return it to the caller, with a short lifetime.

This lifetime is the time that the caller (this service for example) may cache the token. Token caching is a balance between efficiency (not calling the security service every time a token is needed) and security (not caching a token beyond a point when it might be revoked or expire).
</br></br>


----
# Graph API

## Chat Lists

The **ChatList** class collects a list of chats that the service account is part of, which includes the chat type (1:1 or group) and the chat ID.

This is useful, as sending chat messages requires a chat ID.
</br></br>


## Messaging

The **ChatMessage** class manages sending a message to a given chat ID.
</br></br>

