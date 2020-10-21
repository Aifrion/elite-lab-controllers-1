import json
import requests

ROOT_URL = 'http://127.0.0.1:5000'
headers = {'Content-type': 'application/json'}


def print_formatted_response(response):
    """
    Helper function to pretty print the response object
    """
    print("Response Status Code: " + str(response.status_code))
    print("Response data: " + response.text)


def call_create_message_api(body):
    print("Calling the CreateMessage API...")
    url = ROOT_URL + '/messages/'
    response = requests.post(
        url,
        data=json.dumps(body),
        headers=headers
    )
    print_formatted_response(response)
    return response.json()


def call_get_message_api(id):
    print("Calling the GetMessage API...")
    url = ROOT_URL + '/messages/' + str(id)
    response = requests.get(url)
    print_formatted_response(response)
    return response.json()


def call_get_all_message_api():
    print("Calling the GetAllMessages API...")
    url = ROOT_URL + '/messages/'
    response = requests.get(url)
    print_formatted_response(response)
    return response.json()


def call_delete_message_api(id):
    print("Calling the DeleteMessage API...")
    url = ROOT_URL + '/messages/' + str(id)
    response = requests.delete(url)
    print_formatted_response(response)


def call_delete_all_message_api():
    print("Deleting all Messages...")
    url = ROOT_URL + '/messages/'
    response = requests.get(url)
    for message in response.json()['messages']:
        call_delete_message_api(message['id'])
        print("Deleted message ID: " + str(message['id']))


def call_delete_by_chat_api(chat_id):
    print("Deleting by messages by chat_id...")
    url = ROOT_URL + '/chat/' + chat_id
    response = requests.get(url)
    for message in response.json()['messages']:
        call_delete_message_api(message['id'])
        print("Deleted message ID: " + str(message['id']))


def call_get_chat_api(chat_id):
    print("Calling GetChatAPI...")
    url = ROOT_URL + '/chat/' + chat_id
    response = requests.get(url)
    print_formatted_response(response)
    return response.json()


def call_get_last_api(num_messages):
    print("Calling GetLastMessagesAPI...")
    url = ROOT_URL + '/last/?count=' + str(num_messages)
    response = requests.get(url)
    print_formatted_response(response)
    return response.json()


def check_if_lab_complete(body1, body2):
    """
    This function should run to completion without tripping any of the
    assert statements
    """
    # Reassign chat ID to test specific values (so we don't mess with other messages)
    TEST_CHAT_ID1 = "testchat1"
    TEST_CHAT_ID2 = "testchat2"
    body1['chat_id'] = TEST_CHAT_ID1
    body2['chat_id'] = TEST_CHAT_ID2

    # Setup
    # call_delete_by_chat_api(TEST_CHAT_ID1)
    # call_delete_by_chat_api(TEST_CHAT_ID2)

    # Assert that create message api works
    message_id = call_create_message_api(body1)['id']
    assert message_id

    # Assert that get all messages api works
    all_messages = call_get_all_message_api()['messages']
    assert len(all_messages) >= 1

    # Assert that id in all messages
    id_in_all_messages = False
    for message in all_messages:
        if message['id'] == message_id:
            id_in_all_messages = True
            break
    assert id_in_all_messages

    # Assert that a get single message by id works
    message = call_get_message_api(message_id)
    assert message['id'] == message_id

    # Create a message in a separate chat
    call_create_message_api(body2)

    # Assert that filtering by chat works correctly
    chat_messages = call_get_chat_api(TEST_CHAT_ID1)['messages']
    id_in_chat_messages = False
    for message in chat_messages:
        if message['id'] == message_id:
            id_in_chat_messages = True
        if message['chat_id'] != TEST_CHAT_ID1:
            raise AssertionError("Found a rogue message")
    assert id_in_chat_messages

    # Ensure that at least 10 message are in the DB
    test_count = 10
    for i in range(test_count):
        call_create_message_api(body1)

    # Assert that get last api works
    last_messages = call_get_last_api(test_count)['messages']
    assert len(last_messages) == test_count

    # Teardown
    call_delete_by_chat_api(TEST_CHAT_ID1)
    call_delete_by_chat_api(TEST_CHAT_ID2)

    print("\nDone!")


if __name__ == '__main__':
    # The two request bodies we are using for testing
    request_body_1 = {
        "username": "johndoe",
        "content": "hey its me",
        "chat_id": "abcd1234"
    }
    request_body_2 = {
        "username": "janedoe",
        "content": "hey its me in another chat",
        "chat_id": "xyz890"
    }

    # Feel free to comment or uncomment to individually test these functions

    # call_create_message_api(request_body_1)
    # call_create_message_api(request_body_2)
    # call_get_all_message_api()
    # call_delete_message_api(<Insert ID Here>)
    # call_get_chat_api("abcd1234")
    # call_delete_all_message_api()

    # Make sure this successfully runs at completion of your lab
    check_if_lab_complete(request_body_1, request_body_2)
