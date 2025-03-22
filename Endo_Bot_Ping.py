import discord
import csv
import re
import os
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
scheduler = AsyncIOScheduler()

def load_schedule(file_path):
    schedule = []
    now_utc = datetime.now(timezone.utc)

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Normalize date format
                raw_date = row['Date'].strip()
                try:
                    parsed_date = datetime.strptime(raw_date, "%Y-%m-%d")
                except ValueError:
                    parsed_date = datetime.strptime(raw_date, "%m/%d/%Y")

                # Clean up time formatting
                raw_time = row['GMT Start'].strip()
                cleaned_time = re.sub(r':(?=\s*[APap][Mm])', '', raw_time)
                dt_str = f"{parsed_date.strftime('%Y-%m-%d')} {cleaned_time}"

                # Parse full datetime and convert to UTC
                event_time = datetime.strptime(dt_str, '%Y-%m-%d %I:%M %p').replace(tzinfo=timezone.utc)
                notify_time = event_time - timedelta(minutes=10)

                if notify_time > now_utc:
                    schedule.append({
                        'notify_time': notify_time,
                        'event_time': event_time,
                        'driver': row['Driver Discord'],
                        'spotter': row['Spotter Discord']
                    })
                    print(f"📆 Scheduled: {row['Driver Discord']} & {row['Spotter Discord']} at {event_time.isoformat()}")
                else:
                    print(f"⏭️ Skipping past event: {event_time.isoformat()}")

            except Exception as e:
                print(f"⚠️ Error parsing row: {row} – {e}")

    return schedule

async def send_ping(channel, driver, spotter, event_time):
    unix_ts = int(event_time.timestamp())
    time_display = f"<t:{unix_ts}:f>"
    await channel.send(f"Driver! {driver} and Spotter {spotter} – Your next stint starts at {time_display} (in 10 minutes!)")

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    schedule = load_schedule("schedule.csv")

    for event in schedule:
        scheduler.add_job(
            send_ping,
            'date',
            run_date=event['notify_time'],
            args=[channel, event['driver'], event['spotter'], event['event_time']]
        )

    scheduler.start()
    print(f'🟢 Finished scheduling {len(schedule)} events.')

client.run(TOKEN)
