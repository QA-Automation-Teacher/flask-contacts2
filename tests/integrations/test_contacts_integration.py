import pytest
from app import app
from models import db, Contacts
from faker import Factory
from migrations import generate_fake_contacts


def setup_module(module):
    with app.app_context():
        # Clear the database before running tests
        db.drop_all()
        db.create_all()
        generate_fake_contacts(100)


def teardown_module(module):
    with app.app_context():
        # Drop all tables after running tests
        db.session.remove()
        db.drop_all()


def test_get_contacts(client, BASE_URL, contacts_num):
    response = client.get(BASE_URL + "/api/contacts")
    assert response.status_code == 200
    print(response.get_json())
    assert isinstance(response.get_json(), list)
    assert len(response.get_json()) == contacts_num
    

def test_create_contact(client, BASE_URL):
    new_contact = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890"
    }
    response = client.post(BASE_URL + "/api/contacts", json=new_contact)
    assert response.status_code == 201
    created_contact = response.get_json()
    assert created_contact["name"] == new_contact["name"]
    assert created_contact["email"] == new_contact["email"]
    assert created_contact["phone"] == new_contact["phone"]


def test_update_contact(client, BASE_URL):
    updated_contact = {
        "name": "Jane",
        "surname": "Doe",
        "email": "jane.doe@example.com",
        "phone": "098-765-4321"
    }
    response = client.put(BASE_URL + "/api/contacts/1", json=updated_contact)
    assert response.status_code == 200
    updated_contact_response = response.get_json()
    assert updated_contact_response["name"] == updated_contact["name"]
    assert updated_contact_response["email"] == updated_contact["email"]
    assert updated_contact_response["phone"] == updated_contact["phone"]


def test_delete_contact(client, BASE_URL):
    response = client.delete(BASE_URL + "/api/contacts/1")
    assert response.status_code == 204