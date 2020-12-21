def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Test" in response.data.decode('utf-8')
    assert "Test2" in response.data.decode('utf-8')


def test_index_bad_repo_count(client):
    response = client.get('/', query_string={'repo_count': 'Not an Int'})
    assert response.status_code == 200
    assert "Test" in response.data.decode('utf-8')
    assert "Test2" in response.data.decode('utf-8')


def test_update(client, requests_mock):
    requests_mock.get('https://api.github.com/search/repositories', json={"items": [
        {"id": 1, "full_name": "REPO_NAME", "html_url": "http://test",
         "created_at": "2016-03-20T23:49:42Z", "pushed_at": "2016-03-20T23:49:42Z",
         "description": "desc", "stargazers_count": 1}]})
    response = client.post('/update', data={
        "repo_count": 100,
        "updateCheckbox": True
    })
    assert response.status_code == 302


def test_update_exception(client, requests_mock):
    requests_mock.get('https://api.github.com/search/repositories', status_code=500)
    response = client.post('/update', data={
        "repo_count": 100,
        "updateCheckbox": True
    })
    assert response.status_code == 302
