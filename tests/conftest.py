from rest_framework.test import APIClient
import pytest

from tests import factories


@pytest.fixture(scope='function')
def api_client():
    return APIClient()


@pytest.fixture(scope='function')
def user_account():
    return factories.UserAccountFactory.create()
