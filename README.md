# BosS-Talker 🤖

A Discord bot that tracks when specific members connect to a server 
and generates AI-powered chat summaries using the Gemini API.

> Originally built to solve a very real problem: knowing exactly when 
> the boss joins the weekly meeting.

---

## Features

- 🔔 **Connection notifications** — alerts when a target user connects to the server
- 📄 **Chat summaries** — generates concise summaries of any text channel on demand
- 🤖 **Gemini API integration** — powered by Google's generative AI for natural language summaries
- ⚙️ **Persistent deployment** — runs 24/7 on a cloud VM managed by pm2

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Discord library | discord.py |
| AI | Google Gemini API |
| Infrastructure | Oracle Cloud Free Tier (ARM Ampere A1) |
| Process manager | pm2 |

---

## Deployment

BosS-Talker runs on an **Oracle Cloud Always Free** ARM instance 
(`VM.Standard.A1.Flex`) — a permanent, zero-cost VM with 1 OCPU 
and 6 GB RAM hosted in US East (Ashburn). Process persistence and 
automatic restarts are handled by **pm2**, ensuring the bot stays 
online without manual intervention.

This setup was chosen over serverless platforms (Vercel, Railway) 
because Discord bots require a persistent WebSocket connection that 
serverless architectures cannot maintain reliably.

---

## Configuration

Clone the repository and install dependencies:

```bash
git clone https://github.com/Ingetista/boss-talker.git
cd boss-talker
pip3 install -r requirements.txt
```

Create a `.env` file in the root directory with the following variables:

```env
DISCORD_TOKEN=your_discord_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

Start the bot:

```bash
python3 main.py
```

Or with pm2 for persistent deployment:

```bash
pm2 start "python3 main.py" --name boss-talker
```

---

## Author

**Ingetista**  
Electronic & Firmware Engineer  
[LinkedIn](https://www.linkedin.com/in/carlos-lópez-7a166a1b9)

Engineering is art.