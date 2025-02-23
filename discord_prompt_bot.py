import discord
import random
import os

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
        # Send the writing prompt as a response
        await message.channel.send(prompt)

# Get the bot token from the environment variable
token = os.getenv('DISCORD_BOT_TOKEN')
client.run(token)