import discord
import requests

TOKEN = "TVUJ_DISCORD_TOKEN"
API_URL = "https://ai-api-xxxx.onrender.com"
API_KEY = "tvuj_api_klic"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Když někdo pingne bota
    if client.user in message.mentions:
        query = message.content.replace(f"<@{client.user.id}>", "").strip()

        payload = {
            "role": "user",
            "content": query,
            "memory": True,
            "userId": str(message.author.id)
        }

        response = requests.post(f"{API_URL}/api/generate-text", json=payload, headers={"x-api-key": API_KEY})
        data = response.json()
        await message.channel.send(data.get("text", "⚠️ AI neposlala žádnou odpověď."))

client.run(TOKEN)
