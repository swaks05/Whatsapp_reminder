import os
import sqlite3
import time
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()  # Safe locally, ignored on Render if env vars are set there

# Database Path
DB = os.getenv('DB_PATH', 'reminders.db')

# Twilio Credentials from Render Environment Variables
account_sid = os.environ['TWILIO_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
my_whatsapp = os.environ['MY_WHATSAPP']

client = Client(account_sid, auth_token)

def reminder_bot():
    print("📅 Reminder Bot Loop Started...")
    
    while True:
        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M')
        print(f"🔄 Server UTC Time: {now}")

        with sqlite3.connect(DB) as conn:
            reminders = conn.execute("SELECT id, message, datetime FROM reminders").fetchall()

        for rid, msg, dt in reminders:
            print(f"⏳ Checking Reminder ID {rid}: {dt} (Now: {now})")
            if dt == now:
                print(f"📨 Sending WhatsApp Reminder: {msg}")
                
                try:
                    client.messages.create(
                        body=msg,
                        from_='whatsapp:+14155238886',  # Twilio Sandbox Number
                        to=my_whatsapp
                    )
                    print(f"✅ Message Sent to {my_whatsapp}")

                    with sqlite3.connect(DB) as conn:
                        conn.execute("DELETE FROM reminders WHERE id = ?", (rid,))
                        conn.commit()
                        print(f"🗑️ Reminder ID {rid} deleted after sending")

                except Exception as e:
                    print(f"⚠️ Failed to send message: {e}")

        time.sleep(30)
