

def test_register(client):
    data = {
       "email": "test@gmail.com",
       "password": "secret123" 
    }
    res = client.post(
        "/auth/register",
        json=data
    )
    
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "test@gmail.com"
    assert "id" in data
    assert "hashed_password" not in data
    assert "is_active" in data
    

def test_duplicate_email(client):
    data = {
       "email": "test@gmail.com",
       "password": "secret1234" 
    }

    client.post(
        "/auth/register",
        json=data
    )
    res = client.post(
        "/auth/register",
        json=data
    )
    assert res.status_code == 409

def test_login_succed(client):
    data = {
       "email": "test@gmail.com",
       "password": "secret123" 
    }

    register_res = client.post(
        "/auth/register",
        json=data
    )

    login_res = client.post(
        "/auth/login",
        json=data
    )

    assert register_res.status_code == 201
    assert login_res.status_code == 200
    res_data = login_res.json()
    assert "access_token" in res_data
    assert res_data["token_type"] == "bearer"

def test_login_wrong_password(client):
    data = {
        "email": "test@gmail.com",
        "password":"secret123"
    }
    wrong_password_data = {
        "email": "test@gmail.com",
        "password":"secret12345"
    }

    client.post(
        "/auth/register",
        json=data
    )

    res = client.post(
        "/auth/login",
        json=wrong_password_data
    )

    assert res.status_code == 401

    

def test_protected_route(client):
    data = {
        "email": "test@gmail.com",
        "password": "secret123"
    }

    client.post(
        "/auth/register",
        json=data
    )

    res = client.post(
        "/auth/login",
        json=data
    )

    res_data = res.json() 
    token = res_data["access_token"]
    
    login_res = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    login_res_data = login_res.json()
    assert login_res.status_code == 200
    assert "hashed_password" not in login_res_data
    assert "email" in login_res_data
    assert "is_active" in login_res_data

    