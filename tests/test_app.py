import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Verify that the health check endpoint returns 200 without auth."""
    rv = client.get('/health')
    assert rv.status_code == 200
    assert rv.get_json() == {"status": "ok"}

def test_api_models_no_auth(client):
    """Verify that fetching models does not redirect to a login page."""
    rv = client.get('/api/models')
    assert rv.status_code == 200
    assert 'models' in rv.get_json()

def test_process_content_no_auth(client):
    """Verify that a POST to process content handles missing data (400) but does not redirect (302)."""
    rv = client.post('/api/process-content', json={})
    assert rv.status_code == 400
    assert rv.get_json() == {"error": "No content provided (urls, files, text, or topic required)"}

def test_no_auth_redirects_on_root(client):
    """
    Verify that the root path returns a 404 (as there is no root route defined in app.py)
    in the Flask layer, ensuring it's not a 302 redirect.
    """
    rv = client.get('/')
    assert rv.status_code == 404
