# This python file manages chat history for the CLI.
from termcolor import colored

chat_name = "./chats/chat_0.txt"


async def get_history(id):
    # Get the chat history from the ./chats/history.txt file.
    global chat_name
    if await chat_exists(id):
        try:
            history_file = open(chat_name, "r")
            history = history_file.read()
            history_file.close()
        except:
            history = "Couldn't read chat history."
    else:
        history = "No chat history in this thread yet."
    return history

async def add_to_history(prompt="", response=""):
    global chat_name
    # Check if chat file exists.
    try:
        history_file = open(chat_name, "r", encoding="utf-8")
        history_file.close()
    except:
        await create_history()
    # Add the prompt and response to the chat file.
    if prompt == "" or response == "" or prompt == None or response == None:
        print("Error: Prompt or response is empty.")
        return
    history_file = open(chat_name, "a", encoding="utf-8")
    history_file.write("### Human\n")
    history_file.write(str(prompt) + "\n")
    if response != "":
        history_file.write("### Assistant\n")
        history_file.write(response + "\n")
        history_file.close()
    return

async def clear_history():
    # Starts a new chat file.
    id = await get_next_chat_id()
    global chat_name
    chat_name = f"./chats/chat_{id}.txt"
    return id

async def print_history(id = -1):
    # Print the chat history.
    history = await get_history(id)
    print("Chat history:")
    # Split history into messages by ### Human and ### Assistant.
    # Color the human messages light blue and the assistant messages white.
    split_history = history.split("### ")
    for i in range(len(split_history)):
        if i % 2 == 1:
            split_history[i] = colored(split_history[i], "light_blue")
        else:
            split_history[i] = colored(split_history[i], "white")
    history = "> ".join(split_history)
    print(history)
    return

async def get_next_chat_id():
    # Count files in ./chats/ directory. to find the number of chats.
    import os
    chats = os.listdir("./chats/")
    chats = [chat for chat in chats if chat.endswith(".txt")]
    return len(chats)

async def chat_exists(id):
    # Check if chat file exists.
    import os
    chats = os.listdir("./chats/")
    chats = [chat for chat in chats if chat.endswith(".txt")]
    if f"chat_{id}.txt" in chats:
        return True
    else:
        return False

async def create_history():
    id = await get_next_chat_id()
    # Create a new chat file with the next number.
    new_chat = open(f"./chats/chat_{id}.txt", "w")
    new_chat.write("")
    new_chat.close()
    global chat_name
    chat_name = f"./chats/chat_{id}.txt"
    print(f"Created chat_{id}.txt")
    return id

async def load_chat(id = 0):
    looking_for = f"chat_{id}.txt"
    import os
    chats = os.listdir("./chats/")
    print(chats)
    if looking_for in chats:
        global chat_name
        chat_name = f"./chats/chat_{id}.txt"
        return True
    else:
        return False
    
async def get_last_human_message(id):
    # Get the last human message from the chat history.
    history = await get_history(id)
    history = history.split("### Human")
    last_human_message = history[-1]
    last_human_message = last_human_message.split("### Assistant")[0]
    return last_human_message

async def get_last_assistant_message(id):
    # Get the last assistant message from the chat history.
    history = await get_history(id)
    history = history.split("### Assistant")
    last_assistant_message = history[-1]
    return last_assistant_message

async def remove_last_assistant_message(id):
    # Remove the last assistant message from the chat history.
    history = await get_history(id)
    history = history.split("### Assistant")
    history = history[:-1]
    history = "### Assistant".join(history)
    history_file = open(chat_name, "w")
    history_file.write(history)
    history_file.close()
    return

async def remove_last_messages(id):
    # Remove the last human and assistant messages from the chat history. Order is ### Human, ### Assistant.
    history = await get_history(id)
    history = history.split("### Human")
    history = history[:-1]
    history = "### Human".join(history)
    history_file = open(chat_name, "w")
    history_file.write(history)
    history_file.close()
    return
    