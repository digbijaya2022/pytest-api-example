import string

from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_
import random

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

'''
QA comments:
. The fixture always returns an unique pet id. 
. The fixture reads all the id available, gets the random int which is not available in existing ids
. Also tried to make the pet name little unique hence added last name to the pet name

QA Observation:
While Adding a new pet I observe the endpoint accepts status as "pending/sold". 
Not sure but I guess when you are adding new pet then by default the status should be "available"
It should not allow to add a new pet having "pending/sold" status.      
'''


@pytest.fixture()
def get_unique_pet_id_and_last_name():
    pet_id = list()
    for pet in api_helpers.get_api_data("/pets/").json():
        pet_id.append(int(pet["id"]))
    unique_pet_id = int
    for i in range(len(pet_id)*10):
        pet_ids = random.randint(1, len(pet_id)*10)
        if pet_ids not in pet_id:
            unique_pet_id = pet_ids
            break
    return {
        "id": unique_pet_id,
        "last_name": random.choice(string.ascii_lowercase)+random.choice(string.ascii_lowercase)
    }


@pytest.mark.parametrize("pet_type, pet_name, create_status, order_status, expected_status",
                         [
                             ("horse", "Chetak ", "available", "pending", "sold"),
                             ("bird", "Sunny ", "available", "pending", "sold"),
                             ("dog", "Max ", "available", "pending", "sold")
                         ])
def test_patch_order_by_id(get_unique_pet_id_and_last_name,
                           pet_type, pet_name, create_status, order_status, expected_status):
    place_order_endpoint = "/store/order"
    patch_order_endpoint = "/store/order/{}"
    pet_data = get_unique_pet_id_and_last_name
    pet_id = pet_data.pop("id")
    pet_last_name = pet_data.pop("last_name")
    pet_data = {
            "id": pet_id,
            "name": pet_name+pet_last_name,
            "type": pet_type,
            "status": create_status
        }
    create_pet_response = api_helpers.post_api_data("/pets/", pet_data)
    if create_pet_response.status_code == 201:
        place_order_data = {"pet_id": pet_id}
        order_response = api_helpers.post_api_data(place_order_endpoint, place_order_data)
        assert order_response.status_code == 201
        validate(instance=order_response.json(), schema=schemas.order)
        order_id = order_response.json()["id"]
        assert api_helpers.get_api_data("/pets/{}".format(pet_id)).json()["status"] == order_status
        patch_data = {"status": "sold"}
        patch_response = api_helpers.patch_api_data(patch_order_endpoint.format(order_id), patch_data)
        assert patch_response.status_code == 200
        assert patch_response.json()["message"] == "Order and pet status updated successfully"
        assert api_helpers.get_api_data("/pets/{}".format(pet_id)).json()["status"] == expected_status

    else:
        assert False

