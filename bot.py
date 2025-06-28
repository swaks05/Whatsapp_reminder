import os
import threading
import time
import json
from datetime import datetime, timedelta
from twilio.rest import Client

# Load Env Vars (Render handles them automatically)
account_sid = os.environ['TWILIO_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_whatsapp = os.environ['TWILIO_SANDBOX_NUMBER']
my_whatsapp = os.environ['MY_WHATSAPP']

client = Client(account_sid, auth_token)

reminders_file = 'reminders.json'

# Load existing reminders
if not os.path.exists(reminders_file):
    with open(reminders_file, 'w') as f:
        json.dump([], f)

with open(reminders_file, 'r') as f:
    reminders = json.load(f)

# Save reminders persistently
def save_reminders():
    with open(reminders_file, 'w') as f:
        json.dump(reminders, f, indent=2)

# WhatsApp Message Sender
def send_whatsapp(message):
    client.messages.create(
        from_=twilio_whatsapp,
        body=message,
        to=my_whatsapp
    )
    print(f'✅ WhatsApp Sent: {message}')

# Background Loop
def reminder_bot():
    print("📅 Reminder Bot Loop Started...")
    while True:
        now = datetime.utcnow().replace(second=0, microsecond=0).isoformat()
        for reminder in reminders[:]:
            if reminder['datetime_utc'] == now:
                send_whatsapp(f"⏰ Reminder: {reminder['message']}")
                reminders.remove(reminder)
                save_reminders()
        print(f'🔄 Server UTC Time: {now}')
        time.sleep(60)
