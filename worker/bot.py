from telethon import TelegramClient, events
import dotenv
import os
import aiohttp

dotenv.load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
bot_token = os.getenv('bot_token')
chatgpt_api_key = os.getenv('openai_key')
custom_msg = "Created by [Unique Shadows](tg://user?id=1983883642)"

async def get_chatgpt_response(chatgpt_api_key, user_input):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {chatgpt_api_key}',
    }

    data = {
        'model': "gpt-3.5-turbo",
        'messages': [{'role': 'user', 'content': user_input}],
    }

    chatgpt_api_url = 'https://api.openai.com/v1/chat/completions'
    async with aiohttp.ClientSession() as session:
        async with session.post(chatgpt_api_url, json=data, headers=headers) as response:
            chatgpt_response = (await response.json())['choices'][0]['message']['content']


    return chatgpt_response


client = TelegramClient(
    'Bot',
    api_id,
    api_hash

).start(
    bot_token=bot_token
)


@client.on(events.NewMessage(pattern='/start'))
async def handle_start(event):
    await event.respond(f'Hello! I am ChatXpress bot.\n{custom_msg}')


@client.on(events.NewMessage)
async def handle_message(event):
    user_input = event.message.text

    if not user_input.startswith('/start'):
        async with client.action(event.chat_id, 'typing'):
            chatgpt_response = await get_chatgpt_response(chatgpt_api_key, user_input)
            msg = chatgpt_response + custom_msg

            await event.reply(chatgpt_response, parse_mode='md')