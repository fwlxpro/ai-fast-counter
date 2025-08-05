// 🧠 Třída pro komunikaci s AI API s podporou memory
class AIBotHandler {
    constructor(client, apiUrl, apiKey) {
        this.client = client;
        this.apiUrl = apiUrl;
        this.apiKey = apiKey;
    }

    // Metoda pro zpracování zpráv
    async handleMessage(message) {
        // Ignorujeme zprávy od botů
        if (message.author.bot) return;

        // Kontrola, jestli byl bot pingnut
        if (message.mentions.has(this.client.user)) {
            const query = message.content.replace(/<@!?\d+>/, "").trim();

            // Odeslání požadavku na naši API
            const response = await fetch(`${this.apiUrl}/api/generate-text`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "x-api-key": this.apiKey
                },
                body: JSON.stringify({
                    role: "user",
                    content: query,
                    memory: true, // ✅ zapneme paměť
                    userId: message.author.id
                })
            });

            const data = await response.json();
            message.reply(data.text || "⚠️ AI neposlala žádnou odpověď.");
        }
    }
}

// =========================
// Příklad použití
// =========================
const { Client, GatewayIntentBits } = require("discord.js");
const fetch = require("node-fetch");

const client = new Client({
    intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent]
});

// Nastavení API
const API_URL = "https://ai-api-cnon.onrender.com/";
const API_KEY = "tvuj_api_klic";

// Inicializace handleru
const aiHandler = new AIBotHandler(client, API_URL, API_KEY);

client.on("messageCreate", async (message) => {
    await aiHandler.handleMessage(message); // Voláme naši classu
});

client.login("TVUJ_DISCORD_TOKEN");

// Ano tohle je vygenerováno ai pro ty smudly co ani nevi jak se dela print hello world nebudu se tady s vamam srat jako xd
