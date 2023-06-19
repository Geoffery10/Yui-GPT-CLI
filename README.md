# Yui-GPT CLI

[![Pipeline](https://img.shields.io/github/actions/workflow/status/Geoffery10/Yui-GPT-CLI/test.yml)](https://github.com/Geoffery10/Yui-GPT-CLI/actions/workflows/test.yml)

Yui-GPT CLI is a command-line interface tool that uses AI throught the [oobabooga/text-generation-webui](https://github.com/oobabooga/text-generation-webui) api to generate text.

## Installation

1. Clone or Download the Repo
2. Install Python (v3.10 recommended)
3. Install [oobabooga/text-generation-webui](https://github.com/oobabooga/text-generation-webui) and enable API flag
4. Run `pdm install` from your terminal inside the installed folder.
5. Make sure that `server_info.json` `"server"` points to the IP of your Text Generation Web UI.
6. Type `python ./main` or `python3 ./main` to start the program/

## Usage

Simply enter text after `Enter a prompt:` to ask the AI a question.

Addionally you can use:

* Type '!quit' to exit the program.
* Type '!clear' to clear the chat history.
* Type '!history' to print the chat history.
* Type '!load `<chat number>`' to load a chat.
* Type '!retry' to retry the last prompt.
* Type '!file `<file name>` `<question>`' to load a file and ask a question about it.
* Type '!delete `<chat number>` to delete a chat. (Use \"*\" for all)
* Type '!help' to print this message again.

## License

Yui-GPT CLI is licensed under the MIT License. See `LICENSE` for more information.
