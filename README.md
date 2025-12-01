# Boss of the Mob — Discord Game Bot

A small Discord bot that hosts a lightweight social‑deduction mini‑game for 6 players. Users queue up, the game assigns two teams and secretly picks one player as the "Rat" who tries to mislead others. Players submit their reports; the bot tallies who identified the Rat correctly.

> Note: This repository currently contains a single Python file (`mafia_bot.py`) with hard‑coded Discord IDs. See TODOs below for making these values configurable.

---

## Overview
- Language: Python 3.10+ (uses `asyncio`)
- Libraries:
  - `discord.py` (Discord interactions, slash commands via `app_commands`)
  - `python-dotenv` (loads `TOKEN` from `.env`)
  - Standard libs: `asyncio`, `random`, `os`
- Entry point: `mafia_bot.py`
- Bot features:
  - Slash commands to join/leave the queue, view rules/status
  - Admin‑only command to add a member to the queue
  - Starts when queue reaches 6 players, assigns teams, DM’s the Rat
  - Aggregates end‑of‑round "report" submissions and posts the results

---

## Requirements
- Python 3.10 or newer
- A Discord account and a registered bot application with a bot token
- Guild/server where you can add the bot
- Privileged Intents enabled in the Discord Developer Portal (the code uses `discord.Intents.all()`).

Python packages:
```
pip install discord.py python-dotenv
```

If you prefer to pin versions, create a `requirements.txt` similar to:
```
discord.py>=2,<3
python-dotenv>=1,<2
```

---

## Environment Variables
The bot reads configuration from a `.env` file at repository root. Minimal required variable:

```
TOKEN=your_discord_bot_token
```

Optional/Hard‑coded values (TODO to move into env variables):
- `GUILD_ID` (currently hard‑coded: `271191981999259648`)
- `GAME_CHANNEL_ID` (currently hard‑coded: `1321380377461522443`)
- `ADMIN_ROLE_ID` for `/addmafia` (currently hard‑coded: `764088348452323348`)
- `QUEUE_LIMIT` (currently hard‑coded to `6`)
- `MAFIA_ROLE_NAME` (currently `"Rat"`)

---

## Setup
1. Clone the repo and open it in your IDE or terminal.
2. Create and activate a virtual environment (recommended):
   - Windows PowerShell:
     ```powershell
     py -3 -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   or
   ```
   pip install discord.py python-dotenv
   ```
4. Create a `.env` file containing your bot token:
   ```
   TOKEN=your_discord_bot_token
   ```
5. In the Discord Developer Portal:
   - Add a Bot to your application.
   - Enable Privileged Intents (Presence, Server Members, Message Content if needed).
   - Invite the bot to your guild with the required permissions (send messages, read message history, use slash commands).

---

## Running the Bot
From the project root:

- Windows PowerShell:
  ```powershell
  python .\mafia_bot.py
  ```
- macOS/Linux:
  ```bash
  python3 mafia_bot.py
  ```

On startup the bot will:
- Sync application commands for the configured guild (currently hard‑coded).
- Log "Bot is ready as <name>" on success.

---

## Commands (Slash)
These are defined in `mafia_bot.py` via `@tree.command`:

- `/mafia` — Join the queue for the next game.
- `/leave` — Leave the queue.
- `/rules` — Show a brief how‑to‑play message.
- `/status` — Show current queued players and capacity.
- `/report @member` — Submit your report on who the Rat is (call once per round).
- `/addmafia @member` — Admin‑only: Add a member to the queue.
  - Access is restricted via a Discord role ID (currently hard‑coded).

Game flow notes:
- The queue fills to 6 players by default (`queue_limit = 6`).
- When full, the bot shuffles the players into two teams of 3 each, picks one random Rat, DM’s them, and posts teams to the game channel.
- Players submit `/report` naming who they think is the Rat; at the end, the bot posts who guessed correctly and reveals the Rat.

---

## Project Structure
```
bossOfTheMob/
├── mafia_bot.py        # Discord bot implementation (entry point)
└── README.md           # This file
```

There is no `requirements.txt`, `pyproject.toml`, or tests in the repo at this time.

---

## Tests
There are currently no automated tests in this repository.

TODO:
- Add basic unit tests for game state transitions (`queue`, `need_vote`, `report` flow) using pytest and mocks for Discord objects.

---

## Scripts
There are no packaging scripts defined in this repo. Common commands:
- Run bot: `python mafia_bot.py`
- Optional: add a simple run helper on Windows via `run.ps1` or a cross‑platform `make`/`tox` if needed. (TODO)

---

## Configuration & Deployment
- IDs are hard‑coded:
  - Guild: `271191981999259648`
  - Game Channel: `1321380377461522443`
  - Admin Role: `764088348452323348`

TODO:
- Move the above IDs and gameplay constants into environment variables or a config file (e.g., `settings.toml` or `.env` entries such as `GUILD_ID`, `GAME_CHANNEL_ID`, `ADMIN_ROLE_ID`, `QUEUE_LIMIT`, `MAFIA_ROLE_NAME`).
- Add Dockerfile and a production process manager configuration (e.g., systemd or Docker Compose) for hosting.

---

## License
No license file was found in the repository.

TODO:
- Add a `LICENSE` file (e.g., MIT, Apache‑2.0) and reference it here.

---

## Notes & Caveats
- The bot currently syncs commands to a single guild only (fast registration during development). If you plan to use it across multiple guilds, switch to global command registration or multi‑guild sync.
- The bot requests `Intents.all()` and enables members/messages intents; ensure they are enabled in the Developer Portal and truly needed for your use case.
- Error handling and persistence are minimal; game state is in‑memory and resets when the process restarts.
