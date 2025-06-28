from flask import Flask, render_template, request, redirect
import sqlite3
import threading
import os
from bot import reminder_bot
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database Path
DB = os.getenv('DB_PATH', 'reminders.db')

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS reminders
                        (id INTEGER PRIMARY KEY, message TEXT, datetime TEXT)''')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.form['message']
        datetime_str = request.form['datetime']
        
        print(f"📝 Adding Reminder: {msg} at {datetime_str}")

        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO reminders (message, datetime) VALUES (?, ?)", (msg, datetime_str))
            conn.commit()

        return redirect('/')

    with sqlite3.connect(DB) as conn:
        reminders = conn.execute("SELECT id, message, datetime FROM reminders ORDER BY datetime").fetchall()

    return render_template('index.html', reminders=reminders)

if __name__ == "__main__":
    init_db()

    bot_thread = threading.Thread(target=reminder_bot, daemon=True)
    bot_thread.start()

    print("✅ Bot Thread Started, Launching Web Server...")

    app.run(host="0.0.0.0", port=5000)
