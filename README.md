# Endo Ping Discord Bot

A simple Discord bot that reads a schedule CSV file, calculates event start times in GMT, and pings the assigned driver and spotter in a Discord channel 10 minutes before their event begins. It uses Discord's local time formatting so users see the time in their own time zone.

---

## ✅ Features

- Reads a CSV file containing schedule info
- Automatically pings the driver and spotter before each event
- Uses Discord time formatting (`<t:TIMESTAMP:f>`) for local timezone display
- Environment-based config for security

---

## 🧰 Requirements

- Python 3.8 or higher
- A Discord bot token
- Access to the target Discord channel
- `pip` to install dependencies

---

## 🚀 Setup Instructions

### 1. Clone the Bot Repository

```bash
git clone https://github.com/yourusername/endo-ping-bot.git
cd endo-ping-bot
```

> Replace `yourusername` with your actual GitHub username if applicable.

---

### 2. Install Dependencies

Install the required Python packages:

install them manually:

```bash
pip install discord.py apscheduler python-dotenv
```

---

### 3. Create a `.env` File

Create a `.env` file in the root directory of the project:

```
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_CHANNEL_ID=123456789012345678
```

- Replace `your_discord_bot_token_here` with your actual bot token.
- Replace the channel ID with the ID of the text channel where the bot should send pings.
- To get a channel ID, enable **Developer Mode** in Discord settings, then right-click the channel > "Copy ID".

---

### 4. Create the `schedule.csv` File

This file holds your scheduled events.

#### ✅ Required Columns:

```csv
GMT Start,Date,Driver,Spotter,Driver Discord,Spotter Discord
```

#### ✅ Example:

```csv
GMT Start,Date,Driver,Spotter,Driver Discord,Spotter Discord
12:40 PM,2025-03-22,Josh,Chris,<@123456789>,<@987654321>
1:28 PM,2025-03-22,Josh,Trey,<@123456789>,<@222333444>
12:02 AM,2025-03-23,Trey,Chris,<@222333444>,<@987654321>
```

- `GMT Start`: in `hh:mm AM/PM` format
- `Date`: either `YYYY-MM-DD` or `MM/DD/YYYY`
- Use Discord user ID mention format like `<@123456789>` for proper pings

> Make sure the file ends with a newline so the last row isn't skipped.

---

### 5. Run the Bot

Start the bot using:

```bash
python Endo_Ping.py
```

Logs will show which events are scheduled.

---

## 💡 Tips

- Only future events are scheduled.
- Use UTC/GMT for start times — the bot auto-displays local times using Discord’s formatting.
- Keep the bot running on a machine that stays online to ensure all events are processed.


