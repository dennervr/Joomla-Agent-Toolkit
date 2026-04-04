import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import requests
import sys
import joomla_rag.api
from joomla_rag.api import (
    api_login,
    manage_articles,
    manage_categories,
    manage_menus,
    manage_modules,
    api_request,
)


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_api_login(temp_dir):
    creds_path = temp_dir / ".joomla-rag" / "credentials.json"
    with patch.object(joomla_rag.api, "CREDENTIALS_PATH", creds_path):
        url = "https://example.com"
        token = "test_token"
        api_login(url, token)
        assert creds_path.exists()
        with open(creds_path, "r") as f:
            creds = json.load(f)
        assert creds == {
            "url": "https://example.com/api/index.php/v1",
            "token": "test_token",
        }


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_articles_list_no_filters(mock_session_class, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    # Setup creds
    api_login("https://example.com", "test_token")
    # Mock session
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_session.get.return_value = mock_response
    # Call
    manage_articles("list")
    # Assert url
    mock_session.get.assert_called_with("https://example.com/api/index.php/v1/content/articles?page[limit]=5&fields[articles]=id,title,alias,state,catid")


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_articles_list_with_search(mock_session_class, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_session.get.return_value = mock_response
    manage_articles("list", search="test search")
    mock_session.get.assert_called_with("https://example.com/api/index.php/v1/content/articles?page[limit]=5&fields[articles]=id,title,alias,state,catid&filter[search]=test%20search")


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_articles_list_with_category(mock_session_class, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_session.get.return_value = mock_response
    manage_articles("list", category=10)
    mock_session.get.assert_called_with("https://example.com/api/index.php/v1/content/articles?page[limit]=5&fields[articles]=id,title,alias,state,catid&filter[catid]=10")


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_articles_list_with_state(mock_session_class, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_session.get.return_value = mock_response
    manage_articles("list", state=1)
    mock_session.get.assert_called_with("https://example.com/api/index.php/v1/content/articles?page[limit]=5&fields[articles]=id,title,alias,state,catid&filter[state]=1")


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_articles_list_with_all_filters(mock_session_class, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_session.get.return_value = mock_response
    manage_articles("list", search="hello world", category=5, state=0)
    mock_session.get.assert_called_with("https://example.com/api/index.php/v1/content/articles?page[limit]=5&fields[articles]=id,title,alias,state,catid&filter[search]=hello%20world&filter[catid]=5&filter[state]=0")


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_categories_list_no_filters(mock_session_class, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_session.get.return_value = mock_response
    manage_categories("list")
    mock_session.get.assert_called_with("https://example.com/api/index.php/v1/categories?extension=com_content&page[limit]=5&fields[categories]=id,title,alias,published")


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_categories_list_with_search(mock_session_class, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_session.get.return_value = mock_response
    manage_categories("list", search="test search")
    mock_session.get.assert_called_with("https://example.com/api/index.php/v1/categories?extension=com_content&page[limit]=5&fields[categories]=id,title,alias,published&filter[search]=test%20search")


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_categories_list_with_state(mock_session_class, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_session.get.return_value = mock_response
    manage_categories("list", state=1)
    mock_session.get.assert_called_with("https://example.com/api/index.php/v1/categories?extension=com_content&page[limit]=5&fields[categories]=id,title,alias,published&filter[published]=1")


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_menus_list_no_filters(mock_session_class, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_session.get.return_value = mock_response
    manage_menus("list")
    mock_session.get.assert_called_with("https://example.com/api/index.php/v1/menus/site/items?page[limit]=5&fields[items]=id,title,link,published")


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_menus_list_with_menutype(mock_session_class, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_session.get.return_value = mock_response
    manage_menus("list", menutype="mainmenu")
    mock_session.get.assert_called_with("https://example.com/api/index.php/v1/menus/site/items?page[limit]=5&fields[items]=id,title,link,published&filter[menutype]=mainmenu")


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_menus_list_with_state(mock_session_class, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_session.get.return_value = mock_response
    manage_menus("list", state=1)
    mock_session.get.assert_called_with("https://example.com/api/index.php/v1/menus/site/items?page[limit]=5&fields[items]=id,title,link,published&filter[published]=1")


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_modules_get_default_client(mock_session_class, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": {"id": 1, "attributes": {}}}
    mock_session.get.return_value = mock_response
    manage_modules("get", id=1)
    mock_session.get.assert_called_with("https://example.com/api/index.php/v1/modules/site/1")


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_modules_get_admin_client(mock_session_class, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": {"id": 1, "attributes": {}}}
    mock_session.get.return_value = mock_response
    manage_modules("get", id=1, client="admin")
    mock_session.get.assert_called_with("https://example.com/api/index.php/v1/modules/admin/1")


@patch("pathlib.Path.cwd")
@patch("joomla_rag.api.requests.Session")
def test_manage_modules_get_missing_id(mock_session_class, mock_cwd, temp_dir, capsys):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    manage_modules("get", id=None)
    captured = capsys.readouterr()
    assert "[ERROR] ID required for get action." in captured.out
