def test_root_serves_html_landing_page_not_an_error(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    assert "Users, Projects &amp; Tasks API" in r.text


def test_landing_page_links_to_docs_and_lists_real_routes(client):
    body = client.get("/").text
    for expected in ('href="/docs"', 'href="/redoc"', "/users/{user_id}", "/tasks/{task_id}/status"):
        assert expected in body


def test_landing_page_is_not_in_the_openapi_schema(client):
    assert "/" not in client.get("/openapi.json").json()["paths"]


def test_unknown_routes_still_use_the_error_contract(client):
    r = client.get("/nope")
    assert r.status_code == 404 and r.json()["error"]["code"] == "not_found"


def test_public_base_url_forces_https_for_non_local_hosts():
    from app.landing import public_base_url
    assert public_base_url("ih-task2-api.onrender.com", "http") == "https://ih-task2-api.onrender.com"
    assert public_base_url("localhost:8000", "http") == "http://localhost:8000"
