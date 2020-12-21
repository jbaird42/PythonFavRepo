
def test_get_repo(client):
    response = client.get('/repo/1')
    assert response.status_code == 200
    assert "Test" in response.data.decode('utf-8')

def test_get_repo_failure(client):
    response = client.get('/repo/9999999')
    assert response.status_code == 302
