# This code loads files from different sources.

import os
from termcolor import colored
from history import *
import requests

async def load_file(path):
    if not path: return -1
    elif path.startswith("http"): 
        content = await load_internet_file(path)
    else:
        content = await load_local_file(path)

    if content == -1: return -1

    # Start a new chat.
    session_id = await create_history()
    return session_id, content


async def load_local_file(path):
    # Loads files from the local machine.
    # Check if the file exists.
    if not os.path.exists(path):
        print(colored("Error: File not found.", "red"))
        return -1
    # Load the file.
    with open(path, 'r') as file:
        file_contents = file.read()
    file_contents = "Loaded File: " + path + "\nContents: \n" + file_contents
    return file_contents


async def load_internet_file(path):
    # Load the file from the internet. i.e. a .txt or a .json or a .csv file or a .html file... etc.
    # Check if the file exists.
    try:
        file_contents = requests.get(path).text
    except:
        print(colored("Error: Url failed to load.", "red"))
        return -1
    file_contents = "Loaded Web File: " + path + "\nContents: \n" + file_contents
    return file_contents

