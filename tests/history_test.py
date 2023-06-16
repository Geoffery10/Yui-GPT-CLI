from unittest.mock import patch, mock_open
import pytest
from history import *

class TestChatExists:
    @pytest.mark.asyncio
    async def test_chat_does_not_exist(self):
        with patch('os.listdir') as mock_dir:
            id = '5'
            mock_dir.return_value = ['chat_wrongid.txt']
            result = await chat_exists(id)
            assert result == False

    @pytest.mark.asyncio
    async def test_chat_does_exist(self):
        with patch('os.listdir') as mock_dir:
            id = '5'
            mock_dir.return_value = [f'chat_{id}.txt']
            result = await chat_exists(id)
            assert result == True

    @pytest.mark.asyncio
    async def test_handles_when_directory_does_not_exist(self):
        with patch('os.listdir') as mock_dir:
            mock_dir.return_value = None
            result = await chat_exists(id)
            assert result == False

    @pytest.mark.asyncio
    async def test_checks_the_correct_directory(self):
        with patch('os.listdir') as mock_dir:
            await chat_exists(id)
            assert mock_dir.call_count == 1
            assert './chats/' in mock_dir.call_args[0]

class TestGetHistory:
    @pytest.mark.asyncio
    async def test_checks_if_chat_exists(self):
        with patch('history.chat_exists') as mock_exists:
            id = '14'
            await get_history(id)
            assert mock_exists.call_count == 1
            assert id in mock_exists.call_args[0]

    @pytest.mark.asyncio
    async def test_fails_when_no_chats_exist(self):
        with patch('history.chat_exists') as mock_exists:
            id = '14'
            mock_exists.return_value = False
            result = await get_history(id)
            assert "No chat history in this thread yet." == result

    @pytest.mark.asyncio
    async def test_fails_when_file_is_not_readable(self):
        with patch('history.chat_exists') as mock_exists:
            with patch('builtins.open') as mock_open:
                id = '14'
                mock_exists.return_value = True
                mock_open.side_effect = Exception('Failed to load')
                result = await get_history(id)
                assert "Couldn't read chat history." == result
