"""
python3 -m pytest
"""
import httpretty
import pritunl_api
import json

base_url = "http://pritunl-server.com"

pritunl = pritunl_api.Pritunl(base_url, "secret", "secret")

def pritunl_register(path: str, method: str, response_body, status_code=200, **response_headers) -> None:
    method = method.upper()
    httpretty.register_uri(
        method=method,
        uri=f"{base_url}/{path}",
        adding_headers=response_headers,
        body=response_body,
        status=status_code,
        **response_headers)

@httpretty.activate
def test_ping() -> None:
    pritunl_register('ping', httpretty.GET, 'OK', content_type="text/html")
    response = pritunl.ping()
    assert response

@httpretty.activate
def test_check() -> None:
    pritunl_register('check', httpretty.GET, 'OK', content_type="text/html")
    response = pritunl.check()
    assert response

@httpretty.activate
def test_organization() -> None:
    org_name = "testorg"

    pritunl_register(f'organization', httpretty.GET, json.dumps({}), content_type="application/json")

    get = pritunl.organization.get()
    assert isinstance(get, dict)
