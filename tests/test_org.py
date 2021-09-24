import pytest

from pritunl_api.pritunl import Pritunl
from unittest.mock import MagicMock

pritunl = Pritunl("someurl", "sometoken", "somesecret")
org_name = "test"
pritunl.organization.get = MagicMock(return_value={})
pritunl.organization.post = MagicMock(return_value={})


def test_get() -> None:
    assert isinstance(pritunl.organization.get(org_name), dict)


def test_post() -> None:
    assert isinstance(pritunl.organization.post(org_name), dict)
