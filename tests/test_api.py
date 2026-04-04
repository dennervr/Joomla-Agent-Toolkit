import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import urllib.request
import sys
import joomla_rag.api
from joomla_rag.api import api_login, manage_articles, manage_categories, manage_menus, api_request


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_api_login(temp_dir):
    creds_path = temp_dir / ".joomla-rag" / "credentials.json"
    with patch.object(joomla_rag.api, 'CREDENTIALS_PATH', creds_path):
        url = "https://example.com"
        token = "test_token"
        api_login(url, token)
        assert creds_path.exists()
        with open(creds_path, 'r') as f:
            creds = json.load(f)
        assert creds == {"url": "https://example.com/api/index.php/v1", "token": "test_token"}


@patch('pathlib.Path.cwd')
@patch('urllib.request.urlopen')
def test_manage_articles_list_no_filters(mock_urlopen, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    # Setup creds
    api_login("https://example.com", "test_token")
    # Mock response
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"data": []}'
    mock_urlopen.return_value.__enter__.return_value = mock_response
    # Call
    manage_articles("list")
    # Assert url
    call_args = mock_urlopen.call_args[0][0]  # The Request object
    expected_url = "https://example.com/api/index.php/v1/content/articles?page[limit]=5&fields[articles]=id,title,alias,state,catid"
    assert call_args.full_url == expected_url


@patch('pathlib.Path.cwd')
@patch('urllib.request.urlopen')
def test_manage_articles_list_with_search(mock_urlopen, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"data": []}'
    mock_urlopen.return_value.__enter__.return_value = mock_response
    manage_articles("list", search="test search")
    call_args = mock_urlopen.call_args[0][0]
    expected_url = "https://example.com/api/index.php/v1/content/articles?page[limit]=5&fields[articles]=id,title,alias,state,catid&filter[search]=test%20search"
    assert call_args.full_url == expected_url


@patch('pathlib.Path.cwd')
@patch('urllib.request.urlopen')
def test_manage_articles_list_with_category(mock_urlopen, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"data": []}'
    mock_urlopen.return_value.__enter__.return_value = mock_response
    manage_articles("list", category=10)
    call_args = mock_urlopen.call_args[0][0]
    expected_url = "https://example.com/api/index.php/v1/content/articles?page[limit]=5&fields[articles]=id,title,alias,state,catid&filter[catid]=10"
    assert call_args.full_url == expected_url


@patch('pathlib.Path.cwd')
@patch('urllib.request.urlopen')
def test_manage_articles_list_with_state(mock_urlopen, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"data": []}'
    mock_urlopen.return_value.__enter__.return_value = mock_response
    manage_articles("list", state=1)
    call_args = mock_urlopen.call_args[0][0]
    expected_url = "https://example.com/api/index.php/v1/content/articles?page[limit]=5&fields[articles]=id,title,alias,state,catid&filter[state]=1"
    assert call_args.full_url == expected_url


@patch('pathlib.Path.cwd')
@patch('urllib.request.urlopen')
def test_manage_articles_list_with_all_filters(mock_urlopen, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"data": []}'
    mock_urlopen.return_value.__enter__.return_value = mock_response
    manage_articles("list", search="hello world", category=5, state=0)
    call_args = mock_urlopen.call_args[0][0]
    expected_url = "https://example.com/api/index.php/v1/content/articles?page[limit]=5&fields[articles]=id,title,alias,state,catid&filter[search]=hello%20world&filter[catid]=5&filter[state]=0"
    assert call_args.full_url == expected_url


@patch('pathlib.Path.cwd')
@patch('urllib.request.urlopen')
def test_manage_categories_list_no_filters(mock_urlopen, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"data": []}'
    mock_urlopen.return_value.__enter__.return_value = mock_response
    manage_categories("list")
    call_args = mock_urlopen.call_args[0][0]
    expected_url = "https://example.com/api/index.php/v1/categories?extension=com_content&page[limit]=5&fields[categories]=id,title,alias,published"
    assert call_args.full_url == expected_url


@patch('pathlib.Path.cwd')
@patch('urllib.request.urlopen')
def test_manage_categories_list_with_search(mock_urlopen, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"data": []}'
    mock_urlopen.return_value.__enter__.return_value = mock_response
    manage_categories("list", search="test search")
    call_args = mock_urlopen.call_args[0][0]
    expected_url = "https://example.com/api/index.php/v1/categories?extension=com_content&page[limit]=5&fields[categories]=id,title,alias,published&filter[search]=test%20search"
    assert call_args.full_url == expected_url


@patch('pathlib.Path.cwd')
@patch('urllib.request.urlopen')
def test_manage_categories_list_with_state(mock_urlopen, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"data": []}'
    mock_urlopen.return_value.__enter__.return_value = mock_response
    manage_categories("list", state=1)
    call_args = mock_urlopen.call_args[0][0]
    expected_url = "https://example.com/api/index.php/v1/categories?extension=com_content&page[limit]=5&fields[categories]=id,title,alias,published&filter[published]=1"
    assert call_args.full_url == expected_url


@patch('pathlib.Path.cwd')
@patch('urllib.request.urlopen')
def test_manage_menus_list_no_filters(mock_urlopen, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"data": []}'
    mock_urlopen.return_value.__enter__.return_value = mock_response
    manage_menus("list")
    call_args = mock_urlopen.call_args[0][0]
    expected_url = "https://example.com/api/index.php/v1/menus/site/items?page[limit]=5&fields[items]=id,title,route,published"
    assert call_args.full_url == expected_url


@patch('pathlib.Path.cwd')
@patch('urllib.request.urlopen')
def test_manage_menus_list_with_menutype(mock_urlopen, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"data": []}'
    mock_urlopen.return_value.__enter__.return_value = mock_response
    manage_menus("list", menutype="mainmenu")
    call_args = mock_urlopen.call_args[0][0]
    expected_url = "https://example.com/api/index.php/v1/menus/site/items?page[limit]=5&fields[items]=id,title,route,published&filter[menutype]=mainmenu"
    assert call_args.full_url == expected_url


@patch('pathlib.Path.cwd')
@patch('urllib.request.urlopen')
def test_manage_menus_list_with_state(mock_urlopen, mock_cwd, temp_dir):
    mock_cwd.return_value = temp_dir
    api_login("https://example.com", "test_token")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"data": []}'
    mock_urlopen.return_value.__enter__.return_value = mock_response
    manage_menus("list", state=1)
    call_args = mock_urlopen.call_args[0][0]
    expected_url = "https://example.com/api/index.php/v1/menus/site/items?page[limit]=5&fields[items]=id,title,route,published&filter[published]=1"
    assert call_args.full_url == expected_url