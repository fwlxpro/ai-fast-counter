# ai-fast-counter
Official Documentation for fast-couter ai free ai model for discord bots and everything you want !  You can use it for any interaction. 


---

# 🤖 AI API pro Discord Bota

Tento projekt poskytuje **REST API** pro integraci AI do Discord botů.
Podporuje:

* **Paměť konverzací (memory)** 🧠
* **Šifrování zpráv (AES)** 🔒
* **Podporu více API klíčů** 🔑
* **Snadné použití pro JavaScript i Python** 🐍📜

---

## 🚀 Jak to funguje

```
Discord uživatel → Discord Bot → AI API → Together AI → AI API → Discord Bot → Discord uživatel
```

Paměť funguje pomocí ukládání šifrovaných zpráv do souborů ve struktuře:

```
/<API_KEY>/database/<userId>.jsonl
```

Každý uživatel má svůj vlastní "memory slot" (`userId.jsonl`).

---

## 🛠️ Instalace

### 1️⃣ Klonování projektu

```bash
git clone https://github.com/tvuj-username/ai-api.git
cd ai-api
```

### 2️⃣ Instalace závislostí

```bash
npm install
```

### 3️⃣ Konfigurace prostředí

Vytvoř soubor `.env`:

```env
PORT=3000
API_KEY_ONE=tvuj_api_klic_1
API_KEY_TWO=volitelny_druhy_klic
TOGETHER_API_KEY=tvuj_together_api_key
MEMORY_SECRET_KEY=silny_sifrovaci_klic
```

---

## 🌐 Deploy na Render

1. Nahraj projekt na GitHub.
2. Na [Render](https://render.com) vytvoř **Web Service**.
3. Vyplň environment variables (viz výše).
4. Deployni.
5. Render ti vygeneruje veřejnou URL např.:

   ```
   https://ai-api-xxxx.onrender.com
   ```

---

## 🧩 API Endpointy

### 1. `GET /`

Základní test, že API běží.

```http
GET https://ai-api-xxxx.onrender.com/
```

**Odpověď:**

```text
AI API is running!
```

---

### 2. `POST /api/generate-text`

Generování textu pomocí AI.

#### Request

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

### 3. `POST /api/dataview`

Zobrazení historie uživatele.

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

## 🖥️ Struktura projektu

```
ai-api/
├── src/
│   ├── index.js        # Hlavní API server
│   ├── memory/         # Paměť (šifrované JSONL soubory)
├── package.json
├── .env
└── README.md
```

---

## 💻 Použití v Discord.js

```javascript
const { Client, GatewayIntentBits } = require("discord.js");
const fetch = require("node-fetch");

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

const API_URL = "https://ai-api-xxxx.onrender.com";
const API_KEY = "tvuj_api_klic";

client.on("messageCreate", async (message) => {
    if (message.author.bot) return;

    if (message.content.startsWith("!ask")) {
        const query = message.content.slice(4).trim();
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

## 🐍 Použití v Python (discord.py)

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

    if client.user in message.mentions:  # Když někdo pingne bota
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

## 🔒 Jak funguje šifrování

Každá zpráva je uložena takto:

```json
{
  "role": "user",
  "content": "U2FsdGVkX18... (AES-256)",
  "timestamp": "2025-08-05T12:00:00Z"
}
```

* **AES-256**: zprávy jsou šifrované pomocí `MEMORY_SECRET_KEY`.
* Při načtení zpráv API data dešifruje a vrátí v čitelné podobě.

Vzorec:

```
encrypted_content = AES_Encrypt(content, MEMORY_SECRET_KEY)
decrypted_content = AES_Decrypt(encrypted_content, MEMORY_SECRET_KEY)
```

---

## ✅ Shrnutí

* Deploy na Render → API URL.
* Přidat API KEY do bota.
* Použít endpoint `/api/generate-text`.
* Hotovo: AI funguje s pamětí a šifrováním.

---

Chceš, abych k tomu přidal i **sekci s diagramem (Mermaid)** jak teče request/response mezi Discordem, API a Together AI? (vizualizace)
