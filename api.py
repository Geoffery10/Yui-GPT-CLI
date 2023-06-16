import json
import aiohttp
import asyncio

async def api_call(history, prompt):
    # Load config file
    with open('server_info.json', 'r') as f:
        config = json.load(f)

    # Server address
    server = config['server']

    # Generation parameters
    params = config['params']

    # print("Sending request to server...")
    params = {
        'max_new_tokens': params['max_new_tokens'],
        'do_sample': params['do_sample'],
        'temperature': params['temperature'],
        'top_p': params['top_p'],
        'typical_p': params['repetition_penalty'],
        'repetition_penalty': params['repetition_penalty'],
        'encoder_repetition_penalty': params['encoder_repetition_penalty'],
        'top_k': params['top_k'],
        'min_length': params['min_length'],
        'no_repeat_ngram_size': params['no_repeat_ngram_size'],
        'num_beams': params['num_beams'],
        'penalty_alpha': params['penalty_alpha'],
        'length_penalty': params['length_penalty'],
        'early_stopping': params['early_stopping'],
        'seed': params['seed'],
    }

    payload = json.dumps([prompt, params])

    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://{server}:7862/run/textgen", json={
            "data": [
                payload
            ]
        }) as response:
            data = await response.json()
    try:
        reply = data["data"][0]
    except:
        print("Error: No response")
        print(data)
        return 'Sorry, I don\'t know what to say. 😳'

    # Remove the prompt and history from the reply.
    # print(f"Prompt: {prompt}\n")
    # print(f"History: {history}\n")
    # print(f"Reply: {reply}\n")
    reply = reply.replace(prompt, "")
    reply = reply.replace(history, "")

    # Remove anything after ### Human
    reply = reply.split("### Human")[0]

    return reply