import json
import requests
import asyncio


async def setup_params(config, prompt, negative_prompt):
    params = config['params']
    request = {
        'prompt': prompt,
        'max_new_tokens': params['max_new_tokens'],
        'auto_max_new_tokens': params['auto_max_new_tokens'],
        'max_tokens_second': params['max_tokens_second'],

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': params['preset'],
        'do_sample': params['do_sample'],
        'temperature': params['temperature'],
        'top_p': params['top_p'],
        'typical_p': params['typical_p'],
        'epsilon_cutoff': params['epsilon_cutoff'],  # In units of 1e-4
        'eta_cutoff': params['eta_cutoff'],  # In units of 1e-4
        'tfs': params['tfs'],
        'top_a': params['top_a'],
        'repetition_penalty': params['repetition_penalty'],
        'repetition_penalty_range': params['repetition_penalty_range'],
        'top_k': params['top_k'],
        'min_length': params['min_length'],
        'no_repeat_ngram_size': params['no_repeat_ngram_size'],
        'num_beams': params['num_beams'],
        'penalty_alpha': params['penalty_alpha'],
        'length_penalty': params['length_penalty'],
        'early_stopping': params['early_stopping'],
        'mirostat_mode': params['mirostat_mode'],
        'mirostat_tau': params['mirostat_tau'],
        'mirostat_eta': params['mirostat_eta'],
        'guidance_scale': params['guidance_scale'],
        'negative_prompt': negative_prompt,

        'seed': params['seed'],
        'add_bos_token': params['add_bos_token'],
        'truncation_length': params['truncation_length'],
        'ban_eos_token': params['ban_eos_token'],
        'skip_special_tokens': params['skip_special_tokens'],
        'stopping_strings': params['stopping_strings'],
    }
    return request
    

async def api_call(history, prompt, negative_prompt=""):
    # Load config file
    with open('server_info.json', 'r') as f:
        config = json.load(f)
    server = config['server']
    request = await setup_params(config, prompt, negative_prompt)
    
    # Send request to server
    response = requests.post(server, json=request)
    
    # Parse response
    if response.status_code == 200:
        reply = response.json()['results'][0]['text']
    elif response.status_code == 400:
        print("Error: Bad request")
        print(response.json()['results'][0])
        return 'Sorry, I don\'t know what to say. 😳'
    else:
        print("Error: No response")
        print(response.json()['results'][0])
        return 'Sorry, I don\'t know what to say. 😳'

    return await getNewMessages(prompt, history, reply)


async def getNewMessages(prompt, history, reply, username="Assistant"):
    reply = reply.replace(prompt, "")
    reply = reply.replace(history, "")

    # Remove anything after ### Human
    reply = reply.split("### Human")[0]
    return reply

async def main():
    prompt = "### Human\nHello, how are you?\n### Assistant\n"
    history = ""
    reply = await api_call(history, prompt)
    print(prompt + reply)

if __name__ == '__main__':
    asyncio.run(main())
