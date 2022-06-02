# simpleChat

This is a python implementation of a chat application that allows users to send plain text messages with one another. Users can direct messages to other users using an @prefix, and the server needs to forward these messages to the intended recipients. The message could be intended to be sent for a single client (Unicast) or all clients (Broadcast). The messages would be communicated as plain text, so the server will be able to read the messages. This is a simpler version of any commercial chat based application which make use of centralized servers for relaying the messages, except the fact that messages would be encrypted in the case of commercial applications.

It uses multithreading to create multiple threads for each client which the server will handle.

To run the server, use the command:
python3 server.py

To run the clients, use the command:
python3 client.py {serverAddress} {username_for_client}
example:
python3 client.py 127.0.0.1 SampleClient
