import tempfile
from unittest.mock import patch, mock_open
import pytest
from file_loader import load_file, load_local_file, load_internet_file
import os

@pytest.mark.asyncio
async def test_load_local_file_not_found():
    # Test loading a local file that doesn't exist.
    result = await load_local_file('nonexistent.txt')
    assert result == -1

@pytest.mark.asyncio
async def test_load_internet_file_failed():
    # Test loading a file from the internet that fails.
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception('Failed to load')
        result = await load_internet_file('http://example.com/test.txt')

@pytest.mark.asyncio
async def test_load_file_invalid_path():
    # Test loading a file with an invalid path with load_file.
    result = await load_file('')
    assert result == -1
