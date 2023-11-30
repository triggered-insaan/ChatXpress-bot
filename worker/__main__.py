from .bot import client

if __name__=='__main__':
    print("Bot is running 🎉")
    client.run_until_disconnected()