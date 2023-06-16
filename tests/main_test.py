import pytest
from main import code_block
from termcolor import colored

@pytest.mark.asyncio
async def test_code_block(): # Code block contains ``` 
    test_string = "```python\nprint('Hello world!')\n```"
    expected = colored("python\nprint('Hello world!')\n", "cyan")
    assert await code_block(test_string) == expected
