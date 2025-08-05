# ai-fast-counter
Official Documentation for fast-couter ai free ai model for discord bots and everything you want !  You can use it for any interaction. 


---

# 🤖 Jak používat naši AI API v Discord botech

Tento dokument vysvětluje, jak **připojit svůj Discord bot** k naší AI API. Nemusíte nic hostovat – jen voláte naše API a používáte svůj API klíč.

---

## 🔑 Co budete potřebovat

* 🌐 URL naší API (např. `https://ai-api-xxxx.onrender.com`)
* 🔑 Váš **API klíč**, který vám poskytneme
* 🤖 Discord bota (Node.js nebo Python)
* 📦 Knihovny pro práci s HTTP požadavky (např. `node-fetch` pro Node.js, `requests` pro Python)

---

## 📐 Struktura API volání

```
[Discord bot]  →  [Naše API endpoint]  →  [AI model]
      ↑                                  ↓
  Paměť uživatele ← šifrované zprávy
```

### Datový tok:

1. Uživatel pošle zprávu.
2. Bot odešle požadavek na naše API s parametry (role, content, memory, userId).
3. API vrátí odpověď AI.
4. (Pokud je memory = true) zpráva se uloží do šifrované databáze.

---

## 🧩 API Endpointy

### 1️⃣ `POST /api/generate-text`

Slouží k vygenerování odpovědi od AI.

#### Request body

```json
{
  "role": "user",
  "content": "Ahoj, jak se máš?",
  "memory": true,
  "userId": "123456789"
}
```

| Parametr  | Typ     | Popis                                        |
| --------- | ------- | -------------------------------------------- |
| `role`    | string  | Role mluvčího (`user` nebo `assistant`).     |
| `content` | string  | Textová zpráva.                              |
| `memory`  | boolean | Zapnutí paměti (true = ukládání konverzací). |
| `userId`  | string  | ID uživatele (Discord user ID).              |

#### Headers

```http
x-api-key: <TVŮJ_API_KEY>
Content-Type: application/json
```

#### Response

```json
{
  "text": "Mám se skvěle! A ty?"
}
```

---

### 2️⃣ `POST /api/dataview`

Zobrazení uložené paměti konverzace pro konkrétního uživatele.

#### Request

```json
{
  "apiKey": "<TVŮJ_API_KEY>",
  "userId": "123456789"
}
```

#### Response

```json
[
  { "role": "user", "content": "Ahoj!", "timestamp": "2025-08-05T12:00:00Z" },
  { "role": "assistant", "content": "Ahoj! Jak ti můžu pomoci?", "timestamp": "2025-08-05T12:00:02Z" }
]
```

---

## ⚙️ Instalace závislostí

### Node.js

```bash
npm install node-fetch discord.js
```

### Python

```bash
pip install discord.py requests
```

---

## 💻 Příklad použití v Discord.js

```javascript
const { Client, GatewayIntentBits } = require("discord.js");
const fetch = require("node-fetch");

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

const API_URL = "https://ai-api-xxxx.onrender.com";
const API_KEY = "tvuj_api_klic";

client.on("messageCreate", async (message) => {
    if (message.author.bot) return;

    // Když někdo pingne bota
    if (message.mentions.has(client.user)) {
        const query = message.content.replace(/<@!?\d+>/, "").trim();
        const response = await fetch(`${API_URL}/api/generate-text`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-api-key": API_KEY
            },
            body: JSON.stringify({
                role: "user",
                content: query,
                memory: true,
                userId: message.author.id
            })
        });

        const data = await response.json();
        message.reply(data.text || "⚠️ AI neposlala žádnou odpověď.");
    }
});

client.login("TVUJ_DISCORD_TOKEN");
```

---

## 🐍 Příklad použití v Python (discord.py)

```python
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
```

---

## 🔒 Paměť a šifrování

* Paměť konverzací je ukládána do **šifrovaných souborů**.
* Každý uživatel má svůj vlastní soubor (`userId.jsonl`).
* Šifrování zajišťuje, že k datům nemá přístup nikdo mimo server.

Vzorec šifrování (AES):

```
Encrypted = AES_Encrypt(content, MEMORY_SECRET_KEY)
```

Dešifrování:

```
Decrypted = AES_Decrypt(Encrypted, MEMORY_SECRET_KEY)
```

---

## ✅ Shrnutí

* API běží na našem serveru → nemusíš nic hostovat.
* Stačí ti API KEY.
* Voláš endpointy `/api/generate-text` a `/api/dataview`.
* Funguje v **JavaScriptu** i **Pythonu**.
* Paměť je automaticky šifrována.

Teď můžeš mít AI v botech s pamětí 🧠 a šifrovanou databází 🔒 bez složité konfigurace!

