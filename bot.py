from dotenv import load_dotenv
load_dotenv()
import time
import datetime
import sqlite3
from twilio.rest import Client
import os

twilio_whatsapp_number = 'whatsapp:+14155238886'
DB = 'reminders.db'

def send_whatsapp_message(msg, client, my_whatsapp_number):
    message = client.messages.create(
        body=msg,
        from_=twilio_whatsapp_number,
        to=my_whatsapp_number
    )
    print(f"✅ WhatsApp message sent: SID {message.sid}")

def reminder_bot():
    print("📅 Reminder Bot Running...")

    account_sid = os.environ['TWILIO_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    my_whatsapp_number = os.environ['MY_WHATSAPP']

    client = Client(account_sid, auth_token)

    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')

        with sqlite3.connect(DB) as conn:
            cursor = conn.execute("SELECT id, message FROM reminders WHERE datetime <= ?", (now,))
            due_reminders = cursor.fetchall()

            for reminder in due_reminders:
                send_whatsapp_message(reminder[1], client, my_whatsapp_number)
                conn.execute("DELETE FROM reminders WHERE id = ?", (reminder[0],))
            
            conn.commit()

        time.sleep(60)
