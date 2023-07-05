import requests
import pytest

ENDPOINT = "http://127.0.0.1"
login_url = "http://127.0.0.1/token"
username = "admin"
password = "admin1"


@pytest.fixture
def generate_headers():
    """Generate header with valid access token for next tests"""
    login_data = {
        "username": username,
        "password": password
    } 
    response = requests.post(login_url, data=login_data)
    access_token = response.json()["access_token"]
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    return headers

def test_can_call_endpoint():
    """Is server reachable"""
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_generate_token():
    login_data = {
        "username": username,
        "password": password
    } 
    response = requests.post(login_url, data=login_data)
    assert response.status_code == 200

def test_can_create_contact(generate_headers):
    """Check if contact can be created.
        Will not pass if phone number will be the same as in existing entity.
    """
    payload ={
    "name": "test_name",
    "last_name": "test_lastname",
    "phone_number": "1234567893231",
    "email_address": "test@test.com"
    }
    headers = generate_headers
    response = requests.post(ENDPOINT+"/contacts/", json=payload, headers=headers)
    assert response.status_code == 200
    # data = response.json()
    # return data

def test_can_update_contact(generate_headers):
    """Check if contact can be updated."""
    contact_id = 1
    payload ={
    "name": "test_name2",
    "last_name": "test_lastname2"
    }
    headers = generate_headers
    response = requests.patch(ENDPOINT+"/contacts/" + str(contact_id), json=payload, headers=headers)
    assert response.status_code == 200

def test_can_read_contacts():
    """Check if contacts can be read."""
    response = requests.get(ENDPOINT+"/contacts/")
    assert response.status_code == 200

def test_can_read_single_contact():
    """Check if single contact can be read."""
    contact_id = 1
    response = requests.get(ENDPOINT+"/contacts/"+str(contact_id))
    assert response.status_code == 200

def test_can_read_contact_by_name():
    """Check if contacts can be searched by name"""
    name = "test_name2"
    response = requests.get(ENDPOINT+f"/contacts/?name={name}")
    assert response.status_code == 200   

def test_can_read_contact_by_lastname():
    """Check if contacts can be searched by lastname"""
    last_name = "test_lastname2"
    response = requests.get(ENDPOINT+f"/contacts/?last_name={last_name}")
    assert response.status_code == 200

def test_can_read_contact_by_name_and_lastname():
    """Check if contacts can be searched by name and lastname"""
    name = "test_name2"
    last_name = "test_lastname2"
    response = requests.get(ENDPOINT+f"/contacts/?name={name}&last_name={last_name}")
    assert response.status_code == 200

def test_can_read_contact_by_phone_number():
    """Check if contacts can be searched by phone number"""
    phone_number = "1234567893"
    response = requests.get(ENDPOINT+f"/contacts/?phone_number={phone_number}")
    assert response.status_code == 200

def test_can_read_contact_by_email():
    """Check if contacts can be searched by email address"""
    email = "test@test.com"
    response = requests.get(ENDPOINT+f"/contacts/?email={email}")
    assert response.status_code == 200


# TODO: Non-valid value tests

def test_cannot_read_single_contact_wrong_id():
    contact_id = 12345
    response = requests.get(ENDPOINT+"/contacts/"+str(contact_id))
    assert response.status_code == 404

def test_cannot_create_contact_miss_input(generate_headers):
    payload ={
    "last_name": "test_lastname",
    "phone_number": "1234567893",
    "email_address": "test@test.com"
    }
    headers = generate_headers
    response = requests.post(ENDPOINT+"/contacts/", json=payload, headers=headers)
    assert response.status_code == 422

def test_cannot_update_wrong_id(generate_headers):
    contact_id = 1231
    payload ={
    "name": "test_name2",
    "last_name": "test_lastname2"
    }
    headers = generate_headers
    response = requests.patch(ENDPOINT+"/contacts/" + str(contact_id), json=payload, headers=headers)
    assert response.status_code == 404

def test_cannot_update_wrong_info(generate_headers):
    contact_id = 1
    payload ={
    "wrong": "test_name2",
    "last_name": "test_lastname2"
    }
    headers = generate_headers
    response = requests.patch(ENDPOINT+"/contacts/" + str(contact_id), json=payload, headers=headers)
    assert response.status_code == 422

def test_cannot_update_no_payload(generate_headers):
    contact_id = 1
    payload ={
    }
    headers = generate_headers
    response = requests.patch(ENDPOINT+"/contacts/" + str(contact_id), json=payload, headers=headers)
    assert response.status_code == 422

def test_cannot_delete_contact_wrong_id(generate_headers):
    contact_id = 123545
    headers = generate_headers
    response = requests.delete(ENDPOINT+"/contacts/"+str(contact_id), headers=headers)
    assert response.status_code == 404

def test_cannot_create_contact_wrong_data(generate_headers):
    payload ={
    "wrong": "test_name",
    "last_name": "test_lastname",
    "phone_number": "1234567893",
    "email_address": "test@test.com"
    }
    headers = generate_headers
    response = requests.post(ENDPOINT+"/contacts/", json=payload, headers=headers)
    assert response.status_code == 422

def test_cannot_create_contact_no_data(generate_headers):
    payload ={
    }
    headers = generate_headers
    response = requests.post(ENDPOINT+"/contacts/", json=payload, headers=headers)
    assert response.status_code == 422

def test_can_delete_contact(generate_headers):
    """Check if single contact can be deleted."""
    contact_id = 1
    headers = generate_headers
    response = requests.delete(ENDPOINT+"/contacts/"+str(contact_id), headers=headers)
    assert response.status_code == 204