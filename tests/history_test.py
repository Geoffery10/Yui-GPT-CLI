from unittest.mock import patch, mock_open
import pytest
from history import *

@pytest.mark.asyncio
async def test_chat_does_not_exist():
    with patch('os.listdir') as mock_dir:
        id = '5'
        mock_dir.return_value = ['chat_wrongid.txt']
        result = await chat_exists(id)
        assert result == False

@pytest.mark.asyncio
async def test_chat_does_exist():
    with patch('os.listdir') as mock_dir:
        id = '5'
        mock_dir.return_value = [f'chat_{id}.txt']
        result = await chat_exists(id)
        assert result == True

@pytest.mark.asyncio
async def test_chat_exists_handles_when_directory_does_not_exist():
    with patch('os.listdir') as mock_dir:
        mock_dir.return_value = None
        result = await chat_exists(id)
        assert result == False

@pytest.mark.asyncio
async def test_chat_exists_checks_the_correct_directory():
    with patch('os.listdir') as mock_dir:
        await chat_exists(id)
        assert mock_dir.call_count == 1
        assert './chats/' in mock_dir.call_args[0]
