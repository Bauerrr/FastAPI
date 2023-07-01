import requests

ENDPOINT = "http://127.0.0.1"

def test_can_call_endpoint():
    """Is server reachable"""
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_contact():
    """Check if contact can be created.
        Will not pass if phone number will be the same as in existing entity.
    """
    payload ={
    "name": "test_name",
    "last_name": "test_lastname",
    "phone_number": "1234567893",
    "email_address": "test@test.com"
    }
    response = requests.post(ENDPOINT+"/contacts/", json=payload)
    assert response.status_code == 200
    # data = response.json()
    # return data

def test_can_update_contact():
    contact_id = 1
    payload ={
    "name": "test_name2",
    "last_name": "test_lastname2"
    }
    response = requests.patch(ENDPOINT+"/contacts/" + str(contact_id), json=payload)
    assert response.status_code == 200
    data = response.json()
    return data

def test_can_read_contacts():
    pass

def test_can_read_single_contact():
    pass

def test_can_delete_contact():
    pass

def test_can_read_contact_by_name():
    pass

def test_can_read_contact_by_lastname():
    pass

def test_can_read_contact_by_name_and_lastname():
    pass
