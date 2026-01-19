def test_create_get_project_api(test_auth_client):
    create_response = test_auth_client.post(
        "/projects", json={"name": "Test", "description": "Test"}
    )
    assert create_response.status_code == 201
    assert create_response.json()["name"] == "Test"
    assert create_response.json()["id"] == 1
    assert create_response.json()["description"] == "Test"

    get_response = test_auth_client.get("/projects/1")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test"
    assert get_response.json()["id"] == 1
    assert get_response.json()["description"] == "Test"


def test_get_projects_list_api(test_auth_client):
    test_auth_client.post("/projects", json={"name": "Test 1"})
    test_auth_client.post("/projects", json={"name": "Test 2"})
    test_auth_client.post("/projects", json={"name": "Test 3"})
    response = test_auth_client.get("/projects")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Test 1"
    assert response.json()[1]["name"] == "Test 2"
    assert response.json()[2]["name"] == "Test 3"
    assert len(response.json()) == 3


def test_update_project_api(test_auth_client):
    test_auth_client.post("/projects", json={"name": "Test", "description": "Test"})
    response = test_auth_client.put(
        "/projects/1", json={"name": "Test Test", "description": "Test Test"}
    )
    assert response.status_code == 202
    assert response.json()["name"] == "Test Test"
    assert response.json()["description"] == "Test Test"


def test_delete_project_api(test_auth_client):
    test_auth_client.post("/projects", json={"name": "Test"})
    delete_response = test_auth_client.delete("/projects/1")
    assert delete_response.status_code == 204


def test_get_project_doesnt_exist(test_auth_client):
    response = test_auth_client.get("/projects/1")
    assert response.status_code == 404


def test_create_project_wrong_payload(test_auth_client):
    response = test_auth_client.post("/projects", json={"id": 1})
    assert response.status_code == 422


def test_get_projects_no_auth(test_client):
    response = test_client.get("/projects")
    assert response.status_code == 401
