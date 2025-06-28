import os
from flask import Flask, request, render_template, redirect
from datetime import datetime, timedelta
import threading
import json
from bot import reminder_bot, reminders, save_reminders

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    msg = ""
    if request.method == 'POST':
        message = request.form['message']
        date = request.form['date']
        time_str = request.form['time']

        try:
            # Parse IST Date & Time to UTC
            ist_datetime = datetime.strptime(f"{date} {time_str}", "%d-%m-%Y %H:%M")
            utc_datetime = ist_datetime - timedelta(hours=5, minutes=30)
            utc_datetime_str = utc_datetime.replace(second=0, microsecond=0).isoformat()

            reminders.append({
                'message': message,
                'datetime_utc': utc_datetime_str
            })
            save_reminders()
            msg = f"✅ Reminder set for {date} {time_str} IST"

        except Exception as e:
            msg = f"❌ Error: {e}"

    return render_template('index.html', msg=msg, reminders=reminders)

if __name__ == "__main__":
    threading.Thread(target=reminder_bot, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    print("✅ Bot Thread Started, Launching Web Server...")
    app.run(host="0.0.0.0", port=port)
