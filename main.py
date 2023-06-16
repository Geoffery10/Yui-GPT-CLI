
import os
from history import *
from api import *
import asyncio
from termcolor import colored

async def print_header(session_id = -1):
    # Load ascii art from file.
    with open("ascii-art.txt", "r") as f:
        ascii_art = f.read()
    # Print the ascii art.
    print(colored(f"\033c{ascii_art}", "white"))
    print(colored("\nWelcome to the Yui-GPT CLI!", "white"))
    print(colored("This program will interface with the text-generation-webui API to generate text.", "white"))
    print(colored("It was designed by Geoffery10.\n", "white"))
    if session_id != -1:
        print(colored(f"Session ID: {session_id}", "white"))
    await print_help()
    print("")


async def print_help():
    print(colored("Type a prompt to generate a response.", "white"))
    print(colored("Type " + colored("'!quit'", "light_yellow") + " to exit the program.", "white"))
    print(colored("Type " + colored("'!clear'", "light_yellow") + " to clear the chat history.", "white"))
    print(colored("Type " + colored("'!history'", "light_yellow") + " to print the chat history.", "white"))
    print(colored("Type " + colored("'!help'", "light_yellow") + " to print this message again.", "white"))
    print(colored("Type " + colored("'!load <chat number>'", "light_yellow") + " to load a chat.", "white"))
    print(colored("Type " + colored("'!retry'", "light_yellow") + " to retry the last prompt.", "white"))
    print(colored("Type " + colored("'!file <file name> <question>'", "light_yellow") + " to load a file and ask a question about it.", "white"))



async def main():
    session_id = await get_next_chat_id()
    await print_header(session_id)
    # Loop until the user wants to quit.
    while True:
        user_input = input(colored("Enter a prompt: ", "light_blue"))
        if user_input == "!quit":
            break
        elif user_input == "!clear":
            session_id = await clear_history()
            await print_header(session_id)
            print(colored("History cleared.", "yellow"))
        elif user_input == "!history":
            await print_history(session_id)
        elif user_input == "!help":
            await print_help()
        elif "!load" in user_input:
            # get the chat number from the user input.
            chat_number = user_input.split(" ")[1]
            # Parse the chat number.
            try:
                chat_number = int(chat_number)
            except:
                print(colored("Error: Invalid chat number.", "red"))
                continue
            if await load_chat(chat_number):
                session_id = chat_number
                await print_header(session_id)
                print(colored(f"Loaded chat {chat_number}.", "yellow"))
            else:
                print(colored("Error: Chat number out of range.", "red"))
        elif user_input == "!retry":
            # Get the last prompt from the history.
            last_prompt = await get_last_human_message(session_id)
            # Remove the last prompt from the history.
            await remove_last_messages(session_id)
            await send_prompt(last_prompt, session_id)
        elif "!file" in user_input:
            # Get the file name and question from the user input.
            file_name = user_input.split(" ")[1]
            question = user_input.split(" ")[2:]
            question = " ".join(question)
            # Load the file.
            session_id_temp, file_contents = await load_file(file_name)
            if session_id_temp != -1:
                session_id = session_id_temp
                # await print_header(session_id)
                print(colored(f"Loaded file {file_name}.", "yellow"))
                # Send the question to the API.
                final_question = f"{file_contents}\n### Question\n{question}\n"
                await send_prompt(final_question, session_id)
            else:
                print(colored("Error: File not found.", "red"))
        elif user_input == "": # Empty input.
            continue
        else:
            await send_prompt(user_input, session_id)
            

async def load_file(path):
    # Check if the file exists.
    if not os.path.exists(path):
        print(colored("Error: File not found.", "red"))
        return -1
    # Load the file.
    with open(path, 'r') as file:
        file_contents = file.read()
    # Start a new chat.
    session_id = await create_history()
    return session_id, file_contents
    

async def send_prompt(user_input, session_id):
    user_input = user_input.replace("\\n", "\n") # Replace \n with newlines.
    # Send history with attached prompt to the API.
    history = await get_history(session_id)
    
    prompt = f"{history}\n### Human\n{user_input}\n### Assistant\n"
    reply = await api_call(history, prompt) # Returns a string.
    # Add the prompt and response to the history.
    await add_to_history(user_input, reply)
    # Print the response.
    if '```' in reply: # Response has a code block.
        # Color everything in between the ``` cyan.
        split_reply = []
        for i, s in enumerate(reply.split('```')):
            if i % 2 == 1:
                s = colored(s, "cyan")
            split_reply.append(s)
        reply = '```'.join(split_reply)
        # Remove the ``` from the reply. and empty lines.
        reply = reply.replace('```', '').replace('\n\n', '\n')
    else:
        print(colored(reply, "white"))
        

if __name__ == "__main__":
    # Clear the terminal.
    print("\033c")
    asyncio.run(main())
        