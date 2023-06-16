import pytest
from main import code_block
from termcolor import colored

class TestCodeBlock:
    @pytest.mark.asyncio
    async def test_code_block(): # Code block contains ``` 
        test_string = "```python\nprint('Hello world!')\n```"
        expected = colored("python\nprint('Hello world!')\n", "cyan")
        assert await code_block(test_string) == expected

    @pytest.mark.asyncio
    async def test_code_block_no_code_block(): # Code block doesn't contain ```
        test_string = "Hello world!"
        expected = "Hello world!"
        assert await code_block(test_string) == expected

    @pytest.mark.asyncio
    async def test_code_block_multiple_code_blocks(): # Multiple code blocks
        test_string = "```python\nprint('Hello world!')\n```\nThis is another code block\n```python\nprint('Hello world!')\n```"
        expected = colored("python\nprint('Hello world!')\n", "cyan") + "This is another code block\n" + colored("python\nprint('Hello world!')\n", "cyan")
        assert await code_block(test_string) == expected
    