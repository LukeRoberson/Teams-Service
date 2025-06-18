# API
## Endpoints

There is an API in place so other services can get chat group lists, or send messages to Teams.

| Endpoint       | Methods | Description                                                  |
| -------------- | ------- | ------------------------------------------------------------ |
| /api/health    | GET     | Check the health of the container                            |
| /api/chat_list | GET     | Request a list of chat ID's that the service account can use |
| /api/messsage  | POST    | Send a chat message to a chat ID                             |
</br></br>


## Responses

Unless otherwise specified, all endpoints have a standard JSON response, including a '200 OK' message if everything is successful.

A successful response:
```json
{
    'result': 'success'
}
```

An error:
```json
{
    "result": "error",
    "error": "A description of the error"
}
```
</br></br>


### Health

This is for checking that Flask is responding from the localhost, so Docker can see if this is up.

This just returns a '200 OK' response.
</br></br>


## Endpoint Details
### Chat Group List

This endpoint responds with a list of chat IDs that the service group is part of.

```json
{
    "result": "success",
    "chats": "<List of Chats>"
}
```
</br></br>


### Sending Messages

To send a message, just POST a JSON body to this endpoint, with the chat ID and the message.

```json
{
  "chat-id": "<chat ID as a string>",
  "message": "<message as a string>"
}
```
</br></br>


