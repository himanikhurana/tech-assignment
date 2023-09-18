import requests
import json

# Define the base URL of your Django application
BASE_URL = 'http://127.0.0.1:8000'

# Define test data payloads
create_group_payload = {
    "groupName": "HKGroup",
    "members": "user1, user2",
    "createdBy": "user1",
    "createdTime": "2022-09-18 01:43:23"
}

delete_group_payload = {
    "groupId": "f59da65285d5482f96e0bc4654878e18"
}

get_users_payload = {
    "conditions": {
        "username": "user1"
    }
}

send_message_payload = {
    "message": "Hi, whats up",
    "groupId": "9b768b49eb0e46b5b25e7e54a634f6d0",
    "sentBy": "user1",
    "sentTime": "2022-09-18 01:43:23"
}

like_message_payload = {
    "messageId": "6c5cef5ef71f4fb7a7b1477f89177cf7",
    "username": "user2"
}

get_messages_payload = {
    "groupId": "9b768b49eb0e46b5b25e7e54a634f6d0"
}

# Function to make a POST request and check the response
def test_post_api(endpoint, payload):
    url = f'{BASE_URL}/{endpoint}'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)

    assert response.status_code == 200
    print(f"POST {url} - Response: {response.text}")

# Function to make a GET request and check the response
def test_get_api(endpoint, payload=None):
    url = f'{BASE_URL}/{endpoint}'
    #import pdb; pdb.set_trace()
    response = requests.get(url, params=payload)

    assert response.status_code == 200
    print(f"GET {url} - Response: {response.text}")

if __name__ == '__main__':
    # Test the APIs
    test_post_api('user/login', {})  # Login
    test_post_api('user/logout', {})  # Logout
    test_post_api('user/getUsers', get_users_payload)  # Get Users
    test_post_api('group/create', create_group_payload)  # Create Group
    test_post_api('group/delete', delete_group_payload)  # Delete Group
    test_get_api('group/getGroups')  # Get Groups
    test_post_api('message/sendMessage', send_message_payload)  # Send Message
    test_post_api('message/likeMessage', like_message_payload)  # Like Message
    test_post_api('message/getMessage', get_messages_payload)  # Get Messages
