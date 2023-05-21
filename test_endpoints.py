import pytest
from fastapi.testclient import TestClient
from main import app
from images_prueba import imagen1, imagen2

@pytest.fixture
def client():
    '''creates an api test client'''
    with TestClient(app) as client:
        yield client


@pytest.mark.parametrize(
    "page, page_size, expected_status_code",
    [

        # Test case with valid parameters
        (1, 10, 200),
        # Test case with maximum values for page and page_size
        (100, 100, 200),
        # Test case with page and page_size at lower limits
        (1, 1, 200),
        # Test case with page and page_size at upper limits
        (100, 100, 200),
        # Test case with page and page_size outside of limits (invalid)
        (0, 10, 422),
        (1, 0, 422),
        (1, 101, 422),

    ],
)
def test_list_data_camera(client, page, page_size, expected_status_code):
    response = client.get(f"/cameras?page={page}&page_size={page_size}")
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        data = response.json()
        assert "data" in data
        assert "page" in data
        assert "page_size" in data
        assert isinstance(data["data"], list)
        assert isinstance(data["page"], int)
        assert isinstance(data["page_size"], int)
        assert data["page"] >= 1
        assert 1 <= data["page_size"] <= 100
    


@pytest.mark.parametrize(
    "data, expected_status_code",
    [
        # Test case with valid data
        (
            {
                "camera_id": 1,
                "image_base64": imagen1
            },
            201
        ),
          # Test case with invalid data type for image_base64
        (
            {
                "image_base64": "/9j/4AAQSkZJRgABAQAAAQA",
                "camera_id" : "123456"
            },
            422
        ),
        # Test case with invalid data type for camera_id
        (
            {
                "camera_id": "",
                "image_base64": imagen2
            },
            400
        ),
        # Test case with invalid data type for image_base64
        (
            {
                "camera_id": "123456",
                "image_base64": ""
            },
            400
        ),

    ],
)
def test_create_data(client, data, expected_status_code):
    response = client.post("/cameras/", json=data)
    assert response.status_code == expected_status_code
    if expected_status_code == 201:
        response_data = response.json()
        assert "message" in response_data
        assert "data" in response_data
        

list_to_many_images = {
    "data" : []
}
for index in range(0, 101):
    data = {
        "camera_id": "1",
        "image_base64": imagen1
    }
    list_to_many_images["data"].append(data)




@pytest.mark.parametrize(
    "list_data, expected_status_code",
    [
        #Test case with valid data
        (
            {
                "data": [
                    {
                        "image_base64": imagen1,
                        "camera_id": "1"
                    },
                    {
                        "image_base64": imagen2,
                        "camera_id": "1"
                    },

                ]
            },
            201
        ),
        # Test case with more than 100 data limit, set but can be changed
        (
            list_to_many_images,
            400,
        ),  
        # Test case with missing data
        (
            {
                "data": [
                    {
                        "image_base64": imagen1,
                      
                    },
                    {
                        "image_base64": imagen2,
                        "camera_id": "1"
                    },

                ]
            },
            422
        ), 

                (
            {
                "data": [
                    {
                        "image_base64": imagen1,
                        "camera_id": "1"
                    },
                    {
                       
                        "camera_id": "1"
                    },

                ]
            },
            422
        ), 



    ]
)
def test_upload_data_by_batch(client, list_data, expected_status_code):
   

    response = client.post("/cameras/upload_list/", json=list_data)
    assert response.status_code == expected_status_code

 
    if response.status_code == 201:
        data = response.json()
        assert "message" in data
        assert "data" in data

 

def test_delete_data(client):
    # Create a record in the database for later deletion
    data = {
        "camera_id": "1",
        "image_base64": imagen1
    }
    response = client.post("/cameras/", json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert "message" in response_data
    assert "data" in response_data
    entry_id = response_data["data"]["id"]

    # Send a request to delete the newly created record
    response = client.delete(f"/cameras/{entry_id}")
    assert response.status_code == 204

    # Verify that the record has been correctly deleted
    response = client.get(f"/cameras/{entry_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Entry not found"