import os
import discord
import random
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)

app.config["DISCORD_CLIENT_ID"] = os.environ["DISCORD_CLIENT_ID"]
app.config["DISCORD_PUBLIC_KEY"] = os.environ["DISCORD_PUBLIC_KEY"]
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]
app.config["DISCORD_BOT_TOKEN"] = os.environ["DISCORD_BOT_TOKEN"]

# Create a list of writing prompts
writing_prompts = [
    "You wake up in a world where everyone has superpowers except you.",
    "A detective is on the trail of a thief who can teleport.",
    "You find a diary that predicts the future.",
    "A spaceship lands in your backyard.",
    "You discover a hidden door in your house that leads to another dimension.",
    "A time traveler from the future needs your help.",
    "You inherit a mysterious, ancient artifact with magical powers.",
    "A friendly ghost haunts your new apartment.",
    "You have the ability to speak with animals, and they need your help.",
    "A secret society is trying to recruit you for their cause."
]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@app.route('/')
def index():
   return 'Discord Bot is running!'

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Check if the message contains the word "prompt"
    if 'prompt' in message.content.lower():
        # Select a random writing prompt
        prompt = random.choice(writing_prompts)
        print(f'Sending writing prompt: {prompt}')
        # Send the writing prompt as a response
        await message.channel.send(prompt)

if __name__ == "__main__":
    # Run the web server in a separate thread
    from threading import Thread
    import sys

    if 'serve' in sys.argv:
        # Get the bot token from the environment variable
        token = os.getenv('DISCORD_BOT_TOKEN')

        # Start the bot in a new thread
        bot_thread = Thread(target=client.run, args=(token,))
        bot_thread.start()

        # Start the Flask server
        app.run(host='0.0.0.0', port=8000)
        print('Flask server running...')
    else:
        # Only run the bot
        token = os.getenv('DISCORD_BOT_TOKEN')
        client.run(token)